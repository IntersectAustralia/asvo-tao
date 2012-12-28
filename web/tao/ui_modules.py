from django.conf import settings


def form_classes_and_prefixes():
  return [(__import__('taoui_%s.forms' % x).forms.Form, x) for x in settings.MODULES]
