"""
==================
tao.mail
==================

Helper to send email
"""

from django.conf import settings
from django.template.loader import get_template
from django.core.mail.message import EmailMultiAlternatives


def send_mail(template_name, context, subject, to_addrs, from_addr=None):
    if from_addr is None:
        from_addr = settings.EMAIL_FROM_ADDRESS

    plaintext = get_template('emails/{template_name}.txt'.format(template_name=template_name))
    html = get_template('emails/{template_name}.html'.format(template_name=template_name))
    plaintext_content = plaintext.render(context)
    html_content = html.render(context)

    msg = EmailMultiAlternatives(subject, plaintext_content, from_addr, to_addrs)
    msg.attach_alternative(html_content, 'text/html')

    msg.send(fail_silently=False)
