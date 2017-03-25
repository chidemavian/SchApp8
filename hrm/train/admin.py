from myproject.hrm.train.models import *
from django.contrib import admin

class tblsetupadmin(admin.ModelAdmin):
    list_display = ('name','userid')
    fieldsets = [
        (None, { 'fields': [('name','userid')] } ),

   ]
class locationadmin(admin.ModelAdmin):
    list_display = ('staffid','staffname','sex','designation','department','traintype','description','duration','commdate','recyear','userid')
    fieldsets = [
        (None, { 'fields': [('staffid','staffname','sex','designation','department','traintype','description','duration','commdate','recyear','userid')] } ),

   ]

admin.site.register(tblsetup,tblsetupadmin)
admin.site.register(tbltraining,locationadmin)
