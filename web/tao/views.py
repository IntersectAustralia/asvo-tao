from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
import inspect


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_active = False
            new_user.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {
        'form': form,
    })
