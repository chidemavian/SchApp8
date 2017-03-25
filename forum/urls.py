from django.conf.urls.defaults import patterns, include, url
from views import *

urlpatterns = patterns('myproject.forum.views',
    # Examples:
    url(r'^$', 'home', name='forum_home'),
    url(r'^main/$', 'welcomecode', name='forum_welcome'),
    url(r'^editprofile/$', 'editprofile', name='forum_edit profile'),
    url(r'^logout/$', 'logoutuser', name='forum_logout'),
    url(r'^registration/$', 'registration', name='forum_reg'),
    url(r'^successful/$', 'successful', name='forum_registration success'),
    url(r'^registration/activation/(?P<username>\w{0,550})/$', 'activation', name='forum_regactivation'),
    url(r'^recover password/$', 'recoverpassword', name='forum_recover password'),
    url(r'^comment/(\w+)/$', 'yourcomments', name='forum_comments'),


)
