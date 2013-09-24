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
def job_ctx():
    return reverse('job_index')

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

@register.simple_tag
def custom_error_message(request_path):
    import re
    job_path = re.compile("^/jobs/\d+$")
    m = job_path.match(request_path)
    if m and m.group() == request_path:
        return 'No such job exists'

@register.simple_tag
def google_analytics():
    if hasattr(settings, 'TRACKING_ID') and settings.TRACKING_ID != '':
        return """
<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', '%s']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>
""" % settings.TRACKING_ID
    else:
        return ''
