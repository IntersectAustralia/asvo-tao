from django.contrib.auth import logout
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
