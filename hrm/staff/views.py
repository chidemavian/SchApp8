import os
from django.template import loader, Context,RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import  HttpResponseRedirect
from myproject.hrm.hrm.models import *
from myproject.hrm.staff.models import *
from myproject.hrm.hrm.form import *
from myproject.hrm.staff.form import *
from myproject.hrm.rcwadmin.models import *
from myproject.hrm.rcsetup.models import *
from myproject.hrm.rcwadmin.models import *
from django.db.models import Max,Sum
from django.contrib.sessions.models import Session
import datetime
from datetime import date,time
def enterstaff(request):
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.einventory
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/welcome/')
        varerr =""
        return render_to_response('staff/enterstaff.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')

def staffunauto(request):
     if  "userid" in request.session:
        varuser = request.session['userid']

        varerr =""
        return render_to_response('staff/unautorise.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')

def redeployment(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.stockin
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/staff/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = redeploymentform(request.POST) # A form bound to the POST data
          if form.is_valid():
            name = form.cleaned_data['name']
           # savecon = staffrec(oracleno = p,staffid = k,name = name,address = address,phoneno = phoneno,dateofbirth = birthdate,sex = sex,stateoforigin = stateoforigin,maritalstatus = maritalstatus,designation = designation,department = department,localgovtarea = localgovtarea,qualification = qualification,pensionno = pensionno,pfa = pfa,bankname = bankname,lgscno = lgscno,dateofresum = resumdate,level = level,step = step,nationality = nationality,commno = commno,jobasat = jobasat,spouse = spouse,spouseno = spouseno,spouseadd = spouseadd,reltype = reltype,relname = relname,relno = relno,reladd = reladd,reltype1 = reltype1,relname1 = relname1,relno1 = relno1,reladd1 = reladd1,chilname = chilname,chilsex = chilsex,chilno = chilno,chilname1 = chilname1,chilsex1 = chilsex1,chilno1 = chilno1,chilname2 = chilname2,chilsex2 = chilsex2,chilno2 = chilno2,chilname3 = chilname3,chilsex3 = chilsex3,chilno3 = chilno3,picture = photo_file,userid = varuser,status = 'ACTIVE')
            #savecon.save()
            return HttpResponseRedirect('/hrm/hrm/staffdata/')
          else:
               varerr = "All Fields Are Required"
               getdetails = ""
          return render_to_response('staff/redeployment.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

        else:
            form = redeploymentform()
            getdetails = ""#tbldesig.objects.all().order_by('desgcode')
        return render_to_response('staff/redeployment.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def redajax(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   #gdata = tblaccount.objects.all()
                   gdata = staffrec.objects.filter(staffid__contains = acccode,status = "ACTIVE").order_by('name')[:30]

                   return render_to_response('staff/testajax4.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = ""
                   return render_to_response('staff/testajax4.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('staff/testajax4.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def redajaxall(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   #gdata = tblaccount.objects.all()
                   gdata = staffrec.objects.get(staffid = acccode)

                   return render_to_response('staff/loadform.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = ""
                   return render_to_response('staff/loadform.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('staff/loadform.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def stafftestajaxstaff(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                  # print acccode
                   #print acccode
                   #gdata = staffrec.objects.filter(name__startswith = acccode).order_by('oracleno')
                   gdata = staffrec.objects.filter(name__contains = acccode,status = "ACTIVE").order_by('staffid')[:30]

                   return render_to_response('staff/testajax3.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = staffrec.objects.filter(status = "ACTIVE").order_by('staffid')
                   return render_to_response('staff/testajax3.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('staff/testajax3.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def editredeployment(request,invid):
        varerr =""
        getdetails = ""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.stockin
            if uenter == "False" :
              return HttpResponseRedirect('/hrm/staff/unauto/')
            varerr =""
            if request.method == 'POST':
                getdetails = ""
                staffid = request.POST['staffid']
                staffname = request.POST['staffname']
                sex = request.POST['sex']
                department = request.POST['department']
                newdepartment = request.POST['newdepartment']
                location1 = request.POST['location']
                newlocation1 = request.POST['newlocation']
                dateofred = request.POST['dateofred']


                if  sex == "" or department == "" or staffid == "" or staffname == "" or location1 == "" or dateofred == "":
                    varerr = "ALL FIELDS ARE REQUIRED"
                    gdept = tbldepartment.objects.all().order_by('name')
                    glocal = tbllg.objects.all().order_by('lgname')# location or branch
                    getdetails = staffrec.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    return render_to_response('staff/editredeployment.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'gdept':gdept,'glocal':glocal})
                caldate2 = dateofred.split('/')
                recdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                if department == newdepartment:
                    pass
                else:
                    deptsave = redept(staffid = staffid,staffname = staffname,sex = sex, currentdept = department,newdept = newdepartment,recdate = recdate,userid = varuser)
                    deptsave.save()
                    getstaff = staffrec.objects.get(id = invid)
                    getstaff.department = newdepartment
                    getstaff.save()
                if location1 == newlocation1:
                    pass
                else:
                    relsave = relocate(staffid = staffid,staffname = staffname,sex = sex, currentlocation = location1,newlocation = newlocation1,recdate = recdate,userid = varuser)
                    relsave.save()
                    getstaff1 = staffrec.objects.get(id = invid)
                    getstaff1.branch = newlocation1
                    getstaff1.save()

                #return render_to_response('staff/editredeployment.htm',{'varuser':varuser,'varerr':varerr})
                return HttpResponseRedirect('/hrm/staff/successful/')
            else:
                try:
                  gdept = tbldepartment.objects.all().order_by('name')
                  glocal = tbllg.objects.all().order_by('lgname')# location or branch
                  getdetails = staffrec.objects.get(id = invid)
                  return render_to_response('staff/editredeployment.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'gdept':gdept,'glocal':glocal})
                except:
                    varerr = "Record Not Exist"
                    return render_to_response('staff/editredeployment.htm',{'varuser':varuser,'varerr':varerr})
        else:
         return HttpResponseRedirect('/login/')

def ajaxaredeploy(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #gdata = staffrec.objects.filter(name__startswith = acccode).order_by('oracleno')
                   gdata = redept.objects.filter(staffid = acccode).order_by('id')
                   glocal = relocate.objects.filter(staffid = acccode).order_by('id')

                   return render_to_response('staff/testred.htm',{'gdata':gdata,'glocal':glocal,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = ""
                   glocal = ""
                   return render_to_response('staff/testred.htm',{'gdata':gdata ,'glocal':glocal})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('staff/testred.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def deptreport(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.stockin
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/staff/unauto/')
        varerr =""
        comp = tblcompanyinfo.objects.get(id = 1)
        getdetails = redept.objects.all().order_by('staffid','id')
        return render_to_response('staff/deptreport.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'comp':comp},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')
def locreport(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.stockin
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/staff/unauto/')
        varerr =""
        comp = tblcompanyinfo.objects.get(id = 1)
        getdetails = relocate.objects.all().order_by('staffid','id')
        return render_to_response('staff/localreport.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'comp':comp},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def promotion(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.stockin
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/staff/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = redeploymentform(request.POST) # A form bound to the POST data
          if form.is_valid():
            name = form.cleaned_data['name']
            #savecon = staffrec(oracleno = p,staffid = k,name = name,address = address,phoneno = phoneno,dateofbirth = birthdate,sex = sex,stateoforigin = stateoforigin,maritalstatus = maritalstatus,designation = designation,department = department,localgovtarea = localgovtarea,qualification = qualification,pensionno = pensionno,pfa = pfa,bankname = bankname,lgscno = lgscno,dateofresum = resumdate,level = level,step = step,nationality = nationality,commno = commno,jobasat = jobasat,spouse = spouse,spouseno = spouseno,spouseadd = spouseadd,reltype = reltype,relname = relname,relno = relno,reladd = reladd,reltype1 = reltype1,relname1 = relname1,relno1 = relno1,reladd1 = reladd1,chilname = chilname,chilsex = chilsex,chilno = chilno,chilname1 = chilname1,chilsex1 = chilsex1,chilno1 = chilno1,chilname2 = chilname2,chilsex2 = chilsex2,chilno2 = chilno2,chilname3 = chilname3,chilsex3 = chilsex3,chilno3 = chilno3,picture = photo_file,userid = varuser,status = 'ACTIVE')
            #savecon.save()
            return HttpResponseRedirect('/hrm/hrm/staffdata/')
          else:
               varerr = "All Fields Are Required"
               getdetails = ""
          return render_to_response('staff/promotion.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

        else:
            form = redeploymentform()
            getdetails = ""#tbldesig.objects.all().order_by('desgcode')
        return render_to_response('staff/promotion.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')
def stafftestajaxstaffpromo(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                  # print acccode
                   #print acccode
                   #gdata = staffrec.objects.filter(name__startswith = acccode).order_by('oracleno')
                   gdata = staffrec.objects.filter(name__contains = acccode,status = "ACTIVE").order_by('staffid')[:30]

                   return render_to_response('staff/testajax13.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = staffrec.objects.filter(status = "ACTIVE").order_by('staffid')
                   return render_to_response('staff/testajax13.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('staff/testajax13.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def editredeploymentpromo(request,invid):
        varerr =""
        getdetails = ""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.stockin
            if uenter == "False" :
              return HttpResponseRedirect('/hrm/staff/unauto/')
            varerr =""
            if request.method == 'POST':
                getdetails = ""
                staffid1 = request.POST['staffid']
                staffname = request.POST['staffname']
                sex = request.POST['sex']
                olddesignation = request.POST['olddesignation']
                level = request.POST['level']
                step = request.POST['step']
                newlevel = request.POST['newlevel']
                newstep = request.POST['newstep']
                newdesignation = request.POST['newdesignation']
                oldlevel = level +','+ step
                nlevel = newlevel + ','+ newstep
                dateofred = request.POST['dateofred']
                if  sex == "" or olddesignation == "" or staffid1 == "" or staffname == ""  or dateofred == "" :
                    varerr = "ALL FIELDS ARE REQUIRED"
                    gdept = tbldesig.objects.all().order_by('desc')#designation
                    getdetails = staffrec.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    return render_to_response('staff/editpromotion.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'gdept':gdept})
                caldate2 = dateofred.split('/')
                recdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                if olddesignation == newdesignation and level == newlevel and step == newstep :
                    pass
                else:
                    if olddesignation == newdesignation:
                        desg = olddesignation
                    else:
                        desg = newdesignation
                    if level == newlevel and step == newstep:
                        lev = oldlevel
                        nlev =  level
                    else:
                        lev = nlevel
                        nlev = newlevel
                    if step == newstep:
                        nstep = step
                    else:
                        nstep = newstep
                    getacc =  tblpromotion.objects.filter(staffid = staffid1).order_by('id')
                    for p in getacc:
                        recdate = p.recdate
                    relsave = tblpromotion(staffid = staffid1,staffname = staffname,sex = sex,olddesignation = desg,newdesignation = desg,recdate = recdate,userid = varuser,oldlevel = oldlevel,newlevel = lev)
                    relsave.save()
                    getstaff1 = staffrec.objects.get(id = invid)
                    getstaff1.designation = newdesignation
                    getstaff1.level = nlev
                    getstaff1.step = nstep
                    getstaff1.save()

                #return render_to_response('staff/editredeployment.htm',{'varuser':varuser,'varerr':varerr})
                return HttpResponseRedirect('/hrm/staff/successful/')
            else:
                try:
                  gdept = tbldesig.objects.all().order_by('desc')#designation
                  getdetails = staffrec.objects.get(id = invid)
                  level = tbllevel.objects.all().order_by('level')
                  step = tblstep.objects.all().order_by('level')
                  return render_to_response('staff/editpromotion.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'gdept':gdept,'level':level,'step':step})
                except:
                    varerr = "Record Not Exist"
                    return render_to_response('staff/editpromotion.htm',{'varuser':varuser,'varerr':varerr})
        else:
         return HttpResponseRedirect('/login/')

def ajaxaredeploypromo(request):
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
                   gdata = tblpromotion.objects.filter(staffid = acccode).order_by('id')
                   return render_to_response('staff/testpromo.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = ""
                   return render_to_response('staff/testpromo.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('staff/testpromo.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def promotionreport(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.stockin
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/staff/unauto/')
        varerr =""
        comp = tblcompanyinfo.objects.get(id = 1)
        getdetails = tblpromotion.objects.all().order_by('staffid','id')
        return render_to_response('staff/promotionreport.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'comp':comp},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def termination(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.stockout
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/staff/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = redeploymentform(request.POST) # A form bound to the POST data
          if form.is_valid():

            name = form.cleaned_data['name']


            #savecon = staffrec(oracleno = p,staffid = k,name = name,address = address,phoneno = phoneno,dateofbirth = birthdate,sex = sex,stateoforigin = stateoforigin,maritalstatus = maritalstatus,designation = designation,department = department,localgovtarea = localgovtarea,qualification = qualification,pensionno = pensionno,pfa = pfa,bankname = bankname,lgscno = lgscno,dateofresum = resumdate,level = level,step = step,nationality = nationality,commno = commno,jobasat = jobasat,spouse = spouse,spouseno = spouseno,spouseadd = spouseadd,reltype = reltype,relname = relname,relno = relno,reladd = reladd,reltype1 = reltype1,relname1 = relname1,relno1 = relno1,reladd1 = reladd1,chilname = chilname,chilsex = chilsex,chilno = chilno,chilname1 = chilname1,chilsex1 = chilsex1,chilno1 = chilno1,chilname2 = chilname2,chilsex2 = chilsex2,chilno2 = chilno2,chilname3 = chilname3,chilsex3 = chilsex3,chilno3 = chilno3,picture = photo_file,userid = varuser,status = 'ACTIVE')
            #savecon.save()
            return HttpResponseRedirect('/hrm/hrm/staffdata/')
          else:
               varerr = "All Fields Are Required"
               getdetails = ""
          return render_to_response('staff/termination.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

        else:
            form = redeploymentform()
            getdetails = ""#tbldesig.objects.all().order_by('desgcode')
        return render_to_response('staff/termination.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')
def stafftestajaxstaffterm(request):
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
                   gdata = staffrec.objects.filter(name__contains = acccode,status = "ACTIVE").order_by('staffid')[:30]

                   return render_to_response('staff/testajax133.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = staffrec.objects.filter(status = "ACTIVE").order_by('staffid')
                   return render_to_response('staff/testajax133.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('hrm/testajax133.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def editredeploymentterm(request,invid):
        varerr =""
        getdetails = ""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.stockout
            if uenter == "False" :
              return HttpResponseRedirect('/hrm/staff/unauto/')
            varerr =""
            if request.method == 'POST':
                getdetails = ""
                staffid1 = request.POST['staffid']
                staffname = request.POST['staffname']
                sex = request.POST['sex']
                dateofresumption = request.POST['dateofresumption']
                dateofred = request.POST['dateofred']

                if  sex == "" or dateofresumption == "" or staffid1 == "" or staffname == "" or dateofred == "" or dateofresumption == "":
                    varerr = "ALL FIELDS ARE REQUIRED"
                    gdept = tbldesig.objects.all().order_by('desc')#designation
                    getdetails = staffrec.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    return render_to_response('staff/edittermination.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'gdept':gdept})
                caldate2 = dateofred.split('/')
                recdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                caldate22 = dateofresumption.split('/')
                resdate = date(int(caldate22[2]),int(caldate22[1]),int(caldate22[0]))
                relsave = tbltermination(staffid = staffid1,staffname = staffname,sex = sex,resdate = resdate,recdate = recdate,userid = varuser)
                relsave.save()
                getstaff1 = staffrec.objects.get(id = invid)
                getstaff1.status = "DISMISSED"
                getstaff1.save()
                #return render_to_response('staff/editredeployment.htm',{'varuser':varuser,'varerr':varerr})
                return HttpResponseRedirect('/hrm/staff/successful/')
            else:
                try:
                  #gdept = tbldesig.objects.all().order_by('desc')#designation
                  getdetails = staffrec.objects.get(id = invid)
                  return render_to_response('staff/edittermination.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                except:
                    varerr = "Record Not Exist"
                    return render_to_response('staff/edittermination.htm',{'varuser':varuser,'varerr':varerr})
        else:
         return HttpResponseRedirect('/login/')

def terminationreport(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.stockout
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/staff/unauto/')
        varerr =""
        comp = tblcompanyinfo.objects.get(id = 1)
        getdetails = tbltermination.objects.all().order_by('staffid','id')
        return render_to_response('staff/terminationreport.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'comp':comp},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def resignation(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.stockout
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/staff/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = redeploymentform(request.POST,request.FILES) # A form bound to the POST data
          if form.is_valid():

            name = form.cleaned_data['name']


            #savecon = staffrec(oracleno = p,staffid = k,name = name,address = address,phoneno = phoneno,dateofbirth = birthdate,sex = sex,stateoforigin = stateoforigin,maritalstatus = maritalstatus,designation = designation,department = department,localgovtarea = localgovtarea,qualification = qualification,pensionno = pensionno,pfa = pfa,bankname = bankname,lgscno = lgscno,dateofresum = resumdate,level = level,step = step,nationality = nationality,commno = commno,jobasat = jobasat,spouse = spouse,spouseno = spouseno,spouseadd = spouseadd,reltype = reltype,relname = relname,relno = relno,reladd = reladd,reltype1 = reltype1,relname1 = relname1,relno1 = relno1,reladd1 = reladd1,chilname = chilname,chilsex = chilsex,chilno = chilno,chilname1 = chilname1,chilsex1 = chilsex1,chilno1 = chilno1,chilname2 = chilname2,chilsex2 = chilsex2,chilno2 = chilno2,chilname3 = chilname3,chilsex3 = chilsex3,chilno3 = chilno3,picture = photo_file,userid = varuser,status = 'ACTIVE')
            #savecon.save()
            return HttpResponseRedirect('/hrm/hrm/staffdata/')
          else:
               varerr = "All Fields Are Required"
               getdetails = ""
          return render_to_response('staff/resignation.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

        else:
            form = redeploymentform()
            getdetails = ""#tbldesig.objects.all().order_by('desgcode')
        return render_to_response('staff/resignation.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')
def stafftestajaxstaffresign(request):
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
                   gdata = staffrec.objects.filter(name__contains = acccode,status = "ACTIVE").order_by('staffid')[:30]

                   return render_to_response('staff/testajax1333.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = staffrec.objects.filter(status = "ACTIVE").order_by('staffid')
                   return render_to_response('staff/testajax1333.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('staff/testajax1333.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def editredeploymentresign(request,invid):
        varerr =""
        getdetails = ""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.stockout
            if uenter == "False" :
              return HttpResponseRedirect('/staff/unauto/')
            varerr =""
            if request.method == 'POST':
                getdetails = ""
                staffid1 = request.POST['staffid']
                staffname = request.POST['staffname']
                sex = request.POST['sex']
                dateofresumption = request.POST['dateofresumption']
                dateofred = request.POST['dateofred']

                if  sex == "" or dateofresumption == "" or staffid1 == "" or staffname == "" or dateofred == "" or dateofresumption == "":
                    varerr = "ALL FIELDS ARE REQUIRED"
                    gdept = tbldesig.objects.all().order_by('desc')#designation
                    getdetails = staffrec.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    return render_to_response('staff/editresignation.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'gdept':gdept})
                caldate2 = dateofred.split('/')
                recdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                caldate22 = dateofresumption.split('/')
                resdate = date(int(caldate22[2]),int(caldate22[1]),int(caldate22[0]))
                relsave = tblresignation(staffid = staffid1,staffname = staffname,sex = sex,resdate = resdate,recdate = recdate,userid = varuser)
                relsave.save()
                getstaff1 = staffrec.objects.get(id = invid)
                getstaff1.status = "RESIGNED"
                getstaff1.save()
                #return render_to_response('staff/editredeployment.htm',{'varuser':varuser,'varerr':varerr})
                return HttpResponseRedirect('/hrm/staff/successful/')
            else:
                try:
                  #gdept = tbldesig.objects.all().order_by('desc')#designation
                  getdetails = staffrec.objects.get(id = invid)
                  return render_to_response('staff/editresignation.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                except:
                    varerr = "Record Not Exist"
                    return render_to_response('staff/editresignation.htm',{'varuser':varuser,'varerr':varerr})
        else:
         return HttpResponseRedirect('/login/')

def resignationreport(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.stockout
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/staff/unauto/')
        varerr =""
        comp = tblcompanyinfo.objects.get(id = 1)
        getdetails = tblresignation.objects.all().order_by('staffid','id')
        return render_to_response('staff/resignationreport.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'comp':comp},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')


def retirement(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.stockout
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/staff/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = redeploymentform(request.POST) # A form bound to the POST data
          if form.is_valid():

            name = form.cleaned_data['name']


            #savecon = staffrec(oracleno = p,staffid = k,name = name,address = address,phoneno = phoneno,dateofbirth = birthdate,sex = sex,stateoforigin = stateoforigin,maritalstatus = maritalstatus,designation = designation,department = department,localgovtarea = localgovtarea,qualification = qualification,pensionno = pensionno,pfa = pfa,bankname = bankname,lgscno = lgscno,dateofresum = resumdate,level = level,step = step,nationality = nationality,commno = commno,jobasat = jobasat,spouse = spouse,spouseno = spouseno,spouseadd = spouseadd,reltype = reltype,relname = relname,relno = relno,reladd = reladd,reltype1 = reltype1,relname1 = relname1,relno1 = relno1,reladd1 = reladd1,chilname = chilname,chilsex = chilsex,chilno = chilno,chilname1 = chilname1,chilsex1 = chilsex1,chilno1 = chilno1,chilname2 = chilname2,chilsex2 = chilsex2,chilno2 = chilno2,chilname3 = chilname3,chilsex3 = chilsex3,chilno3 = chilno3,picture = photo_file,userid = varuser,status = 'ACTIVE')
            #savecon.save()
            return HttpResponseRedirect('/hrm/hrm/staffdata/')
          else:
               varerr = "All Fields Are Required"
               getdetails = ""
          return render_to_response('staff/retirement.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

        else:
            form = redeploymentform()
            getdetails = ""#tbldesig.objects.all().order_by('desgcode')
        return render_to_response('staff/retirement.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')
def stafftestajaxstaffretire(request):
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
                   gdata = staffrec.objects.filter(name__contains = acccode,status = "ACTIVE").order_by('staffid')[:30]

                   return render_to_response('staff/testajax13333.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = staffrec.objects.filter(status = "ACTIVE").order_by('staffid')
                   return render_to_response('staff/testajax13333.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('staff/testajax13333.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def editredeploymentretire(request,invid):
        varerr =""
        getdetails = ""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.stockout
            if uenter == "False" :
              return HttpResponseRedirect('/hrm/staff/unauto/')
            varerr =""
            if request.method == 'POST':
                getdetails = ""
                staffid1 = request.POST['staffid']
                staffname = request.POST['staffname']
                sex = request.POST['sex']
                dateofresumption = request.POST['dateofresumption']
                dateofred = request.POST['dateofred']

                if  sex == "" or dateofresumption == "" or staffid1 == "" or staffname == "" or dateofred == "" or dateofresumption == "":
                    varerr = "ALL FIELDS ARE REQUIRED"
                    gdept = tbldesig.objects.all().order_by('desc')#designation
                    getdetails = staffrec.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    return render_to_response('staff/editretirement.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'gdept':gdept})
                caldate2 = dateofred.split('/')
                recdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                caldate22 = dateofresumption.split('/')
                resdate = date(int(caldate22[2]),int(caldate22[1]),int(caldate22[0]))
                relsave = tblretirement(staffid = staffid1,staffname = staffname,sex = sex,resdate = resdate,recdate = recdate,userid = varuser)
                relsave.save()
                getstaff1 = staffrec.objects.get(id = invid)
                getstaff1.status = "RETIRED"
                getstaff1.save()
                #return render_to_response('staff/editredeployment.htm',{'varuser':varuser,'varerr':varerr})
                return HttpResponseRedirect('/hrm/staff/successful/')
            else:
                try:
                  #gdept = tbldesig.objects.all().order_by('desc')#designation
                  getdetails = staffrec.objects.get(id = invid)
                  return render_to_response('staff/editretirement.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                except:
                    varerr = "Record Not Exist"
                    return render_to_response('staff/editretirement.htm',{'varuser':varuser,'varerr':varerr})
        else:
         return HttpResponseRedirect('/login/')

def retirementreport(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.stockout
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/staff/unauto/')
        varerr =""
        comp = tblcompanyinfo.objects.get(id = 1)
        getdetails = tblretirement.objects.all().order_by('staffid','id')
        return render_to_response('staff/retirementreport.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'comp':comp},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def reinstatement(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.stockreport
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/staff/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = redeploymentform(request.POST) # A form bound to the POST data
          if form.is_valid():
            name = form.cleaned_data['name']
            #savecon = staffrec(oracleno = p,staffid = k,name = name,address = address,phoneno = phoneno,dateofbirth = birthdate,sex = sex,stateoforigin = stateoforigin,maritalstatus = maritalstatus,designation = designation,department = department,localgovtarea = localgovtarea,qualification = qualification,pensionno = pensionno,pfa = pfa,bankname = bankname,lgscno = lgscno,dateofresum = resumdate,level = level,step = step,nationality = nationality,commno = commno,jobasat = jobasat,spouse = spouse,spouseno = spouseno,spouseadd = spouseadd,reltype = reltype,relname = relname,relno = relno,reladd = reladd,reltype1 = reltype1,relname1 = relname1,relno1 = relno1,reladd1 = reladd1,chilname = chilname,chilsex = chilsex,chilno = chilno,chilname1 = chilname1,chilsex1 = chilsex1,chilno1 = chilno1,chilname2 = chilname2,chilsex2 = chilsex2,chilno2 = chilno2,chilname3 = chilname3,chilsex3 = chilsex3,chilno3 = chilno3,picture = photo_file,userid = varuser,status = 'ACTIVE')
            #savecon.save()
            return HttpResponseRedirect('/hrm/hrm/staffdata/')
          else:
               varerr = "All Fields Are Required"
               getdetails = ""
          return render_to_response('staff/reinstatement.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

        else:
            form = redeploymentform()
            getdetails = ""#tbldesig.objects.all().order_by('desgcode')
        return render_to_response('staff/reinstatement.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')
def stafftestajaxstaffreinstate(request):
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
                   gdata = staffrec.objects.filter(name__contains = acccode).exclude(status = "ACTIVE").order_by('staffid')[:30]

                   return render_to_response('staff/testajax13333r.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = staffrec.objects.filter().exclude(status = "ACTIVE").order_by('staffid')
                   return render_to_response('staff/testajax13333r.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('staff/testajax13333r.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def editredeploymentreinstate(request,invid):
        varerr =""
        getdetails = ""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.stockreport
            if uenter == "False" :
              return HttpResponseRedirect('/hrm/staff/unauto/')
            varerr =""
            if request.method == 'POST':
                getdetails = ""
                staffid1 = request.POST['staffid']
                staffname = request.POST['staffname']
                sex = request.POST['sex']
                dateofresumption = request.POST['dateofresumption']
                dateofred = request.POST['dateofred']

                if  sex == "" or dateofresumption == "" or staffid1 == "" or staffname == "" or dateofred == "" or dateofresumption == "":
                    varerr = "ALL FIELDS ARE REQUIRED"
                    gdept = tbldesig.objects.all().order_by('desc')#designation
                    getdetails = staffrec.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    return render_to_response('staff/editreinstatement.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'gdept':gdept})
                caldate2 = dateofred.split('/')
                recdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                caldate22 = dateofresumption.split('/')
                resdate = date(int(caldate22[2]),int(caldate22[1]),int(caldate22[0]))
                getstaff1 = staffrec.objects.get(id = invid)
                getstaff1.status = "ACTIVE"
                getstaff1.save()
                if tbltermination.objects.filter(staffid = staffid1).count() == 0:
                    pass
                else:
                    delt = tbltermination.objects.get(staffid = staffid1).delete()
                if tblresignation.objects.filter(staffid = staffid1).count() == 0:
                    pass
                else:
                    delrs = tblresignation.objects.get(staffid = staffid1).delete()
                if tblretirement.objects.filter(staffid = staffid1).count()==0:
                    pass
                else:
                    delrt = tblretirement.objects.get(staffid = staffid1).delete()

                #return render_to_response('staff/editredeployment.htm',{'varuser':varuser,'varerr':varerr})
                return HttpResponseRedirect('/hrm/staff/successful/')
            else:
                try:
                  #gdept = tbldesig.objects.all().order_by('desc')#designation
                  getdetails = staffrec.objects.get(id = invid)
                  return render_to_response('staff/editreinstatement.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                except:
                    varerr = "Record Not Exist"
                    return render_to_response('staff/editreinstatement.htm',{'varuser':varuser,'varerr':varerr})
        else:
         return HttpResponseRedirect('/login/')

def staffsuccessfull(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
       # uenter = user.receipt
        #if uenter == "False" :
         #   return HttpResponseRedirect('/staff/unauto/')
        varerr =""
        #form = editstaform()
        return render_to_response('staff/opsuccessful.htm',{'varuser':varuser,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def getredeployment(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                gdept = tbldepartment.objects.all().order_by('name')
                glocal = tbllg.objects.all().order_by('lgname')# location or branch
                getdetails = staffrec.objects.get(id = acccode)
                return render_to_response('staff/editredeployment.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'gdept':gdept,'glocal':glocal})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def gettermination(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = staffrec.objects.get(id = acccode)
                return render_to_response('staff/edittermination.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')



def getresignation(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = staffrec.objects.get(id = acccode)
                return render_to_response('staff/editresignation.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getretirement(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = staffrec.objects.get(id = acccode)
                return render_to_response('staff/editretirement.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getreinstatement(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = staffrec.objects.get(id = acccode)
                return render_to_response('staff/editreinstatement.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')
