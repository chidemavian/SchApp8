from myproject.ruffwal.rwreport.models import *
from django.contrib import admin


class tblgroupAdmin(admin.ModelAdmin):
    list_display = ('accname','acccode','debit','credit','startdate','enddate','groupcode','groupname','subname','subcode','userid','recreport','disamt','disamt2','disgrp')
    fieldsets = [
        (None, { 'fields': [('accname','acccode','debit','credit','startdate','enddate','groupcode','groupname','subname','subcode','userid','recreport','disamt','disamt2','disgrp')] } ),
        ]

class tblplAdmin(admin.ModelAdmin):
    list_display = ('sortid','accname','amount','groupname','userid','startdate','enddate','disamt','disgrp')
    fieldsets = [
        (None, { 'fields': [('sortid','accname','amount','groupname','userid','startdate','enddate','disamt','disgrp')] } ),
        ]

class tblbslAdmin(admin.ModelAdmin):
    list_display = ('sortid','accname','amount','amount2','groupname','userid','startdate','enddate','disamt','disamt2','disgrp')
    fieldsets = [
        (None, { 'fields': [('sortid','accname','amount','amount2','groupname','userid','startdate','enddate','disamt','disamt2','disgrp')] } ),
        ]

class tblreceivableslAdmin(admin.ModelAdmin):
    list_display = ('accname','acccode','accbal','disamt','disgrp')
    fieldsets = [
        (None, { 'fields': [('accname','acccode','accbal','disamt','disgrp')] } ),
        ]
class tblpayableAdmin(admin.ModelAdmin):
    list_display = ('accname','acccode','accbal','disamt','disgrp')
    fieldsets = [
        (None, { 'fields': [('accname','acccode','accbal','disamt','disgrp')] } ),
        ]

class tblvalueaddedAdmin(admin.ModelAdmin):
    list_display = ('name','recamount','perc','disgrp','transdate','disgrp1')
    fieldsets = [
        (None, { 'fields': [('name','recamount','perc','disgrp','transdate','disgrp1')] } ),
        ]
class tblstatementAdmin(admin.ModelAdmin):
    list_display = ('accname','acccode','debit','credit','balance','transdate')
    fieldsets = [
        (None, { 'fields': [('accname','acccode','debit','credit','balance','transdate')] } ),
    ]


admin.site.register(tbltrialbalance,tblgroupAdmin)
admin.site.register(tblprofitloss,tblplAdmin)
admin.site.register(tblbalancesheet,tblbslAdmin)
admin.site.register(tblreceiavables,tblreceivableslAdmin)
admin.site.register(tblpayable,tblpayableAdmin)
admin.site.register(tblvalue,tblvalueaddedAdmin)
admin.site.register(tblstatement,tblstatementAdmin)
