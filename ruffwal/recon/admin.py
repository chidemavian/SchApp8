from myproject.ruffwal.recon.models import *
from django.contrib import admin


class unpresentedAdmin(admin.ModelAdmin):
    list_display = ('accname','acccode','debit','credit','balance','transdate','particulars','refno','userid','opeaningbal')
    fieldsets = [
        (None, { 'fields': [('accname','acccode','debit','credit','balance','transdate','particulars','refno','userid','opeaningbal')] } ),

   ]

class upresentedtranstempadmin(admin.ModelAdmin):
    list_display = ('accname','acccode','amount','particulars','refno','userid')
    fieldsets = [
        (None, { 'fields': [('accname','acccode','amount','particulars','refno','userid')] } ),

   ]

class uncreditedAdmin(admin.ModelAdmin):
    list_display = ('accname','acccode','debit','credit','balance','transdate','particulars','refno','userid','opeaningbal')
    fieldsets = [
        (None, { 'fields': [('accname','acccode','debit','credit','balance','transdate','particulars','refno','userid','opeaningbal')] } ),

   ]

class uncreditedtempadmin(admin.ModelAdmin):
    list_display = ('accname','acccode','amount','particulars','refno','userid')
    fieldsets = [
        (None, { 'fields': [('accname','acccode','amount','particulars','refno','userid')] } ),

   ]

class reconstaadmin(admin.ModelAdmin):
    list_display = ('name','amount','dispgr','transdate')
    fieldsets = [
        (None, { 'fields': [('name','amount','dispgr','transdate')] } ),

   ]

admin.site.register(upresentedtrans,unpresentedAdmin)
admin.site.register(upresentedtranstemp,upresentedtranstempadmin)
admin.site.register(uncreditedtrans,uncreditedAdmin)
admin.site.register(upcreditedtranstemp,uncreditedtempadmin)
admin.site.register(reconstate,reconstaadmin)