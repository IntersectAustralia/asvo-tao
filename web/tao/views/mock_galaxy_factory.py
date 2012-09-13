from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _

from tao import models
from tao.decorators import admin_required, researcher_required, set_tab
from tao.forms import MockGalaxyFactoryForm


@set_tab('mgf')
@researcher_required
def index(request):
    if request.method == 'POST':
        u = models.User.objects.get(username=request.user)
        j = models.Job(user=u, description=str(request.POST))
        j.save()
        messages.info(request, _("Your job was submitted successfully."))
        return redirect(submitted_jobs)
    else:
        return render(request, 'mock_galaxy_factory/index.html', {
            'form': MockGalaxyFactoryForm(),
        })


@set_tab('mgf')
@researcher_required
def submitted_jobs(request):
    return render(request, 'mock_galaxy_factory/submitted_jobs.html', {
        'jobs': models.Job.objects.filter(user=request.user),
    })
