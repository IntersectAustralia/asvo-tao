import json

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from django.core.urlresolvers import reverse

from django.views.decorators.http import require_POST

from tao import models, workflow
from tao.decorators import researcher_required, set_tab
from tao.ui_modules import UIModulesHolder
from tao.xml_util import xml_parse
from tao.views import jobs
from tao.models import SurveyPreset
import json


@set_tab('mgf')
@researcher_required
def index(request):
    user = request.user
    if not user.check_disk_usage_within_quota():
        message = 'Please reduce your disk usage below ' + user.display_user_disk_quota() + '. ' \
                  'If you would like additional quota, please <a href="' + reverse('support_page') + '">submit</a> ' \
                  'a request with the reason for the request.'
        messages.info(request, mark_safe(message))
        # return jobs.index(request)
        return redirect(reverse('job_index'))

    if request.method == 'POST':
        if len(request.FILES) > 0:
            parameter_file = request.FILES.itervalues().next()
            ui_holder = UIModulesHolder(UIModulesHolder.POST)
            try:
                params_ui_holder = UIModulesHolder(UIModulesHolder.XML, xml_parse(parameter_file.read()))
                message = "Parameter file '%s' uploaded successfully." % parameter_file.name
                messages.info(request, message)
                return render(request, 'mock_galaxy_factory/index.html', {
                    'forms': ui_holder.forms(),
                    'ui_holder': params_ui_holder,
                    'TAB_SUMMARY_ID': settings.MODULE_INDICES['summary'],
                })
            except:
                message = "Failed to process parameter file: '%s'." % parameter_file.name
                messages.error(request, message)
                return render(request, 'mock_galaxy_factory/index.html', {
                    'forms': ui_holder.forms(),
                    # 'ui_holder': params_ui_holder,
                    'TAB_SUMMARY_ID': settings.MODULE_INDICES['summary'],
                })
        elif 'survey_presets' in request.POST:
            preset = SurveyPreset.objects.get(pk=request.POST.get('survey_presets'))
            params_ui_holder = UIModulesHolder(UIModulesHolder.XML, xml_parse(preset.parameters.encode()))
            ui_holder = UIModulesHolder(UIModulesHolder.POST)
            message = "Survey Preset '%s' loaded successfully." % preset.name
            messages.info(request, message)
            return render(request, 'mock_galaxy_factory/index.html', {
                'forms': ui_holder.forms(),
                'ui_holder': params_ui_holder,
                'TAB_SUMMARY_ID': settings.MODULE_INDICES['summary'],
            })
        else:
            ui_holder = UIModulesHolder(UIModulesHolder.POST, request.POST)
            response_dict = {}
            response_dict['job_submitted'] = False
            if ui_holder.validate():
                UserModel = get_user_model()
                user = UserModel.objects.get(username=request.user.username)
                job_description = request.POST.get('job-description')
                response_dict['job_id'] = workflow.save(user, ui_holder, job_description).pk
                messages.info(request, _(settings.INITIAL_JOB_MESSAGE % models.initial_job_status().lower()))
                response_dict['job_submitted'] = True
                response_dict['next_page'] = reverse('job_index')
            else:
                response_dict['errors'] = ui_holder.errors
            # Simple answer the errors dictionary
            # If the dictionary is empty, the client knows the job was created successfully
            response = json.dumps(response_dict)
            callback = request.GET.get('callback', None)
            if callback is not None:
                response = "%s(%s)" % (callback, response)
            return HttpResponse(response, mimetype="application/json")

    # Assume GET
    ui_holder = UIModulesHolder(UIModulesHolder.POST)
    return render(request, 'mock_galaxy_factory/index.html', {
        'forms': ui_holder.forms(),
        # 'forms_size' : len(ui_holder.forms())+1,
        'TAB_SUMMARY_ID': settings.MODULE_INDICES['summary']
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



