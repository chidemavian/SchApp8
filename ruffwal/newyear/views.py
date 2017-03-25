# Create your views here.
from django.template import loader, Context,RequestContext
from django.shortcuts import render_to_response
from django.http import  HttpResponseRedirect
from myproject.ruffwal.posting.form import *
from myproject.ruffwal.rsetup.models import *
from myproject.ruffwal.rwadmin.models import *
from myproject.ruffwal.newyear.models import *
from myproject.utilities.views import *
from django.db.models import Max,Sum
from myproject.ruffwal.posting.fig2wd import *
from datetime import date,time
import locale
locale.setlocale(locale.LC_ALL,'')

def tempenterposting(request):
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.eposting
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/welcome/')
        varerr =""
        return render_to_response('newyear/enterposting.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')

def tempinvoice(request):
     varerr =""
     if  "userid" in request.session:
       if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.invoice
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/newyear/unauto/')
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
             varget = tbltemp1.objects.filter(userid = varuser).count()
             ks = tblcontrol.objects.all()
             for p in ks:
                 s = p.acccode
                 if cuscode == s:
                    varerr = "YOU CAN NOT POST INTO ONE OF THIS ACCOUNT"
                    getdetails = tbltemp1.objects.filter(userid = varuser).order_by('id')
                    return render_to_response('newyear/invoice.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                 if acccode == s:
                    varerr = "YOU CAN NOT POST INTO ONE OF THIS ACCOUNT"
                    getdetails = tbltemp1.objects.filter(userid = varuser).order_by('id')
                    return render_to_response('newyear/invoice.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             if tblcalender.objects.all().count() == 0:
                 varerr = "NO START DATE"
                 getdetails = tbltemp1.objects.filter(userid = varuser).order_by('id')
                 return render_to_response('newyear/invoice.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

             getdate = tblcalender.objects.all()
             stdate = date.today()
             endate = date.today()
             for g in getdate:
                 stdate = g.startmonth
                 endate = g.endtmonth
                 #*******************************
             varyear = stdate.year + 1
             varmon = stdate.month
             varday = stdate.day
             stdate = date(varyear,varmon,varday)#the startdate + 1 i.e new year
             varyear1 = endate.year + 1
             varmon1 = endate.month
             varday1 = endate.day
             endate = date(varyear1,varmon1,varday1)#the endate + 1 i.e new year
             if transdate < stdate or transdate > endate :
                 varerr = "INVALID DATE"
                 getdetails = tbltemp1.objects.filter(userid = varuser).order_by('id')
                 return render_to_response('newyear/invoice.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

             if varget == 0 :
                used = tbltemp1(cusname = cusname,cuscode = cuscode,amount = amount,particular = particular,transdate = transdate,accname = accname,acccode = acccode,userid = varuser,drcr = "CR",invoiceno = invoiceno )
                used.save()
             else:
                    vargetnew = tbltemp1.objects.filter(cuscode=cuscode).count()
                    if vargetnew == 0:
                        varerr = "Invalid Invoice Transaction"
                        getdetails = tbltemp1.objects.filter(userid = varuser).order_by('id')
                        return render_to_response('newyear/invoice.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                    else:
                        used = tbltemp1(cusname = cusname,cuscode = cuscode,amount = amount,particular = particular,transdate = transdate,accname = accname,acccode = acccode,userid = varuser,drcr = "CR",invoiceno = invoiceno )
                        used.save()
                        return HttpResponseRedirect('/SchApp/account/newyear/invoice/')

             #*****************************
             getdetails = tbltemp1.objects.filter(userid = varuser).order_by('id')
             return HttpResponseRedirect('/SchApp/account/newyear/invoice/')
             #now i do insertion
             return render_to_response('newyear/invoice.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:

            form = invoiceform()
            getdetails = tbltemp1.objects.filter(userid = varuser).order_by('transdate')
        return render_to_response('newyear/invoice.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')

def tempeditinvoice(request,invid):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.invoice
            if int(uenter) == 0 :
              return HttpResponseRedirect('/SchApp/account/newyear/unauto/')
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
                    #getdetails = tbltemp1.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    #return render_to_response('newyear/editinvoice.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                    return HttpResponseRedirect('/SchApp/account/newyear/invoice/')

                try:
                    k = float(amount)
                except:
                    #varerr = "INVALID AMOUNT"
                    #getdetails = tbltemp1.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    #return render_to_response('newyear/editinvoice.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                    return HttpResponseRedirect('/SchApp/account/newyear/invoice/')

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
                     #getdetails = tbltemp1.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                     #return render_to_response('newyear/editinvoice.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                    return HttpResponseRedirect('/SchApp/account/newyear/invoice/')
                getdate = tblcalender.objects.all()
                stdate = date.today()
                endate = date.today()
                for g in getdate:
                   stdate = g.startmonth
                   endate = g.endtmonth
                varyear = stdate.year + 1
                varmon = stdate.month
                varday = stdate.day
                stdate = date(varyear,varmon,varday)#the startdate + 1 i.e new year
                varyear1 = endate.year + 1
                varmon1 = endate.month
                varday1 = endate.day
                endate = date(varyear1,varmon1,varday1)#the endate + 1 i.e new year
                if vdate < stdate or vdate > endate :
                   #varerr = "INVALID DATE"
                   #getdetails = tbltemp1.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                   #return render_to_response('newyear/editinvoice.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                   return HttpResponseRedirect('/SchApp/account/newyear/invoice/')
                #********************
                seldata = tbltemp1.objects.get(id = accno)
                seldata.amount = amount
                seldata.particular = particular
                seldata.transdate = vdate

                seldata.invoiceno = invoiceno
                seldata.save()
                return HttpResponseRedirect('/SchApp/account/newyear/invoice/')
            else:
                try:
                  getdetails = tbltemp1.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                  return render_to_response('newyear/editinvoice.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                except:
                    varerr = "Account Not Exist"
                    return render_to_response('newyear/editinvoice.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
        else:
         return HttpResponseRedirect('/login/')

def tempdeleteinvoice(request,invid):
    varerr =""
    if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            #if request.method == 'POST':

            #accno = request.POST['hcode']#the primary key

            seldata = tbltemp1.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/SchApp/account/newyear/invoice/')
            #else:
             #   return HttpResponseRedirect('/posting/invoice/')


    else:
      return HttpResponseRedirect('/login/')

def temptestajax(request):
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

                   return render_to_response('newyear/testajax.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = ""
                   return render_to_response('newyear/testajax.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('newyear/testajax.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')


def temptestajaxcode(request):
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

                   return render_to_response('newyear/testajax.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = ""
                   return render_to_response('newyear/testajax.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('newyear/testajax.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')
def tempprocess(request):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            varyear = date.today()
            if tbltemp1.objects.filter(userid = varuser).count() == 0 :
                return HttpResponseRedirect('/SchApp/account/newyear/invoice/')
            else:
                ll = []
                lk = ""
                vardata = tbltemp1.objects.filter(userid = varuser)
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
                vartransid = str(vayear)+ str(varrid) #trans id
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
                used = tbltransactiontemp(accname = cusname,acccode = cusno,debit = custo,credit = 0,balance = cusbal,transid = vartransid,transdate = vardate,particulars = cuspart,refno = refno,groupname = cusgrp,subname = cussub ,userid = userid,recid = varrecid )
                used.save()
##                #********************
##                selsubdata = tblaccount.objects.get(acccode = cusno)
##                selsubdata.accbal = cusbal #
##                selsubdata.lasttrandate = vardate
##                selsubdata.save()
##                #**********************************
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
                  used = tbltransactiontemp(accname = accname,acccode = acccode,debit = 0,credit = amount,balance = cusbal1,transid = vartransid,transdate = vardate,particulars = part,refno = refno,groupname = grp,subname = sub ,userid = userid, recid = varrecid )
                  used.save()
                    #********************update
##                  selsubdata1 = tblaccount.objects.get(acccode = acccode)
##                  selsubdata1.accbal = cusbal1
##                  selsubdata1.lasttrandate = vardate
##                  selsubdata1.save()
                  we.remove(accname)
                  we.remove(acccode)
                  we.remove(part)
                  we.remove(amount)
                  we.remove(rid)
                  deldata = tbltemp1.objects.filter(userid = varuser).delete()

                return render_to_response('newyear/invsuccess.htm',{'varuser':varuser,'varerr':varerr,'vartransid':vartransid})

        else:
         return HttpResponseRedirect('/login/')

def tempreceipt(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.receipt
        if int(uenter) == 0 :
              return HttpResponseRedirect('/SchApp/account/newyear/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = invoiceform(request.POST) # A form bound to the POST data
          if form.is_valid():
             cusname = form.cleaned_data['cusname']
             cuscode = form.cleaned_data['cuscode'] #customer code
             amount = form.cleaned_data['transamount']
             particular = form.cleaned_data['particulars']
             caldate1 = form.cleaned_data['transdate']
             acccode = form.cleaned_data['acccode']
             accname = form.cleaned_data['accname']
             invoiceno = form.cleaned_data['invoiceno']
             varget = tbltempreceipt1.objects.filter(userid = varuser).count()
             #************************
             caldate2 = caldate1.split('/')
             transdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
             #*************************************************************************
             ks = tblcontrol.objects.all()
             for p in ks:
                 s = p.acccode
                 if cuscode == s:
                    varerr = "YOU CAN NOT POST INTO ONE OF THIS ACCOUNT"
                    getdetails = tbltempreceipt1.objects.filter(userid = varuser).order_by('id')
                    return render_to_response('newyear/receipt.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                 if acccode == s:
                    varerr = "YOU CAN NOT POST INTO ONE OF THIS ACCOUNT"
                    getdetails = tbltempreceipt1.objects.filter(userid = varuser).order_by('id')
                    return render_to_response('newyear/receipt.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

             #**********************************************************getting the date
             if tblcalender.objects.all().count() == 0:
                 varerr = "NO START DATE" 
                 getdetails = tbltempreceipt1.objects.filter(userid = varuser).order_by('id')
                 return render_to_response('newyear/receipt.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             getdate = tblcalender.objects.all()
             stdate = date.today()
             endate = date.today()
             for g in getdate:
                 stdate = g.startmonth
                 endate = g.endtmonth
                 
             varyear = stdate.year + 1
             varmon = stdate.month
             varday = stdate.day
             stdate = date(varyear,varmon,varday)#the startdate + 1 i.e new year
             varyear1 = endate.year + 1
             varmon1 = endate.month
             varday1 = endate.day
             endate = date(varyear1,varmon1,varday1)#the endate + 1 i.e new year
             if transdate < stdate or transdate > endate :
                 varerr = "INVALID DATE "
                 getdetails = tbltempreceipt1.objects.filter(userid = varuser).order_by('id')
                 return render_to_response('newyear/receipt.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             #*************************************************************************
             if varget == 0 :
                used = tbltempreceipt1(cusname = cusname,cuscode = cuscode,amount = amount,particular = particular,transdate = transdate,accname = accname,acccode = acccode,userid = varuser,drcr = "CR",invoiceno = invoiceno )
                used.save()
             else:
                 varerr = "Invalid Receipt Transaction"
                 getdetails = tbltempreceipt1.objects.filter(userid = varuser).order_by('id')
                 return render_to_response('newyear/receipt.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                   # vargetnew = tbltempreceipt1.objects.filter(cuscode=cuscode).count()
                    #if vargetnew == 0:

                    #else:
                     #   used = tbltempreceipt1(cusname = cusname,cuscode = cuscode,amount = amount,particular = particular,transdate = transdate,accname = accname,acccode = acccode,userid = varuser,drcr = "CR",invoiceno = invoiceno )
                      #  used.save()
                       # return HttpResponseRedirect('/newyear/receipt/')
             #*****************************
             getdetails = tbltempreceipt1.objects.filter(userid = varuser).order_by('id')
             #now i do insertion
             return HttpResponseRedirect('/SchApp/account/newyear/receipt/')
             return render_to_response('newyear/receipt.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:

            form = invoiceform()
            getdetails = tbltempreceipt1.objects.filter(userid = varuser).order_by('transdate')
        return render_to_response('newyear/receipt.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')

def tempreceiptprocess(request):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            if tbltempreceipt1.objects.filter(userid = varuser).count() == 0 :
                return HttpResponseRedirect('/SchApp/account/newyear/receipt/')
            else:
                ll = []
                lk = ""
                vardata = tbltempreceipt1.objects.filter(userid = varuser)
                cuspart =""
                custo = 0
                vardate = date.today()
                cusname = ''
                userid = ''
                refno = ''
                varyear = date.today()
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
                vartransid ='R'+ str(vayear)+ str(varrid) #trans id
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
                used = tbltransactiontemp(accname = cusname,acccode = cusno,debit = 0,credit = custo,balance = cusbal,transid = vartransid,transdate = vardate,particulars = cuspart,refno = refno,groupname = cusgrp,subname = cussub ,userid = userid,recid = varrecid )
                used.save()
                #********************
##                selsubdata = tblaccount.objects.get(acccode = cusno)
##                selsubdata.accbal = cusbal
##                selsubdata.lasttrandate = vardate
##                selsubdata.save()
                #**********************************
                k = range(len(ll))

                we =[]
                new = ''
                figwd = ''
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
                  used = tbltransactiontemp(accname = accname,acccode = acccode,debit = amount,credit = 0,balance = cusbal1,transid = vartransid,transdate = vardate,particulars = part,refno = refno,groupname = grp,subname = sub ,userid = userid, recid = varrecid )
                  used.save()
                    #********************update
##                  selsubdata1 = tblaccount.objects.get(acccode = acccode)
##                  selsubdata1.accbal = cusbal1
##                  selsubdata1.lasttrandate = vardate
##                  selsubdata1.save()
                  # here i convert figure into words
                  #print 'the Amount :',amount
                  new = locale.format("%.2f",float(amount),grouping=True)
                  k1 = new.replace(',','')
                  figwd = main(k1)
                  we.remove(accname)
                  we.remove(acccode)
                  we.remove(part)
                  we.remove(amount)
                  we.remove(rid)
                  tbltempreceipt1.objects.filter(userid = varuser).delete()
                comp = tblcompanyinfo.objects.get(id = 1)
                return render_to_response('newyear/printreceipt.htm',{'varuser':varuser,'varerr':varerr,'vartransid':vartransid,'amount':new,'fig2wd':figwd,'vdate':vardate.strftime("%d-%m-%Y"),'particulars':cuspart,'cusname':cusname,'school':comp,'refno':refno})
                #return render_to_response('newyear/invsuccess.htm',{'varuser':varuser,'varerr':varerr,'vartransid':vartransid})
        else:
         return HttpResponseRedirect('/login/')

def temppayment(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.payment
        if int(uenter) == 0 :
              return HttpResponseRedirect('/SchApp/account/newyear/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = invoiceform(request.POST) # A form bound to the POST data
          if form.is_valid():
             cusname = form.cleaned_data['cusname']
             cuscode = form.cleaned_data['cuscode'] #customer code
             amount = form.cleaned_data['transamount']
             particular = form.cleaned_data['particulars']
             caldate1 = form.cleaned_data['transdate']
             acccode = form.cleaned_data['acccode']
             accname = form.cleaned_data['accname']
             invoiceno = form.cleaned_data['invoiceno']
             caldate2 = caldate1.split('/')
             transdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))

             varget = tbltemppayment1.objects.filter(userid = varuser).count()

             #*************************************************************
             ks = tblcontrol.objects.all()
             for p in ks:
                 s = p.acccode
                 if cuscode == s:
                    varerr = "YOU CAN NOT POST INTO ONE OF THIS ACCOUNT"
                    getdetails = tbltemppayment1.objects.filter(userid = varuser).order_by('id')
                    return render_to_response('newyear/payment.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                 if acccode == s:
                    varerr = "YOU CAN NOT POST INTO ONE OF THIS ACCOUNT"
                    getdetails = tbltemppayment1.objects.filter(userid = varuser).order_by('id')
                    return render_to_response('newyear/payment.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             #*******************************************
             #********************************************************

             if tblcalender.objects.all().count() == 0:
                 varerr = "NO START DATE"
                 getdetails = tbltemppayment1.objects.filter(userid = varuser).order_by('id')
                 return render_to_response('newyear/payment.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             getdate = tblcalender.objects.all()
             stdate = date.today()
             endate = date.today()
             for g in getdate:
                 stdate = g.startmonth
                 endate = g.endtmonth
             varyear = stdate.year + 1
             varmon = stdate.month
             varday = stdate.day
             stdate = date(varyear,varmon,varday)#the startdate + 1 i.e new year
             varyear1 = endate.year + 1
             varmon1 = endate.month
             varday1 = endate.day
             endate = date(varyear1,varmon1,varday1)#the endate + 1 i.e new year
             if transdate < stdate or transdate > endate :
                 varerr = "INVALID DATE"
                 getdetails = tbltemppayment1.objects.filter(userid = varuser).order_by('id')
                 return render_to_response('newyear/payment.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

             #*************************************************************
             if varget == 0 :
                used = tbltemppayment1(cusname = cusname,cuscode = cuscode,amount = amount,particular = particular,transdate = transdate,accname = accname,acccode = acccode,userid = varuser,drcr = "CR",invoiceno = invoiceno )
                used.save()
             else:
                    vargetnew = tbltemppayment1.objects.filter(cuscode=cuscode).count()
                    if vargetnew == 0:
                        varerr = "Invalid Payment Transaction"
                        getdetails = tbltemppayment1.objects.filter(userid = varuser).order_by('id')
                        return render_to_response('newyear/payment.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                    else:
                        used = tbltemppayment1(cusname = cusname,cuscode = cuscode,amount = amount,particular = particular,transdate = transdate,accname = accname,acccode = acccode,userid = varuser,drcr = "CR",invoiceno = invoiceno )
                        used.save()
                        #return HttpResponseRedirect('/posting/payment/')
             #*****************************
             getdetails = tbltemppayment1.objects.filter(userid = varuser).order_by('id')
             return HttpResponseRedirect('/SchApp/account/newyear/payment/')
             #now i do insertion
             return render_to_response('newyear/payment.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:

            form = invoiceform()
            getdetails = tbltemppayment1.objects.filter(userid = varuser).order_by('transdate')
        return render_to_response('newyear/payment.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')

def temppaymentajax(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   gdata = tblaccount.objects.filter(acccode__startswith = acccode,groupname = "CURRENT ASSETS",subgroupname ="CASH AND BANK BALANCES").order_by('acccode')
                   return render_to_response('newyear/testajax.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = ""
                   return render_to_response('newyear/testajax.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('newyear/testajax.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def temppaymentajaxcode(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   gdata = tblaccount.objects.filter(acccode__startswith = acccode).order_by('acccode')#filter(acccode__startswith = acccode,groupname = "CURRENT ASSETS",subgroupname ="CASH AND BANK BALANCES").order_by('acccode')
                   return render_to_response('newyear/testajax.htm',{'gdata':gdata,'post':post})
             else:
                   gdata = tblaccount.objects.all()
                   #gdata = ""
                   return render_to_response('newyear/testajax.htm',{'gdata':gdata})
         else:
              gdata = tblaccount.objects.all()
              #gdata = ""
              return render_to_response('newyear/testajax.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def temppaymentprocess(request):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            vardate1 = date.today()
            if tbltemppayment1.objects.filter(userid = varuser).count() == 0 :
                return HttpResponseRedirect('/SchApp/account/newyear/receipt/')
            else:
                ll = []
                lk = ""
                vardata = tbltemppayment1.objects.filter(userid = varuser)
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
                  used = tbltransactiontemp(accname = cusname,acccode = cusno,debit = 0,credit = custo,balance = cusbal,transid = vartransid,transdate = vardate,particulars = part,refno = refno,groupname = cusgrp,subname = cussub ,userid = userid,recid = varrecid )
                  used.save()
                  #********************
##                  selsubdata = tblaccount.objects.get(acccode = cusno)
##                  selsubdata.accbal = cusbal
##                  selsubdata.lasttrandate = vardate
##                  selsubdata.save()
##                  #**********************************
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
                  used = tbltransactiontemp(accname = accname,acccode = acccode,debit = amount,credit = 0,balance = cusbal1,transid = vartransid,transdate = vardate,particulars = part,refno = refno,groupname = grp,subname = sub ,userid = userid, recid = varrecid )
                  used.save()
                    #********************update
##                  selsubdata1 = tblaccount.objects.get(acccode = acccode)
##                  selsubdata1.accbal = cusbal1
##                  selsubdata1.lasttrandate = vardate
##                  selsubdata1.save()

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
                  deldata = tbltemppayment1.objects.filter(userid = varuser).delete()
                return render_to_response('newyear/invsuccess.htm',{'varuser':varuser,'varerr':varerr,'vartransid':vartransid})
        else:
         return HttpResponseRedirect('/login/')


def tempeditpayment(request,invid):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.payment
            if int(uenter) == 0 :
                return HttpResponseRedirect('/SchApp/account/newyear/unauto/')
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
                    #getdetails = tbltemppayment1.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    #return render_to_response('newyear/editpayment.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                    return HttpResponseRedirect('/SchApp/account/newyear/payment/')
                #***********GETTING THE DATE
                try:
                    k = float(amount)
                except:
                    #varerr = "INVALID AMOUNT"
                    #getdetails = tbltemppayment1.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    #return render_to_response('newyear/editpayment.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                    return HttpResponseRedirect('/SchApp/account/newyear/payment/')
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
                     #getdetails = tbltemppayment1.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                     #return render_to_response('newyear/editpayment.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                     return HttpResponseRedirect('/SchApp/account/newyear/payment/')
                getdate = tblcalender.objects.all()
                stdate = date.today()
                endate = date.today()
                for g in getdate:
                   stdate = g.startmonth
                   endate = g.endtmonth
                varyear = stdate.year + 1
                varmon = stdate.month
                varday = stdate.day
                stdate = date(varyear,varmon,varday)#the startdate + 1 i.e new year
                varyear1 = endate.year + 1
                varmon1 = endate.month
                varday1 = endate.day
                endate = date(varyear1,varmon1,varday1)#the endate + 1 i.e new year
                if vdate < stdate or vdate > endate :
                   #varerr = "INVALID DATE"
                   #getdetails = tbltemppayment1.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                   #return render_to_response('newyear/editpayment.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                   return HttpResponseRedirect('/SchApp/account/newyear/payment/')
                #********************
                seldata = tbltemppayment1.objects.get(id = accno)
                seldata.amount = amount
                seldata.particular = particular
                seldata.transdate = vdate
                seldata.invoiceno = invoiceno
                seldata.save()
                return HttpResponseRedirect('/SchApp/account/newyear/payment/')
            else:
                try:
                  getdetails = tbltemppayment1.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                  return render_to_response('newyear/editpayment.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                except:
                    varerr = "Account Not Exist"
                    return render_to_response('newyear/editpayment.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
        else:
         return HttpResponseRedirect('/login/')

def tempdeletepayment(request,invid):
    varerr =""
    if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            #if request.method == 'POST':

            #accno = request.POST['hcode']#the primary key

            seldata = tbltemppayment1.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/SchApp/account/newyear/payment/')
            #else:
             #   return HttpResponseRedirect('/posting/invoice/')
    else:
      return HttpResponseRedirect('/login/')

def tempeditreceipt(request,invid):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.receipt
            if int(uenter) == 0 :
               return HttpResponseRedirect('/SchApp/account/newyear/unauto/')
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
                    #getdetails = tbltempreceipt1.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    #return render_to_response('newyear/editreceipt.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                    return HttpResponseRedirect('/SchApp/account/newyear/receipt/')
                #***********GETTING THE DATE
                try:
                    k = float(amount)
                except:
                    #varerr = "INVALID AMOUNT"
                    #getdetails = tbltempreceipt1.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    #return render_to_response('newyear/editreceipt.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                    return HttpResponseRedirect('/SchApp/account/newyear/receipt/')
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
                     #getdetails = tbltempreceipt1.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                     #return render_to_response('newyear/editreceipt.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                     return HttpResponseRedirect('/SchApp/account/newyear/receipt/')
                getdate = tblcalender.objects.all()
                stdate = date.today()
                endate = date.today()
                for g in getdate:
                   stdate = g.startmonth
                   endate = g.endtmonth
                varyear = stdate.year + 1
                varmon = stdate.month
                varday = stdate.day
                stdate = date(varyear,varmon,varday)#the startdate + 1 i.e new year
                varyear1 = endate.year + 1
                varmon1 = endate.month
                varday1 = endate.day
                endate = date(varyear1,varmon1,varday1)#the endate + 1 i.e new year
                if vdate < stdate or vdate > endate :
                   #varerr = "INVALID DATE"
                   #getdetails = tbltempreceipt1.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                   #return render_to_response('newyear/editreceipt.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                   return HttpResponseRedirect('/SchApp/account/newyear/receipt/')
                #********************
                seldata = tbltempreceipt1.objects.get(id = accno)
                seldata.amount = amount
                seldata.particular = particular
                seldata.transdate = vdate
                seldata.invoiceno = invoiceno
                seldata.save()
                return HttpResponseRedirect('/SchApp/account/newyear/receipt/')
            else:
                try:
                  getdetails = tbltempreceipt1.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                  return render_to_response('newyear/editreceipt.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                except:
                    varerr = "Account Not Exist"
                    return render_to_response('newyear/editreceipt.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
        else:
         return HttpResponseRedirect('/login/')

def tempdeletereceipt(request,invid):
    varerr =""
    if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            #if request.method == 'POST':

            #accno = request.POST['hcode']#the primary key

            seldata = tbltempreceipt1.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/SchApp/account/newyear/receipt/')
            #else:
             #   return HttpResponseRedirect('/posting/invoice/')
    else:
      return HttpResponseRedirect('/login/')


def tempgeneraljournal1(request):
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
             caldate1 = form.cleaned_data['drtransdate']
             caldate2 = caldate1.split('/')
             drtransdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))

              #*****************************************
             ks = tblcontrol.objects.all()
             for p in ks:
                 s = p.acccode
                 if dracccode == s:
                    varerr = "YOU CAN NOT POST INTO THIS ACCOUNT"
                    varrid1 = tbljournal1.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
                    vardebit = varrid1['dr__sum']
                    varcredit = varrid1['cr__sum']
                    return render_to_response('newyear/journal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))
             #****************************************************
             if tblcalender.objects.all().count() == 0:
                 varerr ="INVALID DATE"
                 varrid1 = tbljournal1.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
                 vardebit = varrid1['dr__sum']
                 varcredit = varrid1['cr__sum']
                 return render_to_response('newyear/journal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))
             getdate = tblcalender.objects.all()
             stdate = date.today()
             endate = date.today()
             for g in getdate:
                 stdate = g.startmonth
                 endate = g.endtmonth
             varyear = stdate.year + 1
             varmon = stdate.month
             varday = stdate.day
             stdate = date(varyear,varmon,varday)#the startdate + 1 i.e new year
             varyear1 = endate.year + 1
             varmon1 = endate.month
             varday1 = endate.day
             endate = date(varyear1,varmon1,varday1)#the endate + 1 i.e new year
             if drtransdate < stdate or drtransdate > endate :
                 varerr ="INVALID DATE"
                 varrid1 = tbljournal1.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
                 vardebit = varrid1['dr__sum']
                 varcredit = varrid1['cr__sum']
                 return render_to_response('newyear/journal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))
             #***************************************
             if tbljournal1.objects.filter(userid = varuser).count() == 0:
                 used = tbljournal1(accname = draccname,acccode = dracccode,particular = drparticulars,transdate = drtransdate,dr = dramount,cr = 0,userid = varuser,refno = drrefno )
                 used.save()
             else:
                 varmonth = drtransdate.month
                 varyear = drtransdate.year
                 if tbljournal1.objects.filter(userid = varuser,transdate__month = varmonth,transdate__year = varyear).count() == 0:
                      varerr ="INVALID DATE"
                      varrid1 = tbljournal1.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
                      vardebit = varrid1['dr__sum']
                      varcredit = varrid1['cr__sum']
                      return render_to_response('newyear/journal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))
                 else:
                      used = tbljournal1(accname = draccname,acccode = dracccode,particular = drparticulars,transdate = drtransdate,dr = dramount,cr = 0,userid = varuser,refno = drrefno )
                      used.save()
             #*****************************
             getdetails = tbljournal1.objects.filter(userid = varuser).order_by('id')
             #now i do insertion
             if tbljournal1.objects.filter(userid = varuser).count() == 0 :
               vardebit = 0
               varcredit = 0
             else:
               varrid1 = tbljournal1.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
               vardebit = varrid1['dr__sum']
               varcredit = varrid1['cr__sum']
             return HttpResponseRedirect('/SchApp/account/newyear/generaljournal/')
             #return render_to_response('posting/journal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))
        else:
            getdetails = ""
            form = ledgerform()
            form2 = ledgerform2()
            if tbljournal1.objects.filter(userid = varuser).count() == 0 :
               vardebit = 0
               varcredit = 0
            else:
               varrid1 = tbljournal1.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
               vardebit = varrid1['dr__sum']
               varcredit = varrid1['cr__sum']
        return render_to_response('newyear/journal.htm',{'varuser':varuser,'varerr':varerr,'form2':form2,'form':form,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')
def tempgeneraljournal2(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        getdetails =""
        if tbljournal1.objects.filter(userid = varuser).count() == 0 :
               vardebit = 0
               varcredit = 0
        else:
              varrid1 = tbljournal1.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
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
             #***************************************
             ks = tblcontrol.objects.all()
             for p in ks:
                 s = p.acccode
                 if cracccode == s:
                    varerr = "YOU CAN NOT POST INTO THIS ACCOUNT"
                    varrid1 = tbljournal1.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
                    vardebit = varrid1['dr__sum']
                    varcredit = varrid1['cr__sum']
                    return render_to_response('newyear/journal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))

             #****************************************************
             if tblcalender.objects.all().count() == 0:
                 varerr ="INVALID DATE"
                 varrid1 = tbljournal1.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
                 vardebit = varrid1['dr__sum']
                 varcredit = varrid1['cr__sum']
                 return render_to_response('newyear/journal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))
             getdate = tblcalender.objects.all()
             stdate = date.today()
             endate = date.today()
             for g in getdate:
                 stdate = g.startmonth
                 endate = g.endtmonth
             varyear = stdate.year + 1
             varmon = stdate.month
             varday = stdate.day
             stdate = date(varyear,varmon,varday)#the startdate + 1 i.e new year
             varyear1 = endate.year + 1
             varmon1 = endate.month
             varday1 = endate.day
             endate = date(varyear1,varmon1,varday1)#the endate + 1 i.e new year
             if crtransdate < stdate or crtransdate > endate :
                 varerr ="INVALID DATE"
                 varrid1 = tbljournal1.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
                 vardebit = varrid1['dr__sum']
                 varcredit = varrid1['cr__sum']
                 return render_to_response('newyear/journal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))
             #***************************************
             if tbljournal1.objects.filter(userid = varuser).count() == 0:
                  used = tbljournal1(accname = craccname,acccode = cracccode,particular = crparticulars,transdate = crtransdate,dr = 0,cr = cramount,userid = varuser,refno = crrefno )
                  used.save()
             else:
                 varmonth = crtransdate.month
                 varyear = crtransdate.year
                 if tbljournal1.objects.filter(userid = varuser,transdate__month = varmonth,transdate__year = varyear).count() == 0:
                      varerr ="INVALID DATE"
                      varrid1 = tbljournal1.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
                      vardebit = varrid1['dr__sum']
                      varcredit = varrid1['cr__sum']
                      return render_to_response('newyear/journal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))
                 else:
                       used = tbljournal1(accname = craccname,acccode = cracccode,particular = crparticulars,transdate = crtransdate,dr = 0,cr = cramount,userid = varuser,refno = crrefno )
                       used.save()

             #*****************************
             getdetails = tbljournal1.objects.filter(userid = varuser).order_by('id')
             if tbljournal1.objects.filter(userid = varuser).count() == 0 :
               vardebit = 0
               varcredit = 0
             else:
               varrid1 = tbljournal1.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
               vardebit = varrid1['dr__sum']
               varcredit = varrid1['cr__sum']
             #now i do insertion
             return HttpResponseRedirect('/SchApp/account/newyear/generaljournal/')
             #return render_to_response('posting/journal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))
        else:
            getdetails=""
            #return HttpResponseRedirect('/posting/generaljournal/')
            form = ledgerform()
            form2 = ledgerform2()
            if tbljournal1.objects.filter(userid = varuser).count() == 0 :
               vardebit = 0
               varcredit = 0
            else:
               varrid1 = tbljournal1.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
               vardebit = varrid1['dr__sum']
               varcredit = varrid1['cr__sum']
        return render_to_response('newyear/journal.htm',{'varuser':varuser,'varerr':varerr,'form2':form2,'form':form,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def tempgeneraljournal(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.genledger
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/newyear/unauto/')
        varerr =""
        getdetails =""
        form = ledgerform()
        form2 = ledgerform2()
        if tbljournal1.objects.filter(userid = varuser).count() == 0 :
               vardebit = 0
               varcredit = 0
        else:
               varrid1 = tbljournal1.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
               vardebit = varrid1['dr__sum']
               varcredit = varrid1['cr__sum']
        getdetails = tbljournal1.objects.filter(userid = varuser).order_by('id')
        return render_to_response('newyear/journal.htm',{'varuser':varuser,'varerr':varerr,'form':form,'form2':form2,'getdetails':getdetails,'vardebit':vardebit,'varcredit':varcredit},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')

def tempeditjournal(request,invid):
    varerr =""
    if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.genledger
            if int(uenter) == 0 :
              return HttpResponseRedirect('/SchApp/account/newyear/unauto/')
            varerr =""
            #if request.method == 'POST':

            #accno = request.POST['hcode']#the primary key

            seldata = tbljournal1.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/SchApp/account/newyear/generaljournal/')
            #else:
             #   return HttpResponseRedirect('/posting/invoice/')
    else:
      return HttpResponseRedirect('/login/')

def tempjournalprocess(request):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            if tbljournal1.objects.filter(userid = varuser).count() == 0 :
                return HttpResponseRedirect('/SchApp/account/newyear/generaljournal/')
            else:
                varrid1 = tbljournal1.objects.filter(userid = varuser).aggregate(Sum('dr'),Sum('cr'))
                vardebit = varrid1['dr__sum']
                varcredit = varrid1['cr__sum']
                vardate1 = date.today()
                if vardebit == varcredit:
                    ll = []
                    lk = ""
                    vardata = tbljournal1.objects.filter(userid = varuser)
                    cuspart =""
                    custo = 0
                    for j in vardata:
                        lk = j.accname,j.acccode,j.particular,j.transdate,j.dr,j.cr,j.userid,j.refno,j.id
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
                      used = tbltransactiontemp(accname = accname,acccode = accno,debit = dr,credit = cr,balance = cusbal,transid = vartransid,transdate = vardate,particulars = part,refno = refno,groupname = cusgrp,subname = cussub ,userid = userid,recid = varrecid )
                      used.save()
                      #********************
##                      selsubdata = tblaccount.objects.get(acccode = accno)
##                      selsubdata.accbal = cusbal
##                      selsubdata.lasttrandate = vardate
##                      selsubdata.save()
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
                    deldata = tbljournal1.objects.filter(userid = varuser).delete()

                    return render_to_response('newyear/invsuccess.htm',{'varuser':varuser,'varerr':varerr,'vartransid':vartransid})
                else:
                    return HttpResponseRedirect('/SchApp/account/newyear/generaljournal/')

        else:
         return HttpResponseRedirect('/login/')

def tempstandardjournal(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.standardledger
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/newyear/unauto/')
        varerr =""
        getdetails =""
        if tbltransactiontemp.objects.all().count() == 0:
           return render_to_response('newyear/standard.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
           getdetails = tbltransactiontemp.objects.all().order_by('recid')
           return render_to_response('newyear/standard.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')

def tempeditstandard(request,invid):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.standardledger
            if int(uenter) == 0 :
                return HttpResponseRedirect('/SchApp/account/newyear/unauto/')
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
                if acccode == cracccode :
                    varerr ="INVALID TRANSACTION"
                    getdetails = tblstandard1.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                    return render_to_response('newyear/editstandard.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                else:
                    if particular == "" or refno == "" or amount == "" :
                      varerr = "INVALID TRANSACTION"
                      getdetails = tblstandard1.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                      return render_to_response('newyear/editstandard.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                #***********GETTING THE DATE
                    try:
                        k = float(amount)
                    except:
                        varerr = "INVALID AMOUNT"
                        getdetails = tblstandard1.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                        return render_to_response('newyear/editstandard.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                    seldata = tblstandard1.objects.get(id = accno)
                    seldata.accname = accname
                    seldata.acccode = acccode
                    seldata.particular = particular
                    seldata.amount = amount
                    seldata.refno = refno
                    seldata.craccname = craccname
                    seldata.cracccode = cracccode
                    seldata.duration = duration
                    seldata.save()
                    return HttpResponseRedirect('/SchApp/account/newyear/standardjournal/')
            else:
                try:
                  getdetails = tblstandard1.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                  return render_to_response('newyear/editstandard.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                except:
                    varerr = "Account Not Exist"
                    return render_to_response('newyear/editstandard.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
        else:
         return HttpResponseRedirect('/login/')

def tempdeletestandard(request,invid):
    varerr =""
    if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""

            seldata = tblstandard1.objects.get(id = invid)
            seldata.delete()
            return HttpResponseRedirect('/SchApp/account/newyear/standardjournal/')

    else:
      return HttpResponseRedirect('/login/')

def tempstardardprocess(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = prostandardform(request.POST) # A form bound to the POST data
          if form.is_valid():
             transdate = form.cleaned_data['monthly']
             vardate1 = transdate
             varrmonth = transdate.month
             varryear = transdate.year
             #*******************************************************
             #**********************************************************getting the date
             if tblcalender.objects.all().count() == 0:
                 varerr = "NO START DATE"
                 #varerr ="This Month/Year Has been Process"
                 getdetails = tblstandard1.objects.all().order_by('id')
                 return render_to_response('newyear/standardprocess.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             getdate = tblcalender.objects.all()
             stdate = date.today()
             endate = date.today()
             for g in getdate:
                 stdate = g.startmonth
                 endate = g.endtmonth
             varyear = stdate.year + 1
             varmon = stdate.month
             varday = stdate.day
             stdate = date(varyear,varmon,varday)#the startdate + 1 i.e new year
             varyear1 = endate.year + 1
             varmon1 = endate.month
             varday1 = endate.day
             endate = date(varyear1,varmon1,varday1)#the endate + 1 i.e new year
             if transdate < stdate or transdate > endate :
                 varerr = "INVALID DATE"
                 #varerr ="This Month/Year Has been Process"
                 getdetails = tblstandard1.objects.all().order_by('id')
                 return render_to_response('newyear/standardprocess.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             #print varrmonth,varryear
             #print vardate1
             if tblstandard1.objects.all().count() == 0 :
                return HttpResponseRedirect('/SchApp/account/newyear/standardjournal/')
             else:
                try:
                    ttry = tblstandarddate1.objects.get(transdate__year = varryear,transdate__month = varrmonth)
                    varerr ="This Month/Year Has been Process"
                    getdetails = tblstandard1.objects.all().order_by('id')
                    return render_to_response('newyear/standardprocess.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                except:
                    ll = []
                    lk = ""
                    vardata = tblstandard1.objects.all()
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
                      used = tbltransactiontemp(accname = draccname,acccode = draccno,debit = custo,credit = 0,balance = cusbal,transid = vartransid,transdate = transdate,particulars = part,refno = refno,groupname = cusgrp,subname = cussub ,userid = varuser,recid = varrecid )
                      used.save()
                      #********************
##                      selsubdata = tblaccount.objects.get(acccode = draccno)
##                      selsubdata.accbal = cusbal
##                      selsubdata.lasttrandate = transdate
##                      selsubdata.save()
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
                      used1 = tbltransactiontemp(accname = craccname,acccode = cracccode,debit = 0,credit = custo,balance = cusbal1,transid = vartransid,transdate = transdate,particulars = part,refno = refno,groupname = cusgrp1,subname = cussub1 ,userid = varuser,recid = varrecid )
                      used1.save()
                      #********************
##                      selsubdata1 = tblaccount.objects.get(acccode = cracccode)
##                      selsubdata1.accbal = cusbal1
##                      selsubdata1.lasttrandate = transdate
##                      selsubdata1.save()
                      #********************************** update the standard table
                      duration1 =  duration - 1
                      if duration1 == 0 :
                          deldata = tblstandard1.objects.filter(id = rid).delete()
                      else:
                           selsubdata11 = tblstandard1.objects.get(id = rid)
                           selsubdata11.duration = duration1
                           selsubdata11.save()
                      used11 = tblstandarddate1(transdate = vardate1,userid = varuser)
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
                return HttpResponseRedirect('/SchApp/account/newyear/standardjournal/')
        else:
            if tblstandard1.objects.all().count()== 0:
                return HttpResponseRedirect('/SchApp/account/newyear/standardjournal/')
            form = prostandardform()
            getdetails = tblstandard1.objects.all().order_by('id')
        return render_to_response('newyear/standardprocess.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def tempverifytrans(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = verifytransform(request.POST)
          if form.is_valid():
             transid1 = form.cleaned_data['transid']
             getdetails = tbltransactiontemp.objects.filter(transid = transid1)
             return render_to_response('newyear/verifyposting.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = verifytransform()
        return render_to_response('newyear/verifyposting.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def tempaccountsearch(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = verifytransform(request.POST)
          if form.is_valid():
             transid1 = form.cleaned_data['transid']
             getdetails = tbltransactiontemp.objects.filter(transid = transid1)
             return render_to_response('newyear/accountsearch.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = verifytransform()
        return render_to_response('newyear/accountsearch.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def temppaymentajaxcodesea(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   gdata = tblaccount.objects.filter(accname__startswith = acccode).order_by('acccode')#filter(acccode__startswith = acccode,groupname = "CURRENT ASSETS",subgroupname ="CASH AND BANK BALANCES").order_by('acccode')
                   return render_to_response('newyear/testajax.htm',{'gdata':gdata,'post':post})
             else:
                   gdata = tblaccount.objects.all()
                   #gdata = ""
                   return render_to_response('newyear/testajax.htm',{'gdata':gdata})
         else:
              gdata = tblaccount.objects.all().order_by('acccode')
              #gdata = ""
              return render_to_response('newyear/testajax.htm',{'gdata':gdata})
     else:
       return HttpResponseRedirect('/login/')

def temppounauto(request):
     if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        return render_to_response('newyear/unautorise.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')

def getinvoicenewyear(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails =  tbltemp1.objects.get(id = acccode)
                return render_to_response('newyear/editinvoice.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getreceiptnewyear(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails =  tbltempreceipt1.objects.get(id = acccode)
                return render_to_response('newyear/editreceipt.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getpaymentnewyear(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tbltemppayment1.objects.get(id = acccode)
                return render_to_response('newyear/editpayment.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def tempprintreceipt(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.genledger
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/newyear/unauto/')
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
                if tbltransactiontemp.objects.filter(transid = transid) :
                    trans = tbltransactiontemp.objects.filter(transid = transid)
                    k = len(trans)
                    if k > 2:
                        varerr ='Invalid Receipt Transaction'
                        return render_to_response('newyear/oldreceipt.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
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
                            return render_to_response('newyear/oldreceipt.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

                    new = locale.format("%.2f",float(amt),grouping=True)
                    k1 = new.replace(',','')
                    figwd = main(k1)
                    comp = tblcompanyinfo.objects.get(id = 1)
                    return render_to_response('newyear/printreceipt.htm',{'varuser':varuser,'varerr':varerr,'vartransid':vartransid,'amount':new,'fig2wd':figwd,'vdate':vdate.strftime("%d-%m-%Y"),'particulars':part,'cusname':accname,'school':comp,'refno':refno})
                else:
                    varerr ='Invalid Receipt Transaction'
                    return render_to_response('newyear/oldreceipt.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))


        else:
            form = verifytransform()
        return render_to_response('newyear/oldreceipt.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')





