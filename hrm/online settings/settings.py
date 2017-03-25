# Django settings for orile project.
import os
import sys
SFILE = __file__
SPATH1 = os.path.normpath(os.path.dirname(SFILE))


# Django settings for gradlist project.
SPATH = os.path.realpath(os.path.dirname(__file__))
DEBUG = True
TEMPLATE_DEBUG = DEBUG


ADMINS = (
     ('abaegbu mathew', 'adysys@yahoo.com'),
) #wale@ruffwal.com

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'ruffwal_capital'             # Or path to database file if using sqlite3.
DATABASE_USER = 'ruffwal_capital'             # Not used with sqlite3.
DATABASE_PASSWORD = 'ruffsadmin'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = "/home/ruffwal/webapps/static_media5/"#os.path.join(SPATH, '/static') #"/home/ruffwal/webapps/static_media/"
STATIC_ROOT = "/home/ruffwal/webapps/static_media5/"#os.path.join(SPATH, 'static_media/') #
STATIC_URL =  'http://capitalexpert.ruffwal.com/static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
SITE_URL = 'http://capitalexpert.ruffwal.com/'
#MEDIA_URL = 'http://127.0.0.1:8000/static/'
LOGIN_REDIRECT_URL ='/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = 'http://capitalexpert.ruffwal.com/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'k9hen(791sx)w6e&l-@j8l@vw)+8jhul9ypqu74#f+#e=nr_wn'

STATICFILES_DIRS = (
    #'/home/ruffwal/webapps/django_ruffwal/myproject/static/img',
    # '/home/ruffwal/webapps/django_ruffwal/myproject/static/news',
    #'/path/to/other/static/files/',
    )

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'pagination.middleware.PaginationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    )

ROOT_URLCONF = 'myproject.urls'
TPATH = os.path.join(SPATH, 'templates')
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    TPATH
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.sites',
    'myproject.rsetup',
    'myproject.rwreport',
    'myproject.rwadmin',
    'myproject.hrm',
    'myproject.staff',
    'myproject.train',
    'myproject.leave',
    'myproject.payroll',
    'myproject.query',
   
    
   
)

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

EMAIL_USE_TLS = True
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 587
#EMAIL_HOST_USER = 
#EMAIL_HOST_PASSWORD =
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'adysys@yahoo.com'
EMAIL_HOST_PASSWORD = 'thinkbig' 
DEFAULT_FROM_EMAIL = 'adysys@yahoo.com' 
SERVER_EMAIL = 'adysys@yahoo.com' 
