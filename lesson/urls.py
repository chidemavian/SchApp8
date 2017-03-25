
from django.conf.urls.defaults import patterns, url
from myproject.lesson.views import *

urlpatterns = patterns('myproject.lesson.views',
    # Examples:
    url(r'^wel/$', 'wel'),
    url(r'^set_up/$', 'settopic'),
    url(r'^set_up/gettopajax/$', 'topajax'),
    url(r'^set_up/delete/(\d+)/$', 'deletetopiccode'),
    url(r'^set_up/topic=&?/$', 'settopic'),
    url(r'^setup_sub/$', 'setsub'),
    url(r'^setup_sub/subtopicajaxxxxxx/$', 'filsubtop'),
    #url(r'^setup_sub/lesson/entersub/$', 'subajax'),
    url(r'^setup_sub/topicajax/$', 'gettopajaxx'),
    url(r'^set_up/obj/$', 'setobj'),
    url(r'^set_up/resources/$', 'setresource'),
    url(r'^set_up/students_activities/$', 'sactivities'),
    url(r'^set_up/teacher_activities/$', 'tactivities'),
    url(r'^set_up/lesson_count/$','lesscount'), #for now
    url(r'^setup_sub/getsubj/$', 'getsubajax'),
    url(r'^plan/$', 'setupmyplan'),
    url(r'^note/$', 'setupmynote'),
 )
