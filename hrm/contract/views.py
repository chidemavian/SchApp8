# Create your views here.
from django.template import loader, Context,RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.core.serializers.json import simplejson as json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import  HttpResponseRedirect
from myproject.hrm.utils import *
from myproject.hrm.payroll.form import *
from myproject.hrm.contract.form import *
from myproject.hrm.contract.models import *
from myproject.hrm.rcsetup.models import *
from myproject.hrm.rcwadmin.models import *
from myproject.hrm.payroll.models import *
from myproject.hrm.train.models import *
from myproject.hrm.payroll.capy import *
from myproject.hrm.query.models import *
from django.db.models import Max,Sum
from django.contrib.sessions.models import Session
import datetime
from datetime import date,time,timedelta
import xlwt
from django.core.serializers.json import simplejson as json
import locale
locale.setlocale(locale.LC_ALL,'')


def contractstaff(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.jobsetup
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/contract/unauto/')
            varerr =""
            getdetails =""
            if request.method == 'POST':
                form = contractform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    staffname = form.cleaned_data['staffname']
                    address = form.cleaned_data['address']
                    phoneno = form.cleaned_data['phoneno']
                    nextofkin = form.cleaned_data['nextofkin']
                    nextofkinphone = form.cleaned_data['nextofkinphone']
                    accname = form.cleaned_data['accname']
                    accno = form.cleaned_data['accno']
                    allowance = form.cleaned_data['allowance']
                    if tblcontractstaff.objects.filter(accno = accno).count() == 0:
                        pass
                    else:
                        varerr = "Staff With Account No %s in Existence " %accno
                        getdetails = tblcontractstaff.objects.all().order_by('staffname','id')
                        return render_to_response('contract/staffpension.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                    try:
                        k = float(allowance)
                    except :
                        varerr = "Invalid Allowance "
                        getdetails = tblcontractstaff.objects.all().order_by('staffname','id')
                        return render_to_response('contract/staffpension.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

                    savecon = tblcontractstaff(staffname = staffname,address = address,phoneno = phoneno,nextofkin = nextofkin,nextofkinphone = nextofkinphone ,userid = varuser,accname = accname,accno = accno,allowance = allowance,deduction= 0,overtime = 0)
                    savecon.save()
                    return HttpResponseRedirect('/hrm/contract/contractstaff/')
            else:

                form = contractform()
                getdetails = tblcontractstaff.objects.all().order_by('staffname','id')
            return render_to_response('contract/staffpension.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')

def editcontract(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.jobsetup
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/contract/unauto/')
        varerr =""
        if request.method == 'POST':
            getdetails = ""

            staffname = request.POST['staffname']
            address = request.POST['address']
            phoneno = request.POST['phoneno']
            nextofkin = request.POST['nextofkin']
            nextofkinphone = request.POST['nextofkinphone']
            accname = request.POST['accname']
            accno = request.POST['accno']
            allowance = request.POST['allowance']
            deduction = request.POST['deduction']
            overtime = request.POST['overtime']

            if  address == "" or phoneno == "" or nextofkin == "" or staffname == ""  or nextofkinphone == "" or accname == "" or accno == "" or allowance == "" or deduction == "" or overtime =="":
                varerr = "ALL FIELDS ARE REQUIRED"
                #getdetails = tblcontractstaff.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                return HttpResponseRedirect('/hrm/contract/contractstaff/')
            try:
                k = float(allowance)
            except :
                varerr = "Invalid Allowance "
                #getdetails = tblcontractstaff.objects.get(id = invid)
                return HttpResponseRedirect('/hrm/contract/contractstaff/')
            try:
                j = float(deduction)
            except :
                varerr = "Invalid Allowance "
                #getdetails = tblcontractstaff.objects.get(id = invid)
                return HttpResponseRedirect('/hrm/contract/contractstaff/')
            try:
                p = float(overtime)
            except :
                varerr = "Invalid Overtime "
                #getdetails = tblcontractstaff.objects.get(id = invid)
                return HttpResponseRedirect('/hrm/contract/contractstaff/')


            seldata = tblcontractstaff.objects.get(id = invid)
            seldata.staffname = staffname
            seldata.address = address
            seldata.phoneno = phoneno
            seldata.nextofkin = nextofkin
            seldata.nextofkinphone = nextofkinphone
            seldata.accname = accname
            seldata.accno = accno
            seldata.allowance = k
            seldata.deduction = j
            seldata.overtime = p
            seldata.userid = varuser
            seldata.save()
            return HttpResponseRedirect('/hrm/contract/contractstaff/')
        else:
            try:
                gdata = ""#tblcategory.objects.all().order_by('name')
                getdetails = tblcontractstaff.objects.get(id = invid)
                return render_to_response('contract/editnonpension.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'gdata':gdata})
            except:
                varerr = "Account Not Exist"
                return render_to_response('contract/editnonpension.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')

def getcontract(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                bank = tblbank.objects.all().order_by('name')
                getdetails = tblcontractstaff.objects.get(id = acccode)#.order_by('acccode')#tblaccount_acccode
                return render_to_response('contract/editnonpension.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'bank':bank})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def deletecontract(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        seldata = tblcontractstaff.objects.get(id = invid)
        seldata.delete()
        return HttpResponseRedirect('/hrm/contract/contractstaff/')

    else:
        return HttpResponseRedirect('/login/')


def computepayrollcontract(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.jobsetup
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/contract/unauto/')
            varerr =""
            getdetails =""
            caldate1 = ""
            if request.method == 'POST':
                form = payrollform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    caldate1 = form.cleaned_data['caldate']
                    caldate2 = caldate1.split('/')
                    caldate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))

                    tblcontractpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year).delete()

                    #****************************************ending deletion ************************
                    kp = monthrange(caldate.year,caldate.month)[1]
                    #print kp
                    vmd = int(kp)
                    if tblcontractstaff.objects.all().count() == 0 :
                        return HttpResponseRedirect('/hrm/contract/computepayrollcontract/')
                    else:
                        ll = []
                        lk = ""
                        vardata = tblcontractstaff.objects.all().order_by('staffname')
                        for j in vardata:
                            staffname = j.staffname
                            bankname = j.accname
                            accno = j.accno
                            allowance = j.allowance
                            deduction = j.deduction
                            overtime = j.overtime
                            allsave1 = tblcontractpayroll(staffname = staffname,accname = bankname,accno = accno, allowance = allowance,deduction = deduction,overtime = overtime ,recday = caldate.day,recmonth = caldate.month,recyear = caldate.year,recdate = caldate, userid = varuser)
                            allsave1.save()

                    varerr = "OPERATION SUCCESSFUL"
                    return render_to_response('contract/staffpayroll.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
            else:

                form = payrollform()
                getdetails = ""
            return render_to_response('contract/staffpayroll.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')

def contractschedule(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.jobsetup
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/contract/unauto/')
            #varerr =""
            getdetails =""
            caldate1 = ""
            if request.method == 'POST':
                form = payrollscheduleform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    caldate1 = form.cleaned_data['caldate']
                    caldate2 = caldate1.split('/')
                    caldate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                    if tblcontractpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year).count() == 0:
                        varerr = "No Record For The Selected Month"
                        return render_to_response('contract/printschedule.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))

                    ll =[]
                    stafflist = []
                    #allowance
                    tall = 0
                    tded = 0
                    tover = 0
                    tnetp = 0
                    vda = tblcontractpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year).order_by('staffname')
                    for  jj in vda:
                        staffname = jj.staffname
                        allowance = jj.allowance
                        deduction = jj.deduction
                        overtime = jj.overtime
                        netpay1 = float(allowance) + float(overtime)
                        netpay = netpay1 - float(deduction)
                        tall =  tall + allowance
                        tded = tded + deduction
                        tover = tover + overtime
                        tnetp = tnetp + netpay
                        allo = locale.format("%.2f",allowance,grouping=True)
                        ded = locale.format("%.2f",deduction,grouping=True)
                        ovet = locale.format("%.2f",overtime,grouping=True)
                        net = locale.format("%.2f",netpay,grouping=True)
                        staffdic =  {'staffname':staffname.title(),'allowance':allo,'deduction':ded,'overtime':ovet,'netpay':net}
                        stafflist.append(staffdic)
                    tall1 = locale.format("%.2f",tall,grouping=True)
                    tded1 = locale.format("%.2f",tded,grouping=True)
                    tover1 = locale.format("%.2f",tover,grouping=True)
                    tnetp1 = locale.format("%.2f",tnetp,grouping=True)
                    lldic = {'totalall':tall1,'totalded':tded1,'totalover':tover1,'totalnet':tnetp1,'staffdata':stafflist}
                    ll.append(lldic)

                    comp = tblcompanyinfo.objects.get(id = 1)
                    disdate = caldate.strftime('%b,%Y')
                    if form.cleaned_data['excelfile']:
                        response = HttpResponse(mimetype="application/ms-excel")
                        response['Content-Disposition'] = 'attachment; filename=salaryschedule.xls'
                        wb = xlwt.Workbook()
                        ws = wb.add_sheet('salaryschedule')
                        ws.write(1, 1, comp.name)
                        ws.write(2, 1, comp.address)
                        ws.write(3, 1, disdate)
                        ws.write(3, 2, gettime())
                        ws.write(4, 0, 'Staff Name')
                        ws.write(4, 1, 'Allowance')
                        ws.write(4, 2, 'Deduction')
                        ws.write(4, 3, 'Overtime')
                        ws.write(4, 4, 'Net Pay')
                        k = 5
                        for jd in ll:
                            for p in jd['staffdata']:
                                ws.write(k, 0,p['staffname'])
                                ws.write(k, 1,p['allowance'])
                                ws.write(k, 2,p['deduction'])
                                ws.write(k, 3,p['overtime'])
                                ws.write(k, 4,p['netpay'])
                                k += 1
                            #k = k + 1
                            ws.write(k, 0, 'TOTAL')
                            ws.write(k, 1, jd['totalall'])
                            ws.write(k, 2, jd['totalded'])
                            ws.write(k, 3, jd['totalover'])
                            ws.write(k, 4, jd['totalnet'])
                        wb.save(response)
                        return response
                    else:
                        #jfk = range(ss)
                        return render_to_response('contract/printschedule.htm',{'varuser':varuser,'varerr':varerr,'form':form,'ll':ll,'comp':comp,'disdate':disdate,'printdate': gettime()},context_instance = RequestContext(request))
            else:

                form = payrollscheduleform()
                getdetails = ""
            return render_to_response('contract/printschedule.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')

def contracttobank(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.jobsetup
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/contract/unauto/')
            varerr =""
            getdetails =""
            caldate1 = ""
            if request.method == 'POST':
                form = payrollform2(request.POST) # A form bound to the POST data
                if form.is_valid():
                    bankname = form.cleaned_data['bankname']
                    caldate1 = form.cleaned_data['caldate']
                    caldate2 = caldate1.split('/')
                    caldate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                    #print caldate
                    # return HttpResponseRedirect('/hrm/staffedu/')
                    if tblcontractpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year).count() == 0:
                        varerr = 'Payroll has not been computed for this month'
                        return render_to_response('contract/printtobank.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))

                    if tblcontractstaff.objects.filter(accname = bankname).count() == 0 :
                        #print "No Record"
                        return HttpResponseRedirect('/hrm/contract/contracttobank/')
                    tall = 0
                    tded = 0
                    tover = 0
                    tnetp = 0
                    stafflist =[]
                    ll = []
                    vda = tblcontractpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year).order_by('staffname')
                    for  jj in vda:
                        staffname = jj.staffname
                        allowance = jj.allowance
                        deduction = jj.deduction
                        overtime = jj.overtime
                        netpay1 = float(allowance) + float(overtime)
                        netpay = netpay1 - float(deduction)
                        tall =  tall + allowance
                        tded = tded + deduction
                        tover = tover + overtime
                        tnetp = tnetp + netpay
                        allo = locale.format("%.2f",allowance,grouping=True)
                        ded = locale.format("%.2f",deduction,grouping=True)
                        ovet = locale.format("%.2f",overtime,grouping=True)
                        net = locale.format("%.2f",netpay,grouping=True)
                        staffdic =  {'staffname':staffname.title(),'netpay':net,'accno':jj.accno}
                        stafflist.append(staffdic)
                    tall1 = locale.format("%.2f",tall,grouping=True)
                    tded1 = locale.format("%.2f",tded,grouping=True)
                    tover1 = locale.format("%.2f",tover,grouping=True)
                    tnetp1 = locale.format("%.2f",tnetp,grouping=True)
                    lldic = {'totalnet':tnetp1,'staffdata':stafflist}
                    ll.append(lldic)

                    # ka = {'TOTAL':to}
                    # ll.append(ka)
                    comp = tblcompanyinfo.objects.get(id = 1)
                    disdate = caldate.strftime('%b,%Y')
                    if form.cleaned_data['excelfile']:
                        response = HttpResponse(mimetype="application/ms-excel")
                        response['Content-Disposition'] = 'attachment; filename=salarytobank.xls'
                        wb = xlwt.Workbook()
                        ws = wb.add_sheet('salaryschedule')
                        ws.write(0, 1, comp.name)
                        ws.write(1, 1, comp.address)
                        ws.write(2, 1, disdate)
                        ws.write(2, 2, '%s:SALARY' %bankname)
                        ws.write(2, 3,gettime() )
                       # ws.write(3, 0, 'Staff Id')
                        # ws.write(3, 1, 'Bank Name')
                        ws.write(3, 1, 'Staff Name')
                        ws.write(3, 2, 'Account No')
                        ws.write(3, 3, 'Net Pay')
                        k = 4
                        for jd in ll:
                            for p in jd['staffdata']:
                                ws.write(k, 1,p['staffname'])
                                ws.write(k, 2,p['accno'])
                                ws.write(k, 3,p['netpay'])
                                k += 1
                                #k = k + 1
                            ws.write(k, 2, 'TOTAL')
                            ws.write(k, 3, jd['totalnet'])
                        wb.save(response)
                        return response
                    else:
                        return render_to_response('contract/printtobank.htm',{'varuser':varuser,'varerr':varerr,'form':form,'ll':ll,'comp':comp,'disdate':disdate,'bankname':bankname,'printdate':gettime()},context_instance = RequestContext(request))

            else:

                form = payrollform2()
                getdetails = ""
            return render_to_response('contract/printtobank.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')





