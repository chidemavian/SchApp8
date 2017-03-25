from django.template import loader, Context,RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import  HttpResponseRedirect
from django.contrib.sessions.models import Session
from myproject.hrm.rcwadmin.models import *
from myproject.hrm.rcsetup.form import *
from myproject.hrm.rcsetup.models import *
from myproject.hrm.hrm.models import *
from myproject.hrm.payroll.models import *
from myproject.hrm.payroll.capy import *
import datetime
from datetime import date
import xlrd
import xlwt
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
import os
import sys
from django.utils import simplejson as json

def setuplgcode(request):#branch
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = lgform(request.POST) # A form bound to the POST data
          if form.is_valid():
             name = form.cleaned_data['name']
             address = form.cleaned_data['address']
             sgnamety = str(name)
             sgnamety = sgnamety.replace(' ', '-')
             sgnamety =  sgnamety.upper()
             #pull into the sub table
             try:
                 varvali = tbllg.objects.get(lgname__iexact = sgnamety)
                 varerr = "Name In Existence"
                 return render_to_response('rsetup/entersetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             except:
                 used = tbllg(lgname = sgnamety,lgaddress = address,datecreated = datetime.datetime.today(),userid =varuser )
                 used.save()
                 #*****************************
                 getdetails = tbllg.objects.all().order_by('lgname')
                 #now i do insertion
                 return render_to_response('rsetup/entersetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = lgform()
            getdetails = tbllg.objects.all().order_by('lgname')
        return render_to_response('rsetup/entersetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')


def editlgcode(request,acccode):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/unauto/')
        varerr =""
        if request.method == 'POST':
            getdetails = ""
            brname = request.POST['hcode']

            name = request.POST['accname']
            address = request.POST['subname']
            acname = name.replace(' ', '-')
            acname = acname.upper()
            if name == "" or address == "":
                 varerr ="Invalid Name"
                 return HttpResponseRedirect('/hrm/setuplg/')

            #seldata1 = tbltransaction.objects.filter(acccode = accno).update(accname = acname)
            seldata2 = tbllg.objects.get(id = acccode)
            seldata2.lgname = acname
            seldata2.lgaddress = address
            seldata2.save()
            staffrec.objects.filter(branch = brname).update(branch = acname)

            return HttpResponseRedirect('/hrm/setuplg/')
        else:
            try:
              getdetails = tbllg.objects.get(id = acccode)
              return render_to_response('rsetup/editsubacc.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                varerr = "LG Does Not Exist"
                getdetails = tbllg.objects.get(id = acccode)
                return render_to_response('rsetup/editsubacc.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})

    else:
       return HttpResponseRedirect('/login/')

def deletelgcode(request,invid):
    varerr =""
    if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            getdetails = tbllg.objects.get(id = invid)
            k = getdetails.lgname
            if staffrec.objects.filter(branch = k ).count() == 0 :
               seldata = tbllg.objects.get(id = invid)
               seldata.delete()
               return HttpResponseRedirect('/hrm/setuplg/')
            else:
                return HttpResponseRedirect('/hrm/setuplg/')
    else:
      return HttpResponseRedirect('/login/')



def rentersetupcode(request):#unauto
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.esetup
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/welcome/')
        varerr =""
        return render_to_response('rsetup/renter.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')

def unauto(request):
     if  "userid" in request.session:
        varuser = request.session['userid']

        varerr =""
        return render_to_response('rsetup/unautorise.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')


def setupdepcode(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if uenter == "Fasle" :
            return HttpResponseRedirect('/hrm/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = deptform(request.POST) # A form bound to the POST data
          if form.is_valid():
             name1 = form.cleaned_data['name']
             #address = form.cleaned_data['address']
             name = name1.replace(' ', '-')
             #acname = acname.upper()
             sgnamety =  name.upper()
             #pull into the sub table
             try:
                 varvali = tbldepartment.objects.get(name__iexact = sgnamety)
                 varerr = "Department In Existence"
                 return render_to_response('rsetup/createacc.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             except:
                 used = tbldepartment(name = sgnamety,userid =varuser )
                 used.save()
                 #*****************************
                 getdetails = tbldepartment.objects.all().order_by('name')
                 #now i do insertion
                 return render_to_response('rsetup/createacc.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = deptform()
            getdetails = tbldepartment.objects.all().order_by('name')
        return render_to_response('rsetup/createacc.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def editdepcode(request,acccode):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/unauto/')
        varerr =""
        if request.method == 'POST':
            getdetails = ""
            name = request.POST['accname']
            depname = request.POST['hcode']
            acname = name.replace(' ', '-')
            acname = acname.upper()
            if name == "":
                 varerr ="Invalid Name"
                 return HttpResponseRedirect('/hrm/setupdep/')
            if tbldepartment.objects.filter(name__iexact = acname.upper()).exclude(id = acccode).count() == 0:
                seldata2 = tbldepartment.objects.get(id = acccode)
                seldata2.name = acname
                seldata2.save()
                staffrec.objects.filter(department = depname).update(department = acname)
                return HttpResponseRedirect('/hrm/setupdep/')
            else:

                return HttpResponseRedirect('/hrm/setupdep/')

        else:
            try:
              getdetails = tbldepartment.objects.get(id = acccode)
              return render_to_response('rsetup/editacc.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                varerr = "Department Does Not Exist"
                getdetails = tbldepartment.objects.get(id = acccode)
                return render_to_response('rsetup/editacc.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
    else:
       return HttpResponseRedirect('/login/')

def deletedepcode(request,invid):
    varerr =""
    if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            getdetails = tbldepartment.objects.get(id = invid)
            k = getdetails.name
            if staffrec.objects.filter(department = k ).count() == 0 :
               seldata = tbldepartment.objects.get(id = invid)
               seldata.delete()
               return HttpResponseRedirect('/hrm/setupdep/')
            else:
                return HttpResponseRedirect('/hrm/setupdep/')

    else:
      return HttpResponseRedirect('/login/')

def setupdesgcode(request):
     varerr =""
     if  "userid" in request.session:
       if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = desigform(request.POST) # A form bound to the POST data
          if form.is_valid():
             #descode = form.cleaned_data['descode']
             desname = form.cleaned_data['desname'] #customer code
             #descodestr = str(descode)
             #descode = descode.replace(' ', '-')
             #descode = descode.upper()
             #desnamestr = str(desname)
             desname = desname.replace(' ', '-')
             desname = desname.upper()
             if tbldesig.objects.filter(desc = desname).count() == 0:
                 pass
             else:
                varerr = "DESIGNATION NAME IN EXISTENCE"
                return render_to_response('rsetup/setup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             savecon = tbldesig(desc = desname,userid = varuser)
             savecon.save()
             return HttpResponseRedirect('/hrm/setupdesg/')

             #now i do insertion
             #return render_to_response('posting/invoice.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:

            form = desigform()
            getdetails = tbldesig.objects.all().order_by('desc')
        return render_to_response('rsetup/setup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')

def editdesgn(request,invid):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.createacc
            if uenter == "False":
              return HttpResponseRedirect('/hrm/unauto/')
            varerr =""
            if request.method == 'POST':
                getdetails = ""
                #dcode = request.POST['accname'] # the amount
                accno = request.POST['hcode']#the primary key
                desc = request.POST['acccode']#the particulars

                if  desc == "" :
                    varerr = "ALL FIELDS ARE REQUIRED"
                    return HttpResponseRedirect('/hrm/setupdesg/')
                #dcode = dcode.replace(' ', '-')
                #dcode = dcode.upper()
                #desnamestr = str(desname)
                desc = desc.replace(' ', '-')
                desc = desc.upper()
                seldata = tbldesig.objects.get(id = invid)
                #seldata.desgcode = dcode.upper()
                seldata.desc = desc.upper()
                seldata.userid = varuser
                seldata.save()
                staffrec.objects.filter(designation = accno).update(designation = desc.upper())
                tblallowance.objects.filter(desc = accno).update(desc = desc.upper())
                tbldeduction.objects.filter(desc = accno).update(desc = desc.upper())
                tblpayroll.objects.filter(designation = accno).update(designation = desc.upper())
                return HttpResponseRedirect('/hrm/setupdesg/')
            else:
                try:
                  getdetails = tbldesig.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                  return render_to_response('rsetup/editdesg.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                except:
                    getdetails = ''
                    varerr = "Account Not Exist"
                    return render_to_response('rsetup/editdesg.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
        else:
         return HttpResponseRedirect('/login/')

def deletedesgn(request,invid):
    varerr =""
    if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            getdetails = tbldesig.objects.get(id = invid)
            k = getdetails.desc
            if staffrec.objects.filter(designation = k ).count() == 0 :
               seldata = tbldesig.objects.get(id = invid)
               seldata.delete()
               return HttpResponseRedirect('/hrm/setupdesg/')
            else:
                varerr ="Staff Already in This Designation"
                getdetails = tbldesig.objects.get(id = invid)
                return HttpResponseRedirect('/hrm/setupdesg/')
    else:
      return HttpResponseRedirect('/login/')


def setuppfacode(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = deptform(request.POST) # A form bound to the POST data
          if form.is_valid():
             name = form.cleaned_data['name']
             #address = form.cleaned_data['address']
             sgnamety = name.replace(' ', '-')
             sgnamety =  sgnamety.upper()
             #pull into the sub table
             try:
                 varvali = tblpfa.objects.get(accname__iexact = sgnamety)
                 varerr = "PFA In Existence"
                 return render_to_response('rsetup/creditorsetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             except:
                 used = tblpfa(accname = sgnamety,userid =varuser )
                 used.save()
                 #*****************************
                 getdetails = tblpfa.objects.all().order_by('accname')
                 #now i do insertion
                 return render_to_response('rsetup/creditorsetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = deptform()
            getdetails = tblpfa.objects.all().order_by('accname')
        return render_to_response('rsetup/creditorsetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def editpfacode(request,acccode):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/unauto/')
        varerr =""
        if request.method == 'POST':
            getdetails = ""
            name = request.POST['accname']
           # address = request.POST['subname']
            acname = name.replace(' ', '-')
            acname = acname.upper()
            if name == "":
                 varerr ="Invalid Name"
                 getdetails = tblpfa.objects.get(id = acccode)
                 return HttpResponseRedirect('/hrm/setuppfa/')
            try:
                 varvali = tblpfa.objects.get(accname__iexact = acname.upper())
                 varerr ="PFA In Existence"
                 getdetails = tblpfa.objects.get(id = acccode)
                 return HttpResponseRedirect('/hrm/setuppfa/')
            except:
                seldata2 = tblpfa.objects.get(id = acccode)
                seldata2.accname = acname
                seldata2.save()
                return HttpResponseRedirect('/hrm/setuppfa/')
        else:
            try:
              getdetails = tblpfa.objects.get(id = acccode)
              return render_to_response('rsetup/editcreditor.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                varerr = "PFA Does Not Exist"
                getdetails = tblpfa.objects.get(id = acccode)
                return render_to_response('rsetup/editcreditor.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
    else:
       return HttpResponseRedirect('/login/')

def deletepfacode(request,invid):
    varerr =""
    if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            seldata = tblpfa.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/hrm/setuppfa/')
    else:
      return HttpResponseRedirect('/login/')

def setupbankcode(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = bankkform(request.POST) # A form bound to the POST data
          if form.is_valid():
             name = form.cleaned_data['name']
             sortcode = form.cleaned_data['sortcode']
             name = name.replace(' ', '-')
             #acname = acname.upper()
             sgnamety =  name.upper()
             #pull into the sub table
             try:
                 varvali = tblbank.objects.get(name__iexact = sgnamety)
                 varerr = "BANK In Existence"
                 getdetails = tblbank.objects.all().order_by('name')
                 return render_to_response('rsetup/debtorssetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             except:
                 used = tblbank(name = sgnamety,userid =varuser,sortcode = sortcode )
                 used.save()
                 #*****************************
                 #getdetails = tblbank.objects.all().order_by('name')
                 return HttpResponseRedirect('/hrm/setupbank/')
                 #now i do insertion
                 #return render_to_response('rsetup/debtorssetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = bankkform()
            getdetails = tblbank.objects.all().order_by('name')
        return render_to_response('rsetup/debtorssetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def editbankcode(request,acccode):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/unauto/')
        varerr =""
        if request.method == 'POST':
            getdetails = ""
            name = request.POST['accname']
            sortcode = request.POST['sortcode']
            oldname = request.POST['hcode']
            acname = name.replace(' ', '-')
            acname = acname.upper()
            if name == "":
                 varerr ="Invalid Name"
                 getdetails = tblbank.objects.get(id = acccode)
                 return HttpResponseRedirect('/hrm/setupbank/')
            
            seldata2 = tblbank.objects.get(id = acccode)
            seldata2.name = acname
            seldata2.sortcode = sortcode
            seldata2.save()
            tblbankdetails.objects.filter(bankname = oldname).update(bankname = acname)
            return HttpResponseRedirect('/hrm/setupbank/')
        else:
            try:
              getdetails = tblbank.objects.get(id = acccode)
              return render_to_response('rsetup/editdebtors.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                varerr = "Bank Does Not Exist"
                getdetails = tblbank.objects.get(id = acccode)
                return render_to_response('rsetup/editdebtors.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
    else:
       return HttpResponseRedirect('/login/')

def deletebankcode(request,invid):
    varerr =""
    if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            getdetails = tblbank.objects.get(id = invid)
            k = getdetails.name
            if tblbankdetails.objects.filter(bankname = k ).count() == 0 :
                seldata = tblbank.objects.get(id = invid)
                seldata.delete()
                return HttpResponseRedirect('/hrm/setupbank/')
            else:
                varerr = "Bank already assigned to Staffs "
                getdetails = tblbank.objects.get(id = invid)
                return HttpResponseRedirect('/hrm/setupbank/')

    else:
      return HttpResponseRedirect('/login/')


def setupcategorycode(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = categoryform(request.POST) # A form bound to the POST data
          if form.is_valid():
             name = form.cleaned_data['name']
             #address = form.cleaned_data['address']
             name = name.replace(' ', '-')
             #acname = acname.upper()
             sgnamety =  name.upper()
             #pull into the sub table
             try:
                 varvali = tblcategory.objects.get(name__iexact = sgnamety)
                 varerr = "Category In Existence"
                 return render_to_response('rsetup/setupcategory.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             except:
                 used = tblcategory(name = sgnamety,userid =varuser )
                 used.save()
                 #*****************************
                 getdetails = tblcategory.objects.all().order_by('name')
                 return HttpResponseRedirect('/hrm/setupcategory/')
                 #now i do insertion
                 #return render_to_response('rsetup/setupcategory.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = categoryform()
            getdetails = tblcategory.objects.all().order_by('name')
        return render_to_response('rsetup/setupcategory.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def editcategorycode(request,acccode):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/unauto/')
        varerr =""
        if request.method == 'POST':
            getdetails = ""
            name = request.POST['accname']
           # address = request.POST['subname']
            acname = name.replace(' ', '-')
            acname = acname.upper()
            if name == "":
                 varerr ="Invalid Name"
                 getdetails = tblcategory.objects.get(id = acccode)
                 return render_to_response('rsetup/editcategory.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            try:
                 varvali = tblcategory.objects.get(name__iexact = acname.upper())
                 varerr ="Category In Existence"
                 getdetails = tblcategory.objects.get(id = acccode)
                 return render_to_response('rsetup/editcategory.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                seldata2 = tblcategory.objects.get(id = acccode)
                seldata2.name = acname
                seldata2.save()
                return HttpResponseRedirect('/hrm/setupcategory/')
        else:
            try:
              getdetails = tblcategory.objects.get(id = acccode)
              return render_to_response('rsetup/editcategory.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                varerr = "Category Does Not Exist"
                getdetails = tblcategory.objects.get(id = acccode)
                return render_to_response('rsetup/editcategory.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
    else:
       return HttpResponseRedirect('/login/')

def deletecategorycode(request,invid):
    varerr =""
    if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            seldata = tblcategory.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/hrm/setupcategory/')
    else:
      return HttpResponseRedirect('/login/')

def setupall(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.createacc
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/unauto/')
            varerr =""
            getdetails =""
            if request.method == 'POST':
                form = allform(request.POST) # A form bound to the POST data
                if form.is_valid():

                   # descode = form.cleaned_data['descode']
                    level = form.cleaned_data['level']
                    step = form.cleaned_data['step']
                    amount = form.cleaned_data['amount']
                    paydesc = form.cleaned_data['paydesc']
                    desname = str(level) +','+ str(step)

                    if tblallowance.objects.filter(paydes = paydesc,desc = desname).count() == 0:
                        pass
                    else:
                        varerr = "ALLOWANCE IN EXISTENCE"
                        return render_to_response('rsetup/setupall.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                    savecon = tblallowance(desc = desname,userid = varuser,amount = amount,paydes = paydesc )
                    savecon.save()
                    return HttpResponseRedirect('/hrm/setupall/')
            else:

                form = allform()
                getdetails = ""#tbldesig.objects.all().order_by('desgcode')
            return render_to_response('rsetup/setupall.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')

def allowanceajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            print 'welcome'
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                #print acccode
                #gdata = tblaccount.objects.all()
                gdata = ""
                gdata = tblallowance.objects.filter(desc = acccode).order_by('id')
                return render_to_response('rsetup/testajax.htm',{'gdata':gdata,'post':post})
            else:
                #gdata = tblaccount.objects.all()
                gdata = ""
                return render_to_response('rsetup/testajax.htm',{'gdata':gdata})
            #return render_to_response('rsetup/testajax.htm',{'gdata':gdata})
        else:
            #gdata = tblaccount.objects.all()
            gdata = ""
            return render_to_response('rsetup/testajax.htm',{'gdata':gdata})
        #return render_to_response('rsetup/testajax.htm',{'gdata':gdata})

    else:
        return HttpResponseRedirect('/login/')
def editall(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/unauto/')
        varerr =""
        if request.method == 'POST':
            getdetails = ""
            #dcode = request.POST['accname'] # the amount
            accno = request.POST['hcode']#the primary key
            desc1 = request.POST['acccode']#the particulars
            amt = request.POST['amt']
            desc = request.POST['desc']

            if  desc == "" or amt == "" :
                varerr = "ALL FIELDS ARE REQUIRED"
                return HttpResponseRedirect('/hrm/setupall/')
            try:
                k = float(amt)
            except:
                varerr = "INVALID AMOUNT"
                return HttpResponseRedirect('/hrm/setupall/')
            if tblallowance.objects.filter(paydes = desc,desc = desc1).exclude(id = invid).count() == 0:
                pass
            else:
                varerr = "ALLOWANCE IN EXISTENCE"
                return HttpResponseRedirect('/hrm/setupall/')
            seldata = tblallowance.objects.get(id = accno)
            seldata.amount = amt
            seldata.paydes = desc
            seldata.userid = varuser
            seldata.save()
            return HttpResponseRedirect('/hrm/setupall/')
        else:
            try:
                getdetails = tblallowance.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                return render_to_response('rsetup/editall.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                varerr = "Account Not Exist"
                return render_to_response('rsetup/editall.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')

def deleteall(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        seldata = tblallowance.objects.get(id = invid)
        seldata.delete()
        return HttpResponseRedirect('/hrm/setupall/')

    else:
        return HttpResponseRedirect('/login/')

def setuspall(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.createacc
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/unauto/')
            varerr =""
            getdetails =""
            if request.method == 'POST':
                form = spallform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    staffid = form.cleaned_data['staffid']
                    staffname = form.cleaned_data['staffname']
                    amount = form.cleaned_data['amount']
                    paydesc = form.cleaned_data['paydesc']
                    paydesc = form.cleaned_data['paydesc']
                    duration = form.cleaned_data['duration']
                    caldate1 = form.cleaned_data['effectivedate']
                    caldate2 = caldate1.split('/')
                    effdate = date(int(caldate2[2]),int(caldate2[0]),1)
                    transdate11 = effdate
                    # getting the expire date
                    l = int(duration)
                    l = l - 1
                    for h in xrange(l):
                        vyear = transdate11.year
                        vmon = transdate11.month
                        vday = transdate11.day
                        vmon2 = vmon + 1
                        if vmon2 > 12:
                            vmon2 = 1
                            vyear = vyear + 1
                        transdate11 = date(vyear,vmon2,vday)
                    ck = monthrange(transdate11.year,transdate11.month)[1]
                    lday = int(ck)
                    transdate1 = date(transdate11.year,transdate11.month,lday)
                    if tblspall.objects.filter(paydes = paydesc,staffid = staffid).count() == 0:
                       pass
                    else:
                       varerr = "NAME ALREADY IN EXISTENCE"
                       getdetails = tblspall.objects.all()
                       return render_to_response('rsetup/speall.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'form':form})
                    savecon = tblspall(staffid = staffid,staffname = staffname,amount = amount,paydes = paydesc,userid = varuser,duration = duration,effectivedate = effdate,expiredate = transdate1)
                    savecon.save()
                    return HttpResponseRedirect('/hrm/setuspall/')
               
                else:
                     return HttpResponseRedirect('/hrm/setuspall/')
                    
            else:
                form = spallform()
                getdetails = tblspall.objects.all().order_by('staffid')
                return render_to_response('rsetup/speall.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')

def editspall(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/unauto/')
        varerr =""
        if request.method == 'POST':
            getdetails = ""
            staffid = request.POST['staffid'] # the amount
            staffname = request.POST['staffname']#the primary key
            amount = request.POST['amount']#the particulars
            paydesc = request.POST['paydesc']
            duration = request.POST['duration']
            caldate1 = request.POST['effectivedate']
            caldate2 = caldate1.split('/')
            effdate = date(int(caldate2[2]),int(caldate2[0]),1)
            transdate11 = effdate
            # getting the expire date
            l = int(duration)
            l = l - 1
            for h in xrange(l):
                vyear = transdate11.year
                vmon = transdate11.month
                vday = transdate11.day
                vmon2 = vmon + 1
                if vmon2 > 12:
                   vmon2 = 1
                   vyear = vyear + 1
                transdate11 = date(vyear,vmon2,vday)
            ck = monthrange(transdate11.year,transdate11.month)[1]
            lday = int(ck)
            transdate1 = date(transdate11.year,transdate11.month,lday)

            if  duration == "" or amount == "" :
                return HttpResponseRedirect('/hrm/setuspall/')
            try:
                k = float(amount)
            except:
                return HttpResponseRedirect('/hrm/setuspall/')
            if tblspall.objects.filter(paydes = paydesc,staffid = staffid).exclude(id = invid).count() == 0:
                pass
            else:
                return HttpResponseRedirect('/hrm/setuspall/')

            seldata = tblspall.objects.get(id = invid)
            seldata.amount = amount
            seldata.paydes = paydesc
            seldata.duration = duration
            seldata.effectivedate = effdate
            seldata.expiredate = transdate1
            seldata.userid = varuser
            seldata.save()
            return HttpResponseRedirect('/hrm/setuspall/')
        else:
            try:
                getdetails = tblspall.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                return render_to_response('rsetup/editspall.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                varerr = "Account Not Exist"
                return render_to_response('rsetup/editspall.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')


def deletespall(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        seldata = tblspall.objects.get(id = invid)
        seldata.delete()
        return HttpResponseRedirect('/hrm/setuspall/')

    else:
        return HttpResponseRedirect('/login/')


def setupded(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.createacc
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/unauto/')
            varerr =""
            getdetails =""
            if request.method == 'POST':
                form = allform(request.POST) # A form bound to the POST data
                if form.is_valid():

                    #descode = form.cleaned_data['descode']
                    level = form.cleaned_data['level']
                    step = form.cleaned_data['step']
                    amount = form.cleaned_data['amount']
                    paydesc = form.cleaned_data['paydesc']
                    desname = str(level) +','+ str(step)

                    if tbldeduction.objects.filter(desc = desname,paydes = paydesc).count() == 0:
                        pass
                    else:
                        varerr = "DEDUCTION IN EXISTENCE"
                        return render_to_response('rsetup/setupded.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                    savecon = tbldeduction(desc = desname,userid = varuser,amount = amount,paydes = paydesc )
                    savecon.save()
                    return HttpResponseRedirect('/hrm/setupded/')
            else:

                form = allform()
                getdetails = ""#tbldesig.objects.all().order_by('desgcode')
            return render_to_response('rsetup/setupded.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')

def deductionajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            #print 'welcome'
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                #print acccode
                #gdata = tblaccount.objects.all()
                gdata = ""
                gdata = tbldeduction.objects.filter(desc = acccode).order_by('id')
                return render_to_response('rsetup/testajax1.htm',{'gdata':gdata,'post':post})
            else:
                #gdata = tblaccount.objects.all()
                gdata = ""
                return render_to_response('rsetup/testajax1.htm',{'gdata':gdata})
            #return render_to_response('rsetup/testajax1.htm',{'gdata':gdata})
        else:
            #gdata = tblaccount.objects.all()
            gdata = ""
            return render_to_response('rsetup/testajax1.htm',{'gdata':gdata})
        #return render_to_response('rsetup/testajax1.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')
def editded(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/unauto/')
        varerr =""
        if request.method == 'POST':
            getdetails = ""
            #dcode = request.POST['accname'] # the amount
            accno = request.POST['hcode']#the primary key
            desc1 = request.POST['acccode']#the particulars
            amt = request.POST['amt']
            desc = request.POST['desc']

            if  desc == "" or amt == "" :
                varerr = "ALL FIELDS ARE REQUIRED"
                getdetails = tbldeduction.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                return HttpResponseRedirect('/hrm/setupded/')
            try:
                k = float(amt)
            except:
                varerr = "INVALID AMOUNT"
                getdetails = tbldeduction.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                return HttpResponseRedirect('/hrm/setupded/')
            if tbldeduction.objects.filter(paydes = desc,desc = desc1).exclude(id = invid).count() == 0:
                pass
            else:
                varerr = "%s IN EXISTENCE" % desc
                getdetails = tbldeduction.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                return HttpResponseRedirect('/hrm/setupded/')
            seldata = tbldeduction.objects.get(id = accno)
            seldata.amount = amt
            seldata.paydes = desc
            seldata.userid = varuser
            seldata.save()
            return HttpResponseRedirect('/hrm/setupded/')
        else:
            try:
                getdetails = tbldeduction.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                return render_to_response('rsetup/editded.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                varerr = "Account Not Exist"
                return render_to_response('rsetup/editded.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')

def deleteded(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        seldata = tbldeduction.objects.get(id = invid)
        seldata.delete()
        return HttpResponseRedirect('/hrm/setupded/')
    else:
        return HttpResponseRedirect('/login/')

def setuspded(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.createacc
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/unauto/')
            varerr =""
            getdetails =""
            if request.method == 'POST':
                form = spedform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    staffid = form.cleaned_data['staffid']
                    staffname = form.cleaned_data['staffname']
                    amount = form.cleaned_data['amount']
                    paydesc = form.cleaned_data['paydesc']
                    duration = form.cleaned_data['duration']
                    caldate1 = form.cleaned_data['effectivedate']
                    caldate2 = caldate1.split('/')
                    effdate = date(int(caldate2[2]),int(caldate2[0]),1)
                    transdate11 = effdate
                    # getting the expire date
                    l = int(duration)
                    l = l - 1
                    for h in xrange(l):
                        vyear = transdate11.year
                        vmon = transdate11.month
                        vday = transdate11.day
                        vmon2 = vmon + 1
                        if vmon2 > 12:
                           vmon2 = 1
                           vyear = vyear + 1
                        transdate11 = date(vyear,vmon2,vday)
                        #print 'new date ',transdate11
                    ck = monthrange(transdate11.year,transdate11.month)[1]
                    lday = int(ck)
                    transdate1 = date(transdate11.year,transdate11.month,lday)
                    if tblspded.objects.filter(paydes = paydesc.upper(),staffid = staffid).count() == 0:
                        pass
                    else:
                        varerr = "NAME ALREADY IN EXISTENCE"
                        getdetails = tblspded.objects.all()
                        return render_to_response('rsetup/speded.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'form':form})
                    savecon = tblspded(staffid = staffid,staffname = staffname,amount = amount,paydes = paydesc.upper(),userid = varuser,duration = duration,effectivedate = effdate,expiredate = transdate1)
                    savecon.save()
                    return HttpResponseRedirect('/hrm/setupsded/')
            else:

                #form = spallform()
                form =spedform()
                getdetails = tblspded.objects.all().order_by('staffid')
            return render_to_response('rsetup/speded.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')

def editspdedded(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/unauto/')
        varerr =""
        if request.method == 'POST':
            getdetails = ""
            staffid = request.POST['staffid'] # the amount
            staffname = request.POST['staffname']#the primary key
            amount = request.POST['amount']#the particulars
            paydesc = request.POST['paydesc']
            duration = request.POST['duration']
            caldate1 = request.POST['effectivedate']
            caldate2 = caldate1.split('/')
            effdate = date(int(caldate2[2]),int(caldate2[0]),1)
            transdate11 = effdate
            # getting the expire date
            l = int(duration)
            l = l - 1
            for h in xrange(l):
                vyear = transdate11.year
                vmon = transdate11.month
                vday = transdate11.day
                vmon2 = vmon + 1
                if vmon2 > 12:
                    vmon2 = 1
                    vyear = vyear + 1
                transdate11 = date(vyear,vmon2,vday)
            ck = monthrange(transdate11.year,transdate11.month)[1]
            lday = int(ck)
            transdate1 = date(transdate11.year,transdate11.month,lday)

            if  duration == "" or amount == "" :
                return HttpResponseRedirect('/hrm/setupsded/')
            try:
                k = float(amount)
            except:
                varerr = "INVALID AMOUNT"
                return HttpResponseRedirect('/hrm/setupsded/')
            if tblspded.objects.filter(paydes = paydesc.upper(),staffid = staffid).exclude(id = invid).count() == 0:
                pass
            else:
                return HttpResponseRedirect('/hrm/setupsded/')
            seldata = tblspded.objects.get(id = invid)
            seldata.amount = amount
            seldata.paydes = paydesc.upper()
            seldata.duration = duration
            seldata.effectivedate = effdate
            seldata.expiredate = transdate1
            seldata.userid = varuser
            seldata.save()
            return HttpResponseRedirect('/hrm/setupsded/')
        else:
            try:
                getdetails = tblspded.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                return render_to_response('rsetup/editspded.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                varerr = "Account Not Exist"
                return render_to_response('rsetup/editspded.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')


def deletespdedded(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        seldata = tblspded.objects.get(id = invid)
        seldata.delete()
        return HttpResponseRedirect('/hrm/setupsded/')

    else:
        return HttpResponseRedirect('/login/')



def testexcel(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""

        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"

            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            try:
                for k in num:
                    j1 = k[0]
                    j2 = k[1]
                   # j3 = k[2]
                    #j4 = k[3]
                    #j5 = k[4]
                    #j6 = k[5]
                    #j7 = k[6]
                    #j8 = k[7]
                    #j7_as_date = datetime.date(*xlrd.xldate_as_tuple(j7, 0)[:3])
                    #j8_as_date = datetime.date(*xlrd.xldate_as_tuple(j8, 0)[:3])
                    #insert into changepin
                    sub = tbldesig(desc = j1,userid = j2)
                    sub.save()
                succ = "Record Uploaded !!!"
                return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            except:
                succ ="Uploading Error "
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})

    else:
        form = XlsInputForm()

    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
testexcel = staff_member_required(testexcel)

def uploadall(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""

        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"

            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            try:
                for k in num:
                    j1 = k[0] #amount
                    j2 = k[1] # amt description
                    j3 = k[2]# user
                    j4 = k[3]# designation
                    #j5 = k[4]
                    #j6 = k[5]
                    #j7 = k[6]
                    #j8 = k[7]
                    #j7_as_date = datetime.date(*xlrd.xldate_as_tuple(j7, 0)[:3])
                    #j8_as_date = datetime.date(*xlrd.xldate_as_tuple(j8, 0)[:3])
                    #insert into changepin
                    sub = tblallowance(desc = j4,amount = j1,paydes = j2,userid = j3)
                    sub.save()
                succ = "Record Uploaded !!!"
                return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            except:
                succ ="Uploading Error "
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})

    else:
        form = XlsInputForm()

    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadall = staff_member_required(uploadall)

def uploadbiodata(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""

        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"

            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str

            for k in num:
                    j1 = k[0]#picture
                    j2 = k[1]#staff id
                    j3 = k[2]#name
                    j4 = k[3]#address
                    j5 = k[4]#phone no
                    j6 = k[5]#date of birth
                    j7 = k[6]#sex
                    j8 = k[7]#marital status
                    j9 = k[8]#nationality
                    j10 = k[9]#state of origin
                    j11 = k[10]#local government
                    j12 = k[11]#e-mail
                    j13 = k[12]# next of kin
                    j14 = k[13]# next of kin Address
                    j15 = k[14]#next of kin phone
                    j16 = k[15]#department
                    j17 = k[16]# date of resumption
                    j18 = k[17]#first guarantor
                    j19 = k[18]#first guarantor address
                    j20 = k[19]#second guarantor
                    j21 = k[20]#second guarantor address
                    j22 = k[21]#designation
                    j23 = k[22]#qualification
                    j24 = k[23]#branch
                    j25 = k[24] # profession/residing State
                    j26 = k[25]#worked day
                    j27 = k[26]#status
                    j28 = k[27]#user id
                    level = k[28]
                    step = k[29]
                    j6_as_date = datetime.date(*xlrd.xldate_as_tuple(j6, 0)[:3])
                    j17_as_date = datetime.date(*xlrd.xldate_as_tuple(j17, 0)[:3])
                    #insert into changepin
                    savecon = staffrec(staffid = j2,name = j3,address = j4,phoneno = j5,dateofbirth = j6_as_date,sex = j7,nationality = j9,stateoforigin = j10,localgovt = j11,email = j12,nextofkin = j13,nextofkinaddress = j14,nextofkinphone = j15,maritalstatus = j8,designation = j22,department = j16,dateofresum = j17_as_date,picture = j1,userid = j28,status = j27,firstguarantor = j18,firstguarantoraddress = j19,secondguarantor = j20,secondguarantoraddress = j21,qualification = j23,branch = j24,profession = j25,workedday = j26,level = int(level),step = int(step))
                    savecon.save()
            succ = "Record Uploaded !!!"
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            #except:
            #    succ ="Uploading Error "
            #return render_to_response('upload/upload.htm',{'form': form,'succ':succ})

    else:
        form = XlsInputForm()

    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadbiodata = staff_member_required(uploadbiodata)


def uploadbranch(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""

        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"

            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            try:
                for k in num:
                    j1 = k[0]
                    j2 = k[1]
                    j3 = k[2]
                    j4 = k[3]

                    savecon = tbllg(lgname = j1,lgaddress = j2,datecreated = j3,userid = j4)
                    savecon.save()
                succ = "Record Uploaded !!!"
                return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            except:
                succ ="Uploading Error "
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})

    else:
        form = XlsInputForm()

    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadbranch = staff_member_required(uploadbranch)

def uploadspded(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""

        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"

            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            try:
                for k in num:
                    j1 = k[0]
                    j2 = k[1]
                    j3 = k[2]
                    j4 = k[3]
                    j5 = k[4]
                    savecon = tblspded(staffid = j1,staffname = j2,amount = j3,paydes = j4, userid = j5)
                    savecon.save()
                succ = "Record Uploaded !!!"
                return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            except:
                succ ="Uploading Error "
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})

    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadspded = staff_member_required(uploadspded)

def uploaddep(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""

        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"

            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            try:
                for k in num:
                    j1 = k[0]
                    j2 = k[1]
                    savecon = tbldepartment(name = j1,userid = j2)
                    savecon.save()
                succ = "Record Uploaded !!!"
                return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            except:
                succ ="Uploading Error "
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})

    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploaddep = staff_member_required(uploaddep)

def uploadstaffedu(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""

        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"

            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            try:
                for k in num:
                    j1 = k[0]
                    j2 = k[1]
                    j3 = k[2]
                    j4 = k[3]
                    j5 = k[4]
                    j6 = k[5]
                    j7 = k[6]
                    j8 = k[7]
                    j9 = k[8]
                    savecon = tblstaffedu(staffid = j1,staffname = j2,nameofsch = j3,courseofstu = j4 , certificateob = j5 , gradeobtained = j6, entryyear = j7 , exityear = j8,userid = j9)
                    savecon.save()
                succ = "Record Uploaded !!!"
                return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            except:
                succ ="Uploading Error "
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})

    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadstaffedu = staff_member_required(uploadstaffedu)

def uploadstaffacc(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""

        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"

            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            try:
                for k in num:
                    j1 = k[0]
                    j2 = k[1]
                    j3 = k[2]
                    j4 = k[3]
                    j5 = k[4]
                    savecon = tblbankdetails (staffid = j1,staffname = j2,bankname = j3,accountno = j4 ,userid = j5)
                    savecon.save()
                succ = "Record Uploaded !!!"
                return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            except:
                succ ="Uploading Error "
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})

    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadstaffacc = staff_member_required(uploadstaffacc)


def controldate(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""

        form = controlform(request.POST)
        if form.is_valid():
            recdate = request.POST['recdate']
            savecon = tblcontrol (datecreated = recdate,userid = 'wale')
            savecon.save()
            succ = "Record Saved !!!"
            return render_to_response('upload/controldate.htm',{'form': form,'succ':succ})

    else:
        form = controlform()
    return render_to_response('upload/controldate.htm', {'form': form,'succ':succ})
controldate = staff_member_required(controldate)

def setupstate(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.createacc
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/unauto/')
            varerr =""
            getdetails =""
            form2 = localgovtform()
            if request.method == 'POST':
                form = stateform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    nation = form.cleaned_data['nationality']
                    state = form.cleaned_data['state']
                    if tblstate.objects.filter(country = nation,state = state).count() == 0:
                        pass
                    else:
                        varerr = "STATE ALREADY IN EXISTENCE"
                        getdetails = tblstate.objects.all().order_by('country','state')
                        return render_to_response('rsetup/enterstate.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails})
                    savecon = tblstate(country = nation,state = state,userid = varuser)
                    savecon.save()
                    return HttpResponseRedirect('/hrm/statecapital/')
            else:
                form = stateform()
                form2 = localgovtform
                getdetails = tblstate.objects.all().order_by('country','state')
            return render_to_response('rsetup/enterstate.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails})

    else:
        return HttpResponseRedirect('/login/')

def entersetupstate(request):#unauto
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/unauto/')
        varerr =""
        form = stateform()
        form2 = localgovtform()
        getdetails = tblstate.objects.all().order_by('country','state')
        return render_to_response('rsetup/enterstate.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')


def getstate(request):
    if  "userid" in request.session:
        if request.is_ajax():

            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                #print acccode
                #gdata = tblaccount.objects.all()
                #gdata = ""
                kk = []
                data = tblstate.objects.filter(country = acccode).order_by('state')
                for p in data:
                   #print p.state
                    kk.append(p.state)

                return HttpResponse(json.dumps(kk), mimetype='application/json')
                #return render_to_response('getlg.htm',{'data':data})
            else:
                #gdata = tblaccount.objects.all()
                gdata = ""
                return render_to_response('rsetup/getlg.htm',{'gdata':gdata})

        else:

            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})

    else:
        return HttpResponseRedirect('/login/')

def setuplocalgovt(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.createacc
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/unauto/')
            varerr =""
            getdetails =""
            form = stateform()
            form2 = localgovtform()
            if request.method == 'POST':
                form2 = localgovtform(request.POST) # A form bound to the POST data
                if form2.is_valid():
                    nation = form2.cleaned_data['nationalitylg']
                    state = form2.cleaned_data['statelg']
                    localgt = form2.cleaned_data['localgovt']
                    if tbllocalgovt.objects.filter(country = nation,state = state,localgovt = localgt).count() == 0:
                        pass
                    else:
                        varerr = "LOCAL GOVERNMENT IN EXISTENCE"
                        getdetails = tblstate.objects.all().order_by('country','state')
                        return render_to_response('rsetup/enterstate.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails})
                    savecon = tbllocalgovt(country = nation,state = state,localgovt = localgt,userid = varuser)
                    savecon.save()
                    return HttpResponseRedirect('/hrm/statecapital/')
                else:
                    for i in form2: print(i.errors)
            else:
                form = stateform()
                form2 = localgovtform()
                getdetails = tblstate.objects.all().order_by('country','state')
            return render_to_response('rsetup/enterstate.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails})

    else:
        return HttpResponseRedirect('/login/')

def ajaxstreetlg(request):
    if  "userid" in request.session:
        if request.is_ajax():

            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                nation,state = acccode.split(',')
                data = tbllocalgovt.objects.filter(country = nation,state = state).order_by('localgovt')
                return render_to_response('rsetup/localgt.htm',{'data':data})
            else:
                gdata = ""
                return render_to_response('rsetup/localgt.htm',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/localgt.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def deletestate(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        getdetails = tblstate.objects.get(id = invid)
        k = getdetails.state
        if staffrec.objects.filter(stateoforigin = k ).count() == 0 :
            seldata = tblstate.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/hrm/statecapital/')
        else:
            varerr ="Some Staffs Are From %s State, So the state can not be Removed" %k
            form = stateform()
            form2 = localgovtform
            getdetails = tblstate.objects.all().order_by('country','state')
            return render_to_response('rsetup/enterstate.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')

def deletelocalgt(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        getdetails = tbllocalgovt.objects.get(id = invid)
        k = getdetails.localgovt
        if staffrec.objects.filter(localgovt = k ).count() == 0 :
            seldata = tbllocalgovt.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/hrm/statecapital/')
        else:
            varerr ="Some Staffs Are From %s Local Govt., So the LGA can not be Removed" %k
            form = stateform()
            form2 = localgovtform
            getdetails = tblstate.objects.all().order_by('country','state')
            return render_to_response('rsetup/enterstate.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')

def getlocal(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
               # print acccode
                nation,state = acccode.split(',')
                #print nation,state
                kk = []
                data = tbllocalgovt.objects.filter(country = nation,state = state).order_by('localgovt')
                for p in data:
                    kk.append(p.localgovt)
                   # print kk
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def genlocal(request):
    ll = tbllocalgovt.objects.all().order_by('localgovt')
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=localgovt.xls'
    wb = xlwt.Workbook()
    ws = wb.add_sheet('loalgovt')
    k = 0
    for jd in ll:
        ws.write(k, 0, jd.country)
        ws.write(k, 1, jd.state)
        ws.write(k, 2, jd.localgovt)
        ws.write(k, 3, jd.userid)
        k += 1
    wb.save(response)
    return response

def genstate(request):
    ll = tblstate.objects.all().order_by('state')
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=state.xls'
    wb = xlwt.Workbook()
    ws = wb.add_sheet('state')
    k = 0
    for jd in ll:
        ws.write(k, 0, jd.country)
        ws.write(k, 1, jd.state)
        ws.write(k, 3, jd.userid)
        k += 1
    wb.save(response)
    return response

def uploadstate(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""
        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            try:
                for k in num:
                    j1 = k[0]
                    j2 = k[1]
                    j3 = k[2]
                    savecon = tblstate (country = j1,state = j2,userid = j3,)
                    savecon.save()
                succ = "Record Uploaded !!!"
                return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            except:
                succ ="Uploading Error "
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})

    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadstate = staff_member_required(uploadstate)

def uploadlocal(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""
        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            try:
                for k in num:
                    j1 = k[0]
                    j2 = k[1]
                    j3 = k[2]
                    j4 = k[3]
                    savecon = tbllocalgovt (country = j1,state = j2,localgovt = j3,userid = j4,)
                    savecon.save()
                succ = "Record Uploaded !!!"
                return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            except:
                succ ="Uploading Error "
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})

    else:
        form = XlsInputForm()
    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadlocal = staff_member_required(uploadlocal)

def staffsearch(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        getdetails =""
        if request.method == 'POST':
            form = staffname (request.POST) # A form bound to the POST data
            if form.is_valid():
                name = form.cleaned_data['name']

                return HttpResponseRedirect('/hrm/statecapital/')
        else:
            form = staffname()
            return render_to_response('rsetup/search.htm',{'varuser':varuser,'varerr':varerr,'form':form})

    else:
        return HttpResponseRedirect('/login/')

def ajaxsearchstaff(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                #print acccode
                #print acccode
                #gdata = tblaccount.objects.all()
                gdata = staffrec.objects.filter(name__contains = acccode).order_by('name')[:30]
                return render_to_response('rsetup/testajax3.htm',{'gdata':gdata,'post':post})
            else:
                #gdata = tblaccount.objects.all()
                gdata = staffrec.objects.all().order_by('name')
                return render_to_response('rsetup/testajax3.htm',{'gdata':gdata})
        else:
            #gdata = tblaccount.objects.all()
            gdata = ""
            return render_to_response('rsetup/testajax3.htm',{'gdata':gdata})

    else:
        return HttpResponseRedirect('/login/')

def setuphmo(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.createacc
            if uenter == "False" :
                return HttpResponseRedirect('/unauto/')
            varerr =""
            getdetails =""
            form2 = hmoproviderform()
            if request.method == 'POST':
                form = hmoform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    name = form.cleaned_data['name']
                    address = form.cleaned_data['address']
                    if tblhmo.objects.filter(name = name,address = address).count() == 0:
                        pass
                    else:
                        varerr = "HMO ALREADY IN EXISTENCE"
                        getdetails = tblhmo.objects.all().order_by('name')
                        return render_to_response('rsetup/hmo.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails})
                    savecon = tblhmo(name = name.upper(),address = address)
                    savecon.save()
                    return HttpResponseRedirect('/hrm/hmosetup/')
            else:
                form = hmoform()
                form2 = hmoproviderform()
                getdetails = tblhmo.objects.all().order_by('name')
            return render_to_response('rsetup/hmo.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails})

    else:
        return HttpResponseRedirect('/login/')

def edithmocode(request,acccode):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/unauto/')
        varerr =""
        if request.method == 'POST':
            getdetails = ""
            brname = request.POST['hcode']
            name = request.POST['accname']
            address = request.POST['subname']
            acname = name.replace(' ', '-')
            acname = acname.upper()
            if name == "" or address == "":
                varerr ="Invalid Name"
                #getdetails = tblhmo.objects.get(id = acccode)
                return HttpResponseRedirect('/hrm/hmosetup/')
            try:
                varvali = tblhmo.objects.get(lgname__iexact = acname.upper())
                varerr ="HMO In Existence"
                #getdetails = tblhmo.objects.get(id = acccode)
                return HttpResponseRedirect('/hrm/hmosetup/')
            except:
                #seldata1 = tbltransaction.objects.filter(acccode = accno).update(accname = acname)
                seldata2 = tblhmo.objects.get(id = acccode)
                seldata2.name = acname
                seldata2.address = address
                seldata2.save()
                tblhmoprovide.objects.filter(hmo = brname).update(hmo = acname)
                tblstaffhmo.objects.filter(hmoname = brname).update(hmoname = acname)

                return HttpResponseRedirect('/hrm/hmosetup/')
        else:
            try:
                getdetails = tblhmo.objects.get(id = acccode)
                return render_to_response('rsetup/edithmo.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                varerr = "HMO Does Not Exist"
                getdetails = tblhmo.objects.get(id = acccode)
                return render_to_response('rsetup/edithmo.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})

    else:
        return HttpResponseRedirect('/login/')

def deletehmocode(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        getdetails = tblhmo.objects.get(id = invid)
        k = getdetails.name
        if tblstaffhmo.objects.filter(hmoname = k ).count() == 0 :
            seldata = tblhmo.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/hrm/hmosetup/')
        else:
            varerr ="Staff Already Using This HMO"
            #getdetails = tblhmo.objects.get(id = invid)
            return HttpResponseRedirect('/hrm/hmosetup/')
    else:
        return HttpResponseRedirect('/login/')

def setuphmoprovider(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.createacc
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/unauto/')
            varerr =""
            getdetails =""
            form = hmoform()
            if request.method == 'POST':
                form2 = hmoproviderform(request.POST) # A form bound to the POST data
                if form2.is_valid():
                    hmo = form2.cleaned_data['hmo']
                    name = form2.cleaned_data['name1']
                    address = form2.cleaned_data['address1']
                    if tblhmoprovide.objects.filter(hmo = hmo,name = name).count() == 0:
                        pass
                    else:
                        varerr = "HMO PROVIDER ALREADY IN EXISTENCE"
                        getdetails = tblhmo.objects.all().order_by('name')
                        return render_to_response('rsetup/hmo.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails})
                    savecon = tblhmoprovide(hmo = hmo,name = name,address = address)
                    savecon.save()
                    return HttpResponseRedirect('/hrm/hmosetup/')
            else:
                form = hmoform()
                form2 = hmoproviderform()
                getdetails = tblhmo.objects.all().order_by('name')
            return render_to_response('rsetup/hmo.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails})

    else:
        return HttpResponseRedirect('/login/')

def ajaxstreetlgprovider(request):
    if  "userid" in request.session:
        if request.is_ajax():

            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']

                data = tblhmoprovide.objects.filter(hmo = acccode).order_by('name')
                return render_to_response('rsetup/hmopro.htm',{'data':data})
            else:
                gdata = ""
                return render_to_response('rsetup/hmopro.htm',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/hmopro.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def edithmoprovidercode(request,acccode):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/unauto/')
        varerr =""
        if request.method == 'POST':
            getdetails = ""
            brname = request.POST['hcode']
            name = request.POST['accname']
            address = request.POST['subname']
            acname = name.replace(' ', '-')
            acname = acname.upper()
            if name == "" or address == "":
                varerr ="Invalid Name"
                getdetails = tblhmo.objects.get(id = acccode)
                return render_to_response('rsetup/edithmo.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            try:
                varvali = tblhmo.objects.get(lgname__iexact = acname.upper())
                varerr ="HMO In Existence"
                getdetails = tblhmo.objects.get(id = acccode)
                return render_to_response('rsetup/edithmo.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                #seldata1 = tbltransaction.objects.filter(acccode = accno).update(accname = acname)
                seldata2 = tblhmo.objects.get(id = acccode)
                oldname = seldata2.name
                seldata2.name = acname
                seldata2.address = address
                seldata2.save()

                tblstaffhmo.objects.filter(hmoname = brname).update(hmoname = acname)

                return HttpResponseRedirect('/hrm/hmosetup/')
        else:
            try:
                getdetails = tblhmo.objects.get(id = acccode)
                return render_to_response('rsetup/edithmo.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                varerr = "HMO Does Not Exist"
                getdetails = tblhmo.objects.get(id = acccode)
                return render_to_response('rsetup/edithmo.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})

    else:
        return HttpResponseRedirect('/login/')

def deletehmoprovidercode(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        getdetails = tblhmoprovide.objects.get(id = invid)
        k = getdetails.name
        if tblstaffhmo.objects.filter(hmoprovider = k ).count() == 0 :
            seldata = tblhmoprovide.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/hrm/hmosetup/')
        else:
            varerr ="Staff Already Using This HMO Provider"
            form = hmoform()
            form2 = hmoproviderform()
            getdetails = tblhmo.objects.all().order_by('name')
            return render_to_response('rsetup/hmo.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')

def setuplevel(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.createacc
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/unauto/')
            varerr =""
            getdetails =""
            getlevel = ''
            form = levelform()
            form2 = stepform()
            if request.method == 'POST':
                form = levelform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    level = form.cleaned_data['level']
                    if tbllevel.objects.filter(level = level).count() == 0:
                        pass
                    else:
                        varerr = "LEVEL %s IN EXISTENCE" %level
                        getlevel = tbllevel.objects.all().order_by('level')
                        #getdetails = tblstep.objects.all().order_by('level','step')
                        return render_to_response('rsetup/levelstep.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'getlevel':getlevel})
                    savecon = tbllevel(level = level,userid = varuser)
                    savecon.save()
                    return HttpResponseRedirect('/hrm/setuplevel/')
                else:
                    for i in form: print(i.errors)


            else:
                form = levelform()
                form2 = stepform()
                getlevel = tbllevel.objects.all().order_by('level')
                #getdetails = tblstep.objects.all().order_by('level','step')
            return render_to_response('rsetup/levelstep.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'getlevel':getlevel},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')

def setupstep(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.createacc
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/unauto/')
            varerr =""
            getdetails =""
            getlevel = ''
            form = levelform()
            form2 = stepform()
            if request.method == 'POST':
                form2 = stepform(request.POST) # A form bound to the POST data
                if form2.is_valid():
                    level = form2.cleaned_data['level2']
                    step = form2.cleaned_data['step']
                    if tblstep.objects.filter(level = level,step = step).count() == 0:
                        pass
                    else:
                        varerr = "STEP %s IN EXISTENCE" %step
                        getlevel = tbllevel.objects.all().order_by('level')
                        return render_to_response('rsetup/levelstep.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'getlevel':getlevel})
                    savecon = tblstep(level = level,step = step,userid = varuser)
                    savecon.save()
                    return HttpResponseRedirect('/hrm/setuplevel/')
                else:
                    for i in form: print(i.errors)


            else:
                form = levelform()
                form2 = stepform()
                getlevel = tbllevel.objects.all().order_by('level')
                getdetails = tblstep.objects.all().order_by('level','step')
            return render_to_response('rsetup/levelstep.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'getlevel':getlevel},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')

def ajaxstep(request):
    if  "userid" in request.session:
        if request.is_ajax():
            ##print 'I reach Here !!'
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']

                data = tblstep.objects.filter(level = acccode).order_by('level','step')
                return render_to_response('rsetup/step.htm',{'data':data})
            else:
                gdata = ""
                return render_to_response('rsetup/step.htm',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/step.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getnewstep(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # print acccode
                state = acccode.split(',')
                #print nation,state
                kk = []
                data = tblstep.objects.filter(level = acccode).order_by('step')
                for p in data:
                    kk.append(p.step)
                    # print kk
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
        else:

            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getdescription(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                #getdetails =  tbltemp.objects.get(id = acccode)
                return render_to_response('rsetup/desc.htm',{'varuser':varuser,'varerr':varerr})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def setupdesc(request):
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            if request.method == 'POST':
                     desc = request.POST['desc']
                     savecon = tblspecallow(name = desc.upper(),userid = varuser)
     #               savecon = tblspecallow(name = desc.upper(),userid = varuser)
                     savecon.save()
                     return HttpResponseRedirect('/hrm/setuspall/')
                
            else:
                return HttpResponseRedirect('/hrm/setuspall/')

"""    
def setupdesc(request):
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            if request.method == 'POST':
#                 if form.is_valid:
                     desc = request.POST['desc']
                     savecon = tblspall(name = desc.upper(),userid = varuser)
     #                savecon = tblspecialdedcode(name = desc.upper(),userid = varuser)
                     savecon.save()
                     return HttpResponseRedirect('/hrm/setupsded/')
                
            else:
                return HttpResponseRedirect('/hrm/setupsded/')

"""
def getspdeduction(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tblspded.objects.get(id = acccode)
                desc = tblspecialdedcode.objects.all().order_by('name')
                return render_to_response('rsetup/editspded.htm',{'getdetails':getdetails,'desc':desc})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getspallowance(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tblspall.objects.get(id = acccode)#.order_by('acccode')#tblaccount_acccode
                desc = tblspecialdedcode.objects.all().order_by('name')
                return render_to_response('rsetup/editspall.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def savings(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.createacc
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/unauto/')
            varerr =""
            getdetails =""
            if request.method == 'POST':
                form = savingsform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    staffid = form.cleaned_data['staffid']
                    staffname = form.cleaned_data['staffname']
                    amountbr = form.cleaned_data['amountbf']
                    contribution = form.cleaned_data['contribution']
                    paydesc = form.cleaned_data['paydesc']
                    if tblsavings.objects.filter(paydes = paydesc,staffid = staffid).count() == 0:
                        pass
                    else:
                        varerr = "NAME ALREADY IN EXISTENCE"
                        getdetails = tblsavings.objects.all()
                        return render_to_response('rsetup/savings.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'form':form})
                    savecon = tblsavings(staffid = staffid,staffname = staffname,amountbf = amountbr,paydes = paydesc,userid = varuser,contribution = contribution)
                    savecon.save()
                    return HttpResponseRedirect('/hrm/savings/')
            else:

                form = savingsform()
                getdetails = tblsavings.objects.all().order_by('staffid')
            return render_to_response('rsetup/savings.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')

def getsavings(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tblsavings.objects.get(id = acccode)
                return render_to_response('rsetup/editsaving.htm',{'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def editsavings(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/unauto/')
        varerr =""
        if request.method == 'POST':
            getdetails = ""
            staffid = request.POST['staffid'] # the amount
            staffname = request.POST['staffname']#the primary key
            amountbf = request.POST['amountbf']#the particulars
            paydesc = request.POST['paydesc']
            contribution = request.POST['contribution']

            if  contribution == "" or amountbf == "" :
                return HttpResponseRedirect('/hrm/savings/')
            try:
                k = float(amountbf)
            except:
                varerr = "INVALID AMOUNT"
                return HttpResponseRedirect('/hrm/savings/')
            if tblsavings.objects.filter(paydes = paydesc,staffid = staffid).exclude(id = invid).count() == 0:
                pass
            else:
                return HttpResponseRedirect('/hrm/savings/')
            seldata = tblsavings.objects.get(id = invid)
            seldata.amountbf = amountbf
            seldata.paydes = paydesc
            seldata.contribution = contribution
            seldata.userid = varuser
            seldata.save()
            return HttpResponseRedirect('/hrm/savings/')
        else:
            try:
                getdetails = tblsavings.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                return render_to_response('rsetup/editsavings.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                varerr = "Account Not Exist"
                return render_to_response('rsetup/editsavings.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')
def deletesavings(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        seldata = tblsavings.objects.get(id = invid)
        seldata.delete()
        return HttpResponseRedirect('/hrm/savings/')

    else:
        return HttpResponseRedirect('/login/')

def loan(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.createacc
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/unauto/')
            varerr =""
            getdetails =""
            if request.method == 'POST':
                form = loanform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    staffid = form.cleaned_data['staffid']
                    staffname = form.cleaned_data['staffname']
                    amount = form.cleaned_data['amount']
                    duration = form.cleaned_data['duration']
                    paydesc = form.cleaned_data['paydesc']
                    intrate = form.cleaned_data['intrate']
                    caldate1 = form.cleaned_data['effectivedate']
                    caldate2 = caldate1.split('/')
                    effdate = date(int(caldate2[2]),int(caldate2[0]),1)
                    transdate11 = effdate
                    # getting the expire date
                    l = int(duration)
                    l = l - 1
                    for h in xrange(l):
                        vyear = transdate11.year
                        vmon = transdate11.month
                        vday = transdate11.day
                        vmon2 = vmon + 1
                        if vmon2 > 12:
                            vmon2 = 1
                            vyear = vyear + 1
                        transdate11 = date(vyear,vmon2,vday)
                    ck = monthrange(transdate11.year,transdate11.month)[1]
                    lday = int(ck)
                    transdate1 = date(transdate11.year,transdate11.month,lday)
                    try:
                        kint = float(intrate)
                    except:
                        varerr = "INVALID INTEREST RATE"
                        getdetails = tblloan.objects.all()
                        return render_to_response('rsetup/loan.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'form':form})
                    try:
                        kamt = float(amount)
                    except:
                        varerr = "INVALID AMOUNT"
                        getdetails = tblloan.objects.all()
                        return render_to_response('rsetup/loan.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'form':form})
                    try:
                        kduration = int(duration)
                    except:
                        varerr = "INVALID DURATION"
                        getdetails = tblloan.objects.all()
                        return render_to_response('rsetup/loan.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'form':form})


                    getint = ((kint * kamt )/100) + kamt
                    mrepay = getint / kduration
                    if tblloan.objects.filter(paydes = paydesc,staffid = staffid).count() == 0:
                        pass
                    else:
                        varerr = "NAME ALREADY IN EXISTENCE"
                        getdetails = tblloan.objects.all()
                        return render_to_response('rsetup/loan.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'form':form})
                    savecon = tblloan(staffid = staffid,staffname = staffname,amount = kamt,paydes = paydesc,userid = varuser,duration = duration,intrate = kint,effectivedate = effdate,expiredate = transdate1,monthlyepayment = mrepay)
                    savecon.save()
                    return HttpResponseRedirect('/hrm/loan/')
            else:
                form = loanform()
                getdetails = tblloan.objects.all().order_by('paydes')
            return render_to_response('rsetup/loan.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')

def getdescriptionloan(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                #getdetails =  tbltemp.objects.get(id = acccode)
                return render_to_response('rsetup/desc1.htm',{'varuser':varuser,'varerr':varerr})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def setuploandesc(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        if request.method == 'POST':
            desc = request.POST['desc']
            savecon = tblloancode(name = desc.upper(),userid = varuser)
            savecon.save()
            return HttpResponseRedirect('/hrm/loan/')
        else:
            return HttpResponseRedirect('/hrm/loan/')

def getloan(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tblloan.objects.get(id = acccode)#.order_by('acccode')#tblaccount_acccode
                desc = tblloancode.objects.all().order_by('name')
                return render_to_response('rsetup/editloan.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'desc':desc})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def deleteloan(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        seldata = tblloan.objects.get(id = invid)
        seldata.delete()
        return HttpResponseRedirect('/hrm/loan/')

    else:
        return HttpResponseRedirect('/login/')

def getpension(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails =  tblpension.objects.get(id = 1)
                return render_to_response('rsetup/desc2.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def setuppensionrate(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        if request.method == 'POST':
            amount = request.POST['amount']
            amountemp = request.POST['amountemp']
            try:
                k = float(amount)
            except :
                return HttpResponseRedirect('/hrm/setupded/')
            try:
                k2 = float(amountemp)
            except :
                return HttpResponseRedirect('/hrm/setupded/')

            getdetails =  tblpension.objects.get(id = 1)
            getdetails.amount = k
            getdetails.employeramt = k2
            getdetails.save()
            return HttpResponseRedirect('/hrm/setupded/')
        else:
            return HttpResponseRedirect('/hrm/setupded/')

def getbranch(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tbllg.objects.get(id = acccode)
                return render_to_response('rsetup/editsubacc.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getdepartment(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tbldepartment.objects.get(id = acccode)
                return render_to_response('rsetup/editacc.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getdesignation(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tbldesig.objects.get(id = acccode)#.
                return render_to_response('rsetup/editdesg.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getallowance(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tblallowance.objects.get(id = acccode)
                return render_to_response('rsetup/editall.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getdeduction(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tbldeduction.objects.get(id = acccode)
                return render_to_response('rsetup/editded.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def getbanksetup(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tblbank.objects.get(id = acccode)
                return render_to_response('rsetup/editdebtors.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def getpfa(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tblpfa.objects.get(id = acccode)
                return render_to_response('rsetup/editcreditor.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def gethmo(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tblhmo.objects.get(id = acccode)
                return render_to_response('rsetup/edithmo.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})

            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def getsavingsname(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails =  tblsavingcode.objects.get(id = 1)
                return render_to_response('rsetup/desc3.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def setupsavingsname(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        if request.method == 'POST':
            amount = request.POST['amount']

            if amount == '':
                return HttpResponseRedirect('/hrm/setupded/')

            getdetails =  tblsavingcode.objects.get(id = 1)
            oldname = getdetails.name
            getdetails.name = amount
            getdetails.save()
            tblsavings.objects.filter(paydes = oldname).update(paydes = amount)
            tblpayroll.objects.filter(schdes = oldname.lower()).update(schdes = amount.lower())
            tblpayroll.objects.filter(deddes = oldname.lower()).update(deddes = amount.lower())
            return HttpResponseRedirect('/hrm/setupded/')
        else:
            return HttpResponseRedirect('/hrm/setupded/')

#uploading wabp data
def uploadbiodatawap(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""

        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"

            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            #try:
            for k in num:
                    j1 = k[0]
                    j2 = k[1]
                    j3 = k[2]
                    j4 = k[3]
                    j5 = k[4]
                    j6 = k[5]
                    j7 = k[6]
                    j8 = k[7]
                    j9 = k[8]
                    j10 = k[9]
                    j11 = k[10]
                    j12 = k[11]


                    j7_as_date = datetime.date(*xlrd.xldate_as_tuple(j7, 0)[:3])
                    #j17_as_date = datetime.date(*xlrd.xldate_as_tuple(j17, 0)[:3])
                    #insert into changepin
                    savecon = staffrec(staffid = j1,name = j2,address = 'Nill',phoneno = 'Nill',dateofbirth = '1992-02-15' ,nationality = 'NIGERIAN',stateoforigin = 'Abia',localgovt = 'Aba North',email = 'Nill',nextofkin = 'Nill',nextofkinaddress = 'Nill',nextofkinphone = 'Nill',maritalstatus = 'MARRIED',designation = j4,department = j3,dateofresum = j7_as_date,picture = 'staff/rece.png',userid = 'wale',status = 'ACTIVE',firstguarantor = 'NILL',firstguarantoraddress = 'NILL',secondguarantor = 'NILL',secondguarantoraddress = 'NILL',qualification = 'SSCE',branch = j6,profession = 'Lagos',workedday = 30,level = j8,step = j9,sex = j5)
                    savecon.save()
                    if j11 == 'NIL':
                        pass
                    else:
                        savecon1 = tblstaffpfa(staffid = j1,staffname = j2,hmoname = j11, userid = 'wale',accno = j12 )
                        savecon1.save()
                    #*********************treating
                    effdate = datetime.date.today()
                    transdate11 = effdate
                    # getting the expire date
                    l = int('720')
                    l = l - 1
                    for h in xrange(l):
                        vyear = transdate11.year
                        vmon = transdate11.month
                        vday = transdate11.day
                        vmon2 = vmon + 1
                        if vmon2 > 12:
                            vmon2 = 1
                            vyear = vyear + 1
                        transdate11 = date(vyear,vmon2,vday)
                    ck = monthrange(transdate11.year,transdate11.month)[1]
                    lday = int(ck)
                    transdate1 = date(transdate11.year,transdate11.month,lday)
                    savecon = tblspded(staffid = j1,staffname = j2,amount = float(j10),paydes = 'tax',userid = 'wale',duration = 720,effectivedate = effdate,expiredate = transdate1)
                    savecon.save()
            succ = "Record Uploaded !!!"
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            #except:
             #   succ ="Uploading Error for this"
            #return render_to_response('upload/upload.htm',{'form': form,'succ':succ})

    else:
        form = XlsInputForm()

    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadbiodatawap = staff_member_required(uploadbiodatawap)

#uploading wabp data
def uploadsavingswap(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""

        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"

            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            #try:
            for k in num:
                j1 = k[0]
                j2 = k[1]
                j3 = k[2]
                j4 = k[3]
                j5 = k[4]
                savecon = tblsavings(staffid = j1,staffname = j2,amountbf = j4,paydes = j5,userid = 'wale',contribution = j3)
                savecon.save()
            succ = "Record Uploaded !!!"
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            #except:
            #   succ ="Uploading Error for this"
            #return render_to_response('upload/upload.htm',{'form': form,'succ':succ})

    else:
        form = XlsInputForm()

    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadsavingswap = staff_member_required(uploadsavingswap)

#uploading wabp data
def uploadallowancewap(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""

        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"

            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            #try:
            for k in num:
                j1 = k[0]#name
                j2 = k[1]#amount
                j3 = k[2]#level
                j4 = k[3]#step
                j7 = int(j3)
                j8 = int(j4)
                savecon = tblallowance(desc = str(j7)+','+ str(j8),userid = 'adetowale',amount = float(j2),paydes = j1 )
                savecon.save()

                #deduction
                #savecon2 = tbldeduction(desc = str(j7)+','+ str(j8),userid = 'wale',amount = j6,paydes = 'meal' )
                #savecon2.save()

            succ = "Record Uploaded !!!"
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            #except:
            #   succ ="Uploading Error for this"
            #return render_to_response('upload/upload.htm',{'form': form,'succ':succ})

    else:
        form = XlsInputForm()

    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadallowancewap = staff_member_required(uploadallowancewap)


def uploaddeduction(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""

        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"

            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            #try:
            for k in num:
                j1 = k[0]#name
                j2 = k[1]#amount
                j3 = k[2]#level
                j4 = k[3]#step

                j7 = int(j3)
                j8 = int(j4)
                savecon = tbldeduction(desc = str(j7)+','+ str(j8),userid = 'adetowale',amount = float(j2),paydes = j1 )
                savecon.save()


            succ = "Record Uploaded !!!"
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            #except:
            #   succ ="Uploading Error for this"
            #return render_to_response('upload/upload.htm',{'form': form,'succ':succ})

    else:
        form = XlsInputForm()

    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploaddeduction = staff_member_required(uploaddeduction)



#uploading wabp data
def uploadbankwap(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""
        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"

            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            #try:
            for k in num:
                j1 = k[0]
                j2 = k[1]
                j3 = k[2]#bank name
                j4 = k[3]#account no
                savecon = tblbankdetails(staffid = j1,staffname = j2,bankname = j3,accountno = str(j4),userid = 'wale')
                savecon.save()

            succ = "Record Uploaded !!!"
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            #except:
            #   succ ="Uploading Error for this"
            #return render_to_response('upload/upload.htm',{'form': form,'succ':succ})

    else:
        form = XlsInputForm()

    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadbankwap = staff_member_required(uploadbankwap)


#uploading wabp data
def uploadloanwap(request):
    succ =""
    if request.method == 'POST':
        #row =""
        succ =""
        form = XlsInputForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            num = []
            rows = "testing"

            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            for row_no in range(0, sheet.nrows):
                rows = sheet.row_values(row_no)
                num.append(rows)
                #num = raw_str.split(",")
            ncount = len(num)
            # print raw_str
            #try:
            for k in num:
                j1 = k[0]
                j2 = k[1]
                j3 = k[2]#period
                j4 = k[3]#rate
                j5 = k[4]#monthly repaymnet
                j6 = k[5]#principal amount
                j7 = k[6]#effective date
                j8 = k[7]#loan name
                j7_as_date = datetime.date(*xlrd.xldate_as_tuple(j7, 0)[:3])
                effdate = j7_as_date
                transdate11 = effdate
                # getting the expire date
                l = int(j3)
                l = l - 1
                for h in xrange(l):
                    vyear = transdate11.year
                    vmon = transdate11.month
                    vday = transdate11.day
                    vmon2 = vmon + 1
                    if vmon2 > 12:
                        vmon2 = 1
                        vyear = vyear + 1
                    transdate11 = date(vyear,vmon2,vday)
                ck = monthrange(transdate11.year,transdate11.month)[1]
                lday = int(ck)
                transdate1 = date(transdate11.year,transdate11.month,lday)
                kint = float(j4)
                kamt = float(j6)
                kduration = int(j3)
                getint = ((kint * kamt )/100) + kamt
                mrepay = getint / kduration
                savecon = tblloan(staffid = j1,staffname = j2,amount = kamt,paydes = j8,userid = 'wale',duration = j3,intrate = kint,effectivedate = effdate,expiredate = transdate1,monthlyepayment = mrepay)
                savecon.save()

            succ = "Record Uploaded !!!"
            return render_to_response('upload/upload.htm',{'form': form,'succ':succ})
            #except:
            #   succ ="Uploading Error for this"
            #return render_to_response('upload/upload.htm',{'form': form,'succ':succ})

    else:
        form = XlsInputForm()

    return render_to_response('upload/upload.htm', {'form': form,'succ':succ})
uploadloanwap = staff_member_required(uploadloanwap)



