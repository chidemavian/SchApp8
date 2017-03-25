from myproject.hrm.rcsetup.models import *
from django.contrib import admin

class companyadmin(admin.ModelAdmin):
    list_display = ('name','address','picture')
    fieldsets = [
        (None, { 'fields': [('name','address','picture')] } ),

   ]
class tblallAdmin(admin.ModelAdmin):
    list_display = ('desc','amount','paydes','userid')
    fieldsets = [
        (None, { 'fields': [('desc','amount','paydes','userid')] } ),

    ]

class tbldedAdmin(admin.ModelAdmin):
    list_display = ('desc','amount','paydes','userid')
    fieldsets = [
        (None, { 'fields': [('desc','amount','paydes','userid')] } ),

    ]
class tblspallAdmin(admin.ModelAdmin):
    list_display = ('staffid','staffname','amount','paydes','userid','expiredate')
    fieldsets = [
        (None, { 'fields': [('staffid','staffname','amount','paydes','userid','expiredate')] } ),

    ]

class tblspdedAdmin(admin.ModelAdmin):
    list_display = ('staffid','staffname','amount','paydes','userid')
    fieldsets = [
        (None, { 'fields': [('staffid','staffname','amount','paydes','userid')] } ),

    ]
class tblspdedAdmin(admin.ModelAdmin):
    list_display = ('staffid','staffname','amount','paydes','userid')
    fieldsets = [
        (None, { 'fields': [('staffid','staffname','amount','paydes','userid')] } ),

    ]

class tblcontrolAdmin(admin.ModelAdmin):
    list_display = ('datecreated','userid')
    fieldsets = [
        (None, { 'fields': [('datecreated','userid')] } ),

    ]

class tblstateAdmin(admin.ModelAdmin):
    list_display = ('country','state','userid')
    fieldsets = [
        (None, { 'fields': [('country','state','userid')] } ),

    ]

class tbllocalgovtAdmin(admin.ModelAdmin):
    list_display = ('country','state','localgovt','userid')
    fieldsets = [
        (None, { 'fields': [('country','state','localgovt','userid')] } ),

    ]

admin.site.register(tblcompanyinfo,companyadmin)
admin.site.register(tblallowance,tblallAdmin)
admin.site.register(tbldeduction,tbldedAdmin)
admin.site.register(tblspall,tblspallAdmin)
admin.site.register(tblspded,tblspdedAdmin)
admin.site.register(tblcontrol,tblcontrolAdmin)
admin.site.register(tblstate,tblstateAdmin)
admin.site.register(tbllocalgovt,tbllocalgovtAdmin)
admin.site.register(tblpension)
admin.site.register(tblsavingcode)
admin.site.register(tbllevel)
admin.site.register(tblstep)
admin.site.register(tblloancode)


