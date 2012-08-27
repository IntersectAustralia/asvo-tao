from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
import inspect

from .forms import UserCreationForm


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {
        'form': form,
    })

@login_required
def mock_galaxy_factory(request):
    return render(request, 'mock_galaxy_factory.html')

@staff_member_required
def admin_index(request):
    return render(request, 'admin_index.html')

@staff_member_required
def access_requests(request):
    return render(request, 'access_requests.html', {
        'users': User.objects.all()
    })
