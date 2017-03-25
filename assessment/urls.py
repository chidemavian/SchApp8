
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('myproject.assessment.views',
    # Examples:
    url(r'^enterca/$', 'enterca'),#Continueous Assessment for Secondary School
    url(r'^getclass/$', 'getclass'),
    url(r'^wel/$', 'wel'),
    url(r'^getarm/$', 'getarm'),
    url(r'^getterm/$', 'getterm'),
    url(r'^getsubject/$', 'getsubject'),
    url(r'^getsubjectless/$', 'getsubjectlesson'),
    url(r'^getstudent/$', 'getstudent'),
    url(r'^editca/(\d+)/$', 'editca'),
    url(r'^editcas/(\d+)/$', 'editcas'),
    url(r'^editcap/(\d+)/$', 'editcapry'),
    url(r'^getsubjectscore/$', 'getsubjectscore'),
    url(r'^getsubjectscorep/$', 'getsubjectscorep'),
    url(r'^affective/$', 'affectivedomain'),
    url(r'^getclassaff/$', 'getclassaff'),
    url(r'^getarmaff/$', 'getarmaff'),
    url(r'^getstudentaff/$', 'getstudentaff'),
    url(r'^getaffective/$', 'getaffective'),
    url(r'^getpsyco/$', 'getpsyco'),
    url(r'^getcomment/$', 'getcomment'),
    url(r'^editcomment/(\d+)/$', 'editcomment'),
    url(r'^editpsyco/(\d+)/$', 'editpsyco'),
    url(r'^editaffective/(\d+)/$', 'editaffective'),
    url(r'^addsubject/$', 'addsubject'),
    url(r'^getstudentsubject/$', 'getstudentsubject'),
    url(r'^getsubject4student/$', 'getsubject4student'),
    url(r'^getmoresubject/$', 'getmoresubject'),
    url(r'^addmoresubject/$', 'addmoresubject'),
    url(r'^deletemoresubject/$', 'deletemoresubject'),
    url(r'^confirmdeletemoresubject/(\d+)/$', 'confirmdeletemoresubject'),
    url(r'^principalcomment/$', 'principalcomment'),
    url(r'^getstudentprinicipalcomment/$', 'getstudentprincipalcomment'),
    url(r'^getprinicipalcomment/$', 'getprincipalcomment'),
    url(r'^editcommentprin/(\d+)/$', 'editcommentprin'),
    url(r'^getstudentacademic/$', 'getstudentacademic'),
    url(r'^entercapry/$', 'addsubject4pry'),#Continueous Assessment for Primary School
    url(r'^primary_assessment/(\w+)/(\w+)/(\w+)/(\w+)/(\w+)/$', 'primary_url'),#primary school redirecting
    url(r'^secondary_assessment/(\w+)/(\w+)/(\w+)/(\w+)/(\w+)/$', 'secondary_url'),#secondary school redirecting
    url(r'^secondary_print_assessment/(\w+)/(\w+)/(\w+)/(\w+)/(\w+)/$', 'secondary_teacher_report'),#secondary school redirecting
    url(r'^getsubject4studentpry/$', 'getsubject4studentpry'),
    url(r'^getclassaffpry/$', 'getclassaffpry'),
    url(r'^reportsheet/$', 'reportsheet'),
    url(r'^mid-term-report/$', 'reportsheetmidterm'),
    url(r'^broadsheet/$', 'broadsheet'),
    url(r'^mid-term-broadsheet/$', 'mid_term_broadsheet'),
    url(r'^access-denied/$', 'unautho'),

)


