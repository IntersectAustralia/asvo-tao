from django.shortcuts import render, redirect

from tao.decorators import researcher_required, admin_required

from tao import models, datasets

@researcher_required
def index(request):
    if request.method == 'POST':
        return redirect(submitted_jobs)
    else:
        return render(request, 'mock_galaxy_factory.html', {
            'dark_matter_simulations': datasets.dark_matter_simulations(),
        })
