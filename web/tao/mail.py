"""
==================
tao.mail
==================

Helper to send email
"""

from django.conf import settings
from django.template import Template
from django.template.context import Context
from django.core.mail.message import EmailMultiAlternatives

def send_mail(template_name, context, subject, to_addrs, bcc, from_addr=None):
    from tao.models import GlobalParameter
    if from_addr is None:
        from_addr = settings.EMAIL_FROM_ADDRESS

    if type(context) == dict:
        context = Context(context)

    try:
        html_mail = GlobalParameter.objects.get(parameter_name='{template_name}.html'.format(template_name=template_name))
        html_content = Template(html_mail.parameter_value).render(context)
    except GlobalParameter.DoesNotExist:
        html_content = None

    try:
        text_mail = GlobalParameter.objects.get(parameter_name='{template_name}.txt'.format(template_name=template_name))
        text_content = Template(text_mail.parameter_value).render(context)
        msg = EmailMultiAlternatives(subject, text_content, from_addr, to_addrs, bcc=bcc)
        if html_content is not None:
            msg.attach_alternative(html_content, 'text/html')
        msg.send(fail_silently=False)
    except GlobalParameter.DoesNotExist:
        msg = EmailMultiAlternatives("CONFIGURATION ERROR", "Template {template_name}.txt is not found".format(template_name=template_name), from_addr, (from_addr,))
        msg.send(fail_silently=False)
