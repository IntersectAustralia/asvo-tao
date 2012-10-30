from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _

from django.views.decorators.http import require_POST

from tao import models
from tao.decorators import admin_required, researcher_required, set_tab
from tao.forms import MockGalaxyFactoryForm


@set_tab('mgf')
@researcher_required
def index(request):
    if request.method == 'POST':
        form = MockGalaxyFactoryForm(request.POST)
        if form.is_valid():
            u = models.User.objects.get(username=request.user)
            j = form.save(u)
            
            messages.info(request, _("Your job was submitted successfully."))
            return redirect(my_jobs_with_status)
    else:
        form = MockGalaxyFactoryForm()
        
    return render(request, 'mock_galaxy_factory/index.html', {
        'form': form,
        'simulations': models.Simulation.objects.all(),
        'galaxy_models': models.GalaxyModel.objects.all(),
    })


@set_tab('mgf')
@researcher_required
def my_jobs_with_status(request, status=None):
    user_jobs = models.Job.objects.filter(user=request.user).order_by('-created_time')
    if status:
        filtered_jobs = user_jobs.filter(status=status)
    else:
        filtered_jobs = user_jobs

    return render(request, 'mock_galaxy_factory/submitted_jobs.html', {
        'jobs': filtered_jobs,
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
  <box_type>cone</box_type>
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
    return redirect(my_jobs_with_status, status='')  # TODO shouldn't need an empty string for status?
