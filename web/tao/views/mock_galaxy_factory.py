from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from django.core.urlresolvers import reverse

from django.views.decorators.http import require_POST

from tao import models, workflow
from tao.decorators import researcher_required, set_tab
from tao.ui_modules import UIModulesHolder
from tao.xml_util import xml_parse


@set_tab('mgf')
@researcher_required
def index(request):
    if request.method == 'POST':
        if len(request.FILES) > 0:
            parameter_file = request.FILES.itervalues().next().read()
            ui_holder = UIModulesHolder(UIModulesHolder.XML, xml_parse(parameter_file))
            # print(ui_holder.forms()[1])
            return render(request, 'mock_galaxy_factory/index.html', {
                'forms': ui_holder.forms(),
                'forms_size' : len(ui_holder.forms())+1,
            })
        else:
            #import pdb; pdb.set_trace()
            ui_holder = UIModulesHolder(UIModulesHolder.POST, request.POST)
            if ui_holder.validate():
                UserModel = get_user_model()
                user = UserModel.objects.get(username=request.user.username)
                job_description = request.POST.get('job-description')
                workflow.save(user, ui_holder, job_description)
                messages.info(request, _(settings.INITIAL_JOB_MESSAGE % models.initial_job_status().lower()))
                return redirect(reverse('job_index'))
    else:
        ui_holder = UIModulesHolder(UIModulesHolder.POST)
    
    return render(request, 'mock_galaxy_factory/index.html', {
        'forms': ui_holder.forms(),
        'forms_size' : len(ui_holder.forms())+1,
    })

@set_tab('mgf')
@researcher_required
def my_jobs_with_status(request, status=None):
    user_jobs = models.Job.objects.filter(user=request.user).order_by('-created_time')
    if status:
        filtered_jobs = user_jobs.filter(status=status)
    else:
        filtered_jobs = user_jobs

    if status in [models.Job.HELD, models.Job.SUBMITTED, models.Job.QUEUED, models.Job.IN_PROGRESS]:
        show_field = {
                      'submitted_at': True,
                      'parameters': True,
                      }
    elif status == models.Job.COMPLETED:
        show_field = {
                      'output_path': True,
                      }
    else:
        show_field = {
                      'user': True,
                      'status': True,
                      'output_path': True,
                      }

    return render(request, 'mock_galaxy_factory/jobs_table.html', {
        'jobs': filtered_jobs,
        'show_field': show_field,
        'status': status or 'All',
    })
