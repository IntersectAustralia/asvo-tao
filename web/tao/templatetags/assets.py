from django import template

register = template.Library()
from django.core.urlresolvers import reverse


@register.simple_tag
def js_asset(path):
    js_path = 'js/%s' % path

    asset_path = reverse('asset', args=[js_path])

    return "<script src='%s'></script>" % asset_path

@register.simple_tag
def json_ctx():
    return reverse('json_ctx')
