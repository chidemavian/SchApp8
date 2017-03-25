from myproject.ruffwal.newyear.models import *
from django.contrib import admin


class tbltempAdmin(admin.ModelAdmin):
    list_display = ('cusname','cuscode','amount','particular','accname','acccode','userid','drcr')
    fieldsets = [
        (None, { 'fields': [('cusname','cuscode','amount','particular','accname','acccode','userid','drcr')] } ),

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

class tbltransatemp(admin.ModelAdmin):
    list_display = ('accname','acccode','debit','credit','balance','transid','transdate','particulars','refno','groupname','subname','userid','recid')
    fieldsets = [
        (None, { 'fields': [('accname','acccode','debit','credit','balance','transid','transdate','particulars','refno','groupname','subname','userid','recid')] } ),

   ]


admin.site.register(tbltemp1,tbltempAdmin)
admin.site.register(tbltempreceipt1,tbltempreceiptAdmin)
admin.site.register(tbltemppayment1,tbltemppaymentAdmin)
admin.site.register(tbljournal1,tbltempjournalAdmin)
admin.site.register(tblstandard1,tbltempstandardAdmin)
admin.site.register(tblstandarddate1,tblstandardpostAdmin)
admin.site.register(tbltransactiontemp,tbltransatemp)