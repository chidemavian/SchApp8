from myproject.ruffwal.stock.models import *
from django.contrib import admin


class tbltransAdmin(admin.ModelAdmin):
    list_display = ('stockname','acccode','qty','stin','stout','stbal','unitprice','totalprice','particulars','userid','transcreated')
    fieldsets = [
        (None, { 'fields': [('stockname','acccode','qty','stin','stout','stbal','unitprice','totalprice','particulars','userid','transcreated')] } ),

   ]

admin.site.register(tblstocktransaction,tbltransAdmin)