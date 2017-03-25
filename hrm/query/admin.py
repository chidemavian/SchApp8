from myproject.hrm.query.models import *
from django.contrib import admin

class tblsetupadmin(admin.ModelAdmin):
    list_display = ('name','userid')
    fieldsets = [
        (None, { 'fields': [('name','userid')] } ),

    ]
class locationadmin(admin.ModelAdmin):
    list_display = ('staffid','staffname','designation','department','querytype','querydate','querygiver','reasonforquery','actiontaken','userid')
    fieldsets = [
        (None, { 'fields': [('staffid','staffname','designation','department','querytype','querydate','querygiver','reasonforquery','actiontaken','userid')] } ),

    ]

class locationadmin2(admin.ModelAdmin):
    list_display = ('staffid','staffname','querytype','querydate','querygiver','reasonforquery','actiontaken','userid','reasonfordeletion')
    fieldsets = [
        (None, { 'fields': [('staffid','staffname','querytype','querydate','querygiver','reasonforquery','actiontaken','userid','reasonfordeletion')] } ),

    ]

admin.site.register(tblquerysetup,tblsetupadmin)
admin.site.register(tblstaffquery,locationadmin)
admin.site.register(tblstaffquerydeleted,locationadmin2)
