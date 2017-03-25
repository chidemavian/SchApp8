import os
from django.template import loader, Context,RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import  HttpResponseRedirect
from myproject.hrm.hrm.models import *
from myproject.hrm.train.form import *
from myproject.hrm.utils import *
from myproject.hrm.rcsetup.models import *
from myproject.hrm.rcwadmin.models import *
import datetime
from datetime import date,time

def entertraining(request):
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.ereonciliation
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/welcome/')
        varerr =""
        return render_to_response('train/entertraining.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')

def trainunauto(request):
     if  "userid" in request.session:
        varuser = request.session['userid']

        varerr =""
        return render_to_response('train/unautorise.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')

def trainingsetup(request):
     varerr =""
     if  "userid" in request.session:
       if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/train/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = setupform(request.POST) # A form bound to the POST data
          if form.is_valid():
            name = form.cleaned_data['name']
            name = name.replace(' ','-')
            name = name.upper()
            if tblsetup.objects.filter(name = name).count() == 0:
                 pass
            else:
                varerr = "%s in existence" % name
                getdetails = tblsetup.objects.all().order_by('name')
                return render_to_response('train/trainingsetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
            savecon = tblsetup(name = name,userid = varuser)
            savecon.save()
            return HttpResponseRedirect('/hrm/train/trainingsetup/')
          else:
               varerr = "All Fields Are Required/Check Inputed Picture"
               getdetails = ""
          return render_to_response('train/trainingsetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = setupform()
            getdetails = tblsetup.objects.all().order_by('name')
        return render_to_response('train/trainingsetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def edittrainsetup(request,invid):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.unpresented
            if uenter == "False" :
              return HttpResponseRedirect('/hrm/train/unauto/')
            varerr =""
            getdetails =''
            if request.method == 'POST':
                name = request.POST['name']
                name = name.replace(' ','-')
                name = name.upper()
                if  tblsetup.objects.filter(name = name).exclude(id = invid).count() == 0 :
                    pass
                else:
                    varerr = "%s In Existence" % name
                    getdetails = tblsetup.objects.get(id = invid)
                    return render_to_response('train/edittraining.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})

                if  name == "" :
                    varerr = "ALL FIELDS ARE REQUIRED"
                    getdetails = tblsetup.objects.get(id = invid)
                    return render_to_response('train/edittraining.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                seldata = tblsetup.objects.get(id = invid)
                seldata.name = name
                seldata.save()
                return HttpResponseRedirect('/hrm/train/trainingsetup/')
            else:
                try:
                  getdetails = tblsetup.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                  return render_to_response('train/edittraining.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                except:
                    varerr = ""
                return render_to_response('train/edittraining.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})

        else:
         return HttpResponseRedirect('/login/')

def deletetrainsetup(request,invid):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.unpresented
            if uenter == "False" :
              return HttpResponseRedirect('/hrm/train/unauto/')
            varerr =""
            try:
                 uacc = tblsetup.objects.get(id = invid)
                 uacc.delete()
                 return HttpResponseRedirect('/hrm/train/trainingsetup/')
            except :
                return HttpResponseRedirect('/hrm/train/trainingsetup/')
        else:
         return HttpResponseRedirect('/login/')

def stafftraining(request):
     varerr =""
     if  "userid" in request.session:
       if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/train/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = setupform(request.POST) # A form bound to the POST data
          if form.is_valid():
            name = form.cleaned_data['name']
            name = name.replace(' ','-')
            name = name.upper()

            if tblsetup.objects.filter(name = name).count() == 0:
                 pass
            else:
                varerr = "%s in existence" % name
                getdetails = tblsetup.objects.all().order_by('name')
                return render_to_response('train/trainingsetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
           # savecon = tblsetup(name = name,userid = varuser)
            #savecon.save()
            return HttpResponseRedirect('/hrm/train/trainingsetup/')
          else:
               varerr = "All Fields Are Required/Check Inputed Picture"
               getdetails = ""
          return render_to_response('train/stafftraining.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = setupform()
            getdetails = ""#tblsetup.objects.all().order_by('name')
        return render_to_response('train/stafftraining.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def trainingstaffajax(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   #print acccode
                   #gdata = staffrec.objects.filter(name__startswith = acccode).order_by('oracleno')
                   gdata = staffrec.objects.filter(name__contains = acccode,status = "ACTIVE").order_by('name')

                   return render_to_response('train/testajax3.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = staffrec.objects.filter(status = "ACTIVE").order_by('name')
                   return render_to_response('train/testajax3.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('train/testajax3.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def trainingeditstaff(request,invid):
        varerr =""
        getdetails = ""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.unpresented
            if uenter == "False" :
              return HttpResponseRedirect('/hrm/train/unauto/')
            varerr =""
            if request.method == 'POST':
                getdetails = ""
                staffid = request.POST['staffid']
                staffname = request.POST['staffname']
                sex = request.POST['sex']
                designation = request.POST['designation']
                department = request.POST['department']
                trainingtype = request.POST['trainingtype']
                description = request.POST['description']
                duration = request.POST['duration']
                dateofred = request.POST['dateofred']

                if  sex == "" or designation == "" or staffid == "" or staffname == "" or department == "" or dateofred == "" or trainingtype == "" or description == "" or duration == "":
                    varerr = "ALL FIELDS ARE REQUIRED"
                    gdept = tblsetup.objects.all().order_by('name')#designation
                    getdetails = staffrec.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    return render_to_response('train/editstafftraining.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'gdept':gdept})
                caldate2 = dateofred.split('/')
                recdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                relsave = tbltraining(staffid = staffid,staffname = staffname,sex = sex,designation = designation,department = department,traintype = trainingtype,description = description,duration = duration,commdate = recdate,userid = varuser,recyear = recdate.year)
                relsave.save()
                gdept = tblsetup.objects.all().order_by('name')#designation
                getdetails = staffrec.objects.get(staffid = staffid)
                return render_to_response('train/editstafftraining.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'gdept':gdept})
               # return HttpResponseRedirect('/train/trainingstaff/')
            else:
                try:
                  gdept = tblsetup.objects.all().order_by('name')#designation
                  getdetails = staffrec.objects.get(id = invid)
                  return render_to_response('train/editstafftraining.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'gdept':gdept})
                except:
                    varerr = "Record Not Exist"
                    return render_to_response('train/editstafftraining.htm',{'varuser':varuser,'varerr':varerr})
        else:
         return HttpResponseRedirect('/login/')

def trainingstaffajaxtrain(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   print acccode
                   #print acccode
                   #gdata = staffrec.objects.filter(name__startswith = acccode).order_by('oracleno')
                   gdata = tbltraining.objects.filter(staffid = acccode).order_by('id')
                   return render_to_response('train/testtrain.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = ""
                   return render_to_response('train/testtrain.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('train/testtrain.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def trainingdeletestaff(request,invid):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.unpresented
            if uenter == "False" :
              return HttpResponseRedirect('/hrm/train/unauto/')
            varerr =""
            try:
               uacc = tbltraining.objects.get(id = invid)
               oracode = uacc.staffid
               uacc.delete()
               gdept = tblsetup.objects.all().order_by('name')#designation
               getdetails = staffrec.objects.get(staffid = oracode)
               return render_to_response('train/editstafftraining.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'gdept':gdept})
            except :
               gdept = ""
               getdetails = ""
               return render_to_response('train/editstafftraining.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'gdept':gdept})

            # return HttpResponseRedirect('/train/trainingstaff/')
        else:
         return HttpResponseRedirect('/login/')

def trainingreport(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/train/unauto/')
        varerr =""
        if request.method == 'POST':
          form = yettotrainform(request.POST) # A form bound to the POST data
          if form.is_valid():
            typeoftrain = form.cleaned_data['typeoftrain']
            trainyear = form.cleaned_data['trainyear']
            comp = tblcompanyinfo.objects.get(id = 1)
            tra = typeoftrain
            tye = trainyear
            getdetails = tbltraining.objects.filter(traintype = typeoftrain,recyear = trainyear).order_by('staffid','id')
            return render_to_response('train/trainingreport.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'comp':comp,'tra':tra,'tye':tye,'printdate':gettime()},context_instance = RequestContext(request))
          else:
               varerr = "All Fields Are Required/Check Training Year"
               getdetails = ""
          return render_to_response('train/trainingreport.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = yettotrainform()
            getdetails = ""#tblsetup.objects.all().order_by('name')
        return render_to_response('train/trainingreport.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def yettobetrained(request):
     varerr =""
     if  "userid" in request.session:
       if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/train/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = yettotrainform(request.POST) # A form bound to the POST data
          if form.is_valid():
            typeoftrain = form.cleaned_data['typeoftrain']
            trainyear = form.cleaned_data['trainyear']
            #tbltraining
            totstaff = staffrec.objects.filter(status= "ACTIVE").count()
            staffdata = []
            staffdata1 = []
            lk = ""
            if totstaff == 0:
                pass
            else:
                getdt = staffrec.objects.filter(status="ACTIVE").order_by('staffid')
                for p in getdt:
                    gcode = p.staffid
                    if tbltraining.objects.filter(staffid = gcode,traintype = typeoftrain,recyear = trainyear).count() == 0:
                        trdata = staffrec.objects.get(staffid = gcode)
                        staffdata1.append(trdata)
                    else:
                        pass
                #print staffdata
                comp = tblcompanyinfo.objects.get(id = 1)
                tra = typeoftrain
                tye = trainyear
                return render_to_response('train/yettobetrained.htm',{'varuser':varuser,'varerr':varerr,'form':form,'staffdata1':staffdata1,'comp':comp,'tra':tra,'tye':tye,'printdate':gettime()},context_instance = RequestContext(request))

            return HttpResponseRedirect('/hrm/train/trainingsetup/')
          else:
               varerr = "All Fields Are Required/Check Training Year"
               getdetails = ""
          return render_to_response('train/yettobetrained.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = yettotrainform()
            getdetails = ""#tblsetup.objects.all().order_by('name')
        return render_to_response('train/yettobetrained.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def getrainsetup(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tblsetup.objects.get(id = acccode)
                return render_to_response('train/edittraining.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')
