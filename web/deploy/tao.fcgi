
##!path-to-virtualenv/python
import sys, os

webdir = os.path.abspath(os.path.dirname(sys.argv[0])+'/..')
sys.path.insert(0, webdir)

# Switch to the directory of your project. (Optional.)
os.chdir(webdir)

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "tao.production"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")

