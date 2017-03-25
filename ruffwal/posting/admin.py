from myproject.ruffwal.posting.models import *
from django.contrib import admin


class tbltempAdmin(admin.ModelAdmin):
    list_display = ('cusname','cuscode','amount','particular','accname','acccode','userid','drcr')
    fieldsets = [
        (None, { 'fields': [('cusname','cuscode','amount','particular','accname','acccode','userid','drcr')] } ),

   ]

class tbltransa(admin.ModelAdmin):
    list_display = ('accname','acccode','debit','credit','balance','transid','transdate','particulars','refno','groupname','subname','userid','recid')
    fieldsets = [
        (None, { 'fields': [('accname','acccode','debit','credit','balance','transid','transdate','particulars','refno','groupname','subname','userid','recid')] } ),

   ]

class tbltempreceiptAdmin(admin.ModelAdmin):
    list_display = ('cusname','cuscode','amount','particular','accname','acccode','userid','drcr')
    fieldsets = [
        (None, { 'fields': [('cusname','cuscode','amount','particular','accname','acccode','userid','drcr')] } ),

   ]


class tbltemppaymentAdmin(admin.ModelAdmin):
    list_display = ('cusname','cuscode','amount','particular','accname','acccode','userid','drcr')
    fieldsets = [
        (None, { 'fields': [('cusname','cuscode','amount','particular','accname','acccode','userid','drcr')] } ),

   ]

class tbltempjournalAdmin(admin.ModelAdmin):
    list_display = ('accname','acccode','particular','dr','cr','refno','userid')
    fieldsets = [
        (None, { 'fields': [('accname','acccode','particular','dr','cr','refno','userid')] } ),

   ]

class tbltempstandardAdmin(admin.ModelAdmin):
    list_display = ('accname','acccode','particular','amount','userid','refno','craccname','cracccode','duration')
    fieldsets = [
        (None, { 'fields': [('accname','acccode','particular','amount','userid','refno','craccname','cracccode','duration')] } ),

   ]

class tblstandardpostAdmin(admin.ModelAdmin):
    list_display = ('transdate','userid')
    fieldsets = [
        (None, { 'fields': [('transdate','userid')] } ),

   ]


admin.site.register(tbltemp,tbltempAdmin)
admin.site.register(tbltransaction,tbltransa)
admin.site.register(tbltempreceipt,tbltempreceiptAdmin)
admin.site.register(tbltemppayment,tbltemppaymentAdmin)
admin.site.register(tbljournal,tbltempjournalAdmin)
admin.site.register(tblstandard,tbltempstandardAdmin)
admin.site.register(tblstandarddate,tblstandardpostAdmin)
