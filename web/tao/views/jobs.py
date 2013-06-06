from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.servers.basehttp import FileWrapper # TODO use sendfile
from django.http import StreamingHttpResponse, Http404
from django.shortcuts import render
from tao.decorators import researcher_required, set_tab, \
    object_permission_required
from tao.models import Job, JobFile
from tao.ui_modules import UIModulesHolder
from tao.xml_util import xml_parse
import os
import zipstream

@researcher_required
@object_permission_required('can_read_job')
@set_tab('jobs')
def view_job(request, id):
    job = Job.objects.get(id=id)

    # xml_string = job.parameters
    ui_holder = UIModulesHolder(UIModulesHolder.XML, xml_parse(job.parameters.encode('utf-8')))
    forms = ui_holder.forms()

    return render(request, 'jobs/view.html', {
        'job': job,
        'forms': forms,
        'forms_size' : len(forms)+1,
    })

@researcher_required
@object_permission_required('can_read_job')
def get_file(request, id, file_path):
    job = Job.objects.get(pk=id)

    the_one = [file for file in job.files() if file.file_name == file_path]
    if len(the_one) == 0:
        raise Http404
    
    job_file = the_one[0]
    if not job_file.can_be_downloaded():
        raise PermissionDenied

    response = StreamingHttpResponse(streaming_content=FileWrapper(open(job_file.file_path)))

    # TODO sanitise filename
    response['Content-Disposition'] = 'attachment; filename="%s"' % job_file.file_name.replace('/','_')
    return response

class TaoZipPath(zipstream.ZipPath):
    def __init__(self, file_path, dir_iter = None):
        self._file_path = file_path
        self._dir_iter = dir_iter
        self._basename = os.path.basename(file_path)

    def basename(self):
        """
        Returns the basename of this ZipPath instance
        """
        return self._basename.encode("utf8")

    def isdir(self):
        """
        Returns true if this ZipPath instance represents a directory
        """
        return self._dir_iter is not None

    def listdir(self):
        """
        If self.isdir(), this should be an iterator of ZipPath instances inside
        """
        return self._dir_iter

    def file(self):
        """
        If not self.isdir(), this should return a filename to open
        """
        return self._file_path

@researcher_required
@object_permission_required('can_read_job')
def get_zip_file(request, id):
    job = Job.objects.get(pk=id)

    # generator mapping data from files_tree into TaoZipPath
    def to_tao_zip_path(dir_iterator):
        for fn, iter in dir_iterator:
            if iter is None:
                yield TaoZipPath(fn)
            else:
                yield TaoZipPath(fn, to_tao_zip_path(iter))

    archive = zipstream.ZipStream(to_tao_zip_path(job.files_tree()))
    response = StreamingHttpResponse(streaming_content=archive, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="tao_output.zip"'
    return response

@set_tab('jobs')
def index(request):
    user_jobs = Job.objects.filter(user=request.user).order_by('-id')
    return render(request, 'jobs/index.html', {
        'jobs': user_jobs,
    })