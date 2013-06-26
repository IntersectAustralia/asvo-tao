#!/usr/bin/env python

import sys
from docutils import core

with open(sys.argv[1]) as f:
    content = f.readlines()
a_line = ''.join(content)
html = core.publish_string(source=a_line, writer_name='html')
html = html[html.find('<body>')+6:html.find('</body>')].strip()
print html

