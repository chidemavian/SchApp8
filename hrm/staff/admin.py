from myproject.hrm.staff.models import *
from django.contrib import admin

class redeploymentadmin(admin.ModelAdmin):
    list_display = ('staffid','staffname','sex','currentdept','newdept','recdate','userid')
    fieldsets = [
        (None, { 'fields': [('staffid','staffname','sex','currentdept','newdept','recdate','userid')] } ),

   ]
class locationadmin(admin.ModelAdmin):
    list_display = ('staffid','staffname','sex','currentlocation','newlocation','recdate','userid')
    fieldsets = [
        (None, { 'fields': [('staffid','staffname','sex','currentlocation','newlocation','recdate','userid')] } ),

   ]

class promotionadmin(admin.ModelAdmin):
    list_display = ('staffid','staffname','sex','olddesignation','newdesignation','recdate','userid')
    fieldsets = [
        (None, { 'fields': [('staffid','staffname','sex','olddesignation','newdesignation','recdate','userid')] } ),

   ]

class terminationadmin(admin.ModelAdmin):
    list_display = ('staffid','staffname','sex','resdate','recdate','userid')
    fieldsets = [
        (None, { 'fields': [('staffid','staffname','sex','resdate','recdate','userid')] } ),

   ]
class resignationadmin(admin.ModelAdmin):
    list_display = ('staffid','staffname','sex','resdate','recdate','userid')
    fieldsets = [
        (None, { 'fields': [('staffid','staffname','sex','resdate','recdate','userid')] } ),

   ]
class retirementadmin(admin.ModelAdmin):
    list_display = ('staffid','staffname','sex','resdate','recdate','userid')
    fieldsets = [
        (None, { 'fields': [('staffid','staffname','sex','resdate','recdate','userid')] } ),

   ]





admin.site.register(redept,redeploymentadmin)
admin.site.register(relocate,locationadmin)
admin.site.register(tblpromotion,promotionadmin)
admin.site.register(tbltermination,terminationadmin)
admin.site.register(tblresignation,resignationadmin)
admin.site.register(tblretirement,retirementadmin)