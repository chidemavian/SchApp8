from myproject.ruffwal.raccount.models import useracc
from django.contrib import admin


class useraccAdmin(admin.ModelAdmin):
    list_display = ('username','password')
    fieldsets = [
        (None, { 'fields': [('username','password')] } ),

   ]

admin.site.register(useracc,useraccAdmin)