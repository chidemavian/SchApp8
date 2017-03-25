import os
from django.template import loader, Context,RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.core.serializers.json import simplejson as json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import  HttpResponseRedirect
from myproject.hrm.hrm.models import *
from myproject.hrm.staff.models import *
from myproject.hrm.hrm.form import *
from myproject.hrm.leave.models import *
from myproject.hrm.rcsetup.models import *
from myproject.hrm.rcwadmin.models import *
from myproject.hrm.payroll.models import *
from myproject.hrm.train.models import *
from myproject.hrm.payroll.capy import *
from myproject.hrm.query.models import *
from myproject.hrm.utils import *
from django.db.models import Max,Sum
from django.contrib.sessions.models import Session
import datetime
from datetime import date,time,timedelta
import xlwt
from django.core.serializers.json import simplejson as json

def enterhrm(request):
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.eposting
        if uenter == "False" :
            return HttpResponseRedirect('/welcome/')
        varerr =""
        return render_to_response('hrm/enterhrm.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')

def pounauto(request):
     if  "userid" in request.session:
        varuser = request.session['userid']

        varerr =""
        return render_to_response('hrm/unautorise.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')


def hrmtestajax(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   #gdata = tblaccount.objects.all()
                   gdata = tbldesig.objects.filter(desgcode__contains = acccode).order_by('desgcode')

                   return render_to_response('hrm/testajax.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = ""
                   return render_to_response('hrm/testajax.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('hrm/testajax.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def hrmtestajaxall(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   #gdata = tblaccount.objects.all()
                   gdata = tblallowance.objects.filter(desgcode = acccode).order_by('id')

                   return render_to_response('hrm/testajax1.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = ""
                   return render_to_response('hrm/testajax1.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('hrm/testajax1.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')


def hrmstaffdata(request):
     varerr =""
     if  "userid" in request.session:
       if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.invoice
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/hrm/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = staffdataform(request.POST,request.FILES) # A form bound to the POST data
          if form.is_valid():
            staffid = form.cleaned_data['staffid']
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            phoneno = form.cleaned_data['phoneno']
            dateofbirth = form.cleaned_data['dateofbirth']
            sex = form.cleaned_data['sex']
            maritalstatus = form.cleaned_data['maritalstatus']
            nationality = form.cleaned_data['nationality']
            stateoforigin = form.cleaned_data['stateoforigin']
            localgovt = form.cleaned_data['localgovt']
            email = form.cleaned_data['email']
            nextofkin = form.cleaned_data['nextofkin']
            nextofkinaddress = form.cleaned_data['nextofkinaddress']
            nextofkinphone = form.cleaned_data['nextofkinphone']
            department = form.cleaned_data['department']
            dateofresum = form.cleaned_data['dateofresum']
            firstguarantor = form.cleaned_data['firstguarantor']
            firstguarantoraddress = form.cleaned_data['firstguarantoraddress']
            secondguarantor = form.cleaned_data['secondguarantor']
            secondguarantoraddress = form.cleaned_data['secondguarantoraddress']
            designation = form.cleaned_data['designation']
            qualification = form.cleaned_data['qualification']
            branch = form.cleaned_data['branch']
            profession = form.cleaned_data['profession']
            level = form.cleaned_data['level']
            step = form.cleaned_data['step']
            caldate2 = dateofbirth.split('/')
            birthdate = date(int(caldate2[2]),int(caldate2[1]),int(caldate2[0]))
            caldate22 = dateofresum.split('/')
            resumdate = date(int(caldate22[2]),int(caldate22[1]),int(caldate22[0]))
            rfile = form.cleaned_data['picture']
            k = str(staffid)
            k = k.upper()

            if rfile is None:
                #print 'no file'
                photo_file = 'staff/user.png'
            else:
                #print 'file exist'
                photo_file = request.FILES['picture']

            if staffrec.objects.filter(staffid = k).count() == 0:
                 pass
            else:
                varerr = "Staff Id No IN EXISTENCE"
                return render_to_response('hrm/staffdata.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

            savecon = staffrec(staffid = k,name = name,address = address,phoneno = phoneno,dateofbirth = birthdate,sex = sex,nationality = nationality,stateoforigin = stateoforigin,localgovt = localgovt,email = email,nextofkin = nextofkin,nextofkinaddress = nextofkinaddress,nextofkinphone = nextofkinphone,maritalstatus = maritalstatus,designation = designation,department = department,dateofresum = resumdate,picture = photo_file,userid = varuser,status = 'ACTIVE',firstguarantor = firstguarantor,firstguarantoraddress = firstguarantoraddress,secondguarantor = secondguarantor,secondguarantoraddress = secondguarantoraddress,qualification = qualification,branch = branch,profession = profession,workedday = 28,level = level,step = step)
            savecon.save()
            return HttpResponseRedirect('/hrm/hrm/successful/')
          else:
               varerr = "All Fields Are Required/Check Inputed Picture"
               getdetails = ""
          return render_to_response('hrm/staffdata.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

        else:
            form = staffdataform()
            getdetails = ""#tbldesig.objects.all().order_by('desgcode')
        return render_to_response('hrm/staffdata.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def editstaff(request):
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.receipt
        if uenter == "False" :
           return HttpResponseRedirect('/hrm/hrm/unauto/')
        varerr =""
        form = editstaform()
        return render_to_response('hrm/editstaffrec.htm',{'varuser':varuser,'varerr':varerr,'form':form})
     else:
       return HttpResponseRedirect('/login/')

def hrmtestajaxstaff(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                  # print acccode
                   #print acccode
                   #gdata = tblaccount.objects.all()
                   gdata = staffrec.objects.filter(name__contains = acccode,status ="ACTIVE").order_by('name')[:20]
                   return render_to_response('hrm/testajax3.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = staffrec.objects.all().order_by('oracleno')
                   return render_to_response('hrm/testajax3.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('hrm/testajax3.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def editstaffid(request,invid):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.receipt
            if uenter == "False" :
              return HttpResponseRedirect('/hrm/hrm/unauto/')
            varerr =""
            if request.method == 'POST':
                getdetails = ""
                staffid = request.POST['staffid']
                name = request.POST['name']
                address = request.POST['address']
                phoneno = request.POST['phoneno']
                dateofbirth = request.POST['dateofbirth']
                sex = request.POST['sex']
                maritalstatus = request.POST['maritalstatus']
                nationality = request.POST['nationality']
                stateoforigin = request.POST['stateoforigin']
                localgovt = request.POST['localgovt']
                email = request.POST['email']
                nextofkin = request.POST['nextofkin']
                nextofkinaddress = request.POST['nextofkinaddress']
                nextofkinphone = request.POST['nextofkinphone']
                department = request.POST['department']
                dateofresum = request.POST['dateofresum']
                firstguarantor = request.POST['firstguarantor']
                firstguarantoraddress = request.POST['firstguarantoraddress']
                secondguarantor = request.POST['secondguarantor']
                secondguarantoraddress = request.POST['secondguarantoraddress']
                status = request.POST['status']
                qualification = request.POST['qualification']
                branch = request.POST['branch']
                profession = request.POST['profession']
                caldate2 = dateofbirth.split('/')
                #print caldate2[1]
                birthdate = date(int(caldate2[2]),int(caldate2[1]),int(caldate2[0]))
                caldate22 = dateofresum.split('/')
                resumdate = date(int(caldate22[2]),int(caldate22[1]),int(caldate22[0]))
                k = str(staffid)
                k = k.upper()
                oldid = request.POST['hcode']
                oldname = request.POST['hcode1']
                #print oldname,oldid
                if 'picture' in request.FILES:
                    photo_file = request.FILES['picture']
                    k1 = str(photo_file.name)
                    j = k1.split('.')[1]
                    j = j.lower()
                    #print k,j
                    if not (j in ['jpeg','jpg','png','bmp']):
                       varerr = "%s is not a required picture" % k1
                       #getdetails = staffrec.objects.get(id = invid)
                       return HttpResponseRedirect('/hrm/hrm/editstaff/')
                      # return render_to_response('hrm/editstaffdata.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                    else:
                       pass
                else:
                     gda =  staffrec.objects.get(id = invid)
                    # print gda.picture
                     photo_file = gda.picture

                if  staffrec.objects.filter(staffid = k).exclude(id = invid).count() == 0 :
                    pass
                else:
                    varerr = "Staff With Staff No %s In Existence" % staffid
                    #getdetails = staffrec.objects.get(id = invid)
                    return HttpResponseRedirect('/hrm/hrm/editstaff/')
                    #return render_to_response('hrm/editstaffrec.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})

                if  staffid == "" or name == "" or address == "" or phoneno == "" or dateofbirth == "" or sex == "" or maritalstatus == "" or nationality == "" or stateoforigin == "" or   localgovt == "" or email == "" or nextofkin == "" or nextofkinaddress == "" or nextofkinphone == "" or department == "" or dateofresum == "" or firstguarantor == "" or firstguarantoraddress == "" or secondguarantor == "" or secondguarantoraddress == ""  or qualification == "" or branch == "" :
                    varerr = "ALL FIELDS ARE REQUIRED"
                    #getdetails = staffrec.objects.get(id = invid)
                    return HttpResponseRedirect('/hrm/hrm/editstaff/')
                    #return render_to_response('hrm/editstaffdata.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                if oldid == staffid and oldname == name :
                   seldata = staffrec.objects.get(id = invid)
                   seldata.name = name
                   seldata.address = address
                   seldata.phoneno = phoneno
                   seldata.dateofbirth = birthdate
                   seldata.sex = sex
                   seldata.maritalstatus = maritalstatus
                   seldata.nationality = nationality
                   seldata.stateoforigin = stateoforigin
                   seldata.localgovt = localgovt
                   seldata.email = email
                   seldata.nextofkin = nextofkin
                   seldata.nextofkinaddress = nextofkinaddress
                   seldata.nextofkinphone = nextofkinphone
                   seldata.department = department
                   seldata.dateofresum = resumdate
                   seldata.firstguarantor = firstguarantor
                   seldata.firstguarantoraddress = firstguarantoraddress
                   seldata.secondguarantor = secondguarantor
                   seldata.secondguarantoraddress = secondguarantoraddress
                   seldata.status = status
                   seldata.qualification = qualification
                   seldata.branch = branch
                   seldata.profession = profession
                   seldata.picture = photo_file
                   seldata.userid = varuser
                   seldata.save()
                   return HttpResponseRedirect('/hrm/hrm/successful/')
                else:
                   if staffrec.objects.filter(staffid = staffid).exclude(id = invid).count() == 0:
                       seldata = staffrec.objects.get(id = invid)
                       seldata.name = name
                       seldata.address = address
                       seldata.phoneno = phoneno
                       seldata.dateofbirth = birthdate
                       seldata.sex = sex
                       seldata.maritalstatus = maritalstatus
                       seldata.nationality = nationality
                       seldata.stateoforigin = stateoforigin
                       seldata.localgovt = localgovt
                       seldata.email = email
                       seldata.nextofkin = nextofkin
                       seldata.nextofkinaddress = nextofkinaddress
                       seldata.nextofkinphone = nextofkinphone
                       seldata.department = department
                       seldata.dateofresum = resumdate
                       seldata.firstguarantor = firstguarantor
                       seldata.firstguarantoraddress = firstguarantoraddress
                       seldata.secondguarantor = secondguarantor
                       seldata.secondguarantoraddress = secondguarantoraddress
                       seldata.status = status
                       seldata.qualification = qualification
                       seldata.branch = branch
                       seldata.profession = profession
                       seldata.picture = photo_file
                       seldata.userid = varuser
                       seldata.staffid = staffid
                       seldata.save()
                       tblpayroll.objects.filter(staffid = oldid).update(staffid = staffid,staffname = name)
                       tblbankdetails.objects.filter(staffid = oldid).update(staffid = staffid,staffname = name)
                       tblstaffedu.objects.filter(staffid = oldid).update(staffid = staffid,staffname = name)
                       tblstaffproff.objects.filter(staffid = oldid).update(staffid = staffid,staffname = name)
                       tblspall.objects.filter(staffid = oldid).update(staffid = staffid,staffname = name)
                       tblspded.objects.filter(staffid = oldid).update(staffid = staffid,staffname = name)#tblsavings
                       tblsavings.objects.filter(staffid = oldid).update(staffid = staffid,staffname = name)#tblloan
                       tblloan.objects.filter(staffid = oldid).update(staffid = staffid,staffname = name)#tblpayrollpension
                       tblpayrollpension.objects.filter(staffid = oldid).update(staffid = staffid)#tblpayrollpension
                       tblleave.objects.filter(staffid = oldid).update(staffid = staffid,staffname = name)
                       redept.objects.filter(staffid = oldid).update(staffid = staffid,staffname = name)
                       relocate.objects.filter(staffid = oldid).update(staffid = staffid,staffname = name)
                       tblpromotion.objects.filter(staffid = oldid).update(staffid = staffid,staffname = name)
                       tbltermination.objects.filter(staffid = oldid).update(staffid = staffid,staffname = name)
                       tblresignation.objects.filter(staffid = oldid).update(staffid = staffid,staffname = name)
                       tblretirement.objects.filter(staffid = oldid).update(staffid = staffid,staffname = name)
                       tbltraining.objects.filter(staffid = oldid).update(staffid = staffid,staffname = name)
                       tblstaffhmo.objects.filter(staffid = oldid).update(staffid = staffid,staffname = name)
                       tblstaffpfa.objects.filter(staffid = oldid).update(staffid = staffid,staffname = name)
                       tblstaffquery.objects.filter(staffid = oldid).update(staffid = staffid,staffname = name)
                       tblstaffquery.objects.filter(querygiverid = oldid).update(querygiverid = staffid,querygiver = name)
                       tblstaffquerydeleted.objects.filter(staffid = oldid).update(staffid = staffid,staffname = name)
                       tblstaffquerydeleted.objects.filter(querygiverid = oldid).update(querygiverid = staffid,querygiver = name)
                       return HttpResponseRedirect('/hrm/hrm/successful/')
            else:
                try:
                  desg =  tbldesig.objects.all().order_by('desc')
                  state = tblstate.objects.all().order_by('state')
                  localgt = tbllocalgovt.objects.all().order_by('localgovt')
                  gdept = tbldepartment.objects.all().order_by('name')
                  glocal = tbllg.objects.all().order_by('lgname')
                  level = tbllevel.objects.all().order_by('level')
                  step = tblstep.objects.all().order_by('level')
                  getdetails = staffrec.objects.get(id = invid)
                  return render_to_response('hrm/editstaffdata.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'desg':desg,'gdept':gdept,'glocal':glocal,'state':state,'localgt':localgt,'level':level,'step':step})
                except:
                    varerr = "Record Not Exist"
                    return render_to_response('hrm/editstaffdata.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
        else:
         return HttpResponseRedirect('/login/')

def hrmstaffedu(request):
     varerr =""
     if  "userid" in request.session:
       if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.payment
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/hrm/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = staffeduform(request.POST) # A form bound to the POST data
          if form.is_valid():
             staffid = form.cleaned_data['staffid']
             staffname = form.cleaned_data['staffname']
             nameofsch = form.cleaned_data['nameofsch']
             courseofstu = form.cleaned_data['courseofstu']
             certificateob = form.cleaned_data['certificateob']
             gradeobtained = form.cleaned_data['gradeobtained']
             entryyear = form.cleaned_data['entryyear']
             exityear = form.cleaned_data['exityear']

##                return render_to_response('hrm/staffedu.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             savecon = tblstaffedu(staffid = staffid,staffname = staffname,nameofsch = nameofsch,courseofstu = courseofstu,certificateob = certificateob,gradeobtained = gradeobtained,entryyear = entryyear,exityear = exityear, userid = varuser )
             savecon.save()
             return HttpResponseRedirect('/hrm/hrm/staffedu/')
        else:

            form = staffeduform()
            getdetails = ""#tbldesig.objects.all().order_by('desgcode')
        return render_to_response('hrm/staffedu.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')


def hrmeduajax(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   #gdata = tblaccount.objects.all()
                   gdata = staffrec.objects.filter(staffid__startswith = acccode,status ="ACTIVE").order_by('name')[:30]
                   return render_to_response('hrm/testajax4.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = ""
                   return render_to_response('hrm/testajax4.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('hrm/testajax4.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def hrmeduajaxall(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   #gdata = tblaccount.objects.all()
                   gdata = tblstaffedu.objects.filter(staffid = acccode).order_by('id')

                   return render_to_response('hrm/testajax5.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = ""
                   return render_to_response('hrm/testajax5.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('hrm/testajax5.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def hrmeduajaxallproff(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   gdata = tblstaffproff.objects.filter(staffid = acccode).order_by('id')
                   return render_to_response('hrm/testajax7.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = ""
                   return render_to_response('hrm/testajax7.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('hrm/testajax7.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def editstaffedu(request,invid):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.payment
            if uenter == "False" :
              return HttpResponseRedirect('/hrm/hrm/unauto/')
            varerr =""
            if request.method == 'POST':
                getdetails = ""
                staffid = request.POST['staffid']
                staffname = request.POST['staffname']
                nameofsch = request.POST['nameofsch']
                courseofstu = request.POST['courseofstu']
                certificateob = request.POST['certificateob']
                gradeobtained = request.POST['gradeobtained']
                entryyear = request.POST['entryyear']
                exityear = request.POST['exityear']
                if  nameofsch == "" or courseofstu == "" or staffid == "" or staffname == "" or entryyear == "" or exityear == "":
                    varerr = "ALL FIELDS ARE REQUIRED"
                    getdetails = tblstaffedu.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    #return render_to_response('hrm/editstaffedu.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                    return HttpResponseRedirect('/hrm/hrm/staffedu/')
                seldata = tblstaffedu.objects.get(id = invid)
                seldata.nameofsch = nameofsch
                seldata.courseofstu = courseofstu
                seldata.certificateob = certificateob
                seldata.gradeobtained = gradeobtained
                seldata.entryyear = entryyear
                seldata.exityear = exityear
                seldata.userid = varuser
                seldata.save()
                return HttpResponseRedirect('/hrm/hrm/staffedu/')
            else:
                try:
                  getdetails = tblstaffedu.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                  return render_to_response('hrm/editstaffedu.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                except:
                    varerr = "Account Not Exist"
                    return render_to_response('hrm/editstaffedu.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
        else:
         return HttpResponseRedirect('/login/')

def deletestaffedu(request,invid):
    varerr =""
    if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            seldata = tblstaffedu.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/hrm/hrm/staffedu/')

    else:
      return HttpResponseRedirect('/login/')

def hrmsetuspded(request):
     varerr =""
     if  "userid" in request.session:
       if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.jobsetup
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/hrm/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = spallform(request.POST) # A form bound to the POST data
          if form.is_valid():
             staffid = form.cleaned_data['staffid']
             staffname = form.cleaned_data['staffname']
             amount = form.cleaned_data['amount']
             paydesc = form.cleaned_data['paydesc']
             ##             if tblstaffdata.objects.filter(staffid = staffid).count() == 0:
##                 pass
##             else:
##                varerr = "STAFF ID IN EXISTENCE"
##                return render_to_response('hrm/staffedu.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             savecon = tblspded(staffid = staffid,staffname = staffname,amount = amount,paydes = paydesc,userid = varuser)
             savecon.save()
             return HttpResponseRedirect('/hrm/hrm/hrmsetuspded/')
        else:

            form = spallform()
            getdetails = tblspded.objects.all().order_by('staffid')
        return render_to_response('hrm/speded.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')

def editspded(request,invid):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.jobsetup
            if uenter == "False" :
              return HttpResponseRedirect('/hrm/hrm/unauto/')
            varerr =""
            if request.method == 'POST':
                getdetails = ""
                staffid = request.POST['staffid'] # the amount
                staffname = request.POST['staffname']#the primary key
                amount = request.POST['amount']#the particulars
                paydesc = request.POST['paydesc']
               # desc = request.POST['desc']

                if  paydesc == "" or amount == "" :
                    varerr = "ALL FIELDS ARE REQUIRED"
                    getdetails = tblspded.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    return render_to_response('hrm/editspded.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                try:
                    k = float(amount)
                except:
                    varerr = "INVALID AMOUNT"
                    getdetails = tblspded.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    return render_to_response('hrm/editspded.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                seldata = tblspded.objects.get(id = invid)
                seldata.amount = amount
                seldata.paydes = paydesc
                seldata.userid = varuser
                seldata.save()
                return HttpResponseRedirect('/hrm/hrm/hrmsetuspded/')
            else:
                try:
                  getdetails = tblspded.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                  return render_to_response('hrm/editspded.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                except:
                    varerr = "Account Not Exist"
                    return render_to_response('hrm/editspded.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
        else:
         return HttpResponseRedirect('/login/')


def deletespded(request,invid):
    varerr =""
    if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            seldata = tblspded.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/hrm/hrm/hrmsetuspded/')

    else:
      return HttpResponseRedirect('/login/')

def ddltest(request):
    form = testdata()
    return render_to_response('hrm/ddltest.htm',{'form':form},context_instance = RequestContext(request))

def ddltestajax(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   #gdata = tblaccount.objects.all()
                   gdata = tbldesig.objects.all().order_by('desgcode')

                   return render_to_response('hrm/testajax6.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = ""
                   return render_to_response('hrm/testajax6.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('hrm/testajax6.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')


def hrmstaffproff(request):
     varerr =""
     if  "userid" in request.session:
       if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.payment
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/hrm/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = proffeduform(request.POST) # A form bound to the POST data
          if form.is_valid():
             staffid = form.cleaned_data['staffid']
             staffname = form.cleaned_data['staffname']
             bodyname = form.cleaned_data['bodyname']
             qualification = form.cleaned_data['qualification']
             exityear = form.cleaned_data['exityear']
             savecon = tblstaffproff(staffid = staffid,staffname = staffname,bodyname = bodyname,qualification = qualification,exityear = exityear,userid = varuser )
             savecon.save()
             return HttpResponseRedirect('/hrm/hrm/staffproff/')
        else:
            form = proffeduform()
            getdetails = ""#tbldesig.objects.all().order_by('desgcode')
        return render_to_response('hrm/staffproff.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')

def hrmstaffnonpension(request):
     varerr =""
     if  "userid" in request.session:
       if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.genledger
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/hrm/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = nonpensionform(request.POST) # A form bound to the POST datahrm
          if form.is_valid():
             category = form.cleaned_data['category']
             staffname = form.cleaned_data['staffname']
             address = form.cleaned_data['address']
             phoneno = form.cleaned_data['phoneno']
             nextofkin = form.cleaned_data['nextofkin']
             sex = form.cleaned_data['sex']
             session = form.cleaned_data['session']
             savecon = tblstaffnonpension(category = category,staffname = staffname,address = address,phoneno = phoneno,nextofkin = nextofkin,sex = sex,session = session ,userid = varuser )
             savecon.save()
             return HttpResponseRedirect('/hrm/hrm/staffnonpension/')
        else:

            form = nonpensionform()
            getdetails = tblstaffnonpension.objects.all().order_by('category','id')
        return render_to_response('hrm/staffpension.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')

def editstaffproff(request,invid):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.payment
            if uenter == "False" :
              return HttpResponseRedirect('/hrm/hrm/unauto/')
            varerr =""
            if request.method == 'POST':
                getdetails = ""
                staffid = request.POST['staffid']
                staffname = request.POST['staffname']
                bodyname = request.POST['bodyname']
                qualification = request.POST['qualification']
                exityear = request.POST['exityear']
                if  bodyname == "" or qualification == "" or staffid == "" or staffname == ""  or exityear == "":
                    varerr = "ALL FIELDS ARE REQUIRED"
                    #getdetails = tblstaffproff.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    #return render_to_response('hrm/editstaffproff.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                    return HttpResponseRedirect('//hrm/staffproff/')
                seldata = tblstaffproff.objects.get(id = invid)
                seldata.bodyname = bodyname
                seldata.qualification = qualification
                seldata.exityear = exityear
                seldata.userid = varuser
                seldata.save()
                return HttpResponseRedirect('/hrm/hrm/staffproff/')
            else:
                try:
                  getdetails = tblstaffproff.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                  return render_to_response('hrm/editstaffproff.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                except:
                    varerr = "Account Not Exist"
                    return render_to_response('hrm/editstaffproff.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
        else:
         return HttpResponseRedirect('/login/')

def deletestaffproff(request,invid):
    varerr =""
    if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            seldata = tblstaffproff.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/hrm/hrm/staffproff/')

    else:
      return HttpResponseRedirect('/login/')
def editstaffnonpension(request,invid):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.genledger
            if uenter == "False" :
              return HttpResponseRedirect('/hrm/hrm/unauto/')
            varerr =""
            if request.method == 'POST':
                getdetails = ""
                category = request.POST['category']
                staffname = request.POST['staffname']
                address = request.POST['address']
                phoneno = request.POST['phoneno']
                nextofkin = request.POST['nextofkin']
                sex = request.POST['sex']
                session = request.POST['session']
                if  address == "" or phoneno == "" or nextofkin == "" or staffname == ""  or session == "":
                    varerr = "ALL FIELDS ARE REQUIRED"
                    getdetails = tblstaffnonpension.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    return render_to_response('hrm/editnonpension.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                seldata = tblstaffnonpension.objects.get(id = invid)
                seldata.category = category
                seldata.staffname = staffname
                seldata.address = address
                seldata.phoneno = phoneno
                seldata.nextofkin = nextofkin
                seldata.sex = sex
                seldata.session = session
                seldata.userid = varuser
                seldata.save()
                return HttpResponseRedirect('/hrm/hrm/staffnonpension/')
            else:
                try:
                  gdata = tblcategory.objects.all().order_by('name')
                  getdetails = tblstaffnonpension.objects.get(id = invid)
                  return render_to_response('hrm/editnonpension.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'gdata':gdata})
                except:
                    varerr = "Account Not Exist"
                    return render_to_response('hrm/editnonpension.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
        else:
         return HttpResponseRedirect('/login/')

def deletestaffnonpension(request,invid):
    varerr =""
    if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            seldata = tblstaffnonpension.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/hrm/hrm/staffnonpension/')

    else:
      return HttpResponseRedirect('/login/')

def hrmstaffreport(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.standardledger
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/hrm/unauto/')
        varerr =""
        if request.method == 'POST':
          form = staffrepform(request.POST) # A form bound to the POST data
          if form.is_valid():
            status = form.cleaned_data['status']
            qualification = form.cleaned_data['qualification']
            sex = form.cleaned_data['sex']
            comp = tblcompanyinfo.objects.get(id = 1)
            tra = status
            quali = ''
            staff_list =[]
            gdept = tbldepartment.objects.all().order_by('name')
            for jj in gdept:
               if qualification == 'Nil' and sex == 'Nil':
                  getdetails = staffrec.objects.filter(status = status,department = jj.name).order_by('staffid')
                  quali =''
               elif qualification == 'Nil':
                   getdetails = staffrec.objects.filter(status = status,department = jj.name,sex = sex).order_by('staffid')
                   quali =  "WITH " +sex
               elif sex == 'Nil':
                   getdetails = staffrec.objects.filter(status = status,department = jj.name,qualification = qualification).order_by('staffid')
                   quali =  "WITH " +qualification
               else:
                   getdetails = staffrec.objects.filter(status = status,qualification = qualification,department = jj.name,sex = sex).order_by('staffid')
                   quali = "WITH " +qualification
               sdic = {'dept':jj.name,'staff':getdetails}
               staff_list.append(sdic)
            if form.cleaned_data['excelfile']:
                response = HttpResponse(mimetype="application/ms-excel")
                response['Content-Disposition'] = 'attachment; filename=staffinfo.xls'
                wb = xlwt.Workbook()
                ws = wb.add_sheet('staffinfo')
                ws.write(0, 1, comp.name)
                ws.write(1, 1, comp.address)
                ws.write(2, 2, '%s STAFF %s' % (tra,quali) )
                ws.write(2, 3, gettime() )
                v = 3
                for p in staff_list:
                    ws.write(v, 0, p['dept'])
                    v = v + 1

                    ws.write(v, 0, 'Staff Id')
                    ws.write(v, 1, 'Staff Name')
                    ws.write(v, 2, 'Staff Address')
                    ws.write(v, 3, 'sex')
                    ws.write(v, 4, 'Phone No')
                    ws.write(v, 5, 'Date Of Birth')
                    ws.write(v, 6, 'Date Of Appointment')
                    ws.write(v, 7, 'Designation')
                    ws.write(v, 8, 'Level/Step')
                    ws.write(v, 9, 'State')
                    ws.write(v, 10, 'Local Govt Area')
                    k = v + 1
                    for jd in p['staff']:
                        ws.write(k, 0, jd.staffid)
                        ws.write(k, 1, jd.name)
                        ws.write(k, 2, jd.address)
                        ws.write(k, 3, jd.sex)
                        ws.write(k, 4, jd.phoneno)
                        ws.write(k, 5, jd.dateofbirth.strftime('%d %b,%Y'))
                        ws.write(k, 6, jd.dateofresum.strftime('%d %b,%Y'))
                        ws.write(k, 7, jd.designation)
                        ws.write(k, 8, str(jd.level) +',' + str(jd.step))
                        ws.write(k, 9, jd.stateoforigin)
                        ws.write(k, 10, jd.localgovt)
                        k = k+ 1
                    v = k


                wb.save(response)
                return response
            else:
                return render_to_response('hrm/staffrep.htm',{'varuser':varuser,'varerr':varerr,'form':form,'staff_list':staff_list,'comp':comp,'tra':tra,'gdept':gdept,'quali':quali,'printdate':gettime()},context_instance = RequestContext(request))
          else:
               varerr = "All Fields Are Required"
               getdetails = ""
          return render_to_response('hrm/staffrep.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = staffrepform()
            getdetails = ""#tblsetup.objects.all().order_by('name')
        return render_to_response('hrm/staffrep.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def hrmstaffindreport(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.standardledger
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/hrm/unauto/')
        varerr =""
        if request.method == 'POST':
          form = staffindrepform(request.POST) # A form bound to the POST data
          if form.is_valid():
            staffid = form.cleaned_data['staffid']
            comp = tblcompanyinfo.objects.get(id = 1)
            try:
               #getdetails = staffrec.objects.get(staffid = status)
               #locared = relocate.objects.filter(staffid = status)
               #prommo = tblpromotion.objects.filter(staffid = status)
               #educ = tblstaffedu.objects.filter(staffid = status)
               #proff = tblstaffproff.objects.filter(staffid = status)
               #train = tbltraining.objects.filter(staffid = status)
               #query = tblstaffquery.objects.filter(staffid = status)

                 
              # pfa = tblstaffpfa.objects.get(staffid = status)
               #hmo = tblstaffhmo.objects.get(staffid = status)

               getdetails = staffrec.objects.get(staffid = staffid)
               locared = relocate.objects.filter(staffid = staffid)
               prommo = tblpromotion.objects.filter(staffid = staffid)
               educ = tblstaffedu.objects.filter(staffid = staffid)
               proff = tblstaffproff.objects.filter(staffid = staffid)
               train = tbltraining.objects.filter(staffid = staffid)
               query = tblstaffquery.objects.filter(staffid = staffid)
              # pfa = tblstaffpfa.objects.get(staffid = status)
               #hmo = tblstaffhmo.objects.get(staffid = status)

               return render_to_response('hrm/staffind2rep.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'comp':comp,'locared':locared,'prommo':prommo,'educ':educ,'proff':proff,'train':train,'query':query},context_instance = RequestContext(request))
            except:
               varerr = "Record Not Found"
               getdetails = ""
               return render_to_response('hrm/staffindrep.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
          else:
               varerr = "All Fields Are Required"
               getdetails = ""
          return render_to_response('hrm/staffindrep.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = staffindrepform()
            getdetails = ""#tblsetup.objects.all().order_by('name')
        return render_to_response('hrm/staffindrep.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def hrmstaffindreportall(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.standardledger
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/hrm/unauto/')
        varerr =""
        j ={}
        jj ={}
        l =[]
        comp = tblcompanyinfo.objects.get(id = 1)
        getdetails = staffrec.objects.all().order_by('staffid')
        if staffrec.objects.all().count() == 0:
            pass
        else:
            da = staffrec.objects.all().order_by('oracleno')
            for p in da:
                sed = tblstaffedu.objects.filter(staffid =  p.staffid).order_by('id')# Staff Education
                proedu = tblstaffproff.objects.filter(staffid =  p.staffid)#Staff Professional
                prommo = tblpromotion.objects.filter(staffid =  p.staffid) # Staff Promotion
                loca = relocate.objects.filter(staffid = p.staffid) # Staff Reocation  'oracleno':p.oracleno
                ss ={'bio':p,'edu':sed,'pedu':proedu,'spromo':prommo,'srel':loca}
                l.append(ss)

        return render_to_response('hrm/staffind22rep.htm',{'varuser':varuser,'varerr':varerr,'l':l,'getdetails':getdetails,'comp':comp,'printdate':gettime()},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def opsuccessfull(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.receipt
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/hrm/unauto/')
        varerr =""
        #form = editstaform()
        return render_to_response('hrm/opsuccessful.htm',{'varuser':varuser,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def lengthofservice(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.standardledger
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/hrm/unauto/')
        varerr =""
        comp = tblcompanyinfo.objects.get(id = 1)
        if request.method == 'POST':
            form = lengthofserviceform(request.POST) # A form bound to the POST data
            if form.is_valid():
                yearvalue = form.cleaned_data['yearvalue']
                caldate1 = form.cleaned_data['caldate']
                caldate2 = caldate1.split('/')
                caldate = datetime.date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                getstaff = staffrec.objects.filter(status = "ACTIVE").order_by('staffid')
                staff_list = []
                getdate = ''
                getyage = ''
                for j in getstaff:
                    staffdic = {}
                    vdate = j.dateofresum
                    vbirth = j.dateofbirth
                    rsumdate = datetime.date(vdate.year,vdate.month,vdate.day)
                    if form.cleaned_data['age']:
                        vardelta = caldate - vbirth
                        vrdate = vbirth
                        getdate ='Date Of Birth'
                        getyage = 'Age'
                    else:
                        vardelta = caldate - rsumdate
                        vrdate = rsumdate
                        getdate = 'Date Of Resumption'
                        getyage = 'Year In Service'
                    difference_in_years = (vardelta.days + vardelta.seconds/86400.0)/365.2425
                    kk = difference_in_years
                    rvalue = int(kk)
                    if rvalue >= yearvalue:
                        staffdic = {'staffid':j.staffid,'staffname':j.name,'designation':j.designation,'department':j.department,'dateofresumption':vrdate,'year':rvalue}
                        staff_list.append(staffdic)
                    else:
                        pass
                return render_to_response('hrm/lengthofservice.htm',{'varuser':varuser,'varerr':varerr,'form':form,'staff_list':staff_list,'comp':comp,'getdate':getdate,'getyage':getyage,'printdate':gettime()},context_instance = RequestContext(request))
            else:
                varerr = "All Fields Are Required"
                getdetails = ""
            return render_to_response('hrm/lengthofservice.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
        else:
            form = lengthofserviceform()
            getdetails = ""#tblsetup.objects.all().order_by('name')
        return render_to_response('hrm/lengthofservice.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def hrmstaffhmo(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.payment
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/hrm/unauto/')
            varerr =""
            getdetails =""
            if request.method == 'POST':
                form = staffhmoform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    staffid = form.cleaned_data['staffid']
                    staffname = form.cleaned_data['staffname']
                    hmoname = form.cleaned_data['hmoname']
                    hmoprovider = form.cleaned_data['hmoprovider']
                    getadd = tblhmoprovide.objects.get(hmo = hmoname,name = hmoprovider)

                    if tblstaffhmo.objects.filter(staffid = staffid).count()== 0:
                        savecon = tblstaffhmo(staffid = staffid,staffname = staffname,hmoname = hmoname, userid = varuser,hmoprovider = hmoprovider,provideraddress = getadd.address )
                        savecon.save()
                        return HttpResponseRedirect('/hrm/hrm/staffhmo/')
                    else:
                        varerr ="Staff Already In Existence"
                        return render_to_response('hrm/staffhmo.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
            else:

                form = staffhmoform()
                getdetails = ""#tbldesig.objects.all().order_by('desgcode')
            return render_to_response('hrm/staffhmo.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')

def hrmeduajaxallhmo(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                comp = tblcompanyinfo.objects.get(id = 1)
                staff_list = []
                data = tblhmoprovide.objects.filter(hmo = acccode).order_by('name')
                for j in data:
                    gdata = tblstaffhmo.objects.filter(hmoname = acccode,hmoprovider = j.name).order_by('staffid')
                    staffdic = {'provider':j.name,'staff':gdata}
                    staff_list.append(staffdic)

                return render_to_response('hrm/textajax51.htm',{'hmo':acccode,'staff_list':staff_list,'comp':comp,'printdate':gettime()})
            else:
                #gdata = tblaccount.objects.all()
                gdata = ""
                return render_to_response('hrm/textajax51.htm',{'gdata':gdata})
        else:
            #gdata = tblaccount.objects.all()
            gdata = ""
            return render_to_response('hrm/textajax51.htm',{'gdata':gdata})

    else:
        return HttpResponseRedirect('/login/')

def hrmproviderajaxa(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                #print acccode
                kk = []
                data = tblhmoprovide.objects.filter(hmo = acccode).order_by('name')
                for p in data:
                   kk.append(p.name)
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                #gdata = tblaccount.objects.all()
                gdata = ""
                return render_to_response('hrm/textajax51.htm',{'gdata':gdata})
        else:
            #gdata = tblaccount.objects.all()
            gdata = ""
            return render_to_response('hrm/textajax51.htm',{'gdata':gdata})

    else:
        return HttpResponseRedirect('/login/')

def deletestaffhmo(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        seldata = tblstaffhmo.objects.get(id = invid)
        seldata.delete()
        return HttpResponseRedirect('/hrm/hrm/staffhmo/')

    else:
        return HttpResponseRedirect('/login/')
#************************************************************
def hrmstaffpfa(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.payment
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/hrm/unauto/')
            varerr =""
            getdetails =""
            if request.method == 'POST':
                form = staffpfaform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    staffid = form.cleaned_data['staffid']
                    staffname = form.cleaned_data['staffname']
                    hmoname = form.cleaned_data['hmoname']
                    accno = form.cleaned_data['accno']
                    if tblstaffpfa.objects.filter(staffid = staffid).count()== 0:
                        savecon = tblstaffpfa(staffid = staffid,staffname = staffname,hmoname = hmoname, userid = varuser,accno = accno )
                        savecon.save()
                        return HttpResponseRedirect('/hrm/hrm/staffpfa/')
                    else:
                        varerr ="Staff Already In Existence"
                        return render_to_response('hrm/staffpfa.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
            else:

                form = staffpfaform()
                getdetails = ""#tbldesig.objects.all().order_by('desgcode')
            return render_to_response('hrm/staffpfa.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')

def editstaffpfa(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.payment
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/hrm/unauto/')
        varerr =""
        if request.method == 'POST':
            getdetails = ""
            staffid = request.POST['staffid']
            staffname = request.POST['staffname']
            hmoname = request.POST['hmoname']
            bodyname = request.POST['bodyname']

            if  bodyname == "" or bodyname == "" or staffid == "" or staffname == "":
                varerr = "ALL FIELDS ARE REQUIRED"
                #getdetails = tblstaffproff.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                #return render_to_response('hrm/editstaffproff.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                return HttpResponseRedirect('/hrm/hrm/staffpfa/')
            seldata = tblstaffpfa.objects.get(id = invid)
            seldata.hmoname = hmoname
            seldata.accno = bodyname
            seldata.userid = varuser
            seldata.save()
            return HttpResponseRedirect('/hrm/hrm/staffpfa/')

    else:
        return HttpResponseRedirect('/login/')


def hrmeduajaxallpfa(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
               # print acccode
                comp = tblcompanyinfo.objects.get(id = 1)
                staff_list = tblstaffpfa.objects.filter(hmoname = acccode).order_by('staffid')
                return render_to_response('hrm/textajax52.htm',{'hmo':acccode,'staff_list':staff_list,'comp':comp,'printdate':gettime()})
            else:
                #gdata = tblaccount.objects.all()
                gdata = ""
                return render_to_response('hrm/textajax52.htm',{'gdata':gdata})
        else:
            #gdata = tblaccount.objects.all()
            gdata = ""
            return render_to_response('hrm/textajax52.htm',{'gdata':gdata})

    else:
        return HttpResponseRedirect('/login/')

def deletestaffpfa(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        seldata = tblstaffpfa.objects.get(id = invid)
        seldata.delete()
        return HttpResponseRedirect('/hrm/hrm/staffpfa/')

    else:
        return HttpResponseRedirect('/login/')


# Wrapper to make a view handle both normal and api request
def json_view(func):
    def wrap(req, *args, **kwargs):
        resp = func(req, *args, **kwargs)
        if isinstance(resp, HttpResponse):
            return resp
        return HttpResponse(json.dumps(resp), mimetype="application/json")

    return wrap

@json_view
def autocomplete(request):
    term = request.GET.get('term')
    #print term

    qset = staffrec.objects.filter(staffid__contains=term)[:10]

    suggestions = []
    for i in qset:
        suggestions.append({'label': '%s %s ' % (i.staffid, i.name), 'staffid': i.staffid,'name':i.name})
    return suggestions

@json_view
def autocompletename(request):
    term = request.GET.get('term')
    #print term
    qset = staffrec.objects.filter(name__contains=term)[:10]
    suggestions = []
    for i in qset:
        suggestions.append({'label': '%s %s ' % ( i.name, i.staffid), 'name':i.name, 'staffid': i.staffid})
    return suggestions

@json_view
def getstaff(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                desg =  tbldesig.objects.all().order_by('desc')
                state = tblstate.objects.all().order_by('state')
                localgt = tbllocalgovt.objects.all().order_by('localgovt')
                gdept = tbldepartment.objects.all().order_by('name')
                glocal = tbllg.objects.all().order_by('lgname')
                level = tbllevel.objects.all().order_by('level')
                step = tblstep.objects.all().order_by('level')
                getdetails = staffrec.objects.get(id = acccode)
                return render_to_response('hrm/editstaffdata.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'desg':desg,'gdept':gdept,'glocal':glocal,'state':state,'localgt':localgt,'level':level,'step':step})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def getstaffeducation(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tblstaffedu.objects.get(id = acccode)
                return render_to_response('hrm/editstaffedu.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def getstaffprofessional(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tblstaffproff.objects.get(id = acccode)#.order_by('acccode')#tblaccount_acccode
                return render_to_response('hrm/editstaffproff.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getstaffno(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                staffno = 0
                dd = []
                if staffrec.objects.filter().count() == 0 :  #  or if staffrec.objects.count() == 0
                    staffno = 0
                else:
                   sdata = staffrec.objects.all()
                   for j in sdata:
                       sno = j.staffid
                       if sno.startswith('L'):
                          curr = sno[2:]
                          currb= int(curr)
                          dd.append(currb)
                   dd.sort(reverse= True)
                   staffno = dd[0]
                stnno = int(staffno)
                stnno1 = stnno + 1
                tday = datetime.date.today()
                ty = tday.year
                typ = str(ty)
                tyy = typ[2:]
                kk = 'LC%.4d'%stnno1#+'/'+tyy
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def hrmstaffreportbydepartment(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.standardledger
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/hrm/unauto/')
        varerr =""
        if request.method == 'POST':
            form = staffrepformbydep(request.POST) # A form bound to the POST data
            if form.is_valid():
                status = form.cleaned_data['status']
                department = form.cleaned_data['department']
                #sex = form.cleaned_data['sex']
                comp = tblcompanyinfo.objects.get(id = 1)
                tra = status
                quali = ''
                staff_list =[]
                gdept = tbldepartment.objects.filter(name = department).order_by('name')
                for jj in gdept:
                    if department == 'Nil':
                        getdetails = staffrec.objects.filter(status = status,department = jj.name).order_by('staffid')
                        quali =''
                    else:
                        getdetails = staffrec.objects.filter(status = status,department = jj.name).order_by('staffid')
                        quali = "WITH "  +department
                    sdic = {'dept':jj.name,'staff':getdetails}
                    staff_list.append(sdic)
                if form.cleaned_data['excelfile']:
                    response = HttpResponse(mimetype="application/ms-excel")
                    response['Content-Disposition'] = 'attachment; filename=staffinfo.xls'
                    wb = xlwt.Workbook()
                    ws = wb.add_sheet('staffinfo')
                    ws.write(0, 1, comp.name)
                    ws.write(1, 1, comp.address)
                    ws.write(2, 2, '%s STAFF %s' % (tra,quali) )
                    ws.write(2, 3, gettime() )
                    v = 3
                    for p in staff_list:
                        ws.write(v, 0, p['dept'])
                        v = v + 1

                        ws.write(v, 0, 'Staff Id')
                        ws.write(v, 1, 'Staff Name')
                        ws.write(v, 2, 'Staff Address')
                        ws.write(v, 3, 'sex')
                        ws.write(v, 4, 'Phone No')
                        ws.write(v, 5, 'Date Of Birth')
                        ws.write(v, 6, 'Date Of Appointment')
                        ws.write(v, 7, 'Designation')
                        ws.write(v, 8, 'Level/Step')
                        ws.write(v, 9, 'State')
                        ws.write(v, 10, 'Local Govt Area')
                        k = v + 1
                        for jd in p['staff']:
                            ws.write(k, 0, jd.staffid)
                            ws.write(k, 1, jd.name)
                            ws.write(k, 2, jd.address)
                            ws.write(k, 3, jd.sex)
                            ws.write(k, 4, jd.phoneno)
                            ws.write(k, 5, jd.dateofbirth.strftime('%d %b,%Y'))
                            ws.write(k, 6, jd.dateofresum.strftime('%d %b,%Y'))
                            ws.write(k, 7, jd.designation)
                            ws.write(k, 8, str(jd.level) +',' + str(jd.step))
                            ws.write(k, 9, jd.stateoforigin)
                            ws.write(k, 10, jd.localgovt)
                            k = k+ 1
                        v = k
                    wb.save(response)
                    return response
                else:
                    return render_to_response('hrm/staffrepdept.htm',{'varuser':varuser,'varerr':varerr,'form':form,'staff_list':staff_list,'comp':comp,'tra':tra,'gdept':gdept,'quali':quali,'printdate':gettime()},context_instance = RequestContext(request))
            else:
                varerr = "All Fields Are Required"
                getdetails = ""
            return render_to_response('hrm/staffrepdept.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = staffrepformbydep()
            getdetails = ""#tblsetup.objects.all().order_by('name')
        return render_to_response('hrm/staffrepdept.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


def hrmstaffreportbydesg(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.standardledger
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/hrm/unauto/')
        varerr =""
        if request.method == 'POST':
            form = staffrepformbydesg(request.POST) # A form bound to the POST data
            if form.is_valid():
                status = form.cleaned_data['status']
                designation = form.cleaned_data['designation']
                #sex = form.cleaned_data['sex']
                comp = tblcompanyinfo.objects.get(id = 1)
                tra = status
                quali = ''
                staff_list =[]
                gdept = tbldepartment.objects.all().order_by('name')
                for jj in gdept:
                    if designation == 'Nil':
                        getdetails = staffrec.objects.filter(status = status,department = jj.name).order_by('staffid')
                        quali =''
                    else:
                        getdetails = staffrec.objects.filter(status = status,department = jj.name,designation = designation).order_by('staffid')
                        quali = "WITH "  +designation
                    sdic = {'dept':jj.name,'staff':getdetails}
                    staff_list.append(sdic)
                if form.cleaned_data['excelfile']:
                    response = HttpResponse(mimetype="application/ms-excel")
                    response['Content-Disposition'] = 'attachment; filename=staffinfo.xls'
                    wb = xlwt.Workbook()
                    ws = wb.add_sheet('staffinfo')
                    ws.write(0, 1, comp.name)
                    ws.write(1, 1, comp.address)
                    ws.write(2, 2, '%s STAFF %s' % (tra,quali) )
                    ws.write(2, 3, gettime() )
                    v = 3
                    for p in staff_list:
                        ws.write(v, 0, p['dept'])
                        v = v + 1

                        ws.write(v, 0, 'Staff Id')
                        ws.write(v, 1, 'Staff Name')
                        ws.write(v, 2, 'Staff Address')
                        ws.write(v, 3, 'sex')
                        ws.write(v, 4, 'Phone No')
                        ws.write(v, 5, 'Date Of Birth')
                        ws.write(v, 6, 'Date Of Appointment')
                        ws.write(v, 7, 'Designation')
                        ws.write(v, 8, 'Level/Step')
                        ws.write(v, 9, 'State')
                        ws.write(v, 10, 'Local Govt Area')
                        k = v + 1
                        for jd in p['staff']:
                            ws.write(k, 0, jd.staffid)
                            ws.write(k, 1, jd.name)
                            ws.write(k, 2, jd.address)
                            ws.write(k, 3, jd.sex)
                            ws.write(k, 4, jd.phoneno)
                            ws.write(k, 5, jd.dateofbirth.strftime('%d %b,%Y'))
                            ws.write(k, 6, jd.dateofresum.strftime('%d %b,%Y'))
                            ws.write(k, 7, jd.designation)
                            ws.write(k, 8, str(jd.level) +',' + str(jd.step))
                            ws.write(k, 9, jd.stateoforigin)
                            ws.write(k, 10, jd.localgovt)
                            k = k+ 1
                        v = k
                    wb.save(response)
                    return response
                else:
                    return render_to_response('hrm/staffrepdesg.htm',{'varuser':varuser,'varerr':varerr,'form':form,'staff_list':staff_list,'comp':comp,'tra':tra,'gdept':gdept,'quali':quali,'printdate':gettime()},context_instance = RequestContext(request))
            else:
                varerr = "All Fields Are Required"
                getdetails = ""
            return render_to_response('hrm/staffrepdesg.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = staffrepformbydesg()
            getdetails = ""#tblsetup.objects.all().order_by('name')
        return render_to_response('hrm/staffrepdesg.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def getstaffpfa(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getpfa = tblpfa.objects.all()
                getdetails = tblstaffpfa.objects.get(id = acccode)
                return render_to_response('hrm/editpfa.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'getpfa':getpfa})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

