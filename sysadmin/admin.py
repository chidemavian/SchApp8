__author__ = 'metro'

from django.contrib import admin
from myproject.sysadmin.models import *

admin.site.register([ClassTeacher, subjectteacher, userprofile,currentsession,Principal])
