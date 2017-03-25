from myproject.ruffwal.rsetup.models import *
from django.contrib import admin

class companyadmin(admin.ModelAdmin):
    list_display = ('name','address','picture','phonenumber','email','website')
    fieldsets = [
        (None, { 'fields': [('name','address','picture','phonenumber','email','website')] } ),
        ]

class tblgroupAdmin(admin.ModelAdmin):
    list_display = ('groupname','groupcode')
    fieldsets = [
        (None, { 'fields': [('groupname','groupcode')] } ),

   ]

class tblsubgroupAdmin(admin.ModelAdmin):
    list_display = ('subgroupname','subgroupcode','userid','groupname','groupcode')
    fieldsets = [
        (None, { 'fields': [('subgroupname','subgroupcode','userid','groupname','groupcode')] } ),

   ]

class tblaccountAdmin(admin.ModelAdmin):
    list_display = ('accname','acccode','accbal','subgroupname','subgroupcode','userid','groupname','groupcode','accstatus')
    fieldsets = [
        (None, { 'fields': [('accname','acccode','accbal','subgroupname','subgroupcode','userid','groupname','groupcode','accstatus')] } ),

   ]

class receivablesadmin(admin.ModelAdmin):
    list_display = ('accname','acccode','address','phoneno','userid')
    fieldsets = [
        (None, { 'fields': [('accname','acccode','address','phoneno','userid')] } ),

   ]
class payablesadmin(admin.ModelAdmin):
    list_display = ('accname','acccode','address','phoneno','userid')
    fieldsets = [
        (None, { 'fields': [('accname','acccode','address','phoneno','userid')] } ),

   ]

class stockadmin(admin.ModelAdmin):
    list_display = ('stockname','acccode','accbal','subname','subcode','qtybal','userid','avgprice')
    fieldsets = [
        (None, { 'fields': [('stockname','acccode','accbal','subname','subcode','qtybal','userid','avgprice')] } ),

   ]

admin.site.register(tblcompanyinfo,companyadmin)
admin.site.register(tblgroup,tblgroupAdmin)
admin.site.register(tblsubgroup,tblsubgroupAdmin)
admin.site.register(tblaccount,tblaccountAdmin)
admin.site.register(tblstock,stockadmin)
admin.site.register(receivables,receivablesadmin)
admin.site.register(payables,payablesadmin)
admin.site.register(staffonloan,receivablesadmin)