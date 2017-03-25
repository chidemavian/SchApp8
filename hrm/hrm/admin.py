from myproject.hrm.hrm.models import *
from django.contrib import admin

class staffadmin(admin.ModelAdmin):
    list_display = ('staffid','name','address','sex','designation','branch','stateoforigin','profession','localgovt','status','department','level','step')
    fieldsets = [
        (None, { 'fields': [('staffid','name','address','sex','designation','branch','stateoforigin','profession','localgovt','status','department','level','step')] } ),

   ]

class staffeduadmin(admin.ModelAdmin):
    list_display = ('staffid','staffname','nameofsch','courseofstu','certificateob','gradeobtained','entryyear','exityear','userid')
    fieldsets = [
        (None, { 'fields': [('staffid','staffname','nameofsch','courseofstu','certificateob','gradeobtained','entryyear','exityear','userid')] } ),

   ]
class staffproffadmin(admin.ModelAdmin):
    list_display = ('staffid','staffname','bodyname','qualification','exityear','userid')
    fieldsets = [
        (None, { 'fields': [('staffid','staffname','bodyname','qualification','exityear','userid')] } ),

   ]
class staffnonpensionadmin(admin.ModelAdmin):
    list_display = ('category','staffname','address','phoneno','nextofkin','sex','session','userid')
    fieldsets = [
        (None, { 'fields': [('category','staffname','address','phoneno','nextofkin','sex','session','userid')] } ),
   ]

admin.site.register(staffrec,staffadmin)
admin.site.register(tblstaffedu,staffeduadmin)
admin.site.register(tblstaffproff,staffproffadmin)
admin.site.register(tblstaffnonpension,staffnonpensionadmin)