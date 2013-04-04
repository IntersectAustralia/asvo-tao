from django import template

register = template.Library()
from django.core.urlresolvers import reverse



@register.simple_tag
def semirequired_field_ids():
    from taoui_light_cone.forms import Form as LightConeForm

    id_prefixed_fields = [('#id_light_cone-%s' % field_name) for field_name in LightConeForm.SEMIREQUIRED_FIELDS]
    return ', '.join(id_prefixed_fields)

@register.simple_tag
def no_filter():
    from tao.forms import NO_FILTER
    return "{'pk':'%s', 'type':'X', 'fields':{'label':'No Filter'}}" % NO_FILTER
