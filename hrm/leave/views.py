import os
from django.template import loader, Context,RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import  HttpResponseRedirect
from myproject.hrm.leave.models import *
from myproject.hrm.hrm.models import *
from myproject.hrm.leave.form import *
from myproject.hrm.rcwadmin.models import *
from myproject.hrm.rcsetup.models import *
from myproject.hrm.rcwadmin.models import *
from myproject.hrm.utils import *
import datetime
from datetime import date,time

def enterleave(request):
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.ereport
        if uenter == "False" :
            return HttpResponseRedirect('/welcome/')
        varerr =""
        return render_to_response('leave/enterleave.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')

def leaveunauto(request):
     if  "userid" in request.session:
        varuser = request.session['userid']

        varerr =""
        return render_to_response('leave/unautorise.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')

def leavesetup(request):
     varerr =""
     if  "userid" in request.session:
       if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.statutory
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/leave/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = setupform(request.POST) # A form bound to the POST data
          if form.is_valid():
            name = form.cleaned_data['name']
            name = name.replace(' ','-')
            name = name.upper()

            if tblleavesetup.objects.filter(name = name).count() == 0:
                 pass
            else:
                varerr = "%s in existence" % name
                getdetails = tblleavesetup.objects.all().order_by('name')
                return render_to_response('leave/leavesetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
            savecon = tblleavesetup(name = name,userid = varuser)
            savecon.save()
            return HttpResponseRedirect('/hrm/leave/leavesetup/')
          else:
               varerr = "All Fields Are Required/Check Inputed Picture"
               getdetails = ""
          return render_to_response('leave/leavesetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = setupform()
            getdetails = tblleavesetup.objects.all().order_by('name')
        return render_to_response('leave/leavesetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def editleavesetup(request,invid):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.statutory
            if uenter == "False" :
              return HttpResponseRedirect('/hrm/leave/unauto/')
            varerr =""
            if request.method == 'POST':
                getdetails = ""
                name = request.POST['name']
                name = name.replace(' ','-')
                name = name.upper()
                if  tblleavesetup.objects.filter(name = name).exclude(id = invid).count() == 0 :
                    pass
                else:
                    varerr = "%s In Existence" % name
                    getdetails = tblleavesetup.objects.get(id = invid)
                    return render_to_response('leave/editleave.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})

                if  name == "" :
                    varerr = "ALL FIELDS ARE REQUIRED"
                    getdetails = tblleavesetup.objects.get(id = invid)
                    #return render_to_response('leave/editleave.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                    return HttpResponseRedirect('/hrm/leave/leavesetup/')
                seldata = tblleavesetup.objects.get(id = invid)
                seldata.name = name
                seldata.save()
                return HttpResponseRedirect('/hrm/leave/leavesetup/')
            else:
                try:
                  getdetails = tblleavesetup.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                  return render_to_response('leave/editleave.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'desg':desg,'gpfa':gpfa,'gbank':gbank,'gdept':gdept,'glocal':glocal})
                except:
                    varerr = ""
                return render_to_response('leave/editleave.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})

        else:
         return HttpResponseRedirect('/login/')

def deleteleavesetup(request,invid):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.statutory
            if uenter == "False" :
              return HttpResponseRedirect('/hrm/leave/unauto/')
            varerr =""
            uacc = tblleavesetup.objects.get(id = invid)
            uacc.delete()
            return HttpResponseRedirect('/hrm/leave/leavesetup/')
        else:
         return HttpResponseRedirect('/login/')

def staffleave(request):
     varerr =""
     if  "userid" in request.session:
       if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.statutory
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/leave/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = setupform(request.POST) # A form bound to the POST data
          if form.is_valid():
            name = form.cleaned_data['name']
            name = name.replace(' ','-')
            name = name.upper()

            if tblleavesetup.objects.filter(name = name).count() == 0:
                 pass
            else:
                varerr = "%s in existence" % name
                getdetails = tblleavesetup.objects.all().order_by('name')
                return render_to_response('leave/leavesetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
            return HttpResponseRedirect('/hrm/leave/leavestaff/')
          else:
               varerr = "All Fields Are Required/Check Inputed Picture"
               getdetails = ""
          return render_to_response('leave/staffleave.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = setupform()
            getdetails = ""#tblsetup.objects.all().order_by('name')
        return render_to_response('leave/staffleave.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def leavestaffajax(request):
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

                   return render_to_response('leave/testajax3.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = staffrec.objects.filter(status = "ACTIVE").order_by('name')
                   return render_to_response('leave/testajax3.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('leave/testajax3.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def leaveeditstaff(request,invid):
        varerr =""
        getdetails = ""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.statutory
            if uenter == "False" :
              return HttpResponseRedirect('/hrm/leave/unauto/')
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
                enddate = request.POST['enddate']

                if  sex == "" or designation == "" or staffid == "" or staffname == "" or department == "" or dateofred == "" or trainingtype == "" or description == "" or duration == "" or enddate == "":
                    varerr = "ALL FIELDS ARE REQUIRED"
                    gdept = tblleavesetup.objects.all().order_by('name')#designation
                    getdetails = staffrec.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    return render_to_response('leave/editstaffleave.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'gdept':gdept})
                caldate2 = dateofred.split('/')
                recdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                caldate22 = enddate.split('/')
                recdate2 = date(int(caldate22[2]),int(caldate22[0]),int(caldate22[1]))
                relsave = tblleave(staffid = staffid,staffname = staffname,sex = sex,designation = designation,department = department,traintype = trainingtype,description = description,duration = duration,commdate = recdate,userid = varuser,recyear = recdate.year,enddate = recdate2,recendyear = recdate2.year)
                relsave.save()
                gdept = tblleavesetup.objects.all().order_by('name')#designation
                getdetails = staffrec.objects.get(staffid = staffid)
                return render_to_response('leave/editstaffleave.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'gdept':gdept})
               # return HttpResponseRedirect('/train/trainingstaff/')
            else:
                try:
                  gdept = tblleavesetup.objects.all().order_by('name')#designation
                  getdetails = staffrec.objects.get(id = invid)
                  return render_to_response('leave/editstaffleave.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'gdept':gdept})
                except:
                    varerr = "Record Not Exist"
                    return render_to_response('leave/editstaffleave.htm',{'varuser':varuser,'varerr':varerr})
        else:
         return HttpResponseRedirect('/login/')

def leavestaffajaxleave(request):
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
                   gdata = tblleave.objects.filter(staffid = acccode).order_by('id')
                   return render_to_response('leave/testleave.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = ""
                   return render_to_response('leave/testleave.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('leave/testleave.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def leavedeletestaff(request,invid):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.statutory
            if uenter == "False" :
              return HttpResponseRedirect('/hrm/leave/unauto/')
            varerr =""
            try:
                uacc = tblleave.objects.get(id = invid)
                oracode = uacc.staffid
                uacc.delete()
                gdept = tblleavesetup.objects.all().order_by('name')#designation
                getdetails = staffrec.objects.get(staffid = oracode)
                return HttpResponseRedirect('/hrm/leave/leavestaff/')
                #return render_to_response('leave/editstaffleave.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'gdept':gdept})
            except:
                 return HttpResponseRedirect('/hrm/leave/leavestaff/')
           # return HttpResponseRedirect('/train/trainingstaff/')
        else:
         return HttpResponseRedirect('/login/')

def leavereport(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.statutory
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/leave/unauto/')
        varerr =""
        if request.method == 'POST':
          form = yettotrainform(request.POST) # A form bound to the POST data
          if form.is_valid():
            typeoftrain = form.cleaned_data['typeoftrain']
            trainyear = form.cleaned_data['trainyear']
            comp = tblcompanyinfo.objects.get(id = 1)
            tra = typeoftrain
            tye = trainyear
            getdetails = tblleave.objects.filter(traintype = typeoftrain,recyear = trainyear).order_by('staffid','id')
            return render_to_response('leave/leavereport.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'comp':comp,'tra':tra,'tye':tye,'printdate':gettime()},context_instance = RequestContext(request))
          else:
               varerr = "All Fields Are Required/Check Training Year"
               getdetails = ""
          return render_to_response('leave/leavereport.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = yettotrainform()
            getdetails = ""#tblsetup.objects.all().order_by('name')
        return render_to_response('leave/leavereport.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def yettobeleave(request):
     varerr =""
     if  "userid" in request.session:
       if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.statutory
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/leave/unauto/')
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
                getdt = staffrec.objects.filter(status="ACTIVE").order_by('name')
                for p in getdt:
                    gcode = p.staffid
                    if tblleave.objects.filter(staffid = gcode,traintype = typeoftrain,recyear = trainyear).count() == 0:
                        trdata = staffrec.objects.get(staffid = gcode)
                        staffdata1.append(trdata)
                    else:
                        pass
                #print staffdata
                comp = tblcompanyinfo.objects.get(id = 1)
                tra = typeoftrain
                tye = trainyear
                return render_to_response('leave/yettobeleave.htm',{'varuser':varuser,'varerr':varerr,'form':form,'staffdata1':staffdata1,'comp':comp,'tra':tra,'tye':tye,'printdate':gettime()},context_instance = RequestContext(request))

            return HttpResponseRedirect('/hrm/leave/leavesetup/')
          else:
               varerr = "All Fields Are Required/Check leave Year"
               getdetails = ""
          return render_to_response('leave/yettobeleave.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = yettotrainform()
            getdetails = ""#tblsetup.objects.all().order_by('name')
        return render_to_response('leave/yettobeleave.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def getleave(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tblleavesetup.objects.get(id = acccode)#.order_by('acccode')#tblaccount_acccode
                return render_to_response('leave/editleave.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')
