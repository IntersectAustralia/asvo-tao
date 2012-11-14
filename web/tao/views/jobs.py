from django.conf import settings
from django.core.servers.basehttp import FileWrapper  # TODO use sendfile
from django.http import HttpResponse, Http404
from django.shortcuts import render

from tao.decorators import researcher_required, set_tab, object_permission_required
from tao.models import Job

import os

@researcher_required
@object_permission_required('can_read_job')
@set_tab('jobs')
def view_job(request, id):
    # TODO security
    job = Job.objects.get(id=id)

    if job.is_completed():
        all_files = job.files()
    else:
        all_files = []

    return render(request, 'jobs/view.html', {
        'job': job,
        'files': all_files,
    })

@researcher_required
@object_permission_required('can_read_job')
def get_file(request, id, filepath):
    job = Job.objects.get(pk=id)
            
    if filepath not in job.files():
        raise Http404
    
    fullpath = os.path.join(settings.FILES_BASE, job.output_path, filepath)
    file = open(fullpath)
    response = HttpResponse(FileWrapper(file))

    basename = os.path.basename(fullpath)
    # TODO sanitise filename
    response['Content-Disposition'] = 'attachment; filename="%s"' % basename
    return response


@set_tab('jobs')
def index(request):
    return render(request, 'jobs/index.html')
