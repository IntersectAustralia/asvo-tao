from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.template.context import Context
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_POST

from tao import models
from tao.decorators import researcher_required, admin_required
from tao.forms import UserCreationForm, RejectForm, LoginForm
from tao.mail import send_mail
from tao.pagination import paginate

import logging

logger = logging.getLogger(__name__)


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


@admin_required
def admin_index(request):
    return render(request, 'admin_index.html')


@admin_required
def access_requests(request):
    user_list = models.User.objects.filter(is_active=False, userprofile__rejected=False).order_by('-id')
    users = paginate(user_list, request.GET.get('page'))

    return render(request, 'access_requests.html', {
        'users': users,
        'reject_form': RejectForm(),
    })


@admin_required
@require_POST
def approve_user(request, user_id):
    u = models.User.objects.get(pk=user_id)
    u.is_active = True
    u.save()
    profile = u.get_profile()

    template_name = 'approve'
    subject = settings.EMAIL_ACCEPT_SUBJECT
    to_addrs = [u.email]
    context = Context({'title': profile.title, 'first_name': u.first_name, 'last_name': u.last_name})

    send_mail(template_name, context, subject, to_addrs)

    return redirect(access_requests)


@admin_required
@require_POST
def reject_user(request, user_id):
    u = models.User.objects.get(pk=user_id)
    profile = u.get_profile()
    profile.rejected = True
    profile.save()

    reason = request.POST['reason']

    template_name = 'reject'
    context = Context({'title': profile.title, 'first_name': u.first_name, 'last_name': u.last_name, 'reason': reason})
    subject = settings.EMAIL_REJECT_SUBJECT
    to_addrs = [u.email]

    send_mail(template_name, context, subject, to_addrs)

    return redirect(access_requests)
