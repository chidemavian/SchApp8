from django.contrib import admin
from myproject.hrm.payroll.models import *
class tblpayrollAdmin(admin.ModelAdmin):
    list_display = ('staffid','staffname','designation','allamount','alldes','dedamount','deddes','wokingday','recdate','schdes','schamount','outbal')
    fieldsets = [
        (None, { 'fields': [('staffid','staffname','designation','allamount','alldes','dedamount','deddes','wokingday','recdate','schdes','schamount','outbal')] } ),

    ]

class tblbankdetailsAdmin(admin.ModelAdmin):
    list_display = ('staffid','staffname','bankname','accountno')
    fieldsets = [
        (None, { 'fields': [('staffid','staffname','bankname','accountno')] } ),

    ]

admin.site.register(tblpayroll,tblpayrollAdmin)
admin.site.register(tblbankdetails,tblbankdetailsAdmin)
admin.site.register(tblpayrollpension)
