from django import template
from django.conf import settings
from docutils import core

register = template.Library()

@register.simple_tag
def rst_file_to_html(file_path):
    with open(settings.PROJECT_PATH + '/' + file_path) as f:
        content = f.readlines()
    a_line = ''.join(content)
    html = core.publish_string(source=a_line, writer_name='html')
    html = html[html.find('<body>')+6:html.find('</body>')].strip()
    return html

