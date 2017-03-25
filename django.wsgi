import os, sys  
sys.path.append('C:/windows/www/SchApp/myproject/')
sys.path.append('C:/windows/www/SchApp')
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'  
import django.core.handlers.wsgi  
application = django.core.handlers.wsgi.WSGIHandler()  
