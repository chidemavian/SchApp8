from django.conf.urls.defaults import *
from myproject.signals import *
from django.conf import settings
from myproject.sysadmin.views import *
from myproject.setup.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', index),
    url(r'^login/$', index),
    url(r'^header/$', header),
    url(r'^welcome/$', welcomecode),
    url(r'^online/$', online_result),
    url(r'^subject_report/$', subject_report),
    url(r'^student_search/$', search_student),
    url(r'^logout/$', logoutuser),
    url(r'^unauthorised/$', unatho),
    url(r'^uploadlga/$',uploadlocal ),
    url(r'^uploadsubgroup/$',uploadaccsubgrp),
    url(r'^uploadacc/$',uploadacc),
    url(r'^uploadtransaction/$',uploadtransaction),
    url(r'^getchangepassword/$', getchangepassword),
    url(r'^uploadstudent/$',uploadstudent),
    url(r'^uploadbill/$',uploadbill),#to upload bill setup
    url(r'^uploadbillname/$',uploadbillname),#to upload bill name
    url(r'^uploadadditionalbill/$',uploadadditionalbill),#to upload  additional bills
    url(r'^uploadpostedbill/$',uploadpostedbill),#to upload posted bill

    url(r'^changepassword/$', changepassword),
    url(r'^setup/', include('myproject.setup.urls')),
    url(r'^student/', include('myproject.student.urls')),
    url(r'^bill/', include('myproject.bill.urls')),
    url(r'^sysadmin/', include('myproject.sysadmin.urls')),
    url(r'^assessment/', include('myproject.assessment.urls')),
    url(r'^SchApp/account/', include('myproject.ruffwal.urls')),
    url(r'^hrmes/', include('myproject.hrm.urls')), #hrmes
    url(r'^hrm/', include('myproject.hrm.urls')),
    url(r'^lesson/', include('myproject.lesson.urls')),
    url(r'^utils/', include('myproject.utilities.urls')),
    url(r'^forum/', include('myproject.forum.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
   # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),

    #url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
