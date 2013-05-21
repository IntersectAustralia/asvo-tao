
import sys
# print sys.path
from docutils import core

lines = [line.rstrip('\n') for line in open(sys.argv[1])]
print core.publish_parts(lines, writer_name='html')['html_body']
# print lines