from myproject.ruffwal.rwadmin.models import *
from django.contrib import admin

class tblplAdmin(admin.ModelAdmin):
    list_display = ('recyear','recamount','recdate','userid')
    fieldsets = [
        (None, { 'fields': [('recyear','recamount','recdate','userid')] } ),
        ]

class tbluseradmin(admin.ModelAdmin):
    list_display = ('username','password','expiredate','staffname','status','esetup','eposting','einventory','ereonciliation','ereport','eadmin')
    fieldsets = [
        (None, { 'fields': [('username','password','expiredate','staffname','status','esetup','eposting','einventory','ereonciliation','ereport','eadmin')] } ),
        ]

class tblcalenderdmin(admin.ModelAdmin):
    list_display = ('startmonth','endtmonth')
    fieldsets = [
        (None, { 'fields': [('startmonth','endtmonth')] } ),
        ]
admin.site.register(tblrollover,tblplAdmin)
admin.site.register(tbluseracc,tbluseradmin)
admin.site.register(tblcalender,tblcalenderdmin)
admin.site.register(tblcontrol)