from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _

from django.core.urlresolvers import reverse

from django.views.decorators.http import require_POST

from tao import models, workflow
from tao.decorators import researcher_required, set_tab
from tao.ui_modules import UIModulesHolder


@set_tab('mgf')
@researcher_required
def index(request):
    if request.method == 'POST':
        ui_holder = UIModulesHolder(request.POST)
        if ui_holder.validate():
            user = models.User.objects.get(username=request.user)
            workflow.save(user, ui_holder)
            messages.info(request, _("Your job was held successfully."))
            return redirect(reverse('held_jobs'))
    else:
        ui_holder = UIModulesHolder()

    return render(request, 'mock_galaxy_factory/index.html', {
        'forms': ui_holder.forms(),
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

@require_POST
@researcher_required
def fake_a_job(request):
    # TODO remove me
    parameters = """
<lightcone>
  <database_type>sqlite</database_type>
  <database_name>random.db</database_name>
  <catalogue_geometry>cone</catalogue_geometry>
</lightcone>

<sed>
  <ssp_filename>ssp.ssz</ssp_filename>
  <num_spectra>1221</num_spectra>
  <num_metals>7</num_metals>
</sed>

<filter>
  <waves_filename>wavelengths.dat</waves_filename>
  <filter_filenames>u.dat,v.dat</filter_filenames>
  <vega_filename>A0V_KUR_BB.SED</vega_filename>
</filter>

<skymaker>
  <focal_x>1000</focal_x>
  <focal_y>1000</focal_y>
</skymaker>
    """.strip()
    u = models.User.objects.get(username=request.user)
    j = models.Job(user=u, parameters=parameters)
    j.save()

    messages.info(request, _("You submitted a fake job successfully."))
    return redirect(my_jobs_with_status, status='HELD')  # TODO shouldn't need an empty string for status?
