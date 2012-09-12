from django.shortcuts import render, redirect

from tao import models, datasets
from tao.decorators import researcher_required, admin_required


@researcher_required
def index(request):
    if request.method == 'POST':
        u = models.User.objects.get(username=request.user)
        for x in request.POST.items():
            print x
        j = models.Job(user=u, description=str(request.POST))
        j.save()
        return redirect(submitted_jobs)
    else:
        return render(request, 'mock_galaxy_factory/index.html', {
            'dark_matter_simulations': datasets.dark_matter_simulations(),
        })

@researcher_required
def submitted_jobs(request):
    return render(request, 'mock_galaxy_factory/submitted_jobs.html', {
        'jobs': models.Job.objects.filter(user=request.user),
    })
