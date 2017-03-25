from myproject.hrm.rcwadmin.models import *
from django.contrib import admin

class tbluseraccadmin(admin.ModelAdmin):
    list_display = ('username','password','createuser','expiredate','status','esetup','eposting','einventory','ewip','ereonciliation','ereport','eadmin')
    fieldsets = [
        (None, { 'fields': [('username','password','createuser','expiredate','status','esetup','eposting','einventory','ewip','ereonciliation','ereport','eadmin')] } ),

   ]
admin.site.register(tbluseracc,tbluseraccadmin)

