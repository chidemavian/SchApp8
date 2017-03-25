# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import DetailView, ListView
from django.template import RequestContext
from myproject.forum.forms import *
from myproject.forum.models import *
from myproject.sysadmin.models import *
from myproject.forum.capy import monthrange
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib.sessions.backends.db import SessionStore
import datetime
from datetime import date
import random

def home(request):
    varerr =''
    if request.method == 'POST':
        form = userform(request.POST) # A form bound to the POST data
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            email = email.lower()
            password = password.lower()
            try:
              user = useracc.objects.get(email = email,password=password,active = "Yes")
              if user.password == password :
               request.session['userid'] = user.email
               return HttpResponseRedirect('/forum/main/')
            except:
               varerr = "Invalid User Or activate your account in your e-mail"
               return render_to_response('forum/home.html',{'form':form,'varerr':varerr},context_instance = RequestContext(request))
    else:

        form = userform()
    return render_to_response('forum/home.html',{'varerr':varerr,'form':form},context_instance = RequestContext(request))

def activation(request,username):
    try:
        jj = useracc.objects.get(control = username)
        jj.active= 'Yes'
        jj.save()
        return HttpResponseRedirect('/login/')

    except get_object_or_404:
        get_object_or_404(useracc,email = username)

def registration(request):
    varerr =''
    if request.method == 'POST':
        form = userregform(request.POST) # A form bound to the POST data
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            photo_file = 'user.png'
            email = email.lower()
            password = password.lower()
            name = name.lower()
            s = SessionStore()
            s['mail']= email
            s.save()
            vcontrol = s.session_key
            if useracc.objects.filter(email = email).count() == 0:
               pass
            else:
              varerr ="This email is already used "
              return render_to_response('forum/registration.html',{'varerr':varerr,'form':form},context_instance = RequestContext(request))
            try:
               body ='Thanks for your registration. To start enjoying our forum, please visit this link \n\n http://www.ruffwal.com/forum/registration/activation/%s \n\n\n Support Team \n +2348033204305,+2348062916005' %vcontrol
               send_mail('Thanks For Your Registration',body, 'support@ruffwal.com',[email],fail_silently=False)
            except :
                varerr = "Error occurred, Please Check your connection"
                return render_to_response('forum/registration.html',{'varerr':varerr,'form':form},context_instance = RequestContext(request))
            savecon = useracc(email = email,password = password,name = name,active = 'No',photo = photo_file,control = vcontrol)
            savecon.save()
            return HttpResponseRedirect('/forum/successful/')
    else:

        form = userregform()
        getdetails = ""#tbldesig.objects.all().order_by('desgcode')
    return render_to_response('forum/registration.html',{'varerr':varerr,'form':form},context_instance = RequestContext(request))


def successful(request):
    return render_to_response('forum/successul.html',context_instance=RequestContext(request))


def welcomecode(request):
    if  "userid" in request.session:
        all =[]
        varuser = request.session['userid']
        userdetails = userprofile.objects.get(username = varuser)
        varerr =""
        #form = postform()
        if request.method == 'POST':
            form = postform(request.POST) # A form bound to the POST data
            if form.is_valid():
               posts = form.cleaned_data['post']
               uid = ''
               for m in range(20):
                   kr = random.randint(1,999)
                   uid += str(kr)
               postcomm = post(user = varuser,comment = posts,postid = uid)
               postcomm.save()
               return HttpResponseRedirect('/forum/main/')
            else:
                varerr ='Invalid Entry'
                return render_to_response('forum/welcome.html',{'varuser':varuser,'form':form,'all':all,'varerr':varerr,'userdetails':userdetails})

        else:
            form = postform()
            all = []
            subd ={}
            #getting the date
            maturitydate = date.today()
            vyear = maturitydate.year
            vmon = maturitydate.month
            vday = maturitydate.day
            vd7 = vday - 7
            if vd7 <=0:
                vmon -= 1
                if vmon <= 0:
                    vmon = 12
                    vyear = vyear - 1
                kp = monthrange(vyear,vmon)[1]
                vmd = int(kp)
                vday = vmd + vd7
            else:
                vday = vd7
            maturitydate = date(vyear,vmon,vday)
            print 'The maturity date ',maturitydate
            #*************************************************
            comments = post.objects.filter(recdate__gte=maturitydate).order_by('-id')
            for al in comments:
                auser = al.user
                vid = al.postid
                auseracc = userprofile.objects.get(username = auser)
                subpost = subcomments.objects.filter(commentid = vid)[:3]
                tocomment = subcomments.objects.filter(commentid = vid).count()
                subd ={}
                subdall = []
                for jj in subpost:
                    ajj = jj.user
                    subuser = userprofile.objects.get(username = ajj)
                    #subpost = jj.comment
                    subd ={'subpost':jj,'subuser':subuser}
                    subdall.append(subd)

                di = {'comments':al,'user':auseracc,'subcomments':subdall,'tocomment':tocomment}
                all.append(di)
        return render_to_response('forum/welcome.html',{'varuser':varuser,'form':form,'all':all,'varerr':varerr,'userdetails':userdetails})
    else:
        return HttpResponseRedirect('/login/')



def logoutuser(request):
    try:
        del request.session['userid']
    except KeyError:
        pass
    return HttpResponseRedirect('/forum/')

def editprofile(request):
    if  "userid" in request.session:

        varuser = request.session['userid']
        userdetails = userprofile.objects.get(username = varuser)
        varerr =""
        #print userdetails.photo
        if request.method == 'POST':
            getdetails = ""
            name = request.POST['name']
            if 'image' in request.FILES:
                photo_file = request.FILES['image']
                k1 = str(photo_file.name)
                j = k1.split('.')[1]
                j = j.lower()
                #print k,j
                if not (j in ['jpeg','jpg','png']):
                    varerr = "%s is not a required picture" % k1
                    #getdetails = staffrec.objects.get(id = invid)
                    return render_to_response('forum/editprofile.html',{'varuser':varuser,'varerr':varerr,'userdetails':userdetails})
                else:
                    pass
            else:
                photo_file = userdetails.photo

            if name == "" :
                varerr = "E-mail Can not be empty"
                return render_to_response('forum/editprofile.html',{'varuser':varuser,'varerr':varerr,'userdetails':userdetails})

            userdetails.email = name
            userdetails.photo = photo_file
            userdetails.save()
            return HttpResponseRedirect('/forum/main/')
        else:

            return render_to_response('forum/editprofile.html',{'varuser':varuser,'varerr':varerr,'userdetails':userdetails})
    else:
        return HttpResponseRedirect('/login/')

def recoverpassword(request):
    varerr =''
    if request.method == 'POST':
        form = recoverpassform(request.POST) # A form bound to the POST data
        if form.is_valid():
            email = form.cleaned_data['email']
            email = email.lower()
            try:
                user = useracc.objects.get(email = email)
                username = user.email
                password = user.password
                send_mail('Recovered Password',body, 'support@larry.com',[email],fail_silently=False)
                return HttpResponseRedirect('/forum/successful/')
            except:
                varerr = "Invalid User Or check your connection"
                return render_to_response('forum/recoverpass.html',{'form':form,'varerr':varerr},context_instance = RequestContext(request))
    else:

        form = recoverpassform()
    return render_to_response('forum/recoverpass.html',{'varerr':varerr,'form':form},context_instance = RequestContext(request))

def yourcomments(request,num):
    if  "userid" in request.session:
        all = []
        varuser = request.session['userid']
        userdetails = userprofile.objects.get(username = varuser)
        varerr =""
        #form = postform()
        if request.method == 'POST':
            form = postform(request.POST) # A form bound to the POST data
            if form.is_valid():
                posts = form.cleaned_data['post']
                postcomm = subcomments(user = userdetails.username,comment = posts,commentid = num)
                postcomm.save()
                return HttpResponseRedirect('/forum/main/')
            else:
                varerr = "Invalid Comment"
                return render_to_response('forum/comments.html',{'varuser':varuser,'form':form,'all':all,'varerr':varerr,'userdetails':userdetails})

        else:
            form = postform()
            all = []
            subd ={}
            comments = post.objects.filter(postid = num)
            for al in comments:
                auser = al.user
                vid = al.postid
                auseracc = userprofile.objects.get(username = auser)
                subpost = subcomments.objects.filter(commentid = vid)
                subd ={}
                subdall = []
                for jj in subpost:
                    ajj = jj.user
                    subuser = userprofile.objects.get(username = ajj)
                    #subpost = jj.comment
                    subd ={'subpost':jj,'subuser':subuser}
                    subdall.append(subd)

                di = {'comments':al,'user':auseracc,'subcomments':subdall}
                all.append(di)


        return render_to_response('forum/comments.html',{'varuser':varuser,'form':form,'all':all,'varerr':varerr,'userdetails':userdetails})
    else:
        return HttpResponseRedirect('/login/')
