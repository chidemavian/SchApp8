# Create your views here.
from django.template import loader, Context,RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import  HttpResponseRedirect
from myproject.ruffwal.raccount.form import useraccform
from myproject.ruffwal.posting.form import *
from myproject.ruffwal.rwadmin.models import *
from myproject.ruffwal.rsetup.models import *
from myproject.ruffwal.rwadmin.models import *
from myproject.ruffwal.posting.models import *
from myproject.ruffwal.posting.postbill import *
from myproject.utilities.views import *
from myproject.bill.models import *
from myproject.student.models import *
from django.db.models import Max,Sum
from myproject.ruffwal.posting.fig2wd import *
import datetime
from datetime import date,time
from django.core.serializers.json import simplejson as json
import locale
locale.setlocale(locale.LC_ALL,'')


def wels(request):
    if "userid" in request.session:
        return render_to_response('posting/invoice.html')
    else:
        return HttpResponseRedirect('/login/')

def enterposting(request):
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.eposting
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/welcome/')
        varerr =""
        return render_to_response('posting/enterposting.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')

def invoice(request):
       varerr ='ABOVE ALL LORD JESUS'
     #if  "userid" in request.session:

       if  "userid" in request.session:

        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.invoice
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/posting/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = invoiceformsc(request.POST) # A form bound to the POST data
          if form.is_valid():
             bill_list = []
             session = form.cleaned_data['session']
             klass = form.cleaned_data['klass'] #customer code
             term = form.cleaned_data['term']
             if postedbill.objects.filter(session = session,klass = klass,term = term):
                 varerr = 'The Bill for this Class has already Been Posted'
                 return render_to_response('posting/invoice.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             studata = Student.objects.filter(admitted_class = klass,admitted_session = session,gone = False).order_by('admissionno')
             totbill = 0
             for st in studata:
                 billlist = []
                 if tblbill.objects.filter(klass = klass,term = term,dayboarding = st.dayboarding).count() == 0:
                     varrid = 0
                 else:
                     getbill = tblbill.objects.filter(klass = klass,term = term,dayboarding = st.dayboarding)
                     varrid1 = tblbill.objects.filter(klass = klass,term = term,dayboarding = st.dayboarding).aggregate(Sum('billamount'))
                     varrid = varrid1['billamount__sum']
                     for j in getbill:
                         billdic = {'desc':j.desc,'billamount':locale.format("%.2f",j.billamount,grouping=True)}
                         #print billdic
                         billlist.append(billdic)
                 if tbladditionalbill.objects.filter(session = session,admissionno = st.admissionno,klass = klass,term = term).count() == 0:
                     varrid2 = 0
                     getaddbill = ''
                 else:
                     getaddbill = tbladditionalbill.objects.filter(session = session,admissionno = st.admissionno,klass = klass,term = term)
                     varrid11 = tbladditionalbill.objects.filter(session = session,admissionno = st.admissionno,klass = klass,term = term).aggregate(Sum('billamount'))
                     varrid2 = varrid11['billamount__sum']
                     for h in getaddbill:
                         billdic = {'desc':h.desc,'billamount':locale.format("%.2f",h.billamount,grouping=True)}
                         billlist.append(billdic)
                     #print 'additional bill',varrid2
                 varrid = varrid + varrid2
                 totbill += varrid
                 billdic = {'admno':st.admissionno,'name':st.fullname,'bill':billlist,'totalbill':locale.format("%.2f",varrid,grouping=True)}
                 bill_list.append(billdic)
             #now i do insertion
             return render_to_response('posting/postbill.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':bill_list,'term':term,'klass':klass,'session':session,'total':locale.format("%.2f",totbill,grouping=True)},context_instance = RequestContext(request))
        else:

            form = invoiceformsc()
           # getdetails = tbltemp.objects.filter(userid = varuser).order_by('transdate')
        return render_to_response('posting/invoice.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

       else:
        return HttpResponseRedirect('/login/')

def editinvoice(request,invid):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.invoice
            if int(uenter) == 0 :
              return HttpResponseRedirect('/SchApp/account/posting/unauto/')
            varerr =""
            if request.method == 'POST':
                getdetails = ""
                amount = request.POST['accname'] # the amount
                accno = request.POST['hcode']#the primary key
                particular = request.POST['acccode']#the particulars
                transdate = request.POST['subname'] #the transdate
                invoiceno = request.POST['grpname'] #the invoice
                particular = particular
                if particular == "" or invoiceno == "" or amount == "" or transdate == "":
                    #varerr = "INVALID TRANSACTION"
                    #getdetails = tbltemp.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    #return render_to_response('posting/editinvoice.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                    return HttpResponseRedirect('/SchApp/account/posting/invoice/')

                try:
                    k = float(amount)
                except:
                    #varerr = "INVALID AMOUNT"
                    #getdetails = tbltemp.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    #return render_to_response('posting/editinvoice.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                    return HttpResponseRedirect('/SchApp/account/posting/invoice/')

                #***********GETTING THE DATE
                vyear = str(transdate)
                vk = vyear[0:4]
                if vk.isdigit() == True :
                    #print 'digit value'
                    vdate = date(int(vyear[0:4]),int(vyear[5:7]),int(vyear[8:10]))
                else:
                    #print 'not digit'
                    vdate = date(int(vyear[6:10]),int(vyear[0:2]),int(vyear[3:5]))
                #*888888888888888888888888888888888888888 checking the date
                if tblcalender.objects.all().count() == 0:
                     #varerr = "NO START DATE"
                     #getdetails = tbltemp.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                     #return render_to_response('posting/editinvoice.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                     return HttpResponseRedirect('/SchApp/account/posting/invoice/')
                stdate = datetime.datetime.today()
                endate = datetime.datetime.today()
                getdate = tblcalender.objects.all()
                for g in getdate:
                   stdate = g.startmonth
                   endate = g.endtmonth
                if vdate < stdate or vdate > endate :
                   #varerr = "INVALID DATE"
                   #getdetails = tbltemp.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                   #return render_to_response('posting/editinvoice.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                   return HttpResponseRedirect('/SchApp/account/posting/invoice/')
                #********************
                seldata = tbltemp.objects.get(id = accno)
                seldata.amount = amount
                seldata.particular = particular
                seldata.transdate = vdate

                seldata.invoiceno = invoiceno
                seldata.save()
                return HttpResponseRedirect('/SchApp/account/posting/invoice/')
            else:
                try:
                  getdetails = tbltemp.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                  return render_to_response('posting/editinvoice.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                except:
                    varerr = "Account Not Exist"
                    return render_to_response('posting/editinvoice.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
        else:
         return HttpResponseRedirect('/login/')

def deleteinvoice(request,invid):
    varerr =""
    if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            #if request.method == 'POST':

            #accno = request.POST['hcode']#the primary key

            seldata = tbltemp.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/SchApp/account/posting/invoice/')
            #else:
             #   return HttpResponseRedirect('/posting/invoice/')


    else:
      return HttpResponseRedirect('/login/')

def testajax(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   #gdata = tblaccount.objects.all()
                   gdata = tblaccount.objects.filter(acccode__startswith = acccode,groupname = "CURRENT ASSETS",subgroupname ="RECEIVABLES").exclude(accname = "TRADE-DEBTORS").order_by('acccode')

                   return render_to_response('posting/testajax.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = ""
                   return render_to_response('posting/testajax.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('posting/testajax.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')


def testajaxcode(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   gdata = tblaccount.objects.filter(acccode__startswith = acccode).exclude(groupname = "CURRENT ASSETS",subgroupname ="RECEIVABLES").order_by('acccode')
                   #gdata = tblaccount.objects.filter(acccode__startswith = acccode,groupname = "CURRENT ASSETS",subgroupname ="RECEIVABLES").exclude(accname = "TRADE-DEBTORS")

                   return render_to_response('posting/testajax.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = ""
                   return render_to_response('posting/testajax.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('posting/testajax.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')




def process(request):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            cusno = ''
            varyear = ''
            cusname = ''
            vardate = datetime.datetime.today()
            if tbltemp.objects.filter(userid = varuser).count() == 0 :
                return HttpResponseRedirect('/SchApp/account/posting/invoice/')
            else:
                ll = []
                lk = ""
                vardata = tbltemp.objects.filter(userid = varuser)
                cuspart =""
                custo = 0
                for j in vardata:
                    lk = j.accname,j.acccode,j.particular,j.amount,j.id
                    ll.append(lk)
                    custo = custo + j.amount
                    cuspart =cuspart + j.particular + ","
                    cusno = j.cuscode
                    cusname = j.cusname
                    refno = j.invoiceno
                    vardate = j.transdate
                    varyear = vardate.year
                    userid = j.userid
                #**************************************************************getting transid
                kt = gettransid(varyear)
                if tbltransactiontemp.objects.filter(transdate__year = varyear).count() == 0 :
                    varrid = 1
                else:
                    varrid1 = tbltransactiontemp.objects.filter(transdate__year = varyear).aggregate(Max('recid'))
                    varrid = varrid1['recid__max']
                    varrid = int(varrid)
                if kt > varrid:
                    varrid =  kt + 1
                else:
                    varrid  += 1
                vyear =  str(varyear)
                vayear = vyear[2]+ vyear[3]
                vartransid = str(vayear) + str(varrid) #trans id
                varrecid = int(varrid)
                #**************************************************************************
                cusdet =  tblaccount.objects.get(acccode = cusno)
                cusbal = cusdet.accbal
                cusgrp = cusdet.groupname
                cussub = cusdet.subgroupname
                if cusgrp == "FIXED ASSETS" or cusgrp == "CURRENT ASSETS" or cusgrp == "EXPENSES" or cusgrp == "COST OF SALES":
                    cusbal = cusbal + custo
                else:
                    cusbal = cusbal - custo
               #***********************************************
                used = tbltransaction(accname = cusname,acccode = cusno,debit = custo,credit = 0,balance = cusbal,transid = vartransid,transdate = vardate,particulars = cuspart,refno = refno,groupname = cusgrp,subname = cussub ,userid = userid,recid = varrecid )
                used.save()
                #********************
                selsubdata = tblaccount.objects.get(acccode = cusno)
                selsubdata.accbal = cusbal #
                selsubdata.lasttrandate = vardate
                selsubdata.save()
                #**********************************
                k = range(len(ll))

                we =[]

                for h in k:

                  for m in ll[h]:
                     we.append(m)
                  accname = we[0]
                  acccode = we[1]
                  part = we[2]
                  amount = we[3]
                  rid = we[4]

                  #***************************************
                  cusdet1 =  tblaccount.objects.get(acccode = acccode)
                  bal = cusdet1.accbal
                  grp = cusdet1.groupname
                  sub = cusdet1.subgroupname
                  if grp == "FIXED ASSETS" or grp == "CURRENT ASSETS" or grp == "EXPENSES" or grp == "COST OF SALES":
                       cusbal1 = bal - amount
                  else:
                       cusbal1 = bal + amount

                      #***********************************************8
                  used = tbltransaction(accname = accname,acccode = acccode,debit = 0,credit = amount,balance = cusbal1,transid = vartransid,transdate = vardate,particulars = part,refno = refno,groupname = grp,subname = sub ,userid = userid, recid = varrecid )
                  used.save()
                    #********************update
                  selsubdata1 = tblaccount.objects.get(acccode = acccode)
                  selsubdata1.accbal = cusbal1
                  selsubdata1.lasttrandate = vardate
                  selsubdata1.save()
                  we.remove(accname)
                  we.remove(acccode)
                  we.remove(part)
                  we.remove(amount)
                  we.remove(rid)
                  tbltemp.objects.filter(userid = varuser).delete()

                return render_to_response('posting/invsuccess.htm',{'varuser':varuser,'varerr':varerr,'vartransid':vartransid})

        else:
         return HttpResponseRedirect('/login/')

def receipt(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.receipt
        if int(uenter) == 0 :
              return HttpResponseRedirect('/SchApp/account/posting/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = invoiceform(request.POST) # A form bound to the POST data
          if form.is_valid():
             cusname = form.cleaned_data['cusname']
             cuscode = form.cleaned_data['cuscode'] #customer code
             amount = form.cleaned_data['transamount']
             particular = form.cleaned_data['particulars']
             caldate1 = form.cleaned_data['transdate']#date picked
             acccode = form.cleaned_data['acccode']
             accname = form.cleaned_data['accname']
             invoiceno = form.cleaned_data['invoiceno']
             caldate2 = caldate1.split('/')
             transdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
             varget = tbltempreceipt.objects.filter(userid = varuser).count()
             #**********************************************************getting the date
             if tblcalender.objects.all().count() == 0:
                 varerr = "NO START DATE"
                 getdetails = tbltempreceipt.objects.filter(userid = varuser).order_by('id')
                 return render_to_response('posting/receipt.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

             getdate = tblcalender.objects.all()
             stdate = date.today()
             endate = date.today()
             for g in getdate:
                 stdate = g.startmonth
                 endate = g.endtmonth
             if transdate < stdate or transdate > endate :
                 varerr = "INVALID DATE"
                 getdetails = tbltempreceipt.objects.filter(userid = varuser).order_by('id')
                 return render_to_response('posting/receipt.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             #*************************************************************************
             ks = tblcontrol.objects.all()
             for p in ks:
                 s = p.acccode
                 if cuscode == s:
                    varerr = "YOU CAN NOT POST INTO ONE OF THIS ACCOUNT"
                    getdetails = tbltempreceipt.objects.filter(userid = varuser).order_by('id')
                    return render_to_response('posting/receipt.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                 if acccode == s:
                    varerr = "YOU CAN NOT POST INTO ONE OF THIS ACCOUNT"
                    getdetails = tbltempreceipt.objects.filter(userid = varuser).order_by('id')
                    return render_to_response('posting/receipt.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

             #************************************************************
             if varget == 0 :
                used = tbltempreceipt(cusname = cusname,cuscode = cuscode,amount = amount,particular = particular,transdate = transdate,accname = accname,acccode = acccode,userid = varuser,drcr = "CR",invoiceno = invoiceno )
                used.save()
             else:
                 varerr = "Invalid Receipt Transaction"
                 getdetails = tbltempreceipt.objects.filter(userid = varuser).order_by('id')
                 return render_to_response('posting/receipt.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

                    #vargetnew = tbltempreceipt.objects.filter(cuscode=cuscode).count()
                    #if vargetnew == 0:

                    ##   used = tbltempreceipt(cusname = cusname,cuscode = cuscode,amount = amount,particular = particular,transdate = transdate,accname = accname,acccode = acccode,userid = varuser,drcr = "CR",invoiceno = invoiceno )
                      #  used.save()
                       # return HttpResponseRedirect('/posting/receipt/')
             #*****************************
             getdetails = tbltempreceipt.objects.filter(userid = varuser).order_by('id')
             #now i do insertion
             return HttpResponseRedirect('/SchApp/account/posting/receipt/')
             #return render_to_response('posting/receipt.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = invoiceform()
            getdetails = tbltempreceipt.objects.filter(userid = varuser).order_by('transdate')
        return render_to_response('posting/receipt.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')

def receiptprocess(request):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            vardate = datetime.date.today()
            if tbltempreceipt.objects.filter(userid = varuser).count() == 0 :
                return HttpResponseRedirect('/SchApp/account/posting/receipt/')
            else:
                ll = []
                lk = ""
                vardata = tbltempreceipt.objects.filter(userid = varuser)
                cuspart =""
                custo = 0
                cusname = ''
                cusno = ''
                amount = 0
                figwd = ''
                varyear = date.today().year
                for j in vardata:
                    lk = j.accname,j.acccode,j.particular,j.amount,j.id
                    ll.append(lk)
                    custo = custo + j.amount
                    cuspart = str(cuspart) + str(j.particular)
                    cusno = j.cuscode
                    cusname = j.cusname
                    refno = j.invoiceno
                    vardate = j.transdate
                    varyear = vardate.year
                    userid = j.userid
                #**************************************************************getting transid

                kt = gettransid(varyear)
                if tbltransactiontemp.objects.filter(transdate__year = varyear).count() == 0 :
                    varrid = 1
                else:
                    varrid1 = tbltransactiontemp.objects.filter(transdate__year = varyear).aggregate(Max('recid'))
                    varrid = varrid1['recid__max']
                    varrid = int(varrid)
                if kt > varrid:
                    varrid =  kt + 1
                else:
                    varrid  += 1
                vyear =  str(varyear)
                vayear = vyear[2]+ vyear[3]
                vartransid = str(vayear)+ str(varrid) #trans id
                varrecid = int(varrid)
                #**************************************************************************
                cusdet =  tblaccount.objects.get(acccode = cusno)
                cusbal = cusdet.accbal
                cusgrp = cusdet.groupname
                cussub = cusdet.subgroupname
                if cusgrp == "FIXED ASSETS" or cusgrp == "CURRENT ASSETS" or cusgrp == "EXPENSES" or cusgrp == "COST OF SALES":
                    cusbal = cusbal - custo
                else:
                    cusbal = cusbal + custo
               #***********************************************
                used = tbltransaction(accname = cusname,acccode = cusno,debit = 0,credit = custo,balance = cusbal,transid = vartransid,transdate = vardate,particulars = cuspart,refno = refno,groupname = cusgrp,subname = cussub ,userid = userid,recid = varrecid )
                used.save()
                #********************
                selsubdata = tblaccount.objects.get(acccode = cusno)
                selsubdata.accbal = cusbal
                selsubdata.lasttrandate = vardate
                selsubdata.save()
                #**********************************
                k = range(len(ll))
                we =[]

                for h in k:

                  for m in ll[h]:
                     we.append(m)
                  accname = we[0]
                  acccode = we[1]
                  part = we[2]
                  amount = we[3]
                  rid = we[4]

                  #***************************************
                  cusdet1 =  tblaccount.objects.get(acccode = acccode)
                  bal = cusdet1.accbal
                  grp = cusdet1.groupname
                  sub = cusdet1.subgroupname
                  if grp == "FIXED ASSETS" or grp == "CURRENT ASSETS" or grp == "EXPENSES" or grp == "COST OF SALES":
                       cusbal1 = bal + amount
                  else:
                       cusbal1 = bal - amount
                      #***********************************************8
                  used = tbltransaction(accname = accname,acccode = acccode,debit = amount,credit = 0,balance = cusbal1,transid = vartransid,transdate = vardate,particulars = part,refno = refno,groupname = grp,subname = sub ,userid = userid, recid = varrecid )
                  used.save()
                  # here i convert figure into words
                  #print 'the Amount :',amount
                  new = locale.format("%.2f",float(amount),grouping=True)
                  k1 = new.replace(',','')
                  figwd = main(k1)
                  #********************update
                  selsubdata1 = tblaccount.objects.get(acccode = acccode)
                  selsubdata1.accbal = cusbal1
                  selsubdata1.lasttrandate = vardate
                  selsubdata1.save()
                  we.remove(accname)
                  we.remove(acccode)
                  we.remove(part)
                  we.remove(amount)
                  we.remove(rid)
                  tbltempreceipt.objects.filter(userid = varuser).delete()
                comp = tblcompanyinfo.objects.get(id = 1)
                return render_to_response('posting/printreceipt.htm',{'varuser':varuser,'varerr':varerr,'vartransid':vartransid,'amount':new,'fig2wd':figwd,'vdate':vardate.strftime("%d-%m-%Y"),'particulars':cuspart,'cusname':cusname,'school':comp,'refno':refno})
                #return render_to_response('posting/invsuccess.htm',{'varuser':varuser,'varerr':varerr,'vartransid':vartransid})
        else:
         return HttpResponseRedirect('/login/')

def payment(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.payment
        if int(uenter) == 0 :
              return HttpResponseRedirect('/SchApp/account/posting/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = invoiceform(request.POST) # A form bound to the POST data
          if form.is_valid():
             cusname = form.cleaned_data['cusname']
             cuscode = form.cleaned_data['cuscode'] #customer code
             amount = form.cleaned_data['transamount']
             particular = form.cleaned_data['particulars']
             caldate1 = form.cleaned_data['transdate']#date picked
             acccode = form.cleaned_data['acccode']
             accname = form.cleaned_data['accname']
             invoiceno = form.cleaned_data['invoiceno']
             caldate2 = caldate1.split('/')
             transdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
             varget = tbltemppayment.objects.filter(userid = varuser).count()
             #********************************************************
             if tblcalender.objects.all().count() == 0:
                 varerr = "NO START DATE"
                 getdetails = tbltemppayment.objects.filter(userid = varuser).order_by('id')
                 return render_to_response('posting/payment.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

             getdate = tblcalender.objects.all()
             stdate = date.today()
             endate = date.today()
             for g in getdate:
                 stdate = g.startmonth
                 endate = g.endtmonth
             if transdate < stdate or transdate > endate :
                 varerr = "INVALID DATE"
                 getdetails = tbltemppayment.objects.filter(userid = varuser).order_by('id')
                 return render_to_response('posting/payment.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

             #*************************************************************
             ks = tblcontrol.objects.all()
             for p in ks:
                 s = p.acccode
                 if cuscode == s:
                    varerr = "YOU CAN NOT POST INTO ONE OF THIS ACCOUNT"
                    getdetails = tbltemppayment.objects.filter(userid = varuser).order_by('id')
                    return render_to_response('posting/payment.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                 if acccode == s:
                    varerr = "YOU CAN NOT POST INTO ONE OF THIS ACCOUNT"
                    getdetails = tbltemppayment.objects.filter(userid = varuser).order_by('id')
                    return render_to_response('posting/payment.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             #**************************************************************

             if varget == 0 :
                used = tbltemppayment(cusname = cusname,cuscode = cuscode,amount = amount,particular = particular,transdate = transdate,accname = accname,acccode = acccode,userid = varuser,drcr = "CR",invoiceno = invoiceno )
                used.save()
             else:
                    vargetnew = tbltemppayment.objects.filter(cuscode=cuscode).count()
                    if vargetnew == 0:
                        varerr = "Invalid Payment Transaction"
                        getdetails = tbltemppayment.objects.filter(userid = varuser).order_by('id')
                        return render_to_response('posting/payment.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                    else:
                        used = tbltemppayment(cusname = cusname,cuscode = cuscode,amount = amount,particular = particular,transdate = transdate,accname = accname,acccode = acccode,userid = varuser,drcr = "CR",invoiceno = invoiceno )
                        used.save()
                        #return HttpResponseRedirect('/posting/payment/')
             #*****************************
             getdetails = tbltemppayment.objects.filter(userid = varuser).order_by('id')
             return HttpResponseRedirect('/SchApp/account/posting/payment/')
             #now i do insertion
             #return render_to_response('posting/payment.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:

            form = invoiceform()
            getdetails = tbltemppayment.objects.filter(userid = varuser).order_by('transdate')
        return render_to_response('posting/payment.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')

def paymentajax(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   gdata = tblaccount.objects.filter(acccode__startswith = acccode,groupname = "CURRENT ASSETS",subgroupname ="CASH-AND-BANK-BALANCES").order_by('acccode')
                   return render_to_response('posting/testajax.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = ""
                   return render_to_response('posting/testajax.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('posting/testajax.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def paymentajaxcode(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   gdata = tblaccount.objects.filter(acccode__startswith = acccode).order_by('acccode')#filter(acccode__startswith = acccode,groupname = "CURRENT ASSETS",subgroupname ="CASH AND BANK BALANCES").order_by('acccode')
                   return render_to_response('posting/testajax.htm',{'gdata':gdata,'post':post})
             else:
                   gdata = tblaccount.objects.all()
                   #gdata = ""
                   return render_to_response('posting/testajax.htm',{'gdata':gdata})
         else:
              gdata = tblaccount.objects.all()
              #gdata = ""
              return render_to_response('posting/testajax.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def paymentprocess(request):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            vardate1 = date.today()
            if tbltemppayment.objects.filter(userid = varuser).count() == 0 :
                return HttpResponseRedirect('/SchApp/account/posting/payment/')
            else:
                ll = []
                lk = ""
                vardata = tbltemppayment.objects.filter(userid = varuser)
                cuspart =""
                custo = 0
                for j in vardata:
                    lk = j.cusname,j.cuscode,j.accname,j.acccode,j.transdate,j.invoiceno,j.userid,j.particular,j.amount,j.id
                    ll.append(lk)
                    vardate1 = j.transdate
                varyear = vardate1.year
                #**************************************************************getting transid
                #***************************************

                kt = gettransid(varyear)
                if tbltransactiontemp.objects.filter(transdate__year = varyear).count() == 0 :
                    varrid = 1
                else:
                    varrid1 = tbltransactiontemp.objects.filter(transdate__year = varyear).aggregate(Max('recid'))
                    varrid = varrid1['recid__max']
                    varrid = int(varrid)
                if kt > varrid:
                    varrid =  kt + 1
                else:
                    varrid  += 1
                vyear =  str(varyear)
                vayear = vyear[2]+ vyear[3]
                vartransid = str(vayear)+ str(varrid) #trans id
                varrecid = int(varrid)
                k = range(len(ll))
                we =[]
                for h in k:
                  for m in ll[h]:
                     we.append(m)
                  #**************************************
                  cusno = we[1]
                  cusname = we[0]
                  refno = we[5]
                  vardate = we[4]
                  varyear = vardate.year
                  userid = we[6]
                  accname = we[2]
                  acccode = we[3]
                  part = we[7]
                  amount = we[8]
                  rid = we[9]

                  #******************************************************
                  custo =  amount
                  #vyear =  str(varyear)
                  #vayear = vyear[2]+ vyear[3]
                  #vartransid = str(vayear)+ str(varrid) #trans id
                  #varrecid = varrid # my recid
                  #**************************************************************************
                  cusdet =  tblaccount.objects.get(acccode = cusno)# bank CR
                  cusbal = cusdet.accbal
                  cusgrp = cusdet.groupname
                  cussub = cusdet.subgroupname
                  if cusgrp == "FIXED ASSETS" or cusgrp == "CURRENT ASSETS" or cusgrp == "EXPENSES" or cusgrp == "COST OF SALES":
                      cusbal = cusbal - custo
                  else:
                      cusbal = cusbal + custo
                  #***********************************************
                  used = tbltransaction(accname = cusname,acccode = cusno,debit = 0,credit = custo,balance = cusbal,transid = vartransid,transdate = vardate,particulars = part,refno = refno,groupname = cusgrp,subname = cussub ,userid = userid,recid = varrecid )
                  used.save()
                  #********************
                  selsubdata = tblaccount.objects.get(acccode = cusno)
                  selsubdata.accbal = cusbal
                  selsubdata.lasttrandate = vardate
                  selsubdata.save()
                  #**********************************
                  #***************************************
                  cusdet1 =  tblaccount.objects.get(acccode = acccode)
                  bal = cusdet1.accbal
                  grp = cusdet1.groupname
                  sub = cusdet1.subgroupname
                  if grp == "FIXED ASSETS" or grp == "CURRENT ASSETS" or grp == "EXPENSES" or grp == "COST OF SALES":
                       cusbal1 = bal + amount
                  else:
                       cusbal1 = bal - amount

                      #***********************************************8
                  used = tbltransaction(accname = accname,acccode = acccode,debit = amount,credit = 0,balance = cusbal1,transid = vartransid,transdate = vardate,particulars = part,refno = refno,groupname = grp,subname = sub ,userid = userid, recid = varrecid )
                  used.save()
                    #********************update
                  selsubdata1 = tblaccount.objects.get(acccode = acccode)
                  selsubdata1.accbal = cusbal1
                  selsubdata1.lasttrandate = vardate
                  selsubdata1.save()

                  we.remove(accname)
                  we.remove(acccode)
                  we.remove(part)
                  we.remove(amount)
                  we.remove(cusno)
                  we.remove(cusname)
                  we.remove(refno)
                  we.remove(vardate)
                  we.remove(userid)
                  we.remove(rid)

                  tbltemppayment.objects.filter(userid = varuser).delete()

                return render_to_response('posting/invsuccess.htm',{'varuser':varuser,'varerr':varerr,'vartransid':vartransid})

        else:
         return HttpResponseRedirect('/login/')


def editpayment(request,invid):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.payment
            if int(uenter) == 0 :
                return HttpResponseRedirect('/SchApp/account/posting/unauto/')
            varerr =""
            if request.method == 'POST':
                getdetails = ""
                amount = request.POST['accname'] # the amount
                accno = request.POST['hcode']#the primary key
                particular = request.POST['acccode']#the particulars
                transdate = request.POST['subname'] #the transdate
                invoiceno = request.POST['grpname'] #the invoice
                particular = particular
                if particular == "" or invoiceno == "" or amount == "" or transdate == "":
                    #varerr = "INVALID TRANSACTION"
                    #getdetails = tbltemppayment.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    #return render_to_response('posting/editpayment.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                    return HttpResponseRedirect('/SchApp/account/posting/payment/')
                #***********GETTING THE DATE
                try:
                    k = float(amount)
                except:
                    #varerr = "INVALID AMOUNT"
                    #getdetails = tbltemppayment.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    #return render_to_response('posting/editpayment.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                    return HttpResponseRedirect('/SchApp/account/posting/payment/')
                vyear = str(transdate)
                vk = vyear[0:4]
                if vk.isdigit() == True :
                    #print 'digit value'
                    vdate = date(int(vyear[0:4]),int(vyear[5:7]),int(vyear[8:10]))
                else:
                    #print 'not digit'
                    vdate = date(int(vyear[6:10]),int(vyear[0:2]),int(vyear[3:5]))
                 #*888888888888888888888888888888888888888 checking the date
                if tblcalender.objects.all().count() == 0:
                     #varerr = "NO START DATE"
                     #getdetails = tbltemppayment.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                     #return render_to_response('posting/editpayment.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                     return HttpResponseRedirect('/SchApp/account/posting/payment/')
                getdate = tblcalender.objects.all()
                stdate = date.today()
                endate = date.today()
                for g in getdate:
                   stdate = g.startmonth
                   endate = g.endtmonth
                if vdate < stdate or vdate > endate :
                   #varerr = "INVALID DATE"
                   #getdetails = tbltemppayment.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                   #return render_to_response('posting/editpayment.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                   return HttpResponseRedirect('/SchApp/account/posting/payment/')
                #********************
                seldata = tbltemppayment.objects.get(id = accno)
                seldata.amount = amount
                seldata.particular = particular
                seldata.transdate = vdate
                seldata.invoiceno = invoiceno
                seldata.save()
                return HttpResponseRedirect('/SchApp/account/posting/payment/')
            else:
                try:
                  getdetails = tbltemppayment.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                  return render_to_response('posting/editpayment.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                except:
                    varerr = "Account Not Exist"
                    return render_to_response('posting/editpayment.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
        else:
         return HttpResponseRedirect('/login/')

def deletepayment(request,invid):
    varerr =""
    if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            #if request.method == 'POST':

            #accno = request.POST['hcode']#the primary key

            seldata = tbltemppayment.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/SchApp/account/posting/payment/')
            #else:
             #   return HttpResponseRedirect('/posting/invoice/')
    else:
      return HttpResponseRedirect('/login/')

def editreceipt(request,invid):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.receipt
            if int(uenter) == 0 :
               return HttpResponseRedirect('/SchApp/account/posting/unauto/')
            varerr =""
            if request.method == 'POST':
                getdetails = ""
                amount = request.POST['accname'] # the amount
                accno = request.POST['hcode']#the primary key
                particular = request.POST['acccode']#the particulars
                transdate = request.POST['subname'] #the transdate
                invoiceno = request.POST['grpname'] #the invoice
                particular = particular

                if particular == "" or invoiceno == "" or amount == "" or transdate == "":
                    #varerr = "INVALID TRANSACTION"
                    #getdetails = tbltempreceipt.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    #return render_to_response('posting/editreceipt.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                    return HttpResponseRedirect('/SchApp/account/posting/receipt/')
                #***********GETTING THE DATE
                try:
                    k = float(amount)
                except:
                    #varerr = "INVALID AMOUNT"
                    #getdetails = tbltempreceipt.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    #return render_to_response('posting/editreceipt.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                    return HttpResponseRedirect('/SchApp/account/posting/receipt/')
                vyear = str(transdate)
                vk = vyear[0:4]
                if vk.isdigit() == True :
                    #print 'digit value'
                    vdate = date(int(vyear[0:4]),int(vyear[5:7]),int(vyear[8:10]))
                else:
                    #print 'not digit'
                    vdate = date(int(vyear[6:10]),int(vyear[0:2]),int(vyear[3:5]))
                #*888888888888888888888888888888888888888 checking the date
                if tblcalender.objects.all().count() == 0:
                     #varerr = "NO START DATE"
                     #getdetails = tbltempreceipt.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                     #return render_to_response('posting/editreceipt.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                     return HttpResponseRedirect('/SchApp/account/posting/receipt/')
                getdate = tblcalender.objects.all()
                for g in getdate:
                   stdate = g.startmonth
                   endate = g.endtmonth
                if vdate < stdate or vdate > endate :
                   #varerr = "INVALID DATE"
                   #getdetails = tbltempreceipt.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                   #return render_to_response('posting/editreceipt.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                   return HttpResponseRedirect('/SchApp/account/posting/receipt/')
                #********************
                seldata = tbltempreceipt.objects.get(id = accno)
                seldata.amount = amount
                seldata.particular = particular
                seldata.transdate = vdate
                seldata.invoiceno = invoiceno
                seldata.save()
                return HttpResponseRedirect('/SchApp/account/posting/receipt/')
            else:
                try:
                  getdetails = tbltempreceipt.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                  return render_to_response('posting/editreceipt.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                except:
                    varerr = "Account Not Exist"
                    return render_to_response('posting/editreceipt.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
        else:
         return HttpResponseRedirect('/login/')

def deletereceipt(request,invid):
    varerr =""
    if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            #if request.method == 'POST':

            #accno = request.POST['hcode']#the primary key

            seldata = tbltempreceipt.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/SchApp/account/posting/receipt/')
            #else:
             #   return HttpResponseRedirect('/posting/invoice/')
    else:
      return HttpResponseRedirect('/login/')


def generaljournal1(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        getdetails =""
        form = ledgerform()
        form2 = ledgerform2()
        vardebit = 0
        varcredit = 0
        if request.method == 'POST':
          form = ledgerform(request.POST) # A form bound to the POST data
          if form.is_valid():
             dracccode = form.cleaned_data['dracccode']
             draccname = form.cleaned_data['draccname'] #customer code
             dramount = form.cleaned_data['dramount']
             drparticulars = form.cleaned_data['drparticulars']
             drrefno = form.cleaned_data['drrefno']
             caldate1 = form.cleaned_data['drtransdate'] #transaction date
             caldate2 = caldate1.split('/')
             drtransdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
             #****************************************************
             if tblcalender.objects.all().count() == 0:
                 varerr ="INVALID DATE"
                 varrid1 = tbljournal.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
                 vardebit = varrid1['dr__sum']
                 varcredit = varrid1['cr__sum']
                 return render_to_response('posting/journal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))
             getdate = tblcalender.objects.all()
             stdate = date.today()
             endate = date.today()
             for g in getdate:
                 stdate = g.startmonth
                 endate = g.endtmonth
             if drtransdate < stdate or drtransdate > endate :
                 varerr ="INVALID DATE"
                 varrid1 = tbljournal.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
                 vardebit = varrid1['dr__sum']
                 varcredit = varrid1['cr__sum']
                 return render_to_response('posting/journal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))
             #*****************************************
             ks = tblcontrol.objects.all()
             for p in ks:
                 s = p.acccode
                 if dracccode == s:
                    varerr = "YOU CAN NOT POST INTO THIS ACCOUNT"
                    varrid1 = tbljournal.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
                    vardebit = varrid1['dr__sum']
                    varcredit = varrid1['cr__sum']
                    return render_to_response('posting/journal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))

             #***************************************
             if tbljournal.objects.filter(userid = varuser).count() == 0:
                 used = tbljournal(accname = draccname,acccode = dracccode,particular = drparticulars,transdate = drtransdate,dr = dramount,cr = 0,userid = varuser,refno = drrefno )
                 used.save()
             else:
                 varmonth = drtransdate.month
                 varyear = drtransdate.year
                 if tbljournal.objects.filter(userid = varuser,transdate__month = varmonth,transdate__year = varyear).count() == 0:
                      varerr ="INVALID DATE"
                      varrid1 = tbljournal.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
                      vardebit = varrid1['dr__sum']
                      varcredit = varrid1['cr__sum']
                      return render_to_response('posting/journal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))
                 else:
                      used = tbljournal(accname = draccname,acccode = dracccode,particular = drparticulars,transdate = drtransdate,dr = dramount,cr = 0,userid = varuser,refno = drrefno )
                      used.save()
             #*****************************
             getdetails = tbljournal.objects.filter(userid = varuser).order_by('id')
             #now i do insertion
             if tbljournal.objects.filter(userid = varuser).count() == 0 :
               vardebit = 0
               varcredit = 0
             else:
               varrid1 = tbljournal.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
               vardebit = varrid1['dr__sum']
               varcredit = varrid1['cr__sum']
             return HttpResponseRedirect('/SchApp/account/posting/generaljournal/')
             #return render_to_response('posting/journal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))
        else:
            getdetails = ""
            form = ledgerform()
            form2 = ledgerform2()
            if tbljournal.objects.filter(userid = varuser).count() == 0 :
               vardebit = 0
               varcredit = 0
            else:
               varrid1 = tbljournal.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
               vardebit = varrid1['dr__sum']
               varcredit = varrid1['cr__sum']
        return render_to_response('posting/journal.htm',{'varuser':varuser,'varerr':varerr,'form2':form2,'form':form,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')
def generaljournal2(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        getdetails =""
        if tbljournal.objects.filter(userid = varuser).count() == 0 :
               vardebit = 0
               varcredit = 0
        else:
              varrid1 = tbljournal.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
              vardebit = varrid1['dr__sum']
              varcredit = varrid1['cr__sum']
        form = ledgerform()
        form2 = ledgerform2()
        if request.method == 'POST':
          form2 = ledgerform2(request.POST) # A form bound to the POST data
          if form2.is_valid():
             cracccode = form2.cleaned_data['cracccode']
             craccname = form2.cleaned_data['craccname'] #customer code
             cramount = form2.cleaned_data['cramount']
             crparticulars = form2.cleaned_data['crparticulars']
             crrefno = form2.cleaned_data['crrefno']
             caldate1 = form2.cleaned_data['crtransdate']
             caldate2 = caldate1.split('/')
             crtransdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
             #****************************************************
             if tblcalender.objects.all().count() == 0:
                 varerr ="INVALID DATE"
                 varrid1 = tbljournal.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
                 vardebit = varrid1['dr__sum']
                 varcredit = varrid1['cr__sum']
                 return render_to_response('posting/journal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))
             getdate = tblcalender.objects.all()
             stdate = date.today()
             endate = date.today()
             for g in getdate:
                 stdate = g.startmonth
                 endate = g.endtmonth
             if crtransdate < stdate or crtransdate > endate :
                 varerr ="INVALID DATE"
                 varrid1 = tbljournal.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
                 vardebit = varrid1['dr__sum']
                 varcredit = varrid1['cr__sum']
                 return render_to_response('posting/journal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))
             #***************************************
             ks = tblcontrol.objects.all()
             for p in ks:
                 s = p.acccode
                 if cracccode == s:
                    varerr = "YOU CAN NOT POST INTO THIS ACCOUNT"
                    varrid1 = tbljournal.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
                    vardebit = varrid1['dr__sum']
                    varcredit = varrid1['cr__sum']
                    return render_to_response('posting/journal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))

             if tbljournal.objects.filter(userid = varuser).count() == 0:
                  used = tbljournal(accname = craccname,acccode = cracccode,particular = crparticulars,transdate = crtransdate,dr = 0,cr = cramount,userid = varuser,refno = crrefno )
                  used.save()
             else:
                 varmonth = crtransdate.month
                 varyear = crtransdate.year
                 if tbljournal.objects.filter(userid = varuser,transdate__month = varmonth,transdate__year = varyear).count() == 0:
                      varerr ="INVALID DATE"
                      varrid1 = tbljournal.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
                      vardebit = varrid1['dr__sum']
                      varcredit = varrid1['cr__sum']
                      return render_to_response('posting/journal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))
                 else:
                       used = tbljournal(accname = craccname,acccode = cracccode,particular = crparticulars,transdate = crtransdate,dr = 0,cr = cramount,userid = varuser,refno = crrefno )
                       used.save()

             #*****************************
             getdetails = tbljournal.objects.filter(userid = varuser).order_by('id')
             if tbljournal.objects.filter(userid = varuser).count() == 0 :
               vardebit = 0
               varcredit = 0
             else:
               varrid1 = tbljournal.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
               vardebit = varrid1['dr__sum']
               varcredit = varrid1['cr__sum']
             #now i do insertion
             return HttpResponseRedirect('/SchApp/account/posting/generaljournal/')
             #return render_to_response('posting/journal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))
        else:
            getdetails=""
            #return HttpResponseRedirect('/posting/generaljournal/')
            form = ledgerform()
            form2 = ledgerform2()
            if tbljournal.objects.filter(userid = varuser).count() == 0 :
               vardebit = 0
               varcredit = 0
            else:
               varrid1 = tbljournal.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
               vardebit = varrid1['dr__sum']
               varcredit = varrid1['cr__sum']
        return render_to_response('posting/journal.htm',{'varuser':varuser,'varerr':varerr,'form2':form2,'form':form,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def generaljournal(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.genledger
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/posting/unauto/')
        varerr =""
        getdetails =""
        form = ledgerform()
        form2 = ledgerform2()
        if tbljournal.objects.filter(userid = varuser).count() == 0 :
               vardebit = 0
               varcredit = 0
        else:
               varrid1 = tbljournal.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
               vardebit = varrid1['dr__sum']
               varcredit = varrid1['cr__sum']
        getdetails = tbljournal.objects.filter(userid = varuser).order_by('id')
        return render_to_response('posting/journal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')

def editjournal(request,invid):
    varerr =""
    if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.genledger
            if int(uenter) == 0 :
              return HttpResponseRedirect('/SchApp/account/posting/unauto/')
            varerr =""
            #if request.method == 'POST':

            #accno = request.POST['hcode']#the primary key

            seldata = tbljournal.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/SchApp/account/posting/generaljournal/')
            #else:
             #   return HttpResponseRedirect('/posting/invoice/')
    else:
      return HttpResponseRedirect('/login/')

def journalprocess(request):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            vartransid = ''
            vardate1 = datetime.date.today()
            if tbljournal.objects.filter(userid = varuser).count() == 0 :
                return HttpResponseRedirect('/posting/generaljournal/')
            else:
                varrid1 = tbljournal.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
                vardebit = varrid1['dr__sum']
                varcredit = varrid1['cr__sum']
                if vardebit == varcredit:
                    ll = []
                    lk = ""
                    vardata = tbljournal.objects.filter(userid = varuser)
                    cuspart =""
                    custo = 0
                    for j in vardata:
                        lk = j.accname,j.acccode,j.particular,j.transdate,j.dr,j.cr,j.userid,j.refno,j.id
                        ll.append(lk)
                        vardate1 = j.transdate
                    varyear = vardate1.year
                    #**************************************************************getting transid
                    kt = gettransid(varyear)
                    if tbltransactiontemp.objects.filter(transdate__year = varyear).count() == 0 :
                        varrid = 1
                    else:
                        varrid1 = tbltransactiontemp.objects.filter(transdate__year = varyear).aggregate(Max('recid'))
                        varrid = varrid1['recid__max']
                        varrid = int(varrid)
                    if kt > varrid:
                        varrid =  kt + 1
                    else:
                        varrid  += 1
                    vyear =  str(varyear)
                    vayear = vyear[2]+ vyear[3]
                    vartransid = str(vayear)+ str(varrid) #trans id
                    varrecid = int(varrid)
                    k = range(len(ll))
                    we =[]
                    for h in k:
                      for m in ll[h]:
                         we.append(m)
                      #**************************************
                      accname = we[0]
                      accno = we[1]
                      part = we[2]
                      vardate = we[3]
                      dr = we[4]
                      cr = we[5]
                      userid = we[6]
                      refno = we[7]
                      rid = we[8]
                      #******************************************************
                      #vyear =  str(varyear)
                      #vayear = vyear[2]+ vyear[3]
                      #vartransid = str(vayear)+ str(varrid) #trans id
                      #varrecid = varrid # my recid
                     #*********************************************************
                      #**************************************************************************
                      cusdet =  tblaccount.objects.get(acccode = accno)# bank CR
                      cusbal = cusdet.accbal
                      cusgrp = cusdet.groupname
                      cussub = cusdet.subgroupname
                      if cr == 0:# i.e we want to debit
                          custo = dr
                          if cusgrp == "FIXED ASSETS" or cusgrp == "CURRENT ASSETS" or cusgrp == "EXPENSES" or cusgrp == "COST OF SALES":
                              cusbal = cusbal + custo
                          else:
                              cusbal = cusbal - custo
                      else: #i.e we need to credit the account
                          custo = cr
                          if cusgrp == "FIXED ASSETS" or cusgrp == "CURRENT ASSETS" or cusgrp == "EXPENSES" or cusgrp == "COST OF SALES":
                              cusbal = cusbal - custo
                          else:
                              cusbal = cusbal + custo

                      #***********************************************
                      used = tbltransaction(accname = accname,acccode = accno,debit = dr,credit = cr,balance = cusbal,transid = vartransid,transdate = vardate,particulars = part,refno = refno,groupname = cusgrp,subname = cussub ,userid = userid,recid = varrecid )
                      used.save()
                      #********************
                      selsubdata = tblaccount.objects.get(acccode = accno)
                      selsubdata.accbal = cusbal
                      selsubdata.lasttrandate = vardate
                      selsubdata.save()
                      #**********************************
                      #***************************************
                      we.remove(accname)
                      we.remove(accno)
                      we.remove(part)
                      we.remove(vardate)
                      we.remove(dr)
                      we.remove(cr)
                      we.remove(userid)
                      we.remove(refno)
                      we.remove(rid)
                      tbljournal.objects.filter(userid = varuser).delete()
                    return render_to_response('posting/invsuccess.htm',{'varuser':varuser,'varerr':varerr,'vartransid':vartransid})
                else:
                    return HttpResponseRedirect('/SchApp/account/posting/generaljournal/')

        else:
         return HttpResponseRedirect('/login/')

def standardjournal(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.standardledger
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/posting/unauto/')
        varerr =""
        getdetails =""
        total = 0
        form = standardform()
        if request.method == 'POST':
          form = standardform(request.POST) # A form bound to the POST data
          if form.is_valid():

             dracccode = form.cleaned_data['dracccode']
             draccname = form.cleaned_data['draccname'] #customer code
             dramount = form.cleaned_data['dramount']
             drparticulars = form.cleaned_data['drparticulars']
             drrefno = form.cleaned_data['drrefno']
             cracccode = form.cleaned_data['cracccode']
             craccname = form.cleaned_data['craccname']
             duration = form.cleaned_data['duration']
             if dracccode == cracccode :
                 varerr ="INVALID ENTRY"
                 getdetails = tblstandard.objects.all().order_by('id')
                 if tblstandard.objects.all().count() == 0 :
                    total = 0
                 else:
                    varrid1 = tblstandard.objects.all().aggregate(Sum('amount'))
                    total = varrid1['amount__sum']
                 return render_to_response('posting/standard.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'total':total},context_instance = RequestContext(request))
             else:

                used = tblstandard(accname = draccname,acccode = dracccode,particular = drparticulars,amount = dramount,userid = varuser,refno = drrefno,craccname = craccname,cracccode = cracccode,duration = duration )
                used.save()
             #*****************************
             ks = tblcontrol.objects.all()
             for p in ks:
                 s = p.acccode
                 if dracccode == s:
                    varerr = "YOU CAN NOT POST INTO ONE OF THIS ACCOUNT"
                    getdetails =  tblstandard.objects.all().order_by('id')
                    return render_to_response('posting/standard.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'total':total},context_instance = RequestContext(request))
                 if cracccode == s:
                    varerr = "YOU CAN NOT POST INTO ONE OF THIS ACCOUNT"
                    getdetails =  tblstandard.objects.all().order_by('id')
                    return render_to_response('posting/standard.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'total':total},context_instance = RequestContext(request))
             if tblstandard.objects.all().count() == 0 :
                    total = 0
             else:
                    varrid1 = tblstandard.objects.all().aggregate(Sum('amount'))
                    total = varrid1['amount__sum']
             getdetails = tblstandard.objects.all().order_by('id')
             return HttpResponseRedirect('/SchApp/account/posting/standardjournal/')
             #now i do insertion
            # return render_to_response('posting/standard.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'total':total},context_instance = RequestContext(request))
        else:
            if tblstandard.objects.all().count() == 0 :
                total = 0
            else:
                varrid1 = tblstandard.objects.all().aggregate(Sum('amount'))
                total = varrid1['amount__sum']

            form = standardform()
            getdetails = tblstandard.objects.all().order_by('id')
        return render_to_response('posting/standard.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'total':total},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')

def editstandard(request,invid):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.standardledger
            if int(uenter) == 0 :
                return HttpResponseRedirect('/SchApp/account/posting/unauto/')
            varerr =""
            if request.method == 'POST':
                getdetails = ""
                accname = request.POST['acccode'] # the amount
                acccode = request.POST['accname'] # the amount
                particular = request.POST['subname']#the particulars
                amount = request.POST['grpname'] #the
                refno = request.POST['customer'] #the
                craccname = request.POST['cusname'] #the
                cracccode = request.POST['cuscode'] #the
                duration = request.POST['duration'] #the invoice
                accno = request.POST['hcode']#the primary key
                kl = float(duration)
                jj = int(kl)
                if acccode == cracccode :
                    #varerr ="INVALID TRANSACTION"
                    #getdetails = tblstandard.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    #return render_to_response('posting/editstandard.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                    return HttpResponseRedirect('/SchApp/account/posting/standardjournal/')
                else:
                    if particular == "" or refno == "" or amount == "" :
                      #varerr = "INVALID TRANSACTION"
                      #getdetails = tblstandard.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                     # return render_to_response('posting/editstandard.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                      return HttpResponseRedirect('/SchApp/account/posting/standardjournal/')
                #***********GETTING THE DATE
                    try:
                        k = float(amount)
                    except:
                        #varerr = "INVALID AMOUNT"
                        #getdetails = tblstandard.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                        #return render_to_response('posting/editstandard.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                        return HttpResponseRedirect('/SchApp/account/posting/standardjournal/')
                    seldata = tblstandard.objects.get(id = accno)
                    seldata.accname = accname
                    seldata.acccode = acccode
                    seldata.particular = particular
                    seldata.amount = amount
                    seldata.refno = refno
                    seldata.craccname = craccname
                    seldata.cracccode = cracccode
                    seldata.duration = jj
                    seldata.save()
                    return HttpResponseRedirect('/SchApp/account/posting/standardjournal/')
            else:
                try:
                  getdetails = tblstandard.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                  return render_to_response('posting/editstandard.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                except:
                    varerr = "Account Not Exist"
                    return render_to_response('posting/editstandard.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
        else:
         return HttpResponseRedirect('/login/')

def deletestandard(request,invid):
    varerr =""
    if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            seldata = tblstandard.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/SchApp/account/posting/standardjournal/')
    else:
      return HttpResponseRedirect('/login/')

def stardardprocess(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = prostandardform(request.POST) # A form bound to the POST data
          if form.is_valid():
             caldate1 = form.cleaned_data['monthly']
             caldate2 = caldate1.split('/')
             transdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
             vardate1 = transdate
             varrmonth = transdate.month
             varryear = transdate.year
             #*******************************************************
             #**********************************************************getting the date
             if tblcalender.objects.all().count() == 0:
                 varerr = "NO START DATE"
                 #varerr ="This Month/Year Has been Process"
                 getdetails = tblstandard.objects.all().order_by('id')
                 return render_to_response('posting/standardprocess.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             getdate = tblcalender.objects.all()
             stdate = date.today()
             endate = date.today()
             for g in getdate:
                 stdate = g.startmonth
                 endate = g.endtmonth
             if transdate < stdate or transdate > endate :
                 varerr = "INVALID DATE"
                 #varerr ="This Month/Year Has been Process"
                 getdetails = tblstandard.objects.all().order_by('id')
                 return render_to_response('posting/standardprocess.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             #print varrmonth,varryear
             #print vardate1
             if tblstandard.objects.all().count() == 0 :
                return HttpResponseRedirect('/SchApp/account/posting/standardjournal/')
             else:
                try:
                    ttry = tblstandarddate.objects.get(transdate__year = varryear,transdate__month = varrmonth)
                    varerr ="This Month/Year Has been Process"
                    getdetails = tblstandard.objects.all().order_by('id')
                    return render_to_response('posting/standardprocess.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                except:
                    ll = []
                    lk = ""
                    vardata = tblstandard.objects.all()
                    for j in vardata:
                        lk = j.accname,j.acccode,j.particular,j.amount,j.refno,j.craccname,j.cracccode,j.duration,j.id
                        ll.append(lk)
                    vardate1 = transdate
                    varyear = vardate1.year
                    #**************************************************************getting transid
                    #***************************************
                    kt = gettransid(varyear)
                    if tbltransactiontemp.objects.filter(transdate__year = varyear).count() == 0 :
                        varrid = 1
                    else:
                        varrid1 = tbltransactiontemp.objects.filter(transdate__year = varyear).aggregate(Max('recid'))
                        varrid = varrid1['recid__max']
                        varrid = int(varrid)
                    if kt > varrid:
                        varrid =  kt + 1
                    else:
                        varrid  += 1
                    vyear =  str(varyear)
                    vayear = vyear[2]+ vyear[3]
                    vartransid = str(vayear)+ str(varrid) #trans id
                    varrecid = int(varrid)
                    k = range(len(ll))
                    we =[]
                    for h in k:
                      for m in ll[h]:
                         we.append(m)
                      #**************************************
                      draccname = we[0]
                      draccno = we[1]
                      part = we[2]
                      amount = we[3]
                      refno = we[4]
                      craccname = we[5]
                      cracccode = we[6]
                      duration = we[7]
                      rid = we[8]
                      #******************************************************
                      #vyear =  str(varyear)
                      #vayear = vyear[2]+ vyear[3]
                      #vartransid = str(vayear)+ str(varrid) #trans id
                      #varrecid = varrid # my recid
                      #*********************************************************
                      #**************************************************************************DR
                      cusdet =  tblaccount.objects.get(acccode = draccno)# bank DR
                      cusbal = cusdet.accbal
                      cusgrp = cusdet.groupname
                      cussub = cusdet.subgroupname
                      custo = amount
                      if cusgrp == "FIXED ASSETS" or cusgrp == "CURRENT ASSETS" or cusgrp == "EXPENSES" or cusgrp == "COST OF SALES":
                         cusbal = cusbal + custo
                      else:
                         cusbal = cusbal - custo
                      #***********************************************
                      used = tbltransaction(accname = draccname,acccode = draccno,debit = custo,credit = 0,balance = cusbal,transid = vartransid,transdate = transdate,particulars = part,refno = refno,groupname = cusgrp,subname = cussub ,userid = varuser,recid = varrecid )
                      used.save()
                      #********************
                      selsubdata = tblaccount.objects.get(acccode = draccno)
                      selsubdata.accbal = cusbal
                      selsubdata.lasttrandate = transdate
                      selsubdata.save()
                      #************************************************************* CR
                      cusdet1 =  tblaccount.objects.get(acccode = cracccode)# bank DR
                      cusbal1 = cusdet1.accbal
                      cusgrp1 = cusdet1.groupname
                      cussub1 = cusdet1.subgroupname
                      custo = amount
                      if cusgrp1 == "FIXED ASSETS" or cusgrp1 == "CURRENT ASSETS" or cusgrp1 == "EXPENSES" or cusgrp1 == "COST OF SALES":
                         cusbal1 = cusbal1 - custo
                      else:
                         cusbal1 = cusbal1 + custo
                      #***********************************************
                      used1 = tbltransaction(accname = craccname,acccode = cracccode,debit = 0,credit = custo,balance = cusbal1,transid = vartransid,transdate = transdate,particulars = part,refno = refno,groupname = cusgrp1,subname = cussub1 ,userid = varuser,recid = varrecid )
                      used1.save()
                      #********************
                      selsubdata1 = tblaccount.objects.get(acccode = cracccode)
                      selsubdata1.accbal = cusbal1
                      selsubdata1.lasttrandate = transdate
                      selsubdata1.save()
                      #********************************** update the standard table
                      duration1 =  duration - 1
                      if duration1 == 0 :
                          deldata = tblstandard.objects.filter(id = rid).delete()
                      else:
                           selsubdata11 = tblstandard.objects.get(id = rid)
                           selsubdata11.duration = duration1
                           selsubdata11.save()
                      used11 = tblstandarddate(transdate = vardate1,userid = varuser)
                      used11.save()
                      #***************************************
                      we.remove(draccname)
                      we.remove(draccno)
                      we.remove(part)
                      we.remove(amount)
                      we.remove(refno)
                      we.remove(craccname)
                      we.remove(cracccode)
                      we.remove(duration)
                      we.remove(rid)
                return HttpResponseRedirect('/SchApp/account/posting/standardjournal/')
        else:
            if tblstandard.objects.all().count()== 0:
                return HttpResponseRedirect('/SchApp/account/posting/standardjournal/')
            form = prostandardform()
            getdetails = tblstandard.objects.all().order_by('id')
        return render_to_response('posting/standardprocess.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def verifytrans(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = verifytransform(request.POST)
          if form.is_valid():
             transid1 = form.cleaned_data['transid']
             getdetails = tbltransaction.objects.filter(transid = transid1)
             return render_to_response('posting/verifyposting.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = verifytransform()
        return render_to_response('posting/verifyposting.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def accountsearch(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = verifytransform(request.POST)
          if form.is_valid():
             transid1 = form.cleaned_data['transid']
             getdetails = tbltransaction.objects.filter(transid = transid1)
             return render_to_response('posting/accountsearch.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = verifytransform()
        return render_to_response('posting/accountsearch.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def paymentajaxcodesea(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   gdata = tblaccount.objects.filter(accname__startswith = acccode).order_by('acccode')#filter(acccode__startswith = acccode,groupname = "CURRENT ASSETS",subgroupname ="CASH AND BANK BALANCES").order_by('acccode')
                   return render_to_response('posting/testajax.htm',{'gdata':gdata,'post':post})
             else:
                   gdata = tblaccount.objects.all()
                   #gdata = ""
                   return render_to_response('posting/testajax.htm',{'gdata':gdata})
         else:
              gdata = tblaccount.objects.all().order_by('acccode')
              #gdata = ""
              return render_to_response('posting/testajax.htm',{'gdata':gdata})
     else:
       return HttpResponseRedirect('/login/')

def ppounauto(request):
     if  "userid" in request.session:
        varuser = request.session['userid']

        varerr =""
        return render_to_response('posting/unautorise.htm',{'varuser':varuser,'varerr':varerr})
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
    gset = tblaccount.objects.filter(accname__contains = term,groupname = "CURRENT ASSETS",subgroupname ="RECEIVABLES").exclude(accname = "TRADE-DEBTORS").order_by('acccode')[:10]
    suggestions = []
    for i in gset:
        k = getbalreal(i.acccode)
        disamt = locale.format("%.2f",k,grouping=True)
        suggestions.append({'label': '%s %s' % (i.accname,i.acccode), 'acccode': i.acccode,'accname': i.accname,'accbal':disamt})
    return suggestions
@json_view
def autocompleteinv(request):
    term = request.GET.get('term')
    gset = tblaccount.objects.filter(accname__contains = term,groupname = "INCOME").order_by('acccode')[:10]
    #.exclude(groupname = "CURRENT ASSETS",subgroupname ="STOCKS").exclude(groupname = "CURRENT ASSETS",subgroupname ="RECEIVABLES").exclude(groupname = "CURRENT LIABILITIES",subgroupname = "PAYABLES",accname = "TRADE-CREDITORS").exclude(groupname = "CURRENT ASSETS",subgroupname = "MINI-STORE",accname = "MINI-STORE-BALANCE").exclude(groupname = "CURRENT ASSETS",subgroupname = "WORK-IN-PROGRESS",accname = "WORK-IN-PROGRESS-BALANCE").
    suggestions = []
    for i in gset:
        suggestions.append({'label': '%s %s' % (i.accname,i.acccode), 'acccode': i.acccode,'accname': i.accname})
    return suggestions
@json_view
def autocompletebank(request):
    term = request.GET.get('term')
    gset = tblaccount.objects.filter(accname__contains = term,groupname = "CURRENT ASSETS",subgroupname ="CASH-AND-BANK-BALANCES").order_by('acccode')[:10]
    #.exclude(groupname = "CURRENT ASSETS",subgroupname ="STOCKS").exclude(groupname = "CURRENT ASSETS",subgroupname ="RECEIVABLES").exclude(groupname = "CURRENT LIABILITIES",subgroupname = "PAYABLES",accname = "TRADE-CREDITORS").exclude(groupname = "CURRENT ASSETS",subgroupname = "MINI-STORE",accname = "MINI-STORE-BALANCE").exclude(groupname = "CURRENT ASSETS",subgroupname = "WORK-IN-PROGRESS",accname = "WORK-IN-PROGRESS-BALANCE").
    suggestions = []
    for i in gset:
        k = k = getbalreal(i.acccode)
        disamt = locale.format("%.2f",k,grouping=True)
        suggestions.append({'label': '%s %s' % (i.accname,i.acccode), 'acccode': i.acccode,'accname': i.accname,'accbal':disamt})
    return suggestions
@json_view
def autocompletebanknot(request):
    term = request.GET.get('term')
    gset = tblaccount.objects.filter(accname__contains = term).exclude(groupname = "CURRENT ASSETS",subgroupname ="STOCKS").exclude(groupname = "CAPITAL AND RESERVES",subgroupname ="SHAREHOLDERS FUND",accname = "CURRENT-YEAR-P/L").exclude(groupname = "CURRENT LIABILITIES",subgroupname = "PAYABLES",accname = "TRADE-CREDITORS").exclude(groupname = "CURRENT ASSETS",subgroupname = "MINI-STORE",accname = "MINI-STORE-BALANCE").exclude(groupname = "CURRENT ASSETS",subgroupname = "WORK-IN-PROGRESS",accname = "WORK-IN-PROGRESS-BALANCE").exclude(groupname = "CURRENT ASSETS",subgroupname = "STAFF-DEBTORS",accname = "STAFF-DEBTORS").exclude(groupname = "CURRENT ASSETS",subgroupname = "RECEIVABLES",accname = "TRADE-DEBTORS").order_by('acccode')[:10]
    #.exclude(groupname = "CURRENT ASSETS",subgroupname ="CASH-AND-BANK-BALANCES").exclude(groupname = "CURRENT ASSETS",subgroupname ="STOCKS").exclude(groupname = "CURRENT ASSETS",subgroupname ="RECEIVABLES").exclude(groupname = "CURRENT LIABILITIES",subgroupname = "PAYABLES",accname = "TRADE-CREDITORS").exclude(groupname = "CURRENT ASSETS",subgroupname = "MINI-STORE",accname = "MINI-STORE-BALANCE").exclude(groupname = "CURRENT ASSETS",subgroupname = "WORK-IN-PROGRESS",accname = "WORK-IN-PROGRESS-BALANCE").
    suggestions = []
    for i in gset:
        k = k = getbalreal(i.acccode)
        disamt = locale.format("%.2f",k,grouping=True)
        suggestions.append({'label': '%s %s' % (i.accname,i.acccode), 'acccode': i.acccode,'accname': i.accname,'accbal':disamt})
    return suggestions

@json_view
def autocompletebankall(request):
    term = request.GET.get('term')
    gset = tblaccount.objects.filter(accname__contains = term).exclude(groupname = "CURRENT ASSETS",subgroupname ="STOCKS").exclude(groupname = "CAPITAL AND RESERVES",subgroupname ="SHAREHOLDERS FUND",accname = "CURRENT-YEAR-P/L").exclude(groupname = "CURRENT LIABILITIES",subgroupname = "PAYABLES",accname = "TRADE-CREDITORS").exclude(groupname = "CURRENT ASSETS",subgroupname = "MINI-STORE",accname = "MINI-STORE-BALANCE").exclude(groupname = "CURRENT ASSETS",subgroupname = "WORK-IN-PROGRESS",accname = "WORK-IN-PROGRESS-BALANCE").exclude(groupname = "CURRENT ASSETS",subgroupname = "STAFF-DEBTORS",accname = "STAFF-DEBTORS").exclude(groupname = "CURRENT ASSETS",subgroupname = "RECEIVABLES",accname = "TRADE-DEBTORS").exclude(groupname = "CURRENT LIABILITIES",subgroupname = "STUDENT ACC").order_by('acccode')[:10]
    #.exclude(groupname = "CURRENT ASSETS",subgroupname ="STOCKS").exclude(groupname = "CURRENT ASSETS",subgroupname ="RECEIVABLES").exclude(groupname = "CURRENT LIABILITIES",subgroupname = "PAYABLES",accname = "TRADE-CREDITORS").exclude(groupname = "CURRENT ASSETS",subgroupname = "MINI-STORE",accname = "MINI-STORE-BALANCE").exclude(groupname = "CURRENT ASSETS",subgroupname = "WORK-IN-PROGRESS",accname = "WORK-IN-PROGRESS-BALANCE").
    suggestions = []
    for i in gset:
        k = k = getbalreal(i.acccode)
        disamt = locale.format("%.2f",k,grouping=True)
        suggestions.append({'label': '%s %s' % (i.accname,i.acccode), 'acccode': i.acccode,'accname': i.accname,'accbal':disamt})
    return suggestions

@json_view
def autocompletebankpocket(request):
    term = request.GET.get('term')
    gset = tblaccount.objects.filter(accname__contains = term,groupname = "CURRENT LIABILITIES",subgroupname = "STUDENT ACC").order_by('acccode')[:10]
    suggestions = []
    for i in gset:
        k =k = getbalreal(i.acccode)
        disamt = locale.format("%.2f",k,grouping=True)
        suggestions.append({'label': '%s %s' % (i.accname,i.acccode), 'acccode': i.acccode,'accname': i.accname,'accbal':disamt})
    return suggestions

def getinvoice(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails =  tbltemp.objects.get(id = acccode)
                return render_to_response('posting/editinvoice.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getreceipt(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails =  tbltempreceipt.objects.get(id = acccode)
                return render_to_response('posting/editreceipt.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def getpayment(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tbltemppayment.objects.get(id = acccode)
                return render_to_response('posting/editpayment.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getstandard(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tblstandard.objects.get(id = acccode)#.order_by('acccode')#tblaccount_acccode
                return render_to_response('posting/editstandard.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def postbill(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.invoice
            if int(uenter) == 0 :
                return HttpResponseRedirect('/SchApp/account/posting/unauto/')
            varerr =""
            getdetails =""
            if request.method == 'POST':
               # form = invoiceformsc(request.POST) # A form bound to the POST data
                #if form.is_valid():
                    bill_list = []
                    session =request.POST['session']
                    klass = request.POST['klass']
                    term = request.POST['term']
                    caldate1 = request.POST['transdate']
                    if caldate1 == '' :
                        varerr = "INVALID DATE"
                        getdetails = ''
                        return HttpResponseRedirect('/SchApp/account/posting/invoice/')
                        #return render_to_response('posting/postbill.htm',{'varuser':varuser,'varerr':varerr},context_instance = RequestContext(request))
                    caldate2 = caldate1.split('/')
                    transdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                    getdate = tblcalender.objects.all() #rwadmin
                    stdate = datetime.date.today()
                    endate = datetime.date.today()
                    for g in getdate:
                       stdate = g.startmonth
                       endate = g.endtmonth

                    #verifying payments*************************
                    tday = transdate
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
                    #*******************************************

                    if transdate < stdate or transdate > endate :
                        varerr = "INVALID DATE"
                        getdetails = ''
#                        return render_to_response('posting/invsuccess.htm',{'varerr':varerr})
                        return HttpResponseRedirect('/SchApp/account/posting/invoice/')
                    varyear = transdate.year
                    kt = gettransid(varyear)
                    if tbltransactiontemp.objects.filter(transdate__year = varyear).count() == 0 :
                        varrid = 1
                    else:
                        varrid1 = tbltransactiontemp.objects.filter(transdate__year = varyear).aggregate(Max('recid'))
                        varrid = varrid1['recid__max']
                        varrid = int(varrid)
                    if kt > varrid:
                        varrid =  kt + 1
                    else:
                        varrid  += 1
                    vyear =  str(varyear)
                    vayear = vyear[2]+ vyear[3]
                    vartransid = str(vayear)+ str(varrid) #trans id
                    varrecid = int(varrid)
                    studata = Student.objects.filter(admitted_class = klass,admitted_session = session,gone = False).order_by('admissionno')
                    for st in studata:
                        if tblbill.objects.filter(klass = klass,term = term,dayboarding = st.dayboarding).count() == 0:
                            varrid = 0
                        else:
                            getbill = tblbill.objects.filter(klass = klass,term = term,dayboarding = st.dayboarding)
                            for j in getbill:
                                particulars = '%s for %s %s Term'%(j.desc,session,term)
                                postacc(transdate,st.admissionno,j.acccode,j.billamount,particulars,vartransid,varrecid,varuser)
                                savebill = oldbill(session = session,admissionno = st.admissionno,name = st.fullname,klass = klass,arm = st.admitted_arm,term = term,billamount = j.billamount,desc =j.desc,acccode = j.acccode,userid = varuser)
                                savebill.save()
                        if tbladditionalbill.objects.filter(session = session,admissionno = st.admissionno,klass = klass,term = term).count() == 0:
                            varrid2 = 0
                            getaddbill = ''
                        else:
                            getaddbill = tbladditionalbill.objects.filter(session = session,admissionno = st.admissionno,klass = klass,term = term)
                            for h in getaddbill:
                                particulars = '%s for %s %s Term'%(h.desc,session,term)
                                postacc(transdate,st.admissionno,h.acccode,h.billamount,particulars,vartransid,varrecid,varuser)
                                savebill = oldbill(session = session,admissionno = st.admissionno,name = st.fullname,klass = klass,arm = st.admitted_arm,term = term,billamount = h.billamount,desc =h.desc,acccode = h.acccode,userid = varuser)
                                savebill.save()
                    post = postedbill(session = session,klass = klass,term = term,userid = varuser)
                    post.save()
                    return render_to_response('posting/invsuccess.htm',{'varuser':varuser,'varerr':varerr,'vartransid':vartransid})
            else:
                return HttpResponseRedirect('/SchApp/account/posting/invoice/')
    else:
        return HttpResponseRedirect('/login/')


def pocketmoney(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.genledger
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/posting/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
            form = pocketform(request.POST) # A form bound to the POST data
            if form.is_valid():
                cusname = form.cleaned_data['cusname']
                cuscode = form.cleaned_data['cuscode'] #customer code
                amount = form.cleaned_data['transamount']
                particular = form.cleaned_data['particulars']
                caldate1 = form.cleaned_data['transdate']#date picked
                acccode = form.cleaned_data['acccode']
                accname = form.cleaned_data['accname']
                invoiceno = form.cleaned_data['invoiceno']
                caldate2 = caldate1.split('/')
                transdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                varget = tbltempreceipt.objects.filter(userid = varuser).count()
                #**********************************************************getting the date
                if tblcalender.objects.all().count() == 0:
                    varerr = "NO START DATE"
                    getdetails = tbltemppocket.objects.filter(userid = varuser).order_by('id')
                    return render_to_response('posting/pocketmoney.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

                #getdate = tblcalender.objects.all()
                #for g in getdate:
                 #   stdate = g.startmonth
                  #  endate = g.endtmonth
               # if transdate < stdate or transdate > endate :
                #    varerr = "INVALID DATE"
                 #   getdetails = tbltemppocket.objects.filter(userid = varuser).order_by('id')
                  #  return render_to_response('posting/pocketmoney.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                    #*************************************************************************
                ks = tblcontrol.objects.all()
                for p in ks:
                    s = p.acccode
                    if cuscode == s:
                        varerr = "YOU CAN NOT POST INTO ONE OF THIS ACCOUNT"
                        getdetails = tbltemppocket.objects.filter(userid = varuser).order_by('id')
                        return render_to_response('posting/pocketmoney.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                    if acccode == s:
                        varerr = "YOU CAN NOT POST INTO ONE OF THIS ACCOUNT"
                        getdetails = tbltemppocket.objects.filter(userid = varuser).order_by('id')
                        return render_to_response('posting/pocketmoney.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

                #************************************************************
                if varget == 0 :
                    used = tbltemppocket(cusname = cusname,cuscode = cuscode,amount = amount,particular = particular,transdate = transdate,accname = accname,acccode = acccode,userid = varuser,drcr = "CR",invoiceno = invoiceno )
                    used.save()
                else:
                    varerr = "Invalid Receipt Transaction"
                    getdetails = tbltemppocket.objects.filter(userid = varuser).order_by('id')
                    return render_to_response('posting/pocketmoney.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                #*****************************
                getdetails = tbltemppocket.objects.filter(userid = varuser).order_by('id')
                #now i do insertion
                return HttpResponseRedirect('/SchApp/account/posting/pocketmoney/')

        else:

            form = pocketform()
            getdetails = tbltemppocket.objects.filter(userid = varuser).order_by('transdate')
        return render_to_response('posting/pocketmoney.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')

def getpocketm(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tbltemppocket.objects.get(id = acccode)
                return render_to_response('posting/editpocket.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def deletepocket(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        seldata = tbltemppocket.objects.get(id = invid)
        seldata.delete()
        return HttpResponseRedirect('/SchApp/account/posting/pocketmoney/')
    else:
        return HttpResponseRedirect('/login/')

def pocketprocess(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        vardate1 = date.today()
        if tbltemppocket.objects.filter(userid = varuser).count() == 0 :
            return HttpResponseRedirect('/SchApp/account/posting/pocketmoney/')
        else:
            ll = []
            lk = ""
            vardata = tbltemppocket.objects.filter(userid = varuser)
            cuspart =""
            custo = 0
            for j in vardata:
                lk = j.cusname,j.cuscode,j.accname,j.acccode,j.transdate,j.invoiceno,j.userid,j.particular,j.amount,j.id
                ll.append(lk)
                vardate1 = j.transdate
            varyear = vardate1.year
            #**************************************************************getting transid
            #***************************************
            kt = gettransid(varyear)
            if tbltransactiontemp.objects.filter(transdate__year = varyear).count() == 0 :
                varrid = 1
            else:
                varrid1 = tbltransactiontemp.objects.filter(transdate__year = varyear).aggregate(Max('recid'))
                varrid = varrid1['recid__max']
                varrid = int(varrid)
            if kt > varrid:
                varrid =  kt + 1
            else:
                varrid  += 1
            vyear =  str(varyear)
            vayear = vyear[2]+ vyear[3]
            vartransid = str(vayear)+ str(varrid) #trans id
            varrecid = int(varrid)
            k = range(len(ll))
            we =[]
            for h in k:
                for m in ll[h]:
                    we.append(m)
                    #**************************************
                cusno = we[1]
                cusname = we[0]
                refno = we[5]
                vardate = we[4]
                varyear = vardate.year
                userid = we[6]
                accname = we[2]
                acccode = we[3]
                part = we[7]
                amount = we[8]
                rid = we[9]

                #******************************************************
                custo =  amount
                #vyear =  str(varyear)
                #vayear = vyear[2]+ vyear[3]
                #vartransid = str(vayear)+ str(varrid) #trans id
                #varrecid = varrid # my recid
                #**************************************************************************
                cusdet =  tblaccount.objects.get(acccode = cusno)# bank CR
                cusbal = cusdet.accbal
                cusgrp = cusdet.groupname
                cussub = cusdet.subgroupname
                if cusgrp == "FIXED ASSETS" or cusgrp == "CURRENT ASSETS" or cusgrp == "EXPENSES" or cusgrp == "COST OF SALES":
                    cusbal = cusbal - custo
                else:
                    cusbal = cusbal + custo
                    #***********************************************
                used = tbltransaction(accname = cusname,acccode = cusno,debit = 0,credit = custo,balance = cusbal,transid = vartransid,transdate = vardate,particulars = part,refno = refno,groupname = cusgrp,subname = cussub ,userid = userid,recid = varrecid )
                used.save()
                #********************
                selsubdata = tblaccount.objects.get(acccode = cusno)
                selsubdata.accbal = cusbal
                selsubdata.lasttrandate = vardate
                selsubdata.save()
                #**********************************
                #***************************************
                cusdet1 =  tblaccount.objects.get(acccode = acccode)
                bal = cusdet1.accbal
                grp = cusdet1.groupname
                sub = cusdet1.subgroupname
                if grp == "FIXED ASSETS" or grp == "CURRENT ASSETS" or grp == "EXPENSES" or grp == "COST OF SALES":
                    cusbal1 = bal + amount
                else:
                    cusbal1 = bal - amount

                    #***********************************************8
                used = tbltransaction(accname = accname,acccode = acccode,debit = amount,credit = 0,balance = cusbal1,transid = vartransid,transdate = vardate,particulars = part,refno = refno,groupname = grp,subname = sub ,userid = userid, recid = varrecid )
                used.save()
                #********************update
                selsubdata1 = tblaccount.objects.get(acccode = acccode)
                selsubdata1.accbal = cusbal1
                selsubdata1.lasttrandate = vardate
                selsubdata1.save()
                we.remove(accname)
                we.remove(acccode)
                we.remove(part)
                we.remove(amount)
                we.remove(cusno)
                we.remove(cusname)
                we.remove(refno)
                we.remove(vardate)
                we.remove(userid)
                we.remove(rid)
                tbltemppocket.objects.filter(userid = varuser).delete()
            return render_to_response('posting/invsuccess.htm',{'varuser':varuser,'varerr':varerr,'vartransid':vartransid})

    else:
        return HttpResponseRedirect('/login/')


def printreceipt(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.receipt
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/posting/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
            form = verifytransform(request.POST) # A form bound to the POST data
            if form.is_valid():
                transid = form.cleaned_data['transid']
                tid = 1
                vdate = ''
                amt  = 0
                part = ''
                refno = ''
                accname = ''
                vartransid = ''
                groupname = ''
                subname = ''
                if tbltransaction.objects.filter(transid = transid) :
                    trans = tbltransaction.objects.filter(transid = transid)
                    k = len(trans)
                    if k > 2:
                       varerr ='Invalid Receipt Transaction'
                       return render_to_response('posting/oldreceipt.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                    else:
                        varerr = ''
                        for j in trans:
                          amt = j.credit
                          if amt == 0:
                             pass
                          else:
                             vdate = j.transdate
                             amt = j.credit
                             part = j.particulars
                             refno = j.refno
                             accname = j.accname
                             vartransid = j.transid
                             groupname =j.groupname
                             subname = j.subname
                             break
                        if groupname  == 'CURRENT ASSETS' and subname =='RECEIVABLES':
                            pass
                        else:
                            varerr ='Invalid Receipt Transaction'
                            return render_to_response('posting/oldreceipt.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

                    new = locale.format("%.2f",float(amt),grouping=True)
                    k1 = new.replace(',','')
                    figwd = main(k1)
                    comp = tblcompanyinfo.objects.get(id = 1)
                    return render_to_response('posting/printreceipt.htm',{'varuser':varuser,'varerr':varerr,'vartransid':vartransid,'amount':new,'fig2wd':figwd,'vdate':vdate.strftime("%d-%m-%Y"),'particulars':part,'cusname':accname,'school':comp,'refno':refno})
                else:
                    varerr ='Invalid Receipt Transaction'
                    return render_to_response('posting/oldreceipt.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))


        else:
            form = verifytransform()
        return render_to_response('posting/oldreceipt.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')





