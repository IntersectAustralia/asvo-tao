from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
import django.contrib.auth.views as auth_views
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from . import models

from .forms import UserCreationForm, RejectForm, LoginForm
from django.template.loader import get_template
from django.template.context import Context
from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings


def home(request):
    return render(request, 'home.html')


def login(request):
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)  # expires on browser close
    return auth_views.login(request, authentication_form=LoginForm)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, _("You will receive an email when your request has been approved."))
            return redirect(home)
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
        'users': models.User.objects.filter(is_active=False, userprofile__rejected=False).order_by('-id'),
        'reject_form': RejectForm(),
    })


@staff_member_required
@require_POST
def approve_user(request, user_id):
    u = models.User.objects.get(pk=user_id)
    u.is_active = True
    u.save()
    profile = u.get_profile()

    # Send an email
    plaintext = get_template('emails/approve.txt')
    html = get_template('emails/approve.html')
    d = Context({'title': profile.title, 'first_name': u.first_name, 'last_name': u.last_name})
    plaintext_content = plaintext.render(d)
    html_content = html.render(d)
    msg = EmailMultiAlternatives(settings.EMAIL_ACCEPT_SUBJECT, plaintext_content, settings.EMAIL_FROM_ADDRESS, [u.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send(False)

    return redirect(access_requests)


@staff_member_required
@require_POST
def reject_user(request, user_id):
    u = models.User.objects.get(pk=user_id)
    profile = u.get_profile()
    profile.rejected = True
    profile.save()

    # Send an email
    reason = request.POST.__getitem__('reason')
    plaintext = get_template('emails/reject.txt')
    html = get_template('emails/reject.html')
    d = Context({'title': profile.title, 'first_name': u.first_name, 'last_name': u.last_name, 'reason': reason})
    plaintext_content = plaintext.render(d)
    html_content = html.render(d)
    msg = EmailMultiAlternatives(settings.EMAIL_REJECT_SUBJECT, plaintext_content, settings.EMAIL_FROM_ADDRESS, [u.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send(False)

    return redirect(access_requests)
