from django import template
from django.utils.http import urlencode as django_urlencode
from django.utils.safestring import mark_safe
from django.conf import settings

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

@register.simple_tag
def setting(key):
    if key in ['AAF_DS_URL', 'AFF_APP_ID', 'TAO_VERSION'] and hasattr(settings,key):
        return getattr(settings, key)
    else:
        return '[' + key + ']'

#@register.filter(name='aaf_ds', is_safe=True)
## https://researchdata.ands.org.au/Shibboleth.sso/Login?target=https%3A%2F%2Fresearchdata.ands.org.au%2Fregistry%2Flogin.php%3Fpage%3D
#def aaf_ds(target):
#    q_dict = {'target': target}
#    return mark_safe(settings.AAF_SESSION_URL + "?" + django_urlencode(q_dict))
