from django import template
register = template.Library()

@register.simple_tag
def data_type_tag(index, data_types):
    return data_types[index]