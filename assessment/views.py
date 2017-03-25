# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from django.core.serializers.json import simplejson as json
from myproject.assessment.forms import *
from myproject.academics.models import *
from myproject.sysadmin.models import *
from myproject.setup.models import *
from myproject.assessment.getordinal import *
from myproject.assessment.utils import *
from myproject.assessment.bsheet import *
from myproject.utilities.views import *
from django.db.models import Max,Sum
import datetime
from datetime import date
import locale
locale.setlocale(locale.LC_ALL,'')
import xlwt

currse = currentsession.objects.get(id = 1)

sublists=[]

def wel(request):
    if  "userid" in request.session:
        return render_to_response('assessment/success.html')
    else:
        return HttpResponseRedirect('/login/')


def unautho(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =''
        return render_to_response('assessment/unautorise.htm',{'varerr':varerr,'varuser':str(varuser).upper()})
    else:
        return HttpResponseRedirect('/login/')



def enterca(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        varerr =''
        sec = ''
        pry = ''
        for j in appused.objects.all():
            pry = j.primary
            sec = j.secondary
        if sec is True :
            pass
        else:
            return HttpResponseRedirect('/assessment/access-denied/')
        if request.method == 'POST':
            form = caform(request.POST) # A form bound to the POST data
            if form.is_valid():
                session = form.cleaned_data['session']
                klass = form.cleaned_data['klass']
                term = form.cleaned_data['term']
                arm = form.cleaned_data['arm']
                subject = form.cleaned_data['subject']
                return HttpResponseRedirect('/assessment/secondary_print_assessment/%s/%s/%s/%s/%s/'%(str(session).replace('/','j'),str(klass).replace(' ','k'),str(arm).replace(' ','k'),str(subject).replace(' ','z'),str(term).replace(' ','0')))

        else:
            form = caform()
        return render_to_response('assessment/enterca.html',{'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')
"""
def enterca(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        varerr =''
        sec = ''
        pry = ''
        for j in appused.objects.all():
            pry = j.primary
            sec = j.secondary
        if sec is True :
            pass
        else:
            return HttpResponseRedirect('/assessment/access-denied/')
        if request.method == 'POST':
            form = caform(request.POST) # A form bound to the POST data
            if form.is_valid():
                session = form.cleaned_data['session']
                klass = form.cleaned_data['klass']
                term = form.cleaned_data['term']
                arm = form.cleaned_data['arm']
                subject = form.cleaned_data['subject']
                ns = str(subject).replace(' ','z')
                ns = str(subject).replace('$','q')
                return HttpResponseRedirect('/assessment/secondary_print_assessment/%s/%s/%s/%s/%s/'%(str(session).replace('/','j'),str(klass).replace(' ','k'),str(arm).replace(' ','k'),ns,str(term).replace(' ','0')))
        else:
            form = caform()
        return render_to_response('assessment/enterca.html',{'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

"""

def getclass(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state = acccode
                kk = []
                sdic = {}
                data = subjectteacher.objects.filter(teachername = varuser,status = 'ACTIVE',session = state).order_by('klass')
                for j in data:
                    j = j.klass
                    s = {j:j}
                    sdic.update(s)
                klist = sdic.values()
                for p in klist:
                    kk.append(p)
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getarm(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                session,klass = acccode.split(':')
                kk = []
                sdic = {}
                data = subjectteacher.objects.filter(teachername = varuser,status = 'ACTIVE',session = session,klass = klass).order_by('arm')
                for j in data:
                    j = j.arm
                    #print j
                    s = {j:j}
                    sdic.update(s)
                klist = sdic.values()
                for p in klist:
                    kk.append(p)
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getterm(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state = acccode
                kk = []
                sdic = {}
                data = subjectteacher.objects.filter(teachername = varuser,status = 'ACTIVE',session = state).order_by('term')
                for j in data:
                    j = j.term
                    #print j
                    s = {j:j}
                    sdic.update(s)
                klist = sdic.values()
                klist.sort()
                for p in klist:
                    kk.append(p)
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def getsubject(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                #state = acccode
                #print acccode
                session,klass,arm,term = acccode.split(':')
                kk = []
                sdic = {}
                data = subjectteacher.objects.filter(teachername = varuser,status = 'ACTIVE',session = session,klass = klass,arm = arm)
                for j in data:
                    j = j.subject
                    #print j
                    s = {j:j}
                    sdic.update(s)
                klist = sdic.values()
                for p in klist:
                   # print 'The Subject :',p
                    kk.append(p)
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def getsubjectlesson(request):
    if "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr = ""
                post = request.POST.copy()
                acccode = post['userid']
               # state = acccode
                session,klass = acccode.split(':')
                kk = []
                sdic = {}
                data = subjectteacher.objects.filter(teachername = varuser,session=session,klass = klass)
                for j in data:
                    j = j.subject
                    s = {j:j}
                    sdic.update(s)
                kk = sdic.values()
                sublists=kk
                #klist = sdic.values()
                #for p in klist:
                #    kk.append(p)
                return HttpResponse(json.dumps(kk),mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def getstudent(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                session,klass,arm,term, subject= acccode.split(':')
                stlist = []
                if term == 'Third':
                    tday = datetime.date.today()
                    if tday.year < 2212:
                        if tblpin.objects.filter(ydate__year = tday.year):
                           gdate = tblpin.objects.get(ydate__year = tday.year)
                           if tday < gdate.ydate:
                              pass
                           else:
                              gpin = gdate.pin
                              gused = gdate.used
                              k = decrypt1(str(gused))
                              uu = encrypt(k)
                              if str(gpin) == str(uu):
                                 pass
                              else:
                                 return HttpResponseRedirect('/sysadmin/page-expire/%s/'%int(tday.year))
                    else:
                         return HttpResponseRedirect('/sysadmin/page-expire/%s/'%int(tday.year))
                else:
                    pass
                for j in Student.objects.filter(admitted_session = session,admitted_class = klass,admitted_arm = arm,gone = False):
                    if StudentAcademicRecord.objects.filter(student = j,session = session,term = term):
                        st = StudentAcademicRecord.objects.get(student = j,session = session,term = term)
                        if SubjectScore.objects.filter(academic_rec = st,klass = klass,subject = subject,session = session,arm=arm,term =term):
                            gs = SubjectScore.objects.get(academic_rec = st,klass = klass,subject = subject,session = session,arm=arm,term =term)
                            kk = {'id':gs.id,'admissionno':j.admissionno,'third_ca':gs.third_ca,'fourth_ca':gs.fourth_ca,'fullname':j.fullname,'sex':j.sex,'subject':gs.subject,'term':str(term),'first_ca':gs.first_ca,'second_ca':gs.second_ca,'exam_score':gs.exam_score}
                            stlist.append(kk)
                        else:
                            pass
                #data = SubjectScore.objects.filter(subject = subject,klass = klass,arm=arm,term =term,session = session)
                return render_to_response('assessment/ca.html',{'data':stlist})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def editca(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.staffname
        sec = ''
        pry = ''
        for j in appused.objects.all():
            pry = j.primary
            sec = j.secondary
        if sec is True :
            pass
        else:
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails = SubjectScore.objects.get(id = vid)
        admno1 = getdetails.academic_rec.student.admissionno
        klass1 = getdetails.klass
        arm1 = getdetails.arm
        subject1 = getdetails.subject
        session1 = getdetails.session
        term1 = getdetails.term
        if request.method == 'POST':
             ca1 = request.POST['firstca']
             ca2 = request.POST['secondca']
             ca3 = request.POST['thirdca']
             ca4 = request.POST['fourthca']
             exam = request.POST['exam']
             if exam == "":
                 exam = 0
             if ca1 == "":
                 ca1 = 0
             if ca2 == "":
                 ca2 = 0
             if ca3 == "":
                 ca3 = 0
             if ca4 == "":
                 ca4 = 0
             try:
                h = int(exam)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             try:
                 h1 = int(ca1)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             try:
                 h2 = int(ca2)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             try:
                 h3 = int(ca3)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             try:
                 h4 = int(ca4)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             if klass1 =='SS 3' and term1 =='Second':
                 h1 = 0
                 h2 = 0
                 h3 = 0
             elif klass1 =='JS 3' and term1 =='Second':
                 h1 = 0
                 h2 = 0
                 h3 = 0
             else:
                 if h > 70 :
                     h = 0
                 if h1 > 10 :
                     h1 = 0
                 if h2 > 10 :
                     h2 = 0
                 if h3 > 10 :
                     h3 = 0
                 if h4 > 10 :
                     h4 = 0
             getdetails.first_ca = h1
             getdetails.second_ca = h2
             getdetails.third_ca = h3
             getdetails.fourth_ca = h4
        #     getdetails.sixth_ca = h3
        #     getdetails.fifth_ca = h1+h2
             getdetails.exam_score = h
             getdetails.save()
             #**********************getting the class average
             getdetails2 = SubjectScore.objects.get(id = vid)
             admno = getdetails2.academic_rec.student.admissionno
             klass = getdetails2.klass
             arm = getdetails2.arm
             subject = getdetails2.subject
             session = getdetails2.session
             term = getdetails2.term
             fullname = getdetails2.academic_rec.student.fullname
             #************TOTTAL STUDENT IN CLASS offering subject************
             totstudent = SubjectScore.objects.filter(session = session,term = term,klass = klass,arm = arm,subject = subject).count()
             #********************term score total****************
             totsubject = SubjectScore.objects.filter(session = session,term = term,klass = klass,arm = arm,subject = subject).aggregate(Sum('term_score'))
             varrid = totsubject['term_score__sum']
             subavg = varrid/totstudent
             annavg = 0
             if term == 'Third':
                 an = annualaverage(str(admno),str(session),str(arm),str(klass),str(subject))
             SubjectScore.objects.filter(klass = klass,arm = arm,subject = subject,session = session,term = term).update(subject_teacher = uenter.upper(),subject_avg = subavg)
             #***************************getting subject position**************************#
             sp = subjectposition(str(session),str(subject),str(term),str(klass),str(arm))
             #*****************************calculate percentage
             tn = percent(str(session),str(klass),str(arm),str(admno),str(term))
             #***********************getting the class position
             cp = classposition(str(session),str(term),str(klass),str(arm))
             #************getting stream position****************
             cp1 = classposition1(str(session),str(term),str(klass))
             c = klass[0] #if the first alphabet of thee selected class is P FOR PRIMMARY, Y FOR YEAR, B FOR BASIC , N FOR NURSERY C FOR CLASS, L FOR LOWER PRIMARY
             if c.upper() =='P' or c.upper() == 'Y' or c.upper() == 'B' or c.upper() == 'N' or c.upper() == 'C' or c.upper() == 'L':
                 return HttpResponseRedirect('/assessment/primary_assessment/%s/%s/%s/%s/%s/'%(str(session).replace('/','j'),str(klass).replace(' ','k'),str(arm).replace(' ','k'),str(fullname).replace(' ','z'),str(term).replace(' ','0')))
             else:  #for JSS AND SSS
                 #return HttpResponseRedirect('/assessment/enterca/')
                 return HttpResponseRedirect('/assessment/secondary_assessment/%s/%s/%s/%s/%s/'%(str(session).replace('/','j'),str(klass).replace(' ','k'),str(arm).replace(' ','k'),str(subject).replace(' ','z'),str(term).replace(' ','0')))
        else:
            form = caform()
            return render_to_response('assessment/editca.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')


def editcas(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.staffname
        sec = ''
        pry = ''
        for j in appused.objects.all():
            pry = j.primary
            sec = j.secondary
        if sec is True :
            pass
        else:
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails = SubjectScore.objects.get(id = vid)
        admno1 = getdetails.academic_rec.student.admissionno
        klass1 = getdetails.klass
        arm1 = getdetails.arm
        subject1 = getdetails.subject
        session1 = getdetails.session
        term1 = getdetails.term
        if request.method == 'POST':
             ca1 = request.POST['firstca']
             ca2 = request.POST['secondca']
             ca3 = request.POST['thirdca']
       #      ca4 = request.POST['fourthca']
             exam = request.POST['exam']
             if exam == "":
                 exam = 0
             if ca1 == "":
                 ca1 = 0
             if ca2 == "":
                 ca2 = 0
             if ca3 == "":
                 ca3 = 0
        #     if ca4 == "":
        #         ca4 = 0
             try:
                h = int(exam)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             try:
                 h1 = int(ca1)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             try:
                 h2 = int(ca2)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             try:
                 h3 = int(ca3)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
        #     try:
        #         h4 = int(ca4)
        #     except :
        #         return HttpResponseRedirect('/assessment/enterca/')
             if klass1 =='SS 3' and term1 =='Second':
                 h1 = 0
                 h2 = 0
                 h3 = 0
             elif klass1 =='JS 3' and term1 =='Second':
                 h1 = 0
                 h2 = 0
                 h3 = 0
             else:
                 if h > 70 :
                     h = 0
                 if h1 > 10 :
                     h1 = 0
                 if h2 > 10 :
                     h2 = 0
                 if h3 > 10 :
                     h3 = 0
         #        if h4 > 10 :
         #            h4 = 0
             getdetails.first_ca = h1
             getdetails.second_ca = h2
             getdetails.third_ca = h3
         #    getdetails.fourth_ca = h4
        #     getdetails.sixth_ca = h3
        #     getdetails.fifth_ca = h1+h2
             getdetails.exam_score = h
             getdetails.save()
             #**********************getting the class average
             getdetails2 = SubjectScore.objects.get(id = vid)
             admno = getdetails2.academic_rec.student.admissionno
             klass = getdetails2.klass
             arm = getdetails2.arm
             subject = getdetails2.subject
             session = getdetails2.session
             term = getdetails2.term
             fullname = getdetails2.academic_rec.student.fullname
             #************TOTTAL STUDENT IN CLASS offering subject************
             totstudent = SubjectScore.objects.filter(session = session,term = term,klass = klass,arm = arm,subject = subject).count()
             #********************term score total****************
             totsubject = SubjectScore.objects.filter(session = session,term = term,klass = klass,arm = arm,subject = subject).aggregate(Sum('term_score'))
             varrid = totsubject['term_score__sum']
             subavg = varrid/totstudent
             annavg = 0
             if term == 'Third':
                 an = annualaverage(str(admno),str(session),str(arm),str(klass),str(subject))
             SubjectScore.objects.filter(klass = klass,arm = arm,subject = subject,session = session,term = term).update(subject_teacher = uenter.upper(),subject_avg = subavg)
             #***************************getting subject position**************************#
             sp = subjectposition(str(session),str(subject),str(term),str(klass),str(arm))
             #*****************************calculate percentage
             tn = percent(str(session),str(klass),str(arm),str(admno),str(term))
             #***********************getting the class position
             cp = classposition(str(session),str(term),str(klass),str(arm))
             #************getting stream position****************
             cp1 = classposition1(str(session),str(term),str(klass))
             c = klass[0] #if the first alphabet of thee selected class is P FOR PRIMMARY, Y FOR YEAR, B FOR BASIC , N FOR NURSERY C FOR CLASS, L FOR LOWER PRIMARY
             if c.upper() =='P' or c.upper() == 'Y' or c.upper() == 'B' or c.upper() == 'N' or c.upper() == 'C' or c.upper() == 'L':
                 return HttpResponseRedirect('/assessment/primary_assessment/%s/%s/%s/%s/%s/'%(str(session).replace('/','j'),str(klass).replace(' ','k'),str(arm).replace(' ','k'),str(fullname).replace(' ','z'),str(term).replace(' ','0')))
             else:  #for JSS AND SSS
                 #return HttpResponseRedirect('/assessment/enterca/')
                 return HttpResponseRedirect('/assessment/secondary_assessment/%s/%s/%s/%s/%s/'%(str(session).replace('/','j'),str(klass).replace(' ','k'),str(arm).replace(' ','k'),str(subject).replace(' ','z'),str(term).replace(' ','0')))
        else:
            form = caform()
            return render_to_response('assessment/editca.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')




def editcapry(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.staffname
        sec = ''
        pry = ''
        for j in appused.objects.all():
            pry = j.primary
            sec = j.secondary
        if sec is True :
            pass
        else:
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails = SubjectScore.objects.get(id = vid)
        admno1 = getdetails.academic_rec.student.admissionno
        klass1 = getdetails.klass
        arm1 = getdetails.arm
        subject1 = getdetails.subject
        session1 = getdetails.session
        term1 = getdetails.term
        if request.method == 'POST':
             ca1 = request.POST['firstca']
             ca2 = request.POST['secondca']
             ca3 = request.POST['thirdca']
             exam = request.POST['exam']
             if exam == "":
                 exam = 0
             if ca1 == "":
                 ca1 = 0
             if ca2 == "":
                 ca2 = 0
             if ca3 == "":
                 ca3 = 0
             try:
                h = int(exam)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             try:
                 h1 = int(ca1)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             try:
                 h2 = int(ca2)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             try:
                 h3 = int(ca3)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             if klass1 =='SS 3' and term1 =='Second':
                 h1 = 0
                 h2 = 0
                 h3 = 0
             elif klass1 =='JS 3' and term1 =='Second':
                 h1 = 0
                 h2 = 0
                 h3 = 0
             else:
                 if h > 70 :
                     h = 0
                 if h1 > 10 :
                     h1 = 0
                 if h2 > 10 :
                     h2 = 0
                 if h3 > 10 :
                     h3 = 0
             getdetails.first_ca = h1
             getdetails.second_ca = h2
             getdetails.third_ca = h3
             getdetails.sixth_ca = h3
             getdetails.fifth_ca = h1+h2
             getdetails.exam_score = h
             getdetails.save()
             #**********************getting the class average
             getdetails2 = SubjectScore.objects.get(id = vid)
             admno = getdetails2.academic_rec.student.admissionno
             klass = getdetails2.klass
             arm = getdetails2.arm
             subject = getdetails2.subject
             session = getdetails2.session
             term = getdetails2.term
             fullname = getdetails2.academic_rec.student.fullname
             #************TOTTAL STUDENT IN CLASS offering subject************
             totstudent = SubjectScore.objects.filter(session = session,term = term,klass = klass,arm = arm,subject = subject).count()
             #********************term score total****************
             totsubject = SubjectScore.objects.filter(session = session,term = term,klass = klass,arm = arm,subject = subject).aggregate(Sum('term_score'))
             varrid = totsubject['term_score__sum']
             subavg = varrid/totstudent
             annavg = 0
             if term == 'Third':
                 an = annualaverage(str(admno),str(session),str(arm),str(klass),str(subject))
             SubjectScore.objects.filter(klass = klass,arm = arm,subject = subject,session = session,term = term).update(subject_teacher = uenter.upper(),subject_avg = subavg)
             #***************************getting subject position**************************#
             sp = subjectposition(str(session),str(subject),str(term),str(klass),str(arm))
             #*****************************calculate percentage
             tn = percent(str(session),str(klass),str(arm),str(admno),str(term))
             #***********************getting the class position
             cp = classposition(str(session),str(term),str(klass),str(arm))
             #************getting stream position****************
             cp1 = classposition1(str(session),str(term),str(klass))
             c = klass[0] #if the first alphabet of thee selected class is P FOR PRIMMARY, Y FOR YEAR, B FOR BASIC , N FOR NURSERY C FOR CLASS, L FOR LOWER PRIMARY
             if c.upper() =='P' or c.upper() == 'Y' or c.upper() == 'B' or c.upper() == 'N' or c.upper() == 'C' or c.upper() == 'L':
                 return HttpResponseRedirect('/assessment/primary_assessment/%s/%s/%s/%s/%s/'%(str(session).replace('/','j'),str(klass).replace(' ','k'),str(arm).replace(' ','k'),str(fullname).replace(' ','z'),str(term).replace(' ','0')))
             else:  #for JSS AND SSS
                 #return HttpResponseRedirect('/assessment/enterca/')
                 return HttpResponseRedirect('/assessment/secondary_assessment/%s/%s/%s/%s/%s/'%(str(session).replace('/','j'),str(klass).replace(' ','k'),str(arm).replace(' ','k'),str(subject).replace(' ','z'),str(term).replace(' ','0')))
        else:
            form = caform()
            return render_to_response('assessment/editca.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')


"""
def editca(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.staffname
        sec = ''
        pry = ''
        for j in appused.objects.all():
            pry = j.primary
            sec = j.secondary
        #if pry is True :
        #    pass
        #else:
        #    return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails = SubjectScore.objects.get(id = vid)
        if request.method == 'POST':
             ca1 = request.POST['firstca']
             ca2 = request.POST['secondca']
             ca3 = request.POST['thirdca']
             exam = request.POST['exam']
             if exam == "":
                 exam = 0
             if ca1 == "":
                 ca1 = 0
             if ca2 == "":
                 ca2 = 0
             if ca3 == "":
                 ca3 = 0
             try:
                h = float(exam)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             try:
                 h1 = float(ca1)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             try:
                 h2 = float(ca2)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             try:
                 h3 = float(ca3)
             except :
                 return HttpResponseRedirect('/assessment/enterca/')
             if h > 70 :
                 h = 70
             if h1 > 10 :
                 h1 = 10
             if h2 > 10 :
                 h2 = 10
             if h3 > 10 :
                 h3 = 10
             getdetails.first_ca = str(h1)
             getdetails.second_ca = str(h2)
             getdetails.third_ca = str(h3)
             getdetails.exam_score = str(h)
             getdetails.fifth_ca = str(h2)+str(h1)
             getdetails.save()
             #**********************getting the class average
             getdetails2 = SubjectScore.objects.get(id = vid)
             admno = getdetails2.academic_rec.student.admissionno
             klass = getdetails2.klass
             arm = getdetails2.arm
             subject = getdetails2.subject
             session = getdetails2.session
             term = getdetails2.term
             fullname = getdetails2.academic_rec.student.fullname
             totstudent = SubjectScore.objects.filter(klass = klass,arm = arm,subject = subject,session = session,term = term).count()
             totsubject = SubjectScore.objects.filter(klass = klass,arm = arm,subject = subject,session = session,term = term).aggregate(Sum('term_score'))
             varrid = totsubject['term_score__sum']
             subavg = varrid/totstudent
             annavg = 0
             ns1 = str(subject).replace(' ','z')
             ns = str(ns1).replace('$','q')
             if term == 'Third':
                 an = annualaverage(str(admno),str(session),str(arm),str(klass),str(subject))
                 #print 'Annual Average :',an
             SubjectScore.objects.filter(klass = klass,arm = arm,subject = subject,session = session,term = term).update(subject_teacher = uenter.upper(),subject_avg = subavg)

             #*************************************************************************getting subject position
             sp = subjectposition(str(session),str(subject),str(term),str(klass),str(arm))
             #*****************************calculate percentage
             tn = percent(str(session),str(klass),str(arm),str(admno),str(term))
             #***********************getting the class position
             cp = classposition(str(session),str(term),str(klass),str(arm))
             c = klass[0]
             if c.upper() =='P' or c.upper() == 'Y' or c.upper() == 'B' or c.upper() == 'N' or c.upper() == 'C' or c.upper() == 'L':
                #here i redirect to primary page
                 #return primary_url(str(session),str(klass),str(arm),str(fullname),str(term))
                 fname1 = str(fullname).replace(' ','z')
                 fname2 = fname1.replace('-','i')
                 fname  = fname2.replace("'",'u')
                 return HttpResponseRedirect('/assessment/primary_assessment/%s/%s/%s/%s/%s/'%(str(session).replace('/','j'),str(klass).replace(' ','k'),str(arm).replace(' ','k'),fname,str(term).replace(' ','0')))
             else:
                 #return HttpResponseRedirect('/assessment/enterca/')
                 return HttpResponseRedirect('/assessment/secondary_assessment/%s/%s/%s/%s/%s/'%(str(session).replace('/','j'),str(klass).replace(' ','k'),str(arm).replace(' ','k'),ns,str(term).replace(' ','0')))
        else:
            form = caform()
            return render_to_response('assessment/editca.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')
"""

def getsubjectscore(request):
        if  "userid" in request.session:
            if request.is_ajax():
                if request.method == 'POST':
                    varuser = request.session['userid']
                    varerr =""
                    post = request.POST.copy()
                    acccode = post['userid']
                    getdetails = SubjectScore.objects.get(id = acccode)
                    return render_to_response('assessment/editca.html',{'getdetails':getdetails})
                else:
                    gdata = ""
                    return render_to_response('index.html',{'gdata':gdata})
            else:

                gdata = ""
                return render_to_response('getlg.htm',{'gdata':gdata})
        else:
            return HttpResponseRedirect('/login/')

def getsubjectscorep(request):
        if  "userid" in request.session:
            if request.is_ajax():
                if request.method == 'POST':
                    varuser = request.session['userid']
                    varerr =""
                    post = request.POST.copy()
                    acccode = post['userid']
                    getdetails = SubjectScore.objects.get(id = acccode)
                    return render_to_response('assessment/editcap.html',{'getdetails':getdetails})
                else:
                    gdata = ""
                    return render_to_response('index.html',{'gdata':gdata})
            else:

                gdata = ""
                return render_to_response('getlg.htm',{'gdata':gdata})
        else:
            return HttpResponseRedirect('/login/')


def affectivedomain(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        varerr =''
        getdetails =''
        if request.method == 'POST':
            form = caform(request.POST) # A form bound to the POST data
            if form.is_valid():
                expenses = form.cleaned_data['expenses']
                return HttpResponseRedirect('/bill/expensesname/')
        else:
            form = caform()

        return render_to_response('assessment/affective.html',{'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def getclassaff(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state = acccode
                kk = []
                sdic = {}
                data = ClassTeacher.objects.filter(teachername = varuser,session = state).order_by('klass')
                for j in data:
                    j = j.klass
                    s = {j:j}
                    sdic.update(s)
                klist = sdic.values()
                for p in klist:
                    kk.append(p)
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getarmaff(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state = acccode
                kk = []
                sdic = {}
                data = ClassTeacher.objects.filter(teachername = varuser,session = state).order_by('arm')
                for j in data:
                    j = j.arm
                    s = {j:j}
                    sdic.update(s)
                klist = sdic.values()
                for p in klist:
                    kk.append(p)
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getstudentaff(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                session,klass,arm,term = acccode.split(':')
                #print klass
                data = []
                getstu = Student.objects.filter(admitted_class = klass,admitted_arm=arm,admitted_session = session,gone = False).order_by('-sex','fullname')
                for p in getstu:
                    if StudentAcademicRecord.objects.filter(student = p,term = term):
                        comm = StudentAcademicRecord.objects.get(student = p,term = term)
                        affec = AffectiveSkill.objects.get(academic_rec = comm)
                        psyco = PsychomotorSkill.objects.get(academic_rec = comm)
                        stdic = {'studentinfo':p,'comment':comm,'affective':affec,'psyco':psyco}
                        data.append(stdic)
                return render_to_response('assessment/affec.html',{'data':data})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getaffective(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = AffectiveSkill.objects.get(id = acccode)
                return render_to_response('assessment/editaff.html',{'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getaffective2(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.expensedecription
        varerr =''
        getdetails = SubjectScore.objects.get(id = vid)
        if request.method == 'POST':
            ca1 = request.POST['firstca']
            ca2 = request.POST['secondca']
            exam = request.POST['exam']
            if exam == "":
                exam = 0
            if ca1 == "":
                ca1 = 0
            if ca2 == "":
                ca2 = 0
            try:
                h = int(exam)
            except :
                return HttpResponseRedirect('/assessment/enterca/')
            try:
                h1 = int(ca1)
            except :
                return HttpResponseRedirect('/assessment/enterca/')
            try:
                h2 = int(ca2)
            except :
                return HttpResponseRedirect('/assessment/enterca/')
            if h > 60 :
                h = 60
            if h1 > 20 :
                h1 = 20
            if h2 > 20 :
                h2 = 20
            getdetails.first_ca = h1
            getdetails.second_ca = h2
            getdetails.exam_score = h
            getdetails.save()
            return HttpResponseRedirect('/assessment/enterca/')
        else:
            form = caform()

        return render_to_response('assessment/editca.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')


def getpsyco(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = PsychomotorSkill.objects.get(id = acccode)
                return render_to_response('assessment/editpsyco.html',{'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getcomment(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = StudentAcademicRecord.objects.get(id = acccode)
               # print getdetails
                return render_to_response('assessment/editcomment.html',{'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def editcomment(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =''
        getdetails = ''
        if request.method == 'POST':
            comments = request.POST['class_teacher_comment']
            noopen = request.POST['noopen']
            nopresent = request.POST['nopresent']
            nexttem = request.POST['nexttem']
            tday = ''
            if nexttem == "None":
                tday = datetime.date.today()
            else:
                rday,rmonth,ryear = nexttem.split('-')
                tday = date(int(ryear),int(rmonth),int(rday))
            if comments == "" or nopresent =="" or noopen =="":
                return HttpResponseRedirect('/assessment/affective/')
            try:
                j = int(noopen)
            except :
                j = 0
            try:
                k = int(nopresent)
            except :
                k = 0
            l = j - k
            getdetails = StudentAcademicRecord.objects.get(id = vid)
            session = getdetails.session
            term = getdetails.term
            getdetails.class_teacher_comment = comments
            getdetails.days_open = j
            getdetails.days_present = k
            getdetails.days_absent = l
            getdetails.save()
            StudentAcademicRecord.objects.filter(session = session,term = term).update(next_term_start = tday)

            return HttpResponseRedirect('/assessment/affective/')
        else:
            form = caform()
        return render_to_response('assessment/editca.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')

def editpsyco(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =''
        getdetails = ''
        if request.method == 'POST':
            handwriting = request.POST['handwriting']
            games = request.POST['games']
            art = request.POST['art']
            painting = request.POST['painting']
            music = request.POST['music']
            if handwriting == "" or music == "" or painting == "" or art == "" or games == "" :
                return HttpResponseRedirect('/assessment/affective/')
            getdetails = PsychomotorSkill.objects.get(id = vid)
            getdetails.handwriting = handwriting.upper()
            getdetails.games = games.upper()
            getdetails.art = art.upper()
            getdetails.painting = painting.upper()
            getdetails.music = music.upper()
            getdetails.save()
            return HttpResponseRedirect('/assessment/affective/')
        else:
            form = caform()

        return render_to_response('assessment/editca.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')

def editaffective(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =''
        getdetails = ''
        if request.method == 'POST':
            punctuality = request.POST['punctuality']
            neatness = request.POST['neatness']
            honesty = request.POST['honesty']
            initiative = request.POST['initiative']
            self_control = request.POST['self_control']
            reliability = request.POST['reliability']
            perseverance = request.POST['perseverance']
            politeness = request.POST['politeness']
            attentiveness = request.POST['attentiveness']
            rel_with_people = request.POST['rel_with_people']
            cooperation = request.POST['cooperation']
            organizational_ability = request.POST['organizational_ability']
            if punctuality == "" or self_control == "" or initiative == "" or honesty == "" or neatness == "" or reliability == "" or perseverance == "" or politeness == "" or attentiveness == "" or rel_with_people == ""  or cooperation =="" or organizational_ability =="":
                return HttpResponseRedirect('/assessment/affective/')
            getdetails = AffectiveSkill.objects.get(id = vid)
            getdetails.punctuality = punctuality.upper()
            getdetails.neatness = neatness.upper()
            getdetails.honesty = honesty.upper()
            getdetails.initiative = initiative.upper()
            getdetails.self_control = self_control.upper()
            getdetails.reliability = reliability.upper()
            getdetails.perseverance = perseverance.upper()
            getdetails.politeness = politeness.upper()
            getdetails.attentiveness = attentiveness.upper()
            getdetails.rel_with_people = rel_with_people.upper()
            getdetails.cooperation = cooperation.upper()
            getdetails.organizational_ability = organizational_ability.upper()
            getdetails.save()
            return HttpResponseRedirect('/assessment/affective/')
        else:
            form = caform()
        return render_to_response('assessment/editca.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')

def addsubject(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.expensedecription
        if ClassTeacher.objects.filter(teachername = varuser).count() == 0 :
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails =''
        if request.method == 'POST':
            form = addsubjectform(request.POST) # A form bound to the POST data
            if form.is_valid():
                expenses = form.cleaned_data['expenses']
                return HttpResponseRedirect('/bill/expensesname/')
        else:
            form = addsubjectform()
        return render_to_response('assessment/addsubject.html',{'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def getstudentsubject(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                post = request.POST.copy()
                acccode = post['userid']
                session,klass,arm = acccode.split(':')
                kk = []
                data = Student.objects.filter(admitted_session = session,admitted_class = klass,admitted_arm = arm,gone = False).order_by('-sex','fullname')
                for p in data:
                    kk.append(p.fullname)
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def getsubject4student(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                getdetails = ''
                post = request.POST.copy()
                acccode = post['userid']
                session,klass,arm,term,student = acccode.split(':')
                getstu = Student.objects.get(admitted_class = klass,admitted_arm=arm,admitted_session = session,fullname = student,gone = False)
                if StudentAcademicRecord.objects.filter(student = getstu,term = term):
                   comm = StudentAcademicRecord.objects.get(student = getstu,term = term)
                   getdetails = SubjectScore.objects.filter(session = session,klass = klass, arm = arm,term = term,academic_rec = comm).order_by('num')
                return render_to_response('assessment/subject.html',{'getdetails':getdetails,'stuid':getstu.id,'fullname':getstu.fullname})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getmoresubject(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                code = post['userid']
                acccode,ter = str(code).split(':')
                getstu = Student.objects.get(id = acccode)
                session = getstu.admitted_session
                admno = getstu.admissionno
                klass = getstu.admitted_class
                subclass = getstu.subclass
                arm = getstu.admitted_arm
                term = ter
                fullname = getstu.fullname
                #if klass.startswith('N'):
                #    subjectlist = Subject.objects.filter(category = 'Nursery').order_by('num')
                #    fs = {}
                #    for k in subjectlist:
                #        l = {k.subject:k.subject}
                #        fs.update(l)
                #    nlist = fs.keys()
                #elif klass.startswith('Y'):
                #    subjectlist = Subject.objects.filter(category = 'Year').order_by('num')
                #    fs = {}
                #    for k in subjectlist:
                #        l = {k.subject:k.subject}
                #        fs.update(l)
                #    nlist = fs.keys()
                #else:
#                subjectlist = Subject.objects.all().order_by('num')
                subjectlist = Subject.objects.filter(category = subclass, category2 = 'Optional').order_by('num')
                fs = {}
                for k in subjectlist:
                    l = {k.subject:k.subject}
                    fs.update(l)
                nlist = fs.keys()
               # print nlist
                #subjectlist = Subject.objects.filter(category = subclass).order_by('num')
                return render_to_response('assessment/moresubject.html',{'session':session,'fullname':fullname,'admno':admno,'subjectlist':nlist,'klass':klass,'subclass':subclass,'arm':arm,'term':term})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def addmoresubject(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.expensedecription
        varerr =''
        getdetails =''
        term_l = ['First','Second','Third']
        if request.method == 'POST':
            admno = request.POST['admno']
            session = request.POST['session']
            term1 = request.POST['term']
            subclass = request.POST['subclass']
            subjectlist = request.POST['subjectlist']
            stuacarec = Student.objects.get(admissionno = admno,admitted_session = session)
            for term in term_l:
                if StudentAcademicRecord.objects.filter(student = stuacarec,term = term):
                    pass
                else:
                    academic_record = StudentAcademicRecord(student=stuacarec, klass=stuacarec.admitted_class,arm=stuacarec.admitted_arm, term=term, session=stuacarec.admitted_session)
                    academic_record.save()
                    aff =  AffectiveSkill(academic_rec=academic_record)
                    aff.save()
                    psyco = PsychomotorSkill(academic_rec=academic_record)
                    psyco.save()

            gets = Subject.objects.filter(subject = subjectlist)
            num = 1
            for p in gets:
               num = p.num
            if term1 == 'First':
                for term in term_l:
                    stuac = StudentAcademicRecord.objects.get(student = stuacarec,term = term)
                    if SubjectScore.objects.filter(academic_rec = stuac,term = term,subject = subjectlist).count() == 0:
                       SubjectScore(academic_rec = stuac,term = term,subject = subjectlist,num = num,session = session,klass = stuacarec.admitted_class,arm = stuacarec.admitted_arm).save()
                return HttpResponseRedirect('/assessment/addsubject/')
            else:
                stuac = StudentAcademicRecord.objects.get(student = stuacarec,term = term1)
                if SubjectScore.objects.filter(academic_rec = stuac,term = term1,subject = subjectlist).count() == 0:
                    SubjectScore(academic_rec = stuac,term = term1,subject = subjectlist,num = num,session = session,klass = stuacarec.admitted_class,arm = stuacarec.admitted_arm).save()
                    return HttpResponseRedirect('/assessment/addsubject/')
                else:
                   return HttpResponseRedirect('/assessment/addsubject/')
        else:
            form = addsubjectform()
        return render_to_response('assessment/addsubject.html',{'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')


def deletemoresubject(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getstu = SubjectScore.objects.get(id = acccode)
                session = getstu.academic_rec.student.admitted_session
                admno = getstu.academic_rec.student.admissionno
                klass = getstu.academic_rec.student.admitted_class
                subject = getstu.subject
                arm = getstu.academic_rec.student.admitted_arm
                term = getstu.term
                fullname = getstu.academic_rec.student.fullname
                return render_to_response('assessment/deletemoresubject.html',{'session':session,'fullname':fullname,'admno':admno,'klass':klass,'arm':arm,'term':term,'subject':subject,'id':acccode})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def confirmdeletemoresubject(request,pid):
    if  "userid" in request.session:
        getstu = SubjectScore.objects.get(id = pid)
        getstu.delete()
        return HttpResponseRedirect('/assessment/addsubject/')
    else:
        return HttpResponseRedirect('/login/')

def principalcomment(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.expensedecription
        if Principal.objects.filter(teachername = varuser).count() == 0 :
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails =''
        if request.method == 'POST':
            form = caform(request.POST) # A form bound to the POST data
            if form.is_valid():
                expenses = form.cleaned_data['expenses']
                return HttpResponseRedirect('/bill/expensesname/')
        else:
            form = caform()
        return render_to_response('assessment/principalcomment.html',{'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def getstudentprincipalcomment(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                session,klass,arm,term = acccode.split(':')
                #print klass
                data = []
                getstu = Student.objects.filter(admitted_class = klass,admitted_arm=arm,admitted_session = session,gone = False).order_by('-sex','fullname')
                for p in getstu:
                    if StudentAcademicRecord.objects.filter(student = p,term = term):
                        comm = StudentAcademicRecord.objects.get(student = p,term = term)
                        stdic = {'studentinfo':p,'comment':comm}
                        data.append(stdic)
                return render_to_response('assessment/princomment.html',{'data':data})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getprincipalcomment(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = StudentAcademicRecord.objects.get(id = acccode)
                # print getdetails
                return render_to_response('assessment/editprincipalcomment.html',{'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def editcommentprin(request,vid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =''
        getdetails = ''
        if request.method == 'POST':
            comments = request.POST['class_teacher_comment']
            if comments == "":
                return HttpResponseRedirect('/assessment/affective/')
            getdetails = StudentAcademicRecord.objects.get(id = vid)
            getdetails.principal_comment = comments
            getdetails.save()
            return HttpResponseRedirect('/assessment/principalcomment/')
        else:
            form = caform()

        return render_to_response('assessment/editca.html',{'form':form,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')

def getstudentacademic(request):#*******************now
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = StudentAcademicRecord.objects.get(id = acccode)
                academic = SubjectScore.objects.filter(academic_rec = getdetails).order_by('num')
                return render_to_response('assessment/academicrecord.html',{'getdetails':getdetails,'academic':academic})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def addsubject4pry(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.expensedecription
        if ClassTeacher.objects.filter(teachername = varuser).count() == 0 :
            return HttpResponseRedirect('/assessment/access-denied/')
        sec = ''
        pry = ''
        for j in appused.objects.all():
            pry = j.primary
            sec = j.secondary
        if pry is True :
            pass
        else:
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails =''
        if request.method == 'POST':
            form = addsubjectform(request.POST) # A form bound to the POST data
            if form.is_valid():
                expenses = form.cleaned_data['expenses']
                return HttpResponseRedirect('/bill/expensesname/')
        else:
            form = addsubjectform()
        return render_to_response('assessment/capry.html',{'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def getsubject4studentpry(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                getdetails = ''
                post = request.POST.copy()
                acccode = post['userid']
                session,klass,arm,term,student = acccode.split(':')
                getstu = Student.objects.get(admitted_class = klass,admitted_arm=arm,admitted_session = session,fullname = student)
                if StudentAcademicRecord.objects.filter(student = getstu,term = term):
                    comm = StudentAcademicRecord.objects.get(student = getstu,term = term)
                    getdetails = SubjectScore.objects.filter(session = session,klass = klass, arm = arm,term = term,academic_rec = comm).order_by('num')
                return render_to_response('assessment/subjectpry.html',{'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getclassaffpry(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state = acccode
                kk = []
                sdic = {}
                data = ClassTeacher.objects.filter(teachername = varuser,session = state).exclude(klass__startswith ='J').exclude(klass__startswith ='S').order_by('klass')
                for j in data:
                    j = j.klass

                    s = {j:j}
                    sdic.update(s)
                klist = sdic.values()
                for p in klist:
                    kk.append(p)
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def reportsheet(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.reportsheet
        if uenter is False :
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails =''
        school = get_object_or_404(School, pk=1)
        if request.method == 'POST':
            form = reportsheetform(request.POST)
            if form.is_valid():
                session = form.cleaned_data['session']
                klass = form.cleaned_data['klass']
                term = form.cleaned_data['term']
                arm = form.cleaned_data['arm']
                stuno = Student.objects.filter(admitted_session = session,admitted_class = klass,admitted_arm = arm,gone = False).count()
                stuinfo = Student.objects.filter(admitted_session = session,admitted_class = klass,admitted_arm = arm,gone = False).order_by('-sex','fullname')
                replist = []
                varbeg = klass[0]
                getgrading = gradingsys.objects.filter(classsub__startswith = varbeg)
                classtot = 0
                totsub = 0
                totalmarkcount = 0

                if term == "First":
                    for j in stuinfo:
                        if StudentAcademicRecord.objects.filter(student = j,term = term):
                            acaderec = StudentAcademicRecord.objects.get(student = j,term = term)
                            affskill = AffectiveSkill.objects.get(academic_rec = acaderec)
                            psycho = PsychomotorSkill.objects.get(academic_rec = acaderec)
                            subsco = SubjectScore.objects.filter(academic_rec = acaderec,term = term).order_by('num')
                            totsub = SubjectScore.objects.filter(academic_rec = acaderec,term = term).count()
                            totalmark2 = 0
                            if SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term):
                               totalmark = SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).aggregate(Sum('term_score'))
                               totalmark2 = totalmark['term_score__sum']
                            totalmarkcount = SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).count()
                            rtotal = int(totalmark2)
                            if float(totsub) == 0:
                                perc = 0
                            else:
                                perc = float(rtotal)/float(totsub)
                            classtot += rtotal
                            ks = totalmarkcount * 100
                            totsub += ks
                            jdic = {'studentinfo':j,'academic':acaderec,'affective':affskill,'pyscho':psycho,'subject':subsco,'totalmark':rtotal,'getgrading':getgrading,'percentage':locale.format("%.2f",perc,grouping=True)}
                            replist.append(jdic)
                    if classtot == 0 or stuno == 0:
                       clavg = 0.0
                    else:
                        j = classtot/stuno
                        clavg =j/float(totalmarkcount)
                    if klass[0] == 'S':
                        if form.cleaned_data['pdffile']:
                            template ='assessment/reportviewsss.html'
                            context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno}
                            return render_to_pdf(template, context)
                        else:
                            return render_to_response('assessment/reportsss.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno})

                    elif klass[0] == 'N' or klass[0] == 'C' or klass[0] == 'L' or klass[0] == 'P':
                        if form.cleaned_data['pdffile']:
                            template ='assessment/reportnview.html'
                            context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)}
                            return render_to_pdf(template, context)
                        else:
                            return render_to_response('assessment/reportn.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)})

                    else:
                        if form.cleaned_data['pdffile']:
                           template ='assessment/reportview.html'
                           context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)}
                           return render_to_pdf(template, context)
                        else:
                           return render_to_response('assessment/report.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)})
                elif term == 'Second':
                    for j in stuinfo:
                        if StudentAcademicRecord.objects.filter(student = j,term = term):
                            acaderec = StudentAcademicRecord.objects.get(student = j,term = term)
                            acaderec1 = StudentAcademicRecord.objects.get(student = j,term = 'First')
                            affskill = AffectiveSkill.objects.get(academic_rec = acaderec)
                            psycho = PsychomotorSkill.objects.get(academic_rec = acaderec)
                            totsub = SubjectScore.objects.filter(academic_rec = acaderec,term = term).count()
                            totalmarkcount = SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).count()
                            subsco = SubjectScore.objects.filter(academic_rec = acaderec,term = term).order_by('num')
                            secsublist = []
                            sdic = {}
                            for h in subsco:
                                if SubjectScore.objects.filter(academic_rec = acaderec1,term = 'First',subject = h.subject).count() == 0:
                                    fscore = '-'
                                else:
                                    fsc = SubjectScore.objects.get(academic_rec = acaderec1,term = 'First',subject = h.subject)
                                    if float(fsc.term_score) <= 0:
                                        fscore = '-'
                                    else:
                                        fsco = fsc.term_score
                                        fscore = str(fsco)
                                secdic ={'secondterm':h,'firstterm':fscore}
                                secsublist.append(secdic)
                            totalmark2 = 0
                            if SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term):
                                totalmark = SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).aggregate(Sum('term_score'))
                                totalmark2 = totalmark['term_score__sum']
                            rtotal = int(totalmark2)
                            if float(totsub) == 0:
                                perc = 0
                            else:
                                perc = float(rtotal)/float(totsub)
                            classtot += rtotal
                            ks = totalmarkcount * 100
                            totsub += ks

                            #total for first term
                            totalmark2sec = 0
                            rtotalsec = 0
                            if SubjectScore.objects.filter(academic_rec = acaderec1,session = session,term = 'First'):
                                totalmarksec = SubjectScore.objects.filter(academic_rec = acaderec1,session = session,term = 'First').aggregate(Sum('term_score'))
                                totalmark2sec = totalmarksec['term_score__sum']
                                rtotalsec = int(totalmark2sec)

                            jdic = {'studentinfo':j,'academic':acaderec,'affective':affskill,'pyscho':psycho,'subject':secsublist,'totalmark':rtotal,'totalmark1':rtotalsec,'getgrading':getgrading,'percentage':locale.format("%.2f",perc,grouping=True)}
                            replist.append(jdic)
                    if classtot == 0 or stuno == 0:
                            clavg = 0.0
                    else:
                             j = classtot/stuno
                             clavg =j/float(totalmarkcount)
                    if klass[0] == 'S':
                        if form.cleaned_data['pdffile']:
                            template ='assessment/reportviewsecondsss.html'
                            context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno}
                            return render_to_pdf(template, context)
                        else:
                            return render_to_response('assessment/reportsecondsss.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno})
                    elif klass[0] == 'N' or klass[0] == 'C' or klass[0] == 'L':
                        if form.cleaned_data['pdffile']:
                            template ='assessment/reportnviewsecond.html'
                            context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)}
                            return render_to_pdf(template, context)
                        else:
                            return render_to_response('assessment/reportnsecond.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)})

                    else:
                        if form.cleaned_data['pdffile']:
                            template ='assessment/reportviewsecond.html'
                            context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)}
                            return render_to_pdf(template, context)
                        else:
                            return render_to_response('assessment/reportsecond.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)})
                else:
                    stuno = Student.objects.filter(admitted_session = session,admitted_class = klass,gone = False).count()
                    for j in stuinfo:
                        if StudentAcademicRecord.objects.filter(student = j,term = term):
                            acaderec = StudentAcademicRecord.objects.get(student = j,term = term)
                            acaderec1 = StudentAcademicRecord.objects.get(student = j,term = 'First')
                            acaderec2 = StudentAcademicRecord.objects.get(student = j,term = 'Second')
                            affskill = AffectiveSkill.objects.get(academic_rec = acaderec)
                            psycho = PsychomotorSkill.objects.get(academic_rec = acaderec)
                            totsub = SubjectScore.objects.filter(academic_rec = acaderec,term = term).count()
                            totalmarkcount = SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).count()
                            subsco = SubjectScore.objects.filter(academic_rec = acaderec,term = term).order_by('num')
                            secsublist = []
                            sdic = {}
                            for h in subsco:
                                if SubjectScore.objects.filter(academic_rec = acaderec1,term = 'First',subject = h.subject).count() == 0:
                                    fscore = '-'
                                    fscoret = '-'
                                else:
                                    fsc = SubjectScore.objects.get(academic_rec = acaderec1,term = 'First',subject = h.subject)
                                    if float(fsc.term_score) <= 0:
                                        fscore = '-'
                                    else:
                                        fsco = fsc.term_score
                                        fscore = str(fsco)
                                if SubjectScore.objects.filter(academic_rec = acaderec2,term = 'Second',subject = h.subject).count() == 0:
                                    fscoret = '-'
                                else:
                                    fsct = SubjectScore.objects.get(academic_rec = acaderec2,term = 'Second',subject = h.subject)
                                    if float(fsct.term_score) <= 0:
                                        fscoret ='-'
                                    else:
                                        fscot = fsct.term_score
                                        fscoret = str(fscot)
                                secdic ={'thirdterm':h,'firstterm':fscore,'secondterm':fscoret}
                                secsublist.append(secdic)
                            if SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term):
                                totalmark = SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).aggregate(Sum('term_score'))
                                totalmark2 = totalmark['term_score__sum']
                                rtotal = int(totalmark2)
                            else:
                               rtotal = 0
                            if totsub == 0:
                               per = 0
                            else:
                               perc = float(rtotal)/float(totsub)
                            classtot += rtotal
                            ks = totalmarkcount * 100
                            totsub += ks
                            #total for first term
                            totalmark2sec = 0
                            rtotalsec = 0
                            if SubjectScore.objects.filter(academic_rec = acaderec1,session = session,term = 'First'):
                                totalmarksec = SubjectScore.objects.filter(academic_rec = acaderec1,session = session,term = 'First').aggregate(Sum('term_score'))
                                totalmark2sec = totalmarksec['term_score__sum']
                                rtotalsec = int(totalmark2sec)
                            #*********************************************
                            totalmark2sec1 = 0
                            rtotalsec1 = 0
                            if SubjectScore.objects.filter(academic_rec = acaderec2,session = session,term = 'Second'):
                                totalmarksec1 = SubjectScore.objects.filter(academic_rec = acaderec2,session = session,term = 'Second').aggregate(Sum('term_score'))
                                totalmark2sec1 = totalmarksec1['term_score__sum']
                                rtotalsec1 = int(totalmark2sec1)
                            #**************************************************
                            #annual average
                            totalmark24 = 0
                            rtotal4 = 0
                            if SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term):
                                totalmark4 = SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).aggregate(Sum('annual_avg'))
                                totalmark24 = totalmark4['annual_avg__sum']
                                rtotal4 = float(totalmark24)
                            #**********************************************
                            jdic = {'studentinfo':j,'academic':acaderec,'affective':affskill,'pyscho':psycho,'subject':secsublist,'totalmark':rtotal,'totalmark1':rtotalsec,'totalmark2':rtotalsec1,'annualavg':locale.format("%.2f",rtotal4,grouping=True),'getgrading':getgrading,'percentage':locale.format("%.2f",perc,grouping=True)}
                            replist.append(jdic)
                    if classtot == 0 or stuno == 0:
                        clavg = 0.0
                    else:
                        j = classtot/stuno
                        clavg =j/float(totalmarkcount)
                    if klass[0] == 'S':
                        if form.cleaned_data['pdffile']:
                            template ='assessment/reportviewthirdsss.html'
                            context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno}
                            return render_to_pdf(template, context)
                        else:
                            return render_to_response('assessment/reportthirdsss.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno})
                    elif klass[0] == 'N' or klass[0] == 'C' or klass[0] == 'L':
                        if form.cleaned_data['pdffile']:
                            template ='assessment/reportnviewthird.html'
                            context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)}
                            return render_to_pdf(template, context)
                        else:
                            return render_to_response('assessment/reportnthird.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)})

                    else:
                        if form.cleaned_data['pdffile']:
                            template ='assessment/reportviewthird.html'
                            context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)}
                            return render_to_pdf(template, context)
                        else:
                            return render_to_response('assessment/reportthird.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)})
        else:
            form = reportsheetform()
        return render_to_response('assessment/report.html',{'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

#***********************************************treating MID-TERM Report ****************************
def reportsheetmidterm(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.reportsheet
        if uenter is False :
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails =''
        school = get_object_or_404(School, pk=1)
        if request.method == 'POST':
            form = reportsheetform(request.POST)
            if form.is_valid():
                session = form.cleaned_data['session']
                klass = form.cleaned_data['klass']
                term = form.cleaned_data['term']
                arm = form.cleaned_data['arm']
                stuno = Student.objects.filter(admitted_session = session,admitted_class = klass,admitted_arm = arm,gone = False).count()
                stuinfo = Student.objects.filter(admitted_session = session,admitted_class = klass,admitted_arm = arm,gone = False).order_by('-sex','fullname')
                midposition = mid_term_position(session,term,klass,arm)#getting the mid-term position
                replist = [] #empty list
                varbeg = klass[0]
                getgrading = gradingsys.objects.filter(classsub__startswith = varbeg)
                classtot = 0
                totsub = 0
                totalmarkcount = 0
                stuno = Student.objects.filter(admitted_session = session,admitted_class = klass,gone = False,admitted_arm = arm).count()
                for j in stuinfo:
                        if StudentAcademicRecord.objects.filter(student = j,term = term):
                            acaderec = StudentAcademicRecord.objects.get(student = j,term = term)
                            acaderec1 = StudentAcademicRecord.objects.get(student = j,term = 'First')
                            acaderec2 = StudentAcademicRecord.objects.get(student = j,term = 'Second')
                            affskill = AffectiveSkill.objects.get(academic_rec = acaderec)
                            psycho = PsychomotorSkill.objects.get(academic_rec = acaderec)
                            totsub = SubjectScore.objects.filter(academic_rec = acaderec,term = term).count()
                            totalmarkcount = SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).count()
                            subsco = SubjectScore.objects.filter(academic_rec = acaderec,term = term).order_by('num')
                            secsublist = []  #empty list
                            sdic = {}  #empty dictionary
                            for h in subsco:
                                if SubjectScore.objects.filter(academic_rec = acaderec1,term = 'First',subject = h.subject).count() == 0:
                                    fscore = '-'
                                    fscoret = '-'
                                else:
                                    fsc = SubjectScore.objects.get(academic_rec = acaderec1,term = 'First',subject = h.subject)
                                    fsco = fsc.term_score
                                    fscore = str(fsco)
                                if SubjectScore.objects.filter(academic_rec = acaderec2,term = 'Second',subject = h.subject).count() == 0:
                                    fscoret = '-'
                                else:
                                    fsct = SubjectScore.objects.get(academic_rec = acaderec2,term = 'Second',subject = h.subject)
                                    fscot = fsct.term_score
                                    fscoret = str(fscot)
                                secdic ={'thirdterm':h,'firstterm':fscore,'secondterm':fscoret}
                                secsublist.append(secdic)
                            if SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).count() == 0:
                                 rtotal = 0
                            else:
                                totalmark = SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).aggregate(Sum('term_score'))
                                totalmark2 = totalmark['term_score__sum']
                                rtotal = int(totalmark2)
                            if rtotal == 0:
                               perc = 0
                            else:
                               perc = float(rtotal)/float(totsub)
                            classtot += rtotal
                            ks = totalmarkcount * 100
                            totsub += ks
                            #total for first term
                            if SubjectScore.objects.filter(academic_rec = acaderec1,session = session,term = 'First').count()==0:
                               totalmark2sec = 0
                            else:
                                totalmarksec = SubjectScore.objects.filter(academic_rec = acaderec1,session = session,term = 'First').aggregate(Sum('term_score'))
                                totalmark2sec = totalmarksec['term_score__sum']
                            rtotalsec = int(totalmark2sec)
                            #*********************************************
                            if SubjectScore.objects.filter(academic_rec = acaderec2,session = session,term = 'Second').count() == 0:
                                totalmark2sec1 = 0
                            else:
                                totalmarksec1 = SubjectScore.objects.filter(academic_rec = acaderec2,session = session,term = 'Second').aggregate(Sum('term_score'))
                                totalmark2sec1 = totalmarksec1['term_score__sum']
                            rtotalsec1 = int(totalmark2sec1)
                            #**************************************************
                            #***********************#annual average***********************
                            if SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).count() == 0:
                                totalmark24 = 0
                            else:
                                totalmark4 = SubjectScore.objects.filter(academic_rec = acaderec,session = session,term = term).aggregate(Sum('annual_avg'))
                                totalmark24 = totalmark4['annual_avg__sum']
                            rtotal4 = int(totalmark24)
                            tscore = 0
                            submid = 0
                            for uuu in Subject.objects.all():
                                submid = uuu.ca  #totalca obtainable
                            submiddiv = int(submid)/2 #divide total CA by 2 e.g if ca = 30 we need 15
                            if klass [0] == 'N' or klass [0] == 'P':
                                submiddiv = 40
                            else:
                                submiddiv= 30
                            msublist = []
                            for jj in subsco:
                                mca = jj.mid_term
                                fca = jj.first_ca
                                sca = jj.second_ca
                                tca = jj.third_ca
                                foca = jj.fourth_ca
                                totalca=mca
                                #totalca=fca
                                totalperc1 = mca/submiddiv
                                totalperc = totalperc1 * 100 # getting the percentage
                                subjposition = mid_term_subjectposition(session,jj.subject,term,klass,arm,totalca)#getting mid-term subject position
                                if klass[0] == 'S':
                                    remark = seniorgrade(float(totalperc))
                                elif klass[0] == 'N' or klass[0] == 'C' or klass[0] == 'L' or klass[0] == 'B' or klass[0] == 'Y' or klass[0] == 'P':
                                    remark = prygrade(float(totalperc))
                                else:
                                    remark = juniorgrade(float(totalperc))
                                tscore += totalperc
                                msub = {'subject':jj.subject,'first_ca':fca,'second_ca':sca,'third_ca':tca,'fourth_ca':foca,'totalca':totalca,'totalperc':locale.format("%.1f",totalperc,grouping=True),'remark':remark['remark'],'grade':remark['grade'],'teacher':jj.subject_teacher,'position':subjposition}
                                msublist.append(msub)
                            if totalmarkcount == 0:
                               stuper = 0
                            else:
                                stuper = tscore / totalmarkcount
                            #**********************************************
                            jdic = {'studentinfo':j,'academic':acaderec,'affective':affskill,'pyscho':psycho,'subject':msublist,'totalmark':locale.format("%.1f",tscore,grouping=True),'totalmark1':rtotalsec,'totalmark2':rtotalsec1,'annualavg':rtotal4,'getgrading':getgrading,'percentage':locale.format("%.2f",stuper,grouping=True),'classposition':midposition[stuper]}
                            replist.append(jdic)
                if classtot == 0 or stuno == 0:
                        clavg = 0.0
                else:
                        j = classtot/stuno
                        clavg =j/float(totalmarkcount)
                if klass[0] == 'S':
                        if form.cleaned_data['pdffile']:
                            template ='assessment/midreportviewthird.html'
                            context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno}
                            return render_to_pdf(template, context)
                        else:
                            return render_to_response('assessment/midreportthird.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno})
                elif klass[0] == 'N' or klass[0] == 'C' or klass[0] == 'L' or klass[0] == 'B' or klass[0] == 'Y' or klass[0] == 'P':
                        if form.cleaned_data['pdffile']:
                            template ='assessment/midreportnviewthird.html'
                            context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)}
                            return render_to_pdf(template, context)
                        else:
                            return render_to_response('assessment/midreportnthird.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)})

                else:
                        if form.cleaned_data['pdffile']:
                            template ='assessment/midreportviewthird.html'
                            context = {'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)}
                            return render_to_pdf(template, context)
                        else:
                            return render_to_response('assessment/midreportthird.html',{'form':form,'varerr':varerr,'replist':replist,'school':school,'term':term,'stuno':stuno,'classavg':locale.format("%.2f",clavg,grouping=True)})
            else:
                varerr ="All Fields Are Required"
                return render_to_response('assessment/report.html',{'form':form,'varerr':varerr})

        else:
            form = reportsheetform()
        return render_to_response('assessment/report.html',{'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')




#*****************************************************************************************************
def broadsheet(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.reportsheet
        if uenter is False :
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails =''
        school = get_object_or_404(School, pk=1)
        if request.method == 'POST':
            form = broadsheetform(request.POST)
            if form.is_valid():
                session = form.cleaned_data['session']
                klass = form.cleaned_data['klass']
                term = form.cleaned_data['term']
                #***********************************************getting the subjects
                if klass.startswith('J'):
                    k= Subject.objects.filter(category='JS').order_by('num')
                elif klass.startswith('Y'):
                    k= Subject.objects.filter(category='Year').order_by('num')
                else:
                    k= Subject.objects.all().exclude(category='Year').exclude(category='JS').order_by('num')
                subjdic = {}
                for sub in k:
                    jk = {sub.subject:sub.subject}
                    subjdic.update(jk)
                sublist = subjdic.keys()
                #print 'the subject list :',sublist
                #*************************************************************************
                if klass.startswith('S'):
                    ll = bsheetfors(term,session,klass)
                    response = HttpResponse(mimetype="application/ms-excel")
                    response['Content-Disposition'] = 'attachment; filename=broadsheet.xls'
                    wb = xlwt.Workbook()
                    ws = wb.add_sheet('broadsheet')
                    ws.write(0, 2, school.name)
                    ws.write(1, 2, school.address)
                    ws.write(2, 2, '%s %s Term Broad Sheet for %s Session' %(klass,term, session) )
                    v = 2
                    ws.write(3,0,'Admission No')
                    ws.write(3,1,'Student Name')
                    for p in sublist:
                        ws.write(3, v, p)
                        v += 1
                    ws.write(3, v, 'GRADE')
                    k = 4
                    for jd in ll:
                       c = 2
                       ws.write(k, 0, jd['admno'])
                       ws.write(k, 1, jd['stname'])
                       for q in sublist:
                           ws.write(k, c, jd['subjects'][q])
                           c += 1
                       ws.write(k, c, jd['grade'])
                       k += 1
                    wb.save(response)
                    return response
                else:
                   ll = bsheetforj(term,session,klass)
                   response = HttpResponse(mimetype="application/ms-excel")
                   response['Content-Disposition'] = 'attachment; filename=broadsheet.xls'
                   wb = xlwt.Workbook()
                   ws = wb.add_sheet('broadsheet')
                   ws.write(0, 2, school.name)
                   ws.write(1, 2, school.address)
                   ws.write(2, 2, '%s %s Term Broad Sheet for %s Session' %(klass,term, session) )
                   v = 2
                   ws.write(3,0,'Admission No')
                   ws.write(3,1,'Student Name')
                   for p in sublist:
                       ws.write(3, v, p)
                       v += 1
                   ws.write(3, v, 'TOTAL SCORE')
                   v += 1
                   ws.write(3, v, 'AVERAGE SCORE')
                   v += 1
                   ws.write(3, v, 'POSITION')
                   k = 4
                   for jd in ll:
                       c = 2
                       ws.write(k, 0, jd['studentlist']['admno'])
                       ws.write(k, 1, jd['studentlist']['stname'])
                       for q in sublist:
                           ws.write(k, c, jd['studentlist']['subjects'][q])
                           c += 1
                       ws.write(k, c, jd['studentlist']['totalscore'])
                       c += 1
                       ws.write(k, c, '%.2f'%jd['studentlist']['avgscore'])
                       c += 1
                       ws.write(k, c, jd['pos'])
                       k += 1
                   wb.save(response)
                   return response
                return render_to_response('assessment/broadsheet.html',{'form':form,'varerr':varerr})
                        #end of position
        else:
            form = broadsheetform()
        return render_to_response('assessment/broadsheet.html',{'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')
#********************************************************Mid Term Broad Sheet *****************************************
def mid_term_broadsheet(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        uenter = user.reportsheet
        if uenter is False :
            return HttpResponseRedirect('/assessment/access-denied/')
        varerr =''
        getdetails =''
        school = get_object_or_404(School, pk=1)
        if request.method == 'POST':
            form = broadsheetform(request.POST)
            if form.is_valid():
                session = form.cleaned_data['session']
                klass = form.cleaned_data['klass']
                term = form.cleaned_data['term']
                #***********************************************getting the subjects
                if klass.startswith('J'):
                    k= Subject.objects.filter(category='JS').order_by('num')
                elif klass.startswith('Y'):
                    k= Subject.objects.filter(category='Year').order_by('num')
                else:
                    k= Subject.objects.all().exclude(category='Year').exclude(category='JS').order_by('num')
                subjdic = {}
                for sub in k:
                    jk = {sub.subject:sub.subject}
                    subjdic.update(jk)
                sublist = subjdic.keys()
                #print 'the subject list :',sublist
                #*************************************************************************
                if klass.startswith('S'):
                    ll = mid_term_bsheetfors(term,session,klass)
                    response = HttpResponse(mimetype="application/ms-excel")
                    response['Content-Disposition'] = 'attachment; filename=broadsheet.xls'
                    wb = xlwt.Workbook()
                    ws = wb.add_sheet('broadsheet')
                    ws.write(0, 2, school.name)
                    ws.write(1, 2, school.address)
                    ws.write(2, 2, '%s %s Term Broad Sheet for %s Session' %(klass,term, session) )
                    v = 2
                    ws.write(3,0,'Admission No')
                    ws.write(3,1,'Student Name')
                    for p in sublist:
                        ws.write(3, v, p)
                        v += 1
                    ws.write(3, v, 'GRADE')
                    k = 4
                    for jd in ll:
                       c = 2
                       ws.write(k, 0, jd['admno'])
                       ws.write(k, 1, jd['stname'])
                       for q in sublist:
                           ws.write(k, c, jd['subjects'][q])
                           c += 1
                       ws.write(k, c, jd['grade'])
                       k += 1
                    wb.save(response)
                    return response
                else:
                   ll = mid_term_bsheetforj(term,session,klass)
                   response = HttpResponse(mimetype="application/ms-excel")
                   response['Content-Disposition'] = 'attachment; filename=broadsheet.xls'
                   wb = xlwt.Workbook()
                   ws = wb.add_sheet('broadsheet')
                   ws.write(0, 2, school.name)
                   ws.write(1, 2, school.address)
                   ws.write(2, 2, '%s %s Term Broad Sheet for %s Session' %(klass,term, session) )
                   v = 2
                   ws.write(3,0,'Admission No')
                   ws.write(3,1,'Student Name')
                   for p in sublist:
                       ws.write(3, v, p)
                       v += 1
                   ws.write(3, v, 'TOTAL SCORE')
                   v += 1
                   ws.write(3, v, 'AVERAGE SCORE')
                   v += 1
                   ws.write(3, v, 'POSITION')
                   k = 4
                   for jd in ll:
                       c = 2
                       ws.write(k, 0, jd['studentlist']['admno'])
                       ws.write(k, 1, jd['studentlist']['stname'])
                       for q in sublist:
                           ws.write(k, c, jd['studentlist']['subjects'][q])
                           c += 1
                       ws.write(k, c, jd['studentlist']['totalscore'])
                       c += 1
                       ws.write(k, c, '%.2f'%jd['studentlist']['avgscore'])
                       c += 1
                       ws.write(k, c, jd['pos'])
                       k += 1
                   wb.save(response)
                   return response
                return render_to_response('assessment/midtermbroadsheet.html',{'form':form,'varerr':varerr})
                        #end of position
        else:
            form = broadsheetform()
        return render_to_response('assessment/midtermbroadsheet.html',{'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')



#*****************************************Taking Care Of Returning function for primary School**************************
def primary_url(request,session1,klass1,arm1,name1,term1):
        pry = ''
        for j in appused.objects.all():
            pry = j.primary
        if pry is True :
            pass
        else:
            return HttpResponseRedirect('/assessment/access-denied/')
        session = str(session1).replace('j','/')
        klass = str(klass1).replace('k',' ')
        arm = str(arm1).replace('k',' ')
        name11 = str(name1).replace('z',' ')
        fname2 = name11.replace('i','-')
        name  = fname2.replace('u',"'")
        term = str(term1).replace('0',' ')
        getdetails = ''
        getstu = Student.objects.get(admitted_class = klass,admitted_arm=arm,admitted_session = session,fullname = name)
        if StudentAcademicRecord.objects.filter(student = getstu,term = term):
            comm = StudentAcademicRecord.objects.get(student = getstu,term = term)
            getdetails = SubjectScore.objects.filter(session = session,klass = klass, arm = arm,term = term,academic_rec = comm).order_by('num')
        return render_to_response('assessment/subjectpry1.html',{'getdetails':getdetails,'session':session,'klass':klass,'arm':arm , 'd':getstu})

#*****************************************Taking Care Of Returning function for Secondary School**************************
def secondary_url(request,session1,klass1,arm1,name1,term1):
    sec = ''
    for j in appused.objects.all():
        sec = j.secondary
    if sec is True :
        pass
    else:
        return HttpResponseRedirect('/assessment/access-denied/')
    session = str(session1).replace('j','/')
    klass = str(klass1).replace('k',' ')
    arm = str(arm1).replace('k',' ')
    subject1 = str(name1).replace('z',' ')
    subject = str(subject1).replace('q','$')
    term = str(term1).replace('0',' ')
    stlist = []
    for j in Student.objects.filter(admitted_session = session,admitted_class = klass,admitted_arm = arm,gone = False).order_by('fullname'):
        if StudentAcademicRecord.objects.filter(student = j,session = session,term = term):
            st = StudentAcademicRecord.objects.get(student = j,session = session,term = term)
            if SubjectScore.objects.filter(academic_rec = st,klass = klass,subject = subject,session = session,arm=arm,term =term):
                gs = SubjectScore.objects.get(academic_rec = st,klass = klass,subject = subject,session = session,arm=arm,term =term)
                kk = {'id':gs.id,'admissionno':j.admissionno,'fullname':j.fullname,'sex':j.sex,'subject':gs.subject,'term':str(term),'first_ca':gs.first_ca,'second_ca':gs.second_ca,'third_ca':gs.third_ca,'exam_score':gs.exam_score}
                stlist.append(kk)
            else:
                pass
    return render_to_response('assessment/casecond.htm',{'data':stlist,'session':session,'klass':klass,'arm':arm,'subject':subject,'session1':session1,'klass1':klass1,'arm1':arm1,'name1':name1,'term1':term1})

#*****************************************Printing Secondary School Teacher Report**************************

def secondary_teacher_report(request,session1,klass1,arm1,name1,term1):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        session = str(session1).replace('j','/')
        klass = str(klass1).replace('k',' ')
        arm = str(arm1).replace('k',' ')
        subject = str(name1).replace('z',' ')
        term = str(term1).replace('0',' ')
        stlist = []
        school = get_object_or_404(School, pk=1)
        for j in Student.objects.filter(admitted_session = session,admitted_class = klass,admitted_arm = arm,gone = False).order_by('fullname'):
            if StudentAcademicRecord.objects.filter(student = j,session = session,term = term):
                st = StudentAcademicRecord.objects.get(student = j,session = session,term = term)
                if SubjectScore.objects.filter(academic_rec = st,klass = klass,subject = subject,session = session,arm=arm,term =term):
                    gs = SubjectScore.objects.get(academic_rec = st,klass = klass,subject = subject,session = session,arm=arm,term =term)
                    kk = {'id':gs.id,'admissionno':j.admissionno,'fullname':j.fullname,'sex':j.sex,'subject':gs.subject,'term':str(term),'first_ca':gs.first_ca,'second_ca':gs.second_ca,'third_ca':gs.third_ca,'exam_score':gs.exam_score,'termscore':gs.term_score,'remark':gs.grade,'position':gs.subposition}
                    stlist.append(kk)
                else:
                    pass
        return render_to_response('assessment/printca.htm',{'data':stlist,'session':session,'klass':klass,'arm':arm,'subject':subject,'term':term,'teacher':str(user.staffname).title(),'school':school})

    else:
        return HttpResponseRedirect('/login/')
"""
def secondary_teacher_report(request,session1,klass1,arm1,name1,term1):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = userprofile.objects.get(username = varuser)
        session = str(session1).replace('j','/')
        klass = str(klass1).replace('k',' ')
        arm = str(arm1).replace('k',' ')
        subject1 = str(name1).replace('z',' ')
        subject = str(subject1).replace('q','$')
        term = str(term1).replace('0',' ')
        stlist = []
        school = get_object_or_404(School, pk=1)
        for j in Student.objects.filter(admitted_session = session,admitted_class = klass,admitted_arm = arm,gone = False).order_by('fullname'):
            if StudentAcademicRecord.objects.filter(student = j,session = session,term = term):
                if term == "Thirdddd":
                	pass
                else:
                    st = StudentAcademicRecord.objects.get(student = j,session = session,term = term)
                    acaderec1 = StudentAcademicRecord.objects.get(student = j,session = session,term = 'First')
                    acaderec2 = StudentAcademicRecord.objects.get(student = j,session = session,term = 'Second')
                    if SubjectScore.objects.filter(academic_rec = acaderec1,klass = klass,subject = subject,session = session,arm=arm,term ='First'):
                        gs = SubjectScore.objects.get(academic_rec = acaderec1,klass = klass,subject = subject,session = session,arm=arm,term ='First')
                        firstterm = gs.term_score
                    else:
                        firstterm = 0
                    if SubjectScore.objects.filter(academic_rec = acaderec2,klass = klass,subject = subject,session = session,arm=arm,term ='Second'):
                        gs = SubjectScore.objects.get(academic_rec = acaderec2,klass = klass,subject = subject,session = session,arm=arm,term ='Second')
                        secondterm = gs.term_score
                    else:
                        secondterm = 0
                    if SubjectScore.objects.filter(academic_rec = st,klass = klass,subject = subject,session = session,arm=arm,term =term):
                        gs = SubjectScore.objects.get(academic_rec = st,klass = klass,subject = subject,session = session,arm=arm,term =term)
                        kk = {'id':gs.id,'admissionno':j.admissionno,'fullname':j.fullname,'sex':j.sex,'subject':gs.subject,'term':str(term),'first_ca':gs.first_ca,'second_ca':gs.second_ca,'third_ca':gs.third_ca,'exam_score':gs.exam_score,'termscore':gs.term_score,'remark':gs.grade,'position':gs.subposition,'firstterm':firstterm,'secondterm':secondterm,'annual_avg':gs.annual_avg}
                        stlist.append(kk)
                    else:
                        pass
        if term =="Third":
        	return render_to_response('assessment/printcathird.htm',{'data':stlist,'session':session,'klass':klass,'arm':arm,'subject':subject,'term':term,'teacher':str(user.staffname).title(),'school':school})
        else:
            return render_to_response('assessment/printca.htm',{'data':stlist,'session':session,'klass':klass,'arm':arm,'subject':subject,'term':term,'teacher':str(user.staffname).title(),'school':school})

    else:
        return HttpResponseRedirect('/login/')
"""