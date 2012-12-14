from django import template

register = template.Library()
from django.core.urlresolvers import reverse

from tao.forms import LightConeForm


@register.simple_tag
def semirequired_field_ids():
    id_prefixed_fields = [('#id_%s' % field_name) for field_name in LightConeForm.SEMIREQUIRED_FIELDS]
    return ', '.join(id_prefixed_fields)
