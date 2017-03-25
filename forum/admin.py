#  <bb6xt@yahoo.com>


from django.contrib.admin import site
from myproject.forum.models import *
from django.contrib import admin

class useradmin(admin.ModelAdmin):
    list_display = ('name','email','password','active','photo','control')
    fieldsets = [(None, { 'fields': [('name','email','password','active','photo','control')] } ),]

site.register(useracc,useradmin)
