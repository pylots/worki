import os, sys, site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/sites/rekoi/venv/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/sites/rekoi/prod/site')
prodir = os.path.dirname(__file__)
sys.path.append( prodir )
os.environ['DJANGO_SETTINGS_MODULE'] = 'worki.settings.devel'

# Activate your virtual env
activate_env=os.path.expanduser("/sites/rekoi/venv/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()