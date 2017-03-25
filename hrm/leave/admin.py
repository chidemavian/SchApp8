from myproject.hrm.leave.models import *
from django.contrib import admin
class tblsetupadmin(admin.ModelAdmin):
    list_display = ('name','userid')
    fieldsets = [
        (None, { 'fields': [('name','userid')] } ),

   ]
class locationadmin(admin.ModelAdmin):
    list_display = ('staffid','staffname','sex','designation','department','traintype','description','duration','commdate','enddate','recyear','userid')
    fieldsets = [
        (None, { 'fields': [('staffid','staffname','sex','designation','department','traintype','description','duration','commdate','enddate','recyear','userid')] } ),

   ]

admin.site.register(tblleavesetup,tblsetupadmin)
admin.site.register(tblleave,locationadmin)
