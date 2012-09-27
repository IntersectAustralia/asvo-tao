from django.conf import settings
from django.core.servers.basehttp import FileWrapper  # TODO use sendfile
from django.http import HttpResponse
from django.shortcuts import render

from tao.models import Job

import os


def view_job(request, id):
    # TODO security
    job = Job.objects.get(id=id)
    job_base_dir = os.path.join(settings.FILES_BASE, job.output_path)

    all_files = []
    for root, dirs, files in os.walk(job_base_dir):
        all_files += [os.path.join(root, filename)[len(job_base_dir)+1:] for filename in files]

    all_files.sort()

    return render(request, 'jobs/view.html', {
        'job': job,
        'files': all_files,
    })


def get_file(request, id, filepath):
    # TODO secure (only serve files from base dir (check .., /), check job permissions)

    job = Job.objects.get(pk=id)
    fullpath = os.path.join(settings.FILES_BASE, job.output_path, filepath)
    file = open(fullpath)
    response = HttpResponse(FileWrapper(file))

    basename = os.path.basename(fullpath)
    # TODO sanitise filename
    response['Content-Disposition'] = 'attachment; filename="%s"' % basename
    return response
