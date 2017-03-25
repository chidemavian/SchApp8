# Create your views here.
from django.template import loader, Context,RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import  HttpResponseRedirect
from django.contrib.sessions.models import Session
from myproject.hrm.rcwadmin.models import *
from myproject.hrm.rcsetup.models import *
from myproject.hrm.hrm.models import *
from myproject.hrm.payroll.form import *
from myproject.hrm.payroll.models import *
from myproject.hrm.utils import *
from myproject.hrm.payroll.capy import monthrange
from django.db.models import Max,Sum
import datetime
from datetime import date,time,timedelta
from django.core.serializers.json import simplejson as json
import xlwt
import locale
locale.setlocale(locale.LC_ALL,'')

def enterpayroll(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.jobsetup
        if uenter == "False" :
            return HttpResponseRedirect('/welcome/')
        varerr =""
        return render_to_response('payroll/enterpayroll.htm',{'varuser':varuser,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def pounautopayroll(request):
    if  "userid" in request.session:
        varuser = request.session['userid']

        varerr =""
        return render_to_response('payroll/unautorise.htm',{'varuser':varuser,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def enterworkingdays(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.jobsetup
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/payroll/unauto/')
            varerr =""
            getdetails =""
            if request.method == 'POST':
                form = payrollform1(request.POST) # A form bound to the POST data
                if form.is_valid():
                    payrolldate = form.cleaned_data['payrolldate']
                    caldate2 = payrolldate.split('/')
                    paydate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                   # k = paydate.max()
                    kp = monthrange(paydate.year,paydate.month)[1]
                    #print kp
                    vmd = int(kp)
                    seldata = staffrec.objects.all()
                    for da in seldata:
                       p = staffrec.objects.get(staffid = da.staffid)
                       p.workedday = vmd
                       p.save()
                    return HttpResponseRedirect('/hrm/payroll/enterworkingdays/')
            else:

                form = payrollform1()
                getdetails = staffrec.objects.filter(status = 'ACTIVE').order_by('staffid')
            return render_to_response('payroll/setupall.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')

def editworked(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.jobsetup
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/payroll/unauto/')
        varerr =""
        if request.method == 'POST':
            getdetails = ""
            #dcode = request.POST['accname'] # the amount
           # accno = request.POST['hcode']#the primary key
           # desc1 = request.POST['acccode']#the particulars
            amt = request.POST['amt']
           # desc = request.POST['desc']
            if  amt == "" :
                varerr = "DAYS IS REQUIRED"
                getdetails = staffrec.objects.get(id = invid)
                #return render_to_response('payroll/editworked.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                return HttpResponseRedirect('/hrm/payroll/enterworkingdays/')
            try:
                k = int(amt)
            except:
                varerr = "ERROR IN YOUR ENTRY"
                getdetails = staffrec.objects.get(id = invid)
                #return render_to_response('payroll/editworked.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                return HttpResponseRedirect('/hrm/payroll/enterworkingdays/')
            if k > 31:
                varerr = "YOU ENTERED INVALID WORKED DAYS"
                getdetails = staffrec.objects.get(id = invid)
                #return render_to_response('payroll/editworked.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                return HttpResponseRedirect('/hrm/payroll/enterworkingdays/')
            seldata = staffrec.objects.get(id = invid)
            seldata.workedday = k
            seldata.save()
            return HttpResponseRedirect('/hrm/payroll/enterworkingdays/')
        else:
            try:
                getdetails = staffrec.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                return render_to_response('payroll/editworked.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                varerr = "Account Not Exist"
                return render_to_response('payroll/editworked.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')
def bankdetails(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.jobsetup
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/payroll/unauto/')
            varerr =""
            getdetails =""
            if request.method == 'POST':
                form = bankform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    staffid = form.cleaned_data['staffid']
                    staffname = form.cleaned_data['staffname']
                    bankname = form.cleaned_data['bankname']
                    accountno = form.cleaned_data['accountno']
                    if tblbankdetails.objects.filter(staffid = staffid).count() == 0:
                        pass
                    else:
                        varerr = 'STAFF ALREADY IN EXISTENCE'
                        getdetails =   tblbankdetails.objects.all().order_by('staffid')
                        return render_to_response('payroll/bankdetails.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))


                    savecon = tblbankdetails(staffid = staffid,staffname = staffname,bankname = bankname,accountno = accountno,userid = varuser)
                    savecon.save()
                    return HttpResponseRedirect('/hrm/payroll/bankdetails/')
            else:

                form = bankform()
                getdetails =   tblbankdetails.objects.all().order_by('staffid')
            return render_to_response('payroll/bankdetails.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')

def editbank(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.jobsetup
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/payroll/unauto/')
        varerr =""
        if request.method == 'POST':

            bankname = request.POST['bankname']
            accno = request.POST['accno']
            if  accno == "" :
                varerr = "DAYS IS REQUIRED"
                getdetails = staffrec.objects.get(id = invid)
                #return render_to_response('payroll/editworked.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                return HttpResponseRedirect('/hrm/payroll/bankdetails/')

            seldata = tblbankdetails.objects.get(id = invid)
            seldata.bankname = bankname
            seldata.accountno = accno
            seldata.save()
            return HttpResponseRedirect('/hrm/payroll/bankdetails/')
        else:
            getdetails = tblbankdetails.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
            return render_to_response('payroll/editbank.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})

    else:
        return HttpResponseRedirect('/login/')

def deletebank(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        seldata = tblbankdetails.objects.get(id = invid)
        seldata.delete()
        return HttpResponseRedirect('/hrm/payroll/bankdetails/')
    else:
        return HttpResponseRedirect('/login/')

def computepayroll(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.jobsetup
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/payroll/unauto/')
            varerr =""
            getdetails =""
            caldate1 = ""
            if request.method == 'POST':
                form = payrollform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    caldate1 = form.cleaned_data['caldate']
                    caldate2 = caldate1.split('/')
                    kp = monthrange(int(caldate2[2]),int(caldate2[0]))[1]
                    vmd = int(kp)
                    caldate = date(int(caldate2[2]),int(caldate2[0]),vmd)
                    #caldate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                    #******************************************************************
                    if tblpayroll.objects.all().count() == 0 :
                        olddate = caldate
                    else:
                        varrid1 = tblpayroll.objects.all().aggregate(Max('id'))
                        varrid = varrid1['id__max']
                        olddate = tblpayroll.objects.get(id = varrid).recdate

                    if caldate.month == olddate.month and caldate.year == olddate.year :
                        pass
                    else:
                        if olddate > caldate:
                            varerr = "%s has been computed already" %caldate.strftime("%b,%Y")
                            return render_to_response('payroll/staffpayroll.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
                        else:
                            matdate = olddate
                            vyear = matdate.year
                            vmon = matdate.month
                            vday = matdate.day
                            vmon2 = vmon + 1
                            if vmon2 > 12:
                                vmon2 = 1
                                vyear += 1
                            kp = monthrange(vyear,vmon2)[1]
                            vmd = int(kp)
                            newdate = date(vyear,vmon2,vmd)#the month and year to compute naturally
                            if caldate.month == newdate.month and caldate.year == newdate.year:
                                pass
                            else:
                                varerr = "You Are To Compute for %s" %newdate.strftime("%b,%Y")
                                return render_to_response('payroll/staffpayroll.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
                    # deleting some expired data before payroll tblpayrollpension
                    tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year).delete()
                    tblpayrollpension.objects.filter(recmonth = caldate.month,recyear = caldate.year).delete()
                    tblspall.objects.filter(expiredate__lt = caldate).delete()
                    tblspded.objects.filter(expiredate__lt = caldate).delete()
                    tblloan.objects.filter(expiredate__lt = caldate).delete()
                    #****************************************ending deletion ************************
                    kp = monthrange(caldate.year,caldate.month)[1]
                    #print kp
                    vmd = int(kp)
                    if staffrec.objects.filter(status = "ACTIVE").count() == 0 :
                        return HttpResponseRedirect('/hrm/payroll/computepayroll/')
                    else:
                        ll = []
                        lk = ""
                        vardata = staffrec.objects.filter(status = "ACTIVE")
                        #print vardata
                        cuspart =""
                        custo = 0
                        for j in vardata:
                            ndesg = str(j.level) + ','+ str(j.step)
                            lk = j.name,j.staffid,ndesg,j.workedday
                            ll.append(lk)
                        k = range(len(ll))
                        we =[]
                        for h in k:
                            for m in ll[h]:
                                we.append(m)
                                #**************************************
                            fullname1 = we[0]
                            staffid = we[1]
                            designation = we[2]#designation
                            wokingday = we[3]
                            fulln = str(fullname1)
                            fullname = fulln.lower()
                           #******************************************************get  and treat allowance
                            alld =[]
                            lkl =""
                            lpension =['basic','transport','housing']
                            #pensionrate = tblpension.objects.get(id = 1)
                            gprate = 0#pensionrate.amount
                            emprate = 0#pensionrate.employeramt
                            tpen = 0
                            vded = 0
                            vded1 = 0
                            if tblallowance.objects.filter(desc = designation) == 0:
                                pass
                            else:
                                alldata = tblallowance.objects.filter(desc = designation)# here i treat allowances
                                for l in alldata:
                                    lkl = l.amount,l.paydes
                                    fp = l.paydes.lower()
                                    vdaa = l.amount
                                    if fp in lpension:
                                        tpen += vdaa
                                    alld.append(lkl)
                                    #print alld
                                if tblspded.objects.filter(paydes = 'HOUSING DEDUCTION',staffid = staffid).count() == 0:
                                    vded1 = 0
                                else:
                                    getvalue1 = tblspded.objects.get(paydes = 'HOUSING DEDUCTION',staffid = staffid)
                                    vded1 = getvalue1.amount
                                if tblspded.objects.filter(paydes = 'TRANSPORT DEDUCTION',staffid = staffid).count() == 0:
                                    vded = 0
                                else:
                                    getvalue = tblspded.objects.get(paydes = 'TRANSPORT DEDUCTION',staffid = staffid)
                                    vded = getvalue.amount
                                ij = str(tpen)
                                gded =  float(vded1) + float(vded)
                                pended = float(ij) - float(gded)
                                tpen1 = pended * wokingday / vmd
                                tpen = tpen1 * float(gprate)/ 100.0 # calculating pension
                                temppen = tpen1 * float(emprate)/ 100.0 # employer contribution
                                temppen = str(temppen)
                                tpen = str(tpen)
                                #allsave1 = tblpayroll(staffid = staffid,staffname = fullname,wokingday = wokingday,designation = designation, allamount = 0,alldes = '',dedamount = tpen ,deddes = 'pension',schamount = tpen, schdes = 'pension',recday = caldate.day,recmonth = caldate.month,recyear = caldate.year,recdate = caldate, userid = varuser,outbal = 0)
                                #allsave1.save()
                                empsave = tblpayrollpension(staffid = staffid,employeeamount = tpen,employeramount = temppen,recday = caldate.day,recmonth = caldate.month,recyear = caldate.year,recdate = caldate )
                                empsave.save()
                                k1 = range(len(alld))
                                we1 =[]
                                for h1 in k1:
                                    for m1 in alld[h1]:
                                        we1.append(m1)
                                    allamt = we1[0]
                                    alldesc = we1[1]
                                    allde = str(alldesc)
                                    allde = allde.lower()
                                    allamt1 = allamt* wokingday/vmd
                                    #treating tax
                                   # if allde == 'basic':
                                    #   tax = float(allamt1) * 6.0 /100.0
                                     #  tax = str(tax)
                                      # allsave = tblpayroll(staffid = staffid,staffname = fullname,wokingday = wokingday,designation = designation, allamount = 0,alldes = '',dedamount = tax ,deddes = 'tax',schamount = tax, schdes = 'tax',recday = caldate.day,recmonth = caldate.month,recyear = caldate.year,recdate = caldate, userid = varuser)
                                      # allsave.save()
                                    #print allamt, alldesc,designation
                                    #ending tax
                                    #*****************************************do insetion
                                    allsave = tblpayroll(staffid = staffid,staffname = fullname,wokingday = wokingday,designation = designation, allamount = allamt1,alldes = allde,dedamount = 0 ,deddes ="",schamount = allamt1, schdes = allde,recday = caldate.day,recmonth = caldate.month,recyear = caldate.year,recdate = caldate, userid = varuser,outbal = 0)
                                    allsave.save()
                                    we1.remove(allamt)
                                    we1.remove(alldesc)
                            #end allowance
                            #**************************************************SPECIAL ALLOWANCE
                            allddedS =[]
                            lklDS =""
                            if tblspall.objects.filter(staffid = staffid,effectivedate__lte = caldate) == 0:
                                #print 'not available'
                                pass
                            else:
                                #print 'available'
                                alldataDS = tblspall.objects.filter(staffid = staffid,effectivedate__lte = caldate)
                                for l in alldataDS:
                                    lklDS = l.amount,l.paydes
                                    allddedS.append(lklDS)
                                    #print alld
                                k1 = range(len(allddedS))
                                we1DS =[]
                                for h1 in k1:
                                    for m1 in allddedS[h1]:
                                        we1DS.append(m1)
                                    allamt = we1DS[0]
                                    alldesc = we1DS[1]
                                    allde = str(alldesc)
                                    allde = allde.lower()
                                    # print allamt, alldesc
                                    #*****************************************do insetion
                                    allsave = tblpayroll(staffid = staffid,staffname = fullname,wokingday = wokingday,designation = designation, allamount = allamt,alldes = allde,dedamount = 0 ,deddes = "",schamount = allamt, schdes = allde,recday = caldate.day,recmonth = caldate.month,recyear = caldate.year,recdate = caldate, userid = varuser,outbal = 0)
                                    allsave.save()
                                    we1DS.remove(allamt)
                                    we1DS.remove(alldesc)

                            #*****************************************************************************deductions
                            alldded =[]
                            lklD =""
                            if tbldeduction.objects.filter(desc = designation) == 0:
                                pass
                            else:
                                alldataD = tbldeduction.objects.filter(desc = designation)
                                for l in alldataD:
                                    lklD = l.amount,l.paydes
                                    alldded.append(lklD)
                                    #print alld
                                k1 = range(len(alldded))
                                we1D =[]
                                for h1 in k1:
                                    for m1 in alldded[h1]:
                                        we1D.append(m1)
                                    allamt = we1D[0]
                                    alldesc = we1D[1]
                                    allde = str(alldesc)
                                    allde = allde.lower()
                                    # print allamt, alldesc
                                    #*****************************************do insetion
                                    allsave = tblpayroll(staffid = staffid,staffname = fullname,wokingday = wokingday,designation = designation, allamount = 0,alldes = "",dedamount = allamt ,deddes = allde,schamount = allamt, schdes = allde,recday = caldate.day,recmonth = caldate.month,recyear = caldate.year,recdate = caldate, userid = varuser,outbal = 0)
                                    allsave.save()
                                    we1D.remove(allamt)
                                    we1D.remove(alldesc)
                            #ending deductions
                            #*****************************************************************************start special deductions
                            allddedS =[]
                            lklDS =""
                            if tblspded.objects.filter(staffid = staffid,effectivedate__lte = caldate) == 0:
                                pass
                            else:
                                alldataDS = tblspded.objects.filter(staffid = staffid,effectivedate__lte = caldate)
                                for l in alldataDS:
                                    lklDS = l.amount,l.paydes
                                    allddedS.append(lklDS)
                                    #print alld
                                k1 = range(len(allddedS))
                                we1DS =[]
                                for h1 in k1:
                                    for m1 in allddedS[h1]:
                                        we1DS.append(m1)
                                    allamt = we1DS[0]
                                    alldesc = we1DS[1]
                                    allde =str(alldesc)
                                    allde =allde.lower()
                                    # print allamt, alldesc
                                    #*****************************************do insetion
                                    allsave = tblpayroll(staffid = staffid,staffname = fullname,wokingday = wokingday,designation = designation, allamount = 0,alldes = "",dedamount = allamt ,deddes = allde,schamount = allamt, schdes = allde,recday = caldate.day,recmonth = caldate.month,recyear = caldate.year,recdate = caldate, userid = varuser,outbal = 0)
                                    allsave.save()
                                    we1DS.remove(allamt)
                                    we1DS.remove(alldesc)
                            #*******************************************************ending special deduction
                            #*****************************************************************************start Savings i.e contributions
                            allddedS =[]
                            lklDS =""
                            if tblsavings.objects.filter(staffid = staffid) == 0:
                                pass
                            else:
                                alldataDS = tblsavings.objects.filter(staffid = staffid)
                                for l in alldataDS:
                                    lklDS = l.contribution,l.paydes
                                    allddedS.append(lklDS)
                                    #print alld
                                k1 = range(len(allddedS))
                                we1DS =[]
                                tsavings = 0
                                tbalance = 0
                                for h1 in k1:
                                    for m1 in allddedS[h1]:
                                        we1DS.append(m1)
                                    allamt = we1DS[0]
                                    alldesc = we1DS[1]
                                    allde =str(alldesc)
                                    allde =allde.lower()
                                    #******************************************
                                    if tblpayroll.objects.filter(staffid = staffid,schdes = allde).count() == 0:

                                        tcont = 0
                                    else:

                                       nob = tblpayroll.objects.filter(staffid = staffid,schdes = allde).aggregate(Sum('schamount')) #total savings
                                       tcont = nob['schamount__sum']
                                    if tblsavings.objects.filter(staffid = staffid).count() == 0:
                                       tbalance = 0
                                    else:
                                        getstaff = tblsavings.objects.get(staffid = staffid)
                                        balb4 = getstaff.amountbf #savings b4
                                        moncont1 = getstaff.contribution#Monthly Contribution
                                        totalbal1 = float(balb4) + float(tcont) + float(moncont1) # total contribution tilldate
                                        tsavings = tsavings + moncont1 #total monthly savings
                                        tbalance = tbalance + totalbal1 # total balance
                                    tbalance = str(tbalance)
                                    #**************************************
                                    allsave = tblpayroll(staffid = staffid,staffname = fullname,wokingday = wokingday,designation = designation, allamount = 0,alldes = "",dedamount = allamt ,deddes = allde,schamount = allamt, schdes = allde,recday = caldate.day,recmonth = caldate.month,recyear = caldate.year,recdate = caldate, userid = varuser,outbal =tbalance)
                                    allsave.save()
                                    we1DS.remove(allamt)
                                    we1DS.remove(alldesc)
                            #*******************************************************ending savings contribution deduction
                            #*****************************************************************************start loan repayment
                            allddedS =[]
                            lklDS =""
                            if tblloan.objects.filter(staffid = staffid,effectivedate__lte = caldate) == 0:
                                pass
                            else:
                                alldataDS = tblloan.objects.filter(staffid = staffid,effectivedate__lte = caldate)
                                for l in alldataDS:
                                    lklDS = l.monthlyepayment,l.paydes
                                    allddedS.append(lklDS)
                                    #print alld
                                k1 = range(len(allddedS))
                                we1DS =[]
                                for h1 in k1:
                                    for m1 in allddedS[h1]:
                                        we1DS.append(m1)
                                    allamt = we1DS[0]
                                    alldesc = we1DS[1]
                                    allde =str(alldesc)
                                    allde =allde.lower()
                                    nob = 0
                                    #*********************getting outstanding balance
                                    if tblpayroll.objects.filter(staffid = staffid,schdes = allde).count() == 0:
                                        nob = 0
                                        tcont = 0
                                    else:
                                        nob = tblpayroll.objects.filter(staffid = d.staffid,schdes = allde,recdate__gte = d.effectivedate).count() #number of occurence
                                    if tblloan.objects.filter(paydes = allde.upper(),staffid = staffid).count() == 0:
                                       outbal = 0
                                    else:

                                        getstaff = tblloan.objects.get(paydes = allde.upper(),staffid = staffid)
                                        tperiod = getstaff.duration #duration
                                        priamt = getstaff.amount#principal Amount
                                        intrate = getstaff.intrate#interest rate
                                        monrepay = getstaff.monthlyepayment#monthly repayment
                                        calint = float(intrate)/100
                                        intamt = calint *float(priamt) # interest amount
                                        # print 'Interest amount ',intamt,intrate,priamt,calint
                                        tpayable = intamt + float(priamt) #totalm payable
                                        tpay = nob * monrepay # total pay till date
                                        outbal = tpayable - float(tpay) - float(monrepay)# outstanding balance
                                    outbal = str(outbal)
                                    #**************************************************
                                    allsave = tblpayroll(staffid = staffid,staffname = fullname,wokingday = wokingday,designation = designation, allamount = 0,alldes = "",dedamount = allamt ,deddes = allde,schamount = allamt, schdes = allde,recday = caldate.day,recmonth = caldate.month,recyear = caldate.year,recdate = caldate, userid = varuser,outbal = outbal)
                                    allsave.save()
                                    we1DS.remove(allamt)
                                    we1DS.remove(alldesc)
                                    #*******************************************************ending loan repayment deduction
                            #getting the gross pay of the staff
                            if tblpayroll.objects.filter(staffid = staffid,recmonth = caldate.month,recyear = caldate.year).count() == 0 :
                                pass
                            else:
                                varrid1 = tblpayroll.objects.filter(staffid = staffid,recmonth = caldate.month,recyear = caldate.year).aggregate(Sum('allamount'),Sum('dedamount'))
                                varrid = varrid1['allamount__sum']#gross pay
                                # varrid11 = tblpayroll.objects.filter(staffid = staffid).aggregate(Sum('dedamount'))
                                varridded = varrid1['dedamount__sum']#total deduction
                                zznet = varrid - varridded # net pay
                                allsave1 = tblpayroll(staffid = staffid,staffname = fullname,wokingday = wokingday,designation = designation, allamount = 0,alldes = "",dedamount = 0 ,deddes = "",schamount = varrid, schdes = "grosspay",recday = caldate.day,recmonth = caldate.month,recyear = caldate.year,recdate = caldate, userid = varuser,outbal = 0)
                                allsave1.save()
                                allsave2 = tblpayroll(staffid = staffid,staffname = fullname,wokingday = wokingday,designation = designation, allamount = 0,alldes = "",dedamount = 0 ,deddes = "",schamount = zznet, schdes = "netpay",recday = caldate.day,recmonth = caldate.month,recyear = caldate.year,recdate = caldate, userid = varuser,outbal = 0)
                                allsave2.save()
                               # print zznet ,varrid
                            we.remove(fullname1)
                            we.remove(staffid)
                            we.remove(designation)
                            we.remove(wokingday)
                            #*************************CLOSE DEDUCTION, get the gross and the net pay

                    varerr = "OPERATION SUCCESSFUL"
                    return render_to_response('payroll/staffpayroll.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
            else:

                form = payrollform()
                getdetails = ""
            return render_to_response('payroll/staffpayroll.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')

def printtobank(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.jobsetup
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/payroll/unauto/')
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
                    if tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year).count() == 0:
                        varerr = 'Payroll has not been computed for this month'
                        return render_to_response('payroll/printtobank.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))

                    if staffrec.objects.filter(status = "ACTIVE").count() == 0 :
                        #print "No Record"
                        return HttpResponseRedirect('/hrm/payroll/computepayroll/')
                    else:
                        #print "Record exist"
                        ll = []
                        lk = ""
                        vardata = staffrec.objects.filter(status = "ACTIVE").order_by('staffid')
                        #print vardata
                        npay = 0
                        cuspart =""
                        custo = 0
                        toall = 0
                        for j in vardata:
                            lk = j.name,j.staffid
                            if tblbankdetails.objects.filter(staffid = j.staffid,bankname = bankname).count() == 0:
                               pass
                            else:
                                da = tblbankdetails.objects.get(staffid = j.staffid,bankname = bankname)
                                bankcode = ""
                                for h in tblbank.objects.filter(name = bankname):
                                    bankcode = h.sortcode
                               # print j.staffid,bankname
                                payda = tblpayroll.objects.filter(staffid = j.staffid,schdes = 'netpay',recmonth = caldate.month,recyear = caldate.year)
                                for jk in payda:
                                    npay1 = jk.schamount
                                    toall += jk.schamount
                                    npay = locale.format("%.2f",npay1,grouping=True)
                                    #print npay
                                k = {'staffid':da.staffid,'bankname':da.bankname,'name':da.staffname,'accno':da.accountno,'netpay':npay,'sortcode':bankcode}
                                ll.append(k)
                    #asd = tblpayroll.objects.filter(schdes = 'netpay',recmonth = caldate.month,recyear = caldate.year)
                    #toall = 0
                    #for vto in asd:
                     #   toall += vto.schamount
                    toall = locale.format("%.2f",toall,grouping=True)

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
                        ws.write(2, 3, gettime())
                        ws.write(3, 0, 'Account No')
                       # ws.write(3, 1, 'Bank Name')
                        ws.write(3, 1, 'Name')
                        ws.write(3, 2, 'Name')
                        ws.write(3, 3, 'Amount')
                        ws.write(3, 4, 'Bank Sort Code')
                        ws.write(3, 5, 'Account No')
                        ws.write(3, 6, '')
                        ws.write(3, 7, '')
                        ws.write(3, 8, '')
                        k = 4
                        for jd in ll:
                            ws.write(k, 0, jd['accno'])
                            ws.write(k, 1, jd['name'].title())
                            ws.write(k, 2, jd['name'].title())
                            ws.write(k, 3, jd['netpay'])
                            ws.write(k, 4, jd['sortcode'])
                            ws.write(k, 5, jd['accno'])
                            ws.write(k, 6, 0)
                            ws.write(k, 7, 0)
                            ws.write(k, 8, 20)
                            k += 1
                        ws.write(k, 2, 'TOTAL')
                        ws.write(k, 3, toall)
                        wb.save(response)
                        return response
                    else:
                        return render_to_response('payroll/printtobank.htm',{'varuser':varuser,'varerr':varerr,'form':form,'ll':ll,'comp':comp,'disdate':disdate,'bankname':bankname,'total':toall,'printdate':gettime()},context_instance = RequestContext(request))

            else:

                form = payrollform2()
                getdetails = ""
            return render_to_response('payroll/printtobank.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')


def printschedule(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.jobsetup
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/payroll/unauto/')
            varerr =""
            getdetails =""
            caldate1 = ""
            if request.method == 'POST':
                form = payrollscheduleform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    caldate1 = form.cleaned_data['caldate']
                    caldate2 = caldate1.split('/')
                    caldate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                    if tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year).exclude(allamount = 0 ).count() == 0:
                        varerr = "No Record For The Selected Month"
                        return render_to_response('payroll/printschedule.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
                    vdic ={}
                    vrdic = {}
                    lh =[]
                    vdicd ={}
                    vrdicd = {}
                    lhd =[]
                    stafflist = []
                    #allowance
                    vda = tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year).exclude(allamount = 0 )
                    for  jj in vda:
                        vdic ={jj.alldes:0}
                        vrdic.update(vdic)
                    lh = vrdic.keys()
                    lh.sort()
                    gp = ['grosspay']
                    lh.extend(gp)
                    #deductions
                    vdad = tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year).exclude(dedamount = 0 )
                    for  jjd in vdad:
                        vdicd ={jjd.deddes:0}
                        vrdicd.update(vdicd)
                    lhd = vrdicd.keys()
                    lhd.sort()
                    lh.extend(lhd)
                    np = ['netpay']
                    #zne = ['grosspay','netpay']
                    lh.extend(np)
                    if staffrec.objects.filter(status = "ACTIVE").count() == 0 :
                        #print "No Record"
                        return HttpResponseRedirect('/hrm/payroll/printschedule/')
                    else:
                        ll = []
                        lk = ""
                        vardata = staffrec.objects.filter(status = "ACTIVE")
                        npay = 0
                        cuspart =""
                        custo = 0
                        vsal = 0
                        vsal1 = 0
                        lsal = {}
                        for j in vardata:
                            if tblpayroll.objects.filter(staffid = j.staffid,schdes = 'grosspay',recmonth = caldate.month,recyear = caldate.year).count() == 0:
                                vsal = 0
                                #pass
                            else:
                                payda = tblpayroll.objects.filter(staffid = j.staffid,schdes = 'grosspay',recmonth = caldate.month,recyear = caldate.year)
                                for jk in payda:
                                    vsal = jk.schamount
                            gh = locale.format("%.2f",vsal,grouping=True)
                            if tblpayroll.objects.filter(staffid = j.staffid,schdes = 'netpay',recmonth = caldate.month,recyear = caldate.year).count() == 0:
                                vsal1 = 0
                                #pass
                            else:
                                payda = tblpayroll.objects.filter(staffid = j.staffid,schdes = 'netpay',recmonth = caldate.month,recyear = caldate.year)
                                for jk in payda:
                                    vsal1 = jk.schamount
                            nh = locale.format("%.2f",vsal1,grouping=True)
                            staffdic =  {'staffid':j.staffid,'staffname':j.name.title(),'designation':j.designation,'department':j.department,'grosspay':gh,'netpay':nh}
                            stafflist.append(staffdic)
                            lsal = {'staffid':j.staffid,'staffname':j.name,'designation':j.designation,'department':j.department}
                            for vdes in lh:
                                if tblpayroll.objects.filter(staffid = j.staffid,schdes = vdes,recmonth = caldate.month,recyear = caldate.year).count() == 0:
                                    vsal = 0
                                    #pass
                                else:
                                    payda = tblpayroll.objects.filter(staffid = j.staffid,schdes = vdes,recmonth = caldate.month,recyear = caldate.year)
                                    for jk in payda:
                                        vsal = jk.schamount
                                h = locale.format("%.2f",vsal,grouping=True)
                                k = {vdes:h}
                                lsal.update(k)
                            ll.append(lsal)
                    lsal = {'staffid':"",'staffname':"",'designation':"",'department':"TOTAL"}
                    for po in lh:
                        toall = 0
                        k ={}
                        asd = tblpayroll.objects.filter(schdes = po,recmonth = caldate.month,recyear = caldate.year)
                        for vto in asd:
                            toall += vto.schamount
                        h2 = locale.format("%.2f",toall,grouping=True)
                        k = {po:h2}
                        #print k
                        lsal.update(k)
                    ll.append(lsal)
                    varrid1 = tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year,).aggregate(Sum('allamount'),Sum('dedamount'))
                    totalgross1 = varrid1['allamount__sum']#gross pay
                    totalnet1 = varrid1['dedamount__sum']#total deduction
                    vnetpay = totalgross1 - totalnet1
                    totalgross = locale.format("%.2f",totalgross1,grouping=True)
                    totalnet = locale.format("%.2f",vnetpay,grouping=True)
                    k = len(lh)
                    shead =['staffid','staffname','designation','department']
                    shead.extend(lh)
                    ss = len(shead)
                    comp = tblcompanyinfo.objects.get(id = 1)
                    disdate = caldate.strftime('%b,%Y')
                    if form.cleaned_data['excelfile']:
                        response = HttpResponse(mimetype="application/ms-excel")
                        response['Content-Disposition'] = 'attachment; filename=salaryschedule.xls'
                        wb = xlwt.Workbook()
                        ws = wb.add_sheet('salaryschedule')
                        ws.write(1, 1, comp.name)
                        ws.write(2, 1, comp.address)
                        ws.write(2, 2, gettime())
                        bn = 0
                        for nnn in xrange(ss):
                            ws.write(3, bn, shead[nnn])
                            bn += 1
                        k = 4
                        for jd in ll:
                            for ppp in xrange(ss):
                                ws.write(k, ppp, jd[shead[ppp]])
                            k += 1
                        wb.save(response)
                        return response
                    else:
                        jfk = range(ss)
                        return render_to_response('payroll/printschedule.htm',{'varuser':varuser,'varerr':varerr,'form':form,'ll':stafflist,'shead':shead,'comp':comp,'disdate':disdate,'jfk':jfk,'totalgross':totalgross,'totalnet':totalnet,'printdate':gettime()},context_instance = RequestContext(request))
            else:

                form = payrollscheduleform()
                getdetails = ""
            return render_to_response('payroll/printschedule.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')


def printpayslip(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.jobsetup
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/payroll/unauto/')
            varerr =""
            getdetails =""
            caldate1 = ""
            if request.method == 'POST':
                form = payslipform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    caldate1 = form.cleaned_data['caldate']
                    staffid = form.cleaned_data['staffid']
                    caldate2 = caldate1.split('/')
                    caldate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                    staff = ''
                    if staffrec.objects.filter(staffid = staffid):
                        staff = staffrec.objects.get(staffid = staffid)
                    else:
                        varerr = "Staff Not In Existence "
                        return render_to_response('payroll/printpayslip.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))


                    if tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year,staffid = staffid).exclude(allamount = 0 ).count() == 0:
                        varerr = "No Record For The Selected Month"
                        return render_to_response('payroll/printpayslip.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
                    alllist = []
                    dedlist = []
                    getsav = tblsavingcode.objects.get(id = 1)
                    cont = getsav.name # the contribution name
                    vda = tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year,staffid = staffid).exclude(allamount = 0 )
                    totall1 = 0
                    for  jj in vda:
                        totall1 += jj.allamount
                        desc = jj.alldes
                        alamt = jj.allamount
                        getall = locale.format("%.2f",alamt,grouping=True)
                        alldic = {'alldes':desc,'allamount':getall}
                        alllist.append(alldic)
                    totall = locale.format("%.2f",totall1,grouping=True)
                    vdad = tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year,staffid = staffid).exclude(dedamount = 0 )
                    totded1 = 0
                    vdate = ''
                    staffname = ''
                    desig = ''
                    staffcont = ''
                    for  jjd in vdad:
                        totded1 += jjd.dedamount

                        desc = jjd.deddes
                        alamt = jjd.dedamount
                        outbal = jjd.outbal
                        getall = locale.format("%.2f",alamt,grouping=True)
                        outbal1 = locale.format("%.2f",outbal,grouping=True)
                        alldic = {'deddes':desc,'dedamount':getall,'outstanding':outbal1}
                        dedlist.append(alldic)
                    totded = locale.format("%.2f",totded1,grouping=True)
                    #getting staff contribution
                    if tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year,staffid = staffid,schdes = cont.lower()).count() == 0:
                        staffcont = ''
                    else:
                        if tblsavings.objects.filter(staffid = staffid):
                            tsav = tblsavings.objects.get(staffid = staffid)
                            tsat = tsav.amountbf
                            vnet11 = tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year,staffid = staffid,schdes = cont.lower()).aggregate(Sum('schamount'))
                            vnet12 = vnet11['schamount__sum']
                            gtsavt = float(tsat) + float(vnet12)
                            totalcont = locale.format("%.2f",gtsavt,grouping=True)
                            staffcont = 'Total %s :: %s'%(cont.upper(),totalcont)
                        else:
                            pass
                    #zne = ['grosspay','netpay']
                    #vgross = tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year,staffid = staffid,schdes = 'grosspay')
                    vnet1 = tblpayroll.objects.get(recmonth = caldate.month,recyear = caldate.year,staffid = staffid,schdes = 'netpay')
                    vnet1 = vnet1.schamount
                    vnet = locale.format("%.2f",vnet1,grouping=True)
                    comp = tblcompanyinfo.objects.get(id = 1)
                    disdate = caldate.strftime('%b,%Y')
                    staffname = staff.name
                    desig = staff.designation

                    #pslip = {'staffid':staffid,'staffname':staffname,'desig':desig,'allowance':vda,'deduction':vdad,'totalall':totall,'totalded':totded,'netpay':vnet,'disdate':disdate}
                    return render_to_response('payroll/printpayslip.htm',{'varuser':varuser,'varerr':varerr,'form':form,'staffid':staffid,'staffname':staffname,'desig':desig,'allowance':alllist,'deduction':dedlist,'totalall':totall,'totalded':totded,'netpay':vnet,'disdate':disdate,'comp':comp,'totalcont':staffcont,'printdate':gettime()},context_instance = RequestContext(request))

            else:

                form = payslipform()
                getdetails = ""
            return render_to_response('payroll/printpayslip.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')



def printpayslipall(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.jobsetup
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/payroll/unauto/')
            varerr =""
            getdetails =""
            caldate1 = ""
            if request.method == 'POST':
                form = payrollform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    caldate1 = form.cleaned_data['caldate']
                    staffid = ''
                    caldate2 = caldate1.split('/')
                    caldate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                    vdate = caldate
                    if tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year).exclude(allamount = 0 ).count() == 0:
                        varerr = "No Record For The Selected Month"
                        return render_to_response('payroll/printpayslipall.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
                    lh =[]
                    allstaff = staffrec.objects.filter(status = 'ACTIVE').order_by('staffid')
                    staffname =''
                    desig = ''
                    vda = ''
                    vdad = ''

                    staffcont = ''


                    getsav = tblsavingcode.objects.get(id = 1)
                    cont = getsav.name # the contribution name
                    for st in allstaff:
                        staffid = st.staffid
                        staffname = st.name.title()
                        desig = st.designation
                        pslip = {}
                        totded1 = 0
                        totall1 = 0
                        alllist = []
                        dedlist = []
                        totall = 0
                        totded = 0
                        vnet = 0
                        if tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year,staffid = staffid).exclude(allamount = 0 ).count() == 0:
                            pass
                        else:
                            vda = tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year,staffid = staffid).exclude(allamount = 0 )
                            totall = 0
                            for  jj in vda:
                               totall1 += jj.allamount
                               desc = jj.alldes
                               alamt = jj.allamount
                               getall = locale.format("%.2f",alamt,grouping=True)
                               alldic = {'alldes':desc,'allamount':getall}
                               alllist.append(alldic)
                            totall = locale.format("%.2f",totall1,grouping=True)
                               #print jj.alldes,jj.allamount
                        if tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year,staffid = staffid).exclude(dedamount = 0 ).count() == 0:
                            pass
                        else:
                            vdad = tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year,staffid = staffid).exclude(dedamount = 0 )
                            totded = 0
                            vdate = ''
                            staffname = ''
                            desig = ''
                            for  jjd in vdad:
                               totded1 += jjd.dedamount
                               desc = jjd.deddes
                               alamt = jjd.dedamount
                               outbal = jjd.outbal
                               getall = locale.format("%.2f",alamt,grouping=True)
                               outbal1 = locale.format("%.2f",outbal,grouping=True)
                               alldic = {'deddes':desc,'dedamount':getall,'outstanding':outbal1}
                               dedlist.append(alldic)
                            totded = locale.format("%.2f",totded1,grouping=True)
                            vnet1 = tblpayroll.objects.get(recmonth = caldate.month,recyear = caldate.year,staffid = staffid,schdes = 'netpay')
                            vnet2 = vnet1.schamount
                            vnet = locale.format("%.2f",vnet2,grouping=True)
                            #lh.extend(zne)grosspay
                            #getting staff contribution
                            if tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year,staffid = staffid,schdes = cont.lower()).count() == 0:
                               staffcont = ''
                            else:
                               if tblsavings.objects.filter(staffid = staffid):
                                   tsav = tblsavings.objects.get(staffid = staffid)
                                   tsat = tsav.amountbf
                                   vnet11 = tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year,staffid = staffid,schdes = cont.lower()).aggregate(Sum('schamount'))
                                   vnet12 = vnet11['schamount__sum']
                                   gtsavt = float(tsat) + float(vnet12)
                                   totalcont = locale.format("%.2f",gtsavt,grouping=True)
                                   staffcont = 'Total %s :: %s'%(cont.upper(),totalcont)
                               else:
                                   pass
                        vnet22 = totall1 -totded1
                        vnet = locale.format("%.2f",vnet22,grouping=True)

                        comp = tblcompanyinfo.objects.get(id = 1)
                        disdate = caldate.strftime('%b,%Y')
                        pslip = {'staffid':staffid,'staffname':st.name,'desig':st.designation,'allowance':alllist,'deduction':dedlist,'totalall':totall,'totalded':totded,'netpay':vnet,'disdate':disdate,'comp':comp,'totalcont':staffcont}
                        lh.append(pslip)

                    return render_to_response('payroll/payall.htm',{'varuser':varuser,'varerr':varerr,'form':form,'lh':lh,'printdate':gettime()},context_instance = RequestContext(request))
            else:
                form = payrollform()
                getdetails = ""
            return render_to_response('payroll/printpayslipall.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')



def deductionreport(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.jobsetup
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/payroll/unauto/')
            varerr =""
            getdetails =""
            caldate1 = ""
            if request.method == 'POST':
                form = dedreportform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    caldate1 = form.cleaned_data['caldate']
                    deductiontype1 = form.cleaned_data['deductiontype']
                    deductiontype = str(deductiontype1).lower()
                    caldate2 = caldate1.split('/')
                    caldate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                    staffrec = tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year,schdes = deductiontype).order_by('staffid')
                    varrid1 = tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year,schdes = deductiontype).aggregate(Sum('schamount'))
                    varrid = varrid1['schamount__sum']
                    comp = tblcompanyinfo.objects.get(id = 1)
                    if form.cleaned_data['excelfile']:
                        response = HttpResponse(mimetype="application/ms-excel")
                        response['Content-Disposition'] = 'attachment; filename=deductionreport.xls'
                        wb = xlwt.Workbook()
                        ws = wb.add_sheet('deductionreport')
                        ws.write(0, 1, comp.name)
                        ws.write(1, 1, comp.address)
                        ws.write(2, 1, '%s :: DEDUCTION REPORT for %s ' %(str(deductiontype).upper(), caldate.strftime('%b,%Y')) )
                        ws.write(2, 2, gettime() )
                        ws.write(3, 0, 'Staff Id')
                        ws.write(3, 1, 'Staff Name')
                        ws.write(3, 2, 'Deduction')
                        k = 4
                        for jd in staffrec:
                           kamt = locale.format("%.2f",jd.schamount,grouping=True)
                           ws.write(k, 0, jd.staffid)
                           ws.write(k, 1, jd.staffname.title())
                           ws.write(k, 2, kamt)
                           k += 1
                        kamt1 = locale.format("%.2f",varrid,grouping=True)
                        ws.write(k, 0, '')
                        ws.write(k, 1, 'Total')
                        ws.write(k, 2, kamt1)
                        wb.save(response)
                        return response
                    else:
                        return render_to_response('payroll/deductionreport.htm',{'varuser':varuser,'varerr':varerr,'form':form,'staffrec':staffrec,'deductiontype':deductiontype,'caldate':caldate,'varrid':varrid,'comp':comp,'printdate':gettime()},context_instance = RequestContext(request))
            else:
                form = dedreportform()
                getdetails = ""
            return render_to_response('payroll/deductionreport.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def payrolldeductionajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                kk = []
                dedlist = []
                for t in tblpayroll.objects.filter(dedamount__gt= 0).order_by('deddes'):
                     if t.deddes in dedlist:
                        pass
                     else:
                        dedlist.append(t.deddes)
                for p in dedlist:
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

def printtopension(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.jobsetup
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/payroll/unauto/')
            varerr =""
            getdetails =""
            caldate1 = ""
            stafflist =[]
            if request.method == 'POST':
                form = pensionscheduleform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    bankname = form.cleaned_data['bankname']
                    caldate1 = form.cleaned_data['caldate']
                    caldate2 = caldate1.split('/')
                    caldate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                    toall = 0
                    emptot = 0
                    #print caldate
                    # return HttpResponseRedirect('/hrm/staffedu/')
                    if tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year).count() == 0:
                        varerr = 'Payroll has not been computed for this month'
                        return render_to_response('payroll/printtopension.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))

                    if tblstaffpfa.objects.filter(hmoname = bankname) == 0 :
                        #print "No Record"
                        return HttpResponseRedirect('/hrm/payroll/computepayroll/')
                    else:
                        #print "Record exist"
                        ll = []
                        lk = ""
                        vardata = tblstaffpfa.objects.filter(hmoname = bankname).order_by('staffid')
                        #print vardata
                        npay = 0
                        cuspart =""
                        custo = 0
                        npay1  = 0
                        for j in vardata:

                            if tblpayrollpension.objects.filter(staffid = j.staffid,recmonth = caldate.month,recyear = caldate.year).count() == 0:
                                pass
                            else:
                                payda = tblpayrollpension.objects.get(staffid = j.staffid,recmonth = caldate.month,recyear = caldate.year)
                                staffrec = tblpayroll.objects.get(staffid = j.staffid,recmonth = caldate.month,recyear = caldate.year,schdes = 'pension').schamount
                                npay = payda.employeeamount
                                empyer = payda.employeramount
                                toall += staffrec
                                emptot += payda.employeramount
                                totcont = float(staffrec) + float(empyer)
                                npay = locale.format("%.2f",staffrec,grouping=True)
                                empyer1 = locale.format("%.2f",empyer,grouping=True)
                                totcont1 = locale.format("%.2f",totcont,grouping=True)
                                #print npay
                                k = {'staffid':j.staffid,'bankname':bankname,'name':j.staffname,'accno':j.accno,'netpay':npay,'empyer':empyer1,'totcont1':totcont1}
                                ll.append(k)
                    grtot = float(toall) + float(emptot)
                    toall = locale.format("%.2f",toall,grouping=True)
                    emptot = locale.format("%.2f",emptot,grouping=True)
                    grtot = locale.format("%.2f",grtot,grouping=True)
                    ka = {'totalstaff':toall,'totalcomp':emptot,'grtotal':grtot,'staffdata':ll}
                    stafflist.append(ka)
                    comp = tblcompanyinfo.objects.get(id = 1)
                    disdate = caldate.strftime('%b,%Y')
                    if form.cleaned_data['excelfile']:
                        response = HttpResponse(mimetype="application/ms-excel")
                        response['Content-Disposition'] = 'attachment; filename=salarytopension.xls'
                        wb = xlwt.Workbook()
                        ws = wb.add_sheet('pensionschedule')
                        ws.write(0, 1, comp.name)
                        ws.write(1, 1, comp.address)
                        ws.write(2, 1, disdate)
                        ws.write(2, 2, '%s:SCHEDULE' %bankname)
                        ws.write(2, 3, gettime())
                        ws.write(3, 0, 'Staff Id')
                        ws.write(3, 1, 'Staff Name')
                        ws.write(3, 2, 'Account No')
                        ws.write(3, 3, 'Employee Contribution')
                        ws.write(3, 4, 'Employer Contribution')
                        ws.write(3, 5, 'Total Contribution')
                        k = 4
                        for jd in stafflist:
                            for p in jd['staffdata']:
                               ws.write(k, 0, p['staffid'])
                               ws.write(k, 1, p['name'])
                               ws.write(k, 2, p['accno'])
                               ws.write(k, 3, p['netpay'])
                               ws.write(k, 4, p['empyer'])
                               ws.write(k, 5, p['totcont1'])
                               k += 1

                            ws.write(k, 2,'TOTAL')
                            ws.write(k, 3, jd['totalstaff'])
                            ws.write(k, 4, jd['totalcomp'])
                            ws.write(k, 5, jd['grtotal'])
                        wb.save(response)
                        return response
                    else:
                        return render_to_response('payroll/printtopension.htm',{'varuser':varuser,'varerr':varerr,'form':form,'stafflist':stafflist,'comp':comp,'disdate':disdate,'bankname':bankname,'printdate':gettime()},context_instance = RequestContext(request))

            else:

                form = pensionscheduleform()
                getdetails = ""
            return render_to_response('payroll/printtopension.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')

def getworkedday(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = staffrec.objects.get(id = acccode)
                return render_to_response('payroll/editworked.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def bankajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            #print 'welcome'
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                gdata = tblbankdetails.objects.filter(bankname = acccode).order_by('staffid')
                return render_to_response('payroll/bank.htm',{'gdata':gdata})
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

def getbank(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                bank = tblbank.objects.all().order_by('name')
                getdetails = tblbankdetails.objects.get(id = acccode)
                return render_to_response('payroll/editbank.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'bank':bank})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def printtostate(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.jobsetup
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/payroll/unauto/')
            varerr =""
            getdetails =""
            caldate1 = ""
            if request.method == 'POST':
                form = payrollscheduleform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    caldate1 = form.cleaned_data['caldate']
                    caldate2 = caldate1.split('/')
                    caldate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                    vdate = caldate
                    if tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year).exclude(allamount = 0 ).count() == 0:
                        varerr = "No Record For The Selected Month"
                        return render_to_response('payroll/printtostate.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
                    lh =[]
                    statelist = []
                    alist = []
                    staffdic = {}
                    datalist = []
                    ll = [] # template list
                    npay = 0

                    comp = tblcompanyinfo.objects.get(id = 1)
                    allstaff = staffrec.objects.filter(status = 'ACTIVE').order_by('staffid')
                    for p in allstaff:
                        jdic = {p.profession:p.profession}
                        staffdic.update(jdic)
                        #print staffdic
                    statelist.append(staffdic.values())

                    for b in statelist:
                        for h in b:
                            alist.append(h)
                    for m in alist:

                        datalist = []
                        tot = 0
                        getstaff = staffrec.objects.filter(status = 'ACTIVE',profession = m).order_by('staffid')
                        for d in getstaff:
                            if tblpayroll.objects.filter(staffid = d.staffid,schdes__contains = 'tax',recmonth = caldate.month,recyear = caldate.year).count() == 0:
                                npay = 0
                            else:
                                payda = tblpayroll.objects.filter(staffid = d.staffid,schdes__contains = 'tax',recmonth = caldate.month,recyear = caldate.year)
                                for jk in payda:
                                   npay = jk.schamount
                            tot = float(tot) + float(npay)
                            npay1 = locale.format("%.2f",npay,grouping=True)

                            datadic = {'staffid':d.staffid,'staffname':d.name,'amount':npay1}
                            datalist.append(datadic)
                        tot1 = locale.format("%.2f",tot,grouping=True)
                        lldic = {'state':m,'statedata':datalist,'statetotal':tot1}
                        ll.append(lldic)
                    disdate = caldate.strftime('%b,%Y')
                    if form.cleaned_data['excelfile']:
                            response = HttpResponse(mimetype="application/ms-excel")
                            response['Content-Disposition'] = 'attachment; filename=taxtostate.xls'
                            wb = xlwt.Workbook()
                            ws = wb.add_sheet('taxtostate')
                            ws.write(0, 1, comp.name)
                            ws.write(1, 1, comp.address)
                            ws.write(2, 1, disdate)
                            ws.write(2, 2, 'TAX SCHEDULE')
                            ws.write(2, 3, gettime())
                            k = 3
                            for jd in ll:
                                ws.write(k, 0, jd['state'])
                                k += 1
                                ws.write(k, 1, 'Staff Id')
                                ws.write(k, 2, 'Staff Name')
                                ws.write(k, 3, 'Amount')
                                k += 1
                                for p in jd['statedata']:
                                    ws.write(k, 1, p['staffid'])
                                    ws.write(k, 2, p['staffname'])
                                    ws.write(k, 3, p['amount'])
                                    k += 1

                                ws.write(k, 2,'TOTAL')
                                ws.write(k, 3, jd['statetotal'])
                                k += 1
                            wb.save(response)
                            return response
                    else:
                            return render_to_response('payroll/printtostate.htm',{'varuser':varuser,'varerr':varerr,'form':form,'ll':ll,'vdate':vdate,'comp':comp,'printdate':gettime()},context_instance = RequestContext(request))


            else:
                form = payrollscheduleform()
                getdetails = ""
            return render_to_response('payroll/printtostate.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')



def printloanschedule(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.jobsetup
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/payroll/unauto/')
            varerr =""
            getdetails =""
            caldate1 = ""
            if request.method == 'POST':
                form = loanform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    caldate1 = form.cleaned_data['caldate']#bankname
                    bankname = form.cleaned_data['bankname']#bankname
                    caldate2 = caldate1.split('/')
                    caldate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                    vdate = caldate
                    if tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year).exclude(allamount = 0 ).count() == 0:
                        varerr = "No Record For The Selected Month"
                        return render_to_response('payroll/printloanschedule.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))

                    datalist = []
                    ll = [] # template list
                    comp = tblcompanyinfo.objects.get(id = 1)
                    tpamt = 0 #total principal Amount
                    tintamt = 0 # total int amount
                    ttpay = 0 # for total payable
                    tmon  = 0 # for total
                    tpayd = 0 # for total pay todate
                    toutbal = 0 # for total outstanding balance
                    getstaff = tblloan.objects.filter(paydes = bankname).order_by('staffid')
                    for d in getstaff:
                            nob = tblpayroll.objects.filter(staffid = d.staffid,schdes = bankname.lower(),recdate__gte = d.effectivedate).count() #number of occurence
                            tperiod = d.duration #duration
                            priamt = d.amount#principal Amount
                            intrate = d.intrate#interest rate
                            monrepay = d.monthlyepayment#monthly repayment
                            calint = float(intrate)/100
                            intamt = calint *float(priamt) # interest amount
                           # print 'Interest amount ',intamt,intrate,priamt,calint
                            tpayable = intamt + float(priamt) #totalm payable

                            tpay = nob * monrepay # total pay till date
                            outbal = tpayable - float(tpay) # outstanding balance
                            priamt1 = locale.format("%.2f",priamt,grouping=True)
                            monrepay1 = locale.format("%.2f",monrepay,grouping=True)
                            intamt1 = locale.format("%.2f",intamt,grouping=True)
                            tpayable1 = locale.format("%.2f",tpayable,grouping=True)
                            tpay1 = locale.format("%.2f",tpay,grouping=True)
                            outbal1 = locale.format("%.2f",outbal,grouping=True)

                            tpamt = tpamt + priamt
                            tintamt =  tintamt + intamt
                            ttpay = ttpay + tpayable
                            tmon = tmon + monrepay
                            tpayd = tpayd + tpay
                            toutbal = toutbal + outbal
                           #print d.staffname

                            datadic = {'staffid':d.staffid,'staffname':d.staffname,'totalperiod':tperiod,'outperiod':tperiod - nob,'pricipalamt':priamt1,'intrate':intrate,'intamt':intamt1,'totalpayable':tpayable1,'monthlyrep':monrepay1,'totalpaid':tpay1,'outbal':outbal1}
                            datalist.append(datadic)
                    tot1 = 0# locale.format("%.2f",tot,grouping=True)
                    tpamt = locale.format("%.2f",tpamt,grouping=True)
                    tintamt = locale.format("%.2f",tintamt,grouping=True)
                    ttpay = locale.format("%.2f",ttpay,grouping=True)
                    tmon = locale.format("%.2f",tmon,grouping=True)
                    tpayd = locale.format("%.2f",tpayd,grouping=True)
                    toutbal = locale.format("%.2f",toutbal,grouping=True)

                    lldic = {'statedata':datalist,'tpamt':tpamt,'tintamt':tintamt,'ttpay':ttpay,'tmon':tmon,'tpayd':tpayd,'toutbal':toutbal}
                    ll.append(lldic)
                    return render_to_response('payroll/printloanschedule.htm',{'varuser':varuser,'varerr':varerr,'form':form,'ll':ll,'vdate':vdate,'comp':comp,'state':bankname,'printdate':gettime()},context_instance = RequestContext(request))
            else:
                form = loanform()
                getdetails = ""
            return render_to_response('payroll/printloanschedule.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


def printsavings(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.jobsetup
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/payroll/unauto/')
            varerr =""
            getdetails =""
            caldate1 = ""
            if request.method == 'POST':
                form = payrollform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    caldate1 = form.cleaned_data['caldate']
                    caldate2 = caldate1.split('/')
                    caldate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                    vdate = caldate
                    if tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year).exclude(allamount = 0 ).count() == 0:
                        varerr = "No Record For The Selected Month"
                        return render_to_response('payroll/printsavings.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))

                    getsav = tblsavingcode.objects.get(id = 1)
                    cont = getsav.name # the contribution name
                    datalist = []
                    ll = [] # template list
                    comp = tblcompanyinfo.objects.get(id = 1)
                    tsavings = 0 # for total pay todate
                    tbalance = 0 # for total outstanding balance
                    getstaff = tblsavings.objects.all().order_by('staffid')
                    for d in getstaff:
                        if tblpayroll.objects.filter(staffid = d.staffid,schdes = cont.lower()).count() == 0:
                            tcont = 0
                        else:
                            nob = tblpayroll.objects.filter(staffid = d.staffid,schdes = cont.lower()).aggregate(Sum('schamount')) #total savings
                            tcont = nob['schamount__sum']
                        balb4 = d.amountbf #savings b4
                        moncont1 = d.contribution#Monthly Contribution
                        totalbal1 = float(balb4) + float(tcont) # total contribution tilldate
                        tsavings = tsavings + moncont1 #total monthly savings
                        tbalance = tbalance + totalbal1 # total balance
                        moncont = locale.format("%.2f",moncont1,grouping=True)
                        totalbal = locale.format("%.2f",totalbal1,grouping=True)
                        datadic = {'staffid':d.staffid,'staffname':d.staffname,'moncont':moncont,'totalbal':totalbal}
                        datalist.append(datadic)

                    tsavings1 = locale.format("%.2f",tsavings,grouping=True)
                    tbalance1 = locale.format("%.2f",tbalance,grouping=True)

                    lldic = {'statedata':datalist,'tsavings1':tsavings1,'tbalance1':tbalance1}
                    ll.append(lldic)
                    cname = cont.upper() + ' SAVINGS '
                    return render_to_response('payroll/printsavings.htm',{'varuser':varuser,'varerr':varerr,'form':form,'ll':ll,'vdate':vdate,'comp':comp,'cname':cname,'printdate':gettime()},context_instance = RequestContext(request))
            else:
                form = payrollform()
                getdetails = ""
            return render_to_response('payroll/printsavings.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def monthlyjournal(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.jobsetup
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/payroll/unauto/')
            varerr =""
            getdetails =""
            caldate1 = ""
            if request.method == 'POST':
                form = monthlyjournalform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    department = form.cleaned_data['department']
                    caldate1 = form.cleaned_data['caldate']
                    caldate2 = caldate1.split('/')
                    caldate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                    vdate = caldate
                    ll = [] # template list
                    disp = ''
                    comp = tblcompanyinfo.objects.get(id = 1)
                    if tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year).exclude(allamount = 0 ).count() == 0:
                        varerr = "No Record For The Selected Month"
                        return render_to_response('payroll/monthlyjournal.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
                    vrdic = {}
                    vrdicd = {}
                    vda = tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year).exclude(allamount = 0 )
                    for  jj in vda:
                        vdic ={jj.alldes:0}
                        vrdic.update(vdic)
                    alllist = vrdic.keys()
                    alllist.sort()

                    vdad = tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year).exclude(dedamount = 0 )
                    for  jjd in vdad:
                        vdicd ={jjd.deddes:0}
                        vrdicd.update(vdicd)
                    dedlist = vrdicd.keys()
                    dedlist.sort()
                    np = ['netpay']
                    dedlist.extend(np)
                    #print 'Ded list :',dedlist
                    vsal = 0
                    vsal1 = 0
                    lsal = {}
                    replist = []
                    totsum = 0
                    for j in alllist:
                        totsal = 0
                        if form.cleaned_data['excelfile']:
                            vardata = staffrec.objects.filter(department = department)
                            for k in vardata:
                                if tblpayroll.objects.filter(staffid = k.staffid,schdes = j,recmonth = caldate.month,recyear = caldate.year).count() == 0:
                                   vsal = 0
                                else:
                                    payda = tblpayroll.objects.filter(staffid = k.staffid,schdes = j,recmonth = caldate.month,recyear = caldate.year)
                                    for jk in payda:
                                        vsal = jk.schamount
                                totsal = totsal + vsal
                        else:
                            varrid1 = tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year,schdes = j).aggregate(Sum('schamount'))
                            totsal = varrid1['schamount__sum']
                        totsal1 = locale.format("%.2f",totsal,grouping=True)
                        redic = {'all':j.title(), 'debit':totsal1,'credit':''}
                        replist.append(redic)
                        totsum = totsum + totsal
                    totpen = 0
                    for j in dedlist:
                        print 'The Pension Issue :',j
                        totsal = 0
                        if form.cleaned_data['excelfile']:
                            disp = "%s Department Payroll Journal For The Month Of %s "%(department.upper(),vdate.strftime("%b,%Y"))
                            vardata = staffrec.objects.filter(department = department)
                            for k in vardata:
                                if tblpayroll.objects.filter(staffid = k.staffid,schdes = j,recmonth = caldate.month,recyear = caldate.year).count() == 0:
                                    vsal = 0
                                else:
                                    payda = tblpayroll.objects.filter(staffid = k.staffid,schdes = j,recmonth = caldate.month,recyear = caldate.year)
                                    for jk in payda:
                                        vsal = jk.schamount
                                totsal = totsal + vsal
                                if j == 'pension':
                                   if tblpayrollpension.objects.filter(staffid = k.staffid,recmonth = caldate.month,recyear = caldate.year).count() == 0:
                                       pass
                                   else:
                                       payemp = tblpayrollpension.objects.get(staffid = k.staffid,recmonth = caldate.month,recyear = caldate.year)
                                       totpen = totpen + payemp.employeramount
                            if j == 'pension':
                                totpen1 = locale.format("%.2f",totpen,grouping=True)
                                redic = {'all':'Employer Pension Contribution', 'credit':'','debit':totpen1}
                                replist.append(redic)
                                redic1 = {'all':'Employer Pension Contribution', 'credit':totpen1,'debit':''}
                                replist.append(redic1)
                        else:
                            disp = "Payroll Journal For The Month Of %s "%vdate.strftime("%b,%Y")
                            varrid1 = tblpayroll.objects.filter(recmonth = caldate.month,recyear = caldate.year,schdes = j).aggregate(Sum('schamount'))
                            totsal = varrid1['schamount__sum']
                            if j == 'pension':
                                payemp = tblpayrollpension.objects.filter(recmonth = caldate.month,recyear = caldate.year).aggregate(Sum('employeramount'))
                                totpen = payemp['employeramount__sum']
                                totpen1 = locale.format("%.2f",totpen,grouping=True)
                                redic = {'all':'Employer Pension Contribution', 'credit':'','debit':totpen1}
                                replist.append(redic)
                                redic1 = {'all':'Employer Pension Contribution', 'credit':totpen1,'debit':''}
                                replist.append(redic1)
                        totsal1 = locale.format("%.2f",totsal,grouping=True)
                        redic = {'all':j.title(), 'credit':totsal1,'debit':''}
                        replist.append(redic)
                    totsum = totsum + totpen
                    totsum1 = locale.format("%.2f",totsum,grouping=True)
                    fdic = {'total':totsum1,'staffdata':replist}
                    ll.append(fdic)
                    prepareby = 'Prepared by__________________________Sign & Date___________ '
                    checkedby = 'Checked by__________________________Sign & Date___________ '
                    approvedby = 'Approved by__________________________Sign & Date__________ '
                    return render_to_response('payroll/monthlyjournal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'ll':ll,'disp':disp,'comp':comp,'printdate':gettime(),'prepareby':prepareby,'checkedby':checkedby,'approvedby':approvedby,'sn':'S/N','desc':'Description','deb':'Debit','cred':'Credit'},context_instance = RequestContext(request))
            else:
                form = monthlyjournalform()
                getdetails = ""
            return render_to_response('payroll/monthlyjournal.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')



