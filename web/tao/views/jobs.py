from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.servers.basehttp import FileWrapper # TODO use sendfile
from django.http import HttpResponse, Http404
from django.shortcuts import render
from tao.decorators import researcher_required, set_tab, \
    object_permission_required
from tao.models import Job, JobFile
from tao.ui_modules import UIModulesHolder
from tao.xml_util import xml_parse
import os
import zipfile
import StringIO



@researcher_required
@object_permission_required('can_read_job')
@set_tab('jobs')
def view_job(request, id):
    job = Job.objects.get(id=id)

    # xml_string = job.parameters
    ui_holder = UIModulesHolder(UIModulesHolder.XML, xml_parse(job.parameters.encode('utf-8')))

    return render(request, 'jobs/view.html', {
        'job': job,
        'forms': ui_holder.forms(),
        'forms_size' : len(ui_holder.forms())+1,
    })

@researcher_required
@object_permission_required('can_read_job')
def get_file(request, id, filepath):
    job = Job.objects.get(pk=id)
            
    if filepath not in [file.file_name for file in job.files()]:
        raise Http404
    
    job_file = JobFile(os.path.join(settings.FILES_BASE, job.output_path), filepath)
    if not job_file.can_be_downloaded():
        raise PermissionDenied
    
    fullpath = os.path.join(settings.FILES_BASE, job.output_path, filepath)
    file = open(fullpath)
    response = HttpResponse(FileWrapper(file))

    basename = os.path.basename(fullpath)
    # TODO sanitise filename
    response['Content-Disposition'] = 'attachment; filename="%s"' % basename
    return response
    
@researcher_required
@object_permission_required('can_read_job')
def get_zip_file(request, id):
    job = Job.objects.get(pk=id)
    
    # TODO stream the generated content to the browser as the zip is being created
    string_io = StringIO.StringIO()
    archive = zipfile.ZipFile(string_io, 'w', zipfile.ZIP_DEFLATED)
    for job_file in job.files():
        fullpath = job_file.file_path
        archive.write(fullpath, arcname=job_file.file_name) 
    archive.close()

    response = HttpResponse(string_io, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="tao_output.zip"'
    response['Content-Length'] = string_io.tell()
    string_io.seek(0) 
    return response

@set_tab('jobs')
def index(request):
    user_jobs = Job.objects.filter(user=request.user)
    return render(request, 'jobs/index.html', {
        'jobs': user_jobs,
    })