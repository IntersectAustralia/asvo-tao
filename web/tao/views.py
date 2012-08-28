from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.decorators.http import require_POST
import inspect


from .forms import UserCreationForm
from . import models


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
        'users': models.User.objects.all()
    })


@staff_member_required
@require_POST
def approve_user(request, user_id):
    u = User.objects.get(pk=user_id)
    u.is_active = True
    u.save()
    return redirect(access_requests)
