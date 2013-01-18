from django.core import serializers
from django.template import Library
from django.utils.safestring import mark_safe

register = Library()

@register.filter(is_safe=True)
def as_json(object, *args, **kargs):
    return mark_safe(serializers.serialize('json', [object], *args, **kargs)[1:-1])

