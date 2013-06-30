import re
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.core import mail
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template.context import Context
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_POST

from django.utils.http import urlencode as django_urlencode

from tao import models
import tao.settings as tao_settings
from tao.decorators import researcher_required, admin_required, set_tab
from tao.mail import send_mail
from tao.pagination import paginate
from tao.models import TaoUser, GlobalParameter

import logging

logger = logging.getLogger(__name__)

def login(request):
    from tao.forms import LoginForm
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)  # expires on browser close
    q_dict = {'target':request.build_absolute_uri(reverse('home'))}
    aaf_session_url = tao_settings.AAF_SESSION_URL + "?" + django_urlencode(q_dict)
    return auth_views.login(request, authentication_form=LoginForm,extra_context={'aaf_session_url':aaf_session_url})

def fail(request):
    print request.METAS


def register(request):
    if hasattr(request,'user') and hasattr(request.user,'account_registration_status'):
        if request.user.account_registration_status != TaoUser.RS_EMPTY:
            return redirect(account_status)
    from tao.forms import UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            
            admin_emails = TaoUser.objects.admin_emails()
            context = Context({
                          'pending_requests_url': request.build_absolute_uri(reverse('access_requests')),
                          'user': form.cleaned_data
                      })
            send_mail("registration", context, "Registration submitted", admin_emails)
            
            messages.info(request, _("You will receive an email when your request has been approved."))
            return redirect(home)
    else:
        form = UserCreationForm(user=request.user)
        
    return render(request, "register.html", {
        'form': form,
        'user': request.user,
    })

def account_status(request):
    if hasattr(request,'user') and hasattr(request.user,'account_registration_status'):
        if request.user.account_registration_status == TaoUser.RS_EMPTY:
            return redirect(register)
    else:
        return redirect(home)
    return render(request, "account_status.html", {
        'user': request.user
    })

@set_tab('home')
def home(request):
    if hasattr(request,'user') and hasattr(request.user,'account_registration_status'):
        if request.user.account_registration_status == TaoUser.RS_EMPTY:
            return redirect(register)
        elif request.user.account_registration_status == TaoUser.RS_PENDING:
            return redirect(account_status)
    return render(request, 'home.html')


#@aaf_empty_required
#def register_aaf(request):
#    pass

#@aaf_registered_required
#def registration_view(request):
#    pass


@admin_required
def admin_index(request):
    return render(request, 'admin_index.html')


@admin_required
def access_requests(request):
    from tao.forms import RejectForm
    user_list = models.TaoUser.objects.filter(is_active=False, userprofile__rejected=False).order_by('-id')
    users = paginate(user_list, request.GET.get('page'))

    return render(request, 'access_requests.html', {
        'users': users,
        'reject_form': RejectForm(),
    })

@admin_required
@require_POST
def approve_user(request, user_id):
    u = models.TaoUser.objects.get(pk=user_id)
    u.is_active = True
    u.save()
    profile = u.get_profile()

    template_name = 'approve'
    subject = settings.EMAIL_ACCEPT_SUBJECT
    to_addrs = [u.email]
    context = Context({
        'title': profile.title,
        'first_name': u.first_name,
        'last_name': u.last_name,
        'login_url': request.build_absolute_uri(reverse('login')),
    })

    send_mail(template_name, context, subject, to_addrs)

    return redirect(access_requests)


@admin_required
@require_POST
def reject_user(request, user_id):
    u = models.TaoUser.objects.get(pk=user_id)
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

@researcher_required
@set_tab('support')
def support(request):
    from tao.forms import SupportForm
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            to_addrs = _get_support_recipients()
            context = Context({'subject': form.cleaned_data['subject'], 'message': form.cleaned_data['message'], 'user': request.user})
            username = request.user.username
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            user_email = models.User.objects.get(username=username).email
            logger.info('Support email from ' + username)
            logger.info('Subject: ' + subject)
            logger.info('Message: ' + message)
            send_mail('support-template', context, 'TAO Support: ' + subject, [user_email], bcc=to_addrs)
            return render(request, 'email_sent.html')
    else:
        form = SupportForm()

    return render(request, 'support.html', {
        'form': form,
    })

def handle_403(request):
    return render(request, '403.html', status=403)

def _get_support_recipients():
    recipients = GlobalParameter.objects.get(parameter_name='support-recipients')
    return re.split('[ \t\n\r\f\v,]+', recipients.parameter_value)
