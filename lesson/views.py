from django.shortcuts import render_to_response
from myproject.lesson.forms import *
from myproject.setup.models import *
from myproject.sysadmin.models import *
from myproject.student.models import *
from myproject.lesson.models import *
from assessment.views import sublists
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from django.core.serializers.json import simplejson as json


sublists =['AGRICULTURAL SCIENCE','ENGLISH LANGUAGE']


def wel(request):
    if  "userid" in request.session:
        return render_to_response('lesson/success.html')
    else:
        return HttpResponseRedirect('/login/')

def settopic(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr = ''
        if request.method == 'POST':
            form = settopicForm(request.POST)
            if form.is_valid():
                 klass = form.cleaned_data['klass']
                 session = form.cleaned_data['session']
                 term = form.cleaned_data['term']
                 subject= form.cleaned_data['subject']
                 topic=form.cleaned_data['topic']
                 top = topic.upper()
                 if psetup.objects.filter(topic=top, term = term):
                     varerr = 'TOPIC ALREADY ENTERED'
                     return HttpResponseRedirect('/lesson/set_up/')
                   #  return render_to_response('lesson/setup.html',{'form':form,'varerr':varerr})#,'sett':sett
                 if klass[0]=='J':
                     count = psetup.objects.filter(klass=klass, term=term,subject=subject,session=session).count()
                     count=count+1
                     num=1
                 elif klass[0]=='P':
                     count = psetup.objects.filter(klass=klass, term=term,subject=subject,session=session).count()
                     count=count+1
                     num=2
                 elif klass[0]=='S':
                     count = psetup.objects.filter(klass=klass, term=term,subject=subject,session=session).count()
                     count=count+1
                     num=3
                 less = psetup(session=session, term = term,num=num,count=count,klass = klass,topic = topic.upper(),subject=subject).save()
                # varerr = 'TOPIC ENTERED SUCCESSFULLY'
                 return render_to_response('lesson/setup.html',{'form':form,'varerr':varerr})
            else:
                varerr = 'topic not entered'
                return render_to_response('lesson/setup.html',{'form':form,'varerr':varerr})
        else:
            form = settopicForm()
            return render_to_response('lesson/setup.html',{'form':form,'varerr':varerr,})
    else:
        return HttpResponseRedirect('/login/')

def topajax(request):
    if "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varerr = ""
                varuser = request.session['userid']
                post = request.POST.copy()
                accode = post['userid']
                subject,klass,term = accode.split(':') #order must follow that in the autopost script in html
                sett = psetup.objects.filter(klass = klass,term = term, subject = subject)
                return render_to_response('lesson/topajax.html',{'sett':sett,'varerr':varerr})
            else:
                sett = ""
            return render_to_response ('lesson/topajax.html',{'sett':sett})
        else:
            sett = ""
            return render_to_response ('lesson/topajax.html',{'sett':sett})


def deletetopiccode(request, sid):
    if "userid" in request.session:
        varuser = request.session['userid']
        getdetails= psetup.objects.get(id = sid)
        getdetails.delete()
        return HttpResponseRedirect('/lesson/set_up/')
    else:
        return HttpResponseRedirect('/login/')

def getsubajax(request):
    if "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                post = request.POST.copy()
                accode = post['userid']
                subject,klass,term = accode.split(':') #order must follow that in the autopost script in html
                sett = psetup.objects.filter(klass = klass,term = term, subject = subject)
                return render_to_response('lesson/setsub.html',{'sett':sett})
            else:
                sett = ""
            return render_to_response ('lesson/setsub.html',{'sett':sett})
        else:
            sett = ""
            return render_to_response ('lesson/setsub.html',{'sett':sett})


def setsub(request):
    if "userid" in request.session:
        varuser = request.session['userid']
        varerr = ""
        if request.method=='POST':
            form = setsubtopicform(request.POST)
            klass =request.POST['klass']
            term = request.POST['term']
            subject=request.POST['subject']
            topic=request.POST['topic']
            subtopic=request.POST['subtopic']
            if subtopic =="":
                ht = 'enter a subtopic'
                return render_to_response('lesson/subt.html',{'form':form,'varerr':ht})
            if subtopic==subtopic:
                ht = 'subtopic already entered'
                return render_to_response('lesson/subt.html',{'form':form,'varerr':ht})
            else:
                    top = psetsub(subject=subject,klass=klass,term=term,topic=topic,subtopic=subtopic.upper()).save()
                    #top = top.id
                   # upd=psetsub(topic= top,subtopic=subtopic).save()
                    ht = 'done'
            return render_to_response('lesson/subt.html',{'form':form})
        else:
            form = setsubtopicform()
        return render_to_response('lesson/subt.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def filsubtop(request):
    if "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varerr = ""
                varuser = request.session['userid']
                post = request.POST.copy()
                accode=post['userid']
                state=accode
                sott=[]
                kip =[]
                tdic={}
                subject,klass,term=accode.split(':')
                sott = psetup.objects.filter(subject=subject,klass=klass,term=term) #topics based on subject
                sett = psetsub.objects.filter(subject=subject,klass=klass,term=term)
                for j in sott:
                    j=j.topic
                    s= {j:j}
                    tdic.update(s)
                klist =tdic.values()
                for p in klist:
                    kip.append(p)
                return render_to_response('lesson/subtajax.html',{'sett':sett,'sott':sott,'kip':kip,'subject':subject,'sublists':sublists})
            else:
                sett = ""
                upd = 'hkug'
            return render_to_response ('lesson/subtajax.html',{'sett':sett,'upd':upd})
        else:
            sett = ""
        return render_to_response ('lesson/subtajax.html',{'sett':sett,'upd':upd})

def gettopajaxx(request):
    if "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
               varuser = request.session['userid']
               varerr =""
               post = request.POST.copy()
               accode = post['userid']
               state = accode
               subject,klass,term= accode.split(':')
               kk = []
               sdic ={}
               data=psetup.objects.filter(session =session,subject = subject, klass=klass,term = term).order_by('topic')
               for j in data:
                       j=j.topic
                       s= {j:j}
                       sdic.update(s)
               klist =sdic.values()
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

def setupmyplan(request):
    if  "userid" in request.session:
        if request.method == 'POST':
            form = lessonplanform(request.POST)
            if form.is_valid():
                klass = request.POST['klass']
                session = request.POST['session']
                term = request.POST['term']
                subject= request.POST['subject']
                return render_to_response('lesson/lessonp.html',{'form':form})
        else:
            form = lessonplanform()
        return render_to_response('lesson/lessonp.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


def setupmynote(request):
    if  "userid" in request.session:
        if request.method == 'POST':
            return render_to_response('lesson/lessonnote.html')
        else:
            return render_to_response('lesson/lessonnote.html')
    else:
        return HttpResponseRedirect('/login/')

def json_view(func):
    def wrap(req, *args, **kwargs):
        resp = func(req, *args, **kwargs)
        if isinstance(resp, HttpResponse):
            return resp
        return HttpResponse(json.dumps(resp), mimetype="application/json")

    return wrap
