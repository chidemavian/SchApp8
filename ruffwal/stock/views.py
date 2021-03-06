# Create your views here.\
from django.template import loader, Context,RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import  HttpResponseRedirect
from myproject.ruffwal.stock.form import *
from myproject.ruffwal.stock.models import *
from myproject.ruffwal.posting.models import *
from myproject.ruffwal.rwadmin.models import *
from myproject.sysadmin.models import *
from myproject.bill.models import *
from myproject.utilities.views import *
from django.db.models import Max,Sum
from django.core.serializers.json import simplejson as json
from myproject.ruffwal.stock.report import *
from myproject.ruffwal.rwreport.form import *
import locale
locale.setlocale(locale.LC_ALL,'')
import xlwt
import datetime
from datetime import date


def wel(request):
    if  "userid" in request.session:
        return render_to_response('stock/success.html')
    else:
        return HttpResponseRedirect('/login/')


def stockhistory(request):
    if "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.stockin
        if int(uenter) == 0 :
           return HttpResponseRedirect('/SchApp/account/stock/unauto/')
        form = stockhistoryForm()
        varerr = ''
        return render_to_response('stock/history.html',{'form':form,'varerr':varerr})
    else:
          return HttpResponseRedirect('/login/')


def newstock(request):
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.stockin
        if int(uenter) == 0 :
           return HttpResponseRedirect('/SchApp/account/stock/unauto/')
        varerr =""
        getdetails =""
        vardebit = 0
        if request.method == 'POST':
          form = stockform(request.POST) # A form bound to the POST data
          if form.is_valid():
             vendorname = form.cleaned_data['vendorname']
             vendorcode = form.cleaned_data['vendorcode']
             qty = form.cleaned_data['qty']
             caldate1 = form.cleaned_data['transdate']
             particulars = form.cleaned_data['particulars']
             unitprice = form.cleaned_data['price']
             stockname = form.cleaned_data['stockname']
             stockcode = form.cleaned_data['stockcode']
             invoiceno = form.cleaned_data['invoiceno']
             caldate2 = caldate1.split('/')
             transdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
             tot = qty * unitprice
             #**********************************************************getting the date
             if tblcalender.objects.all().count() == 0:
                 varerr = "NO START DATE"
                 #varerr ="This Month/Year Has been Process"
                 varrid1 = tblstocktemp.objects.filter(userid = varuser).aggregate(Sum('totalprice'))
                 vardebit = varrid1['totalprice__sum']
                 getdetails = tblstocktemp.objects.filter(userid = varuser).order_by('id')
                 return render_to_response('stock/newstock.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'vardebit':vardebit},context_instance = RequestContext(request))

             getdate = tblcalender.objects.all()
             stdate = datetime.date.today()
             endate = datetime.date.today()
             for g in getdate:
                 stdate = g.startmonth
                 endate = g.endtmonth
             if transdate < stdate or transdate > endate :
                 varerr = "INVALID DATE"
                 #varerr ="This Month/Year Has been Process"
                 varrid1 = tblstocktemp.objects.filter(userid = varuser).aggregate(Sum('totalprice'))
                 vardebit = varrid1['totalprice__sum']
                 getdetails = tblstocktemp.objects.filter(userid = varuser).order_by('id')
                 return render_to_response('stock/newstock.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'vardebit':vardebit},context_instance = RequestContext(request))
             varget = tblstocktemp.objects.filter(userid = varuser).count()
             if varget == 0 :
                used = tblstocktemp(vendorname = vendorname,vendorcode = vendorcode,qty = qty,transdate = transdate,particulars = particulars,unitprice = unitprice,stockname = stockname,stockcode = stockcode,invoiceno = invoiceno,totalprice = tot,userid = varuser )
                used.save()
             else:
                 if tblstocktemp.objects.filter(userid = varuser,vendorcode = vendorcode,invoiceno = invoiceno).count() == 0 :
                     return HttpResponseRedirect('/SchApp/account/stock/newstock/')
                 else:
                     used = tblstocktemp(vendorname = vendorname,vendorcode = vendorcode,qty = qty,transdate = transdate,particulars = particulars,unitprice = unitprice,stockname = stockname,stockcode = stockcode,invoiceno = invoiceno,totalprice = tot,userid = varuser )
                     used.save()
             #*****************************
             getdetails = tblstocktemp.objects.filter(userid = varuser).order_by('id')
             return HttpResponseRedirect('/SchApp/account/stock/newstock/')
             #now i do insertion
            # return render_to_response('posting/invoice.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:

            form = stockform()
            varrid1 = tblstocktemp.objects.filter(userid = varuser).aggregate(Sum('totalprice'))
            vardebit = varrid1['totalprice__sum']
            getdetails = tblstocktemp.objects.filter(userid = varuser).order_by('id')
        return render_to_response('stock/newstock.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'vardebit':vardebit},context_instance = RequestContext(request))

        #return render_to_response('stock/newstock.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')

def stock_issue(request):
    if "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.stockout
        if int(uenter) == 0 :
           return HttpResponseRedirect('/SchApp/account/stock/unauto/')
        if request.method == 'POST':
                 varerr= ' STOCK ISSUED OUT SUCCESSFULLY'
                 session = request.POST['session']
                 admissionno = request.POST['admissionno']
                 name = request.POST['name']
                 klass= request.POST['klass']
                 arm = request.POST['arm']
                 transdate = request.POST['transdate']
                 qty = request.POST['qty']
                 stockname = request.POST['stockname']
                 acccode = request.POST['acccode']
                 particulars = request.POST['particulars']
                 Balance = request.POST['Balance']

                 vardate=str(transdate)
                 j=tblcalender.objects.get(id=1)
                 js=str(j.startmonth)
                 je=str(j.endtmonth)


                 if name == '':
                    varerr = 'ENTER STUDENT NAME'
                    form = stockoutform()
                    return render_to_response('stock/stockissue.html',{'form':form,'varerr':varerr})
                 if stockname =='':
                    varerr ='ENTER STOCK NAME'
                    form = stockoutform()
                    return render_to_response('stock/stockissue.html',{'form':form,'varerr':varerr})

                 if particulars =='':
                    varerr ='ENTER A DESCRIPTION'
                    form = stockoutform(request.POST)
                    return render_to_response('stock/stockissue.html',{'form':form,'varerr':varerr})

                 if vardate =="":
                    vardate= str(datetime.date.today())
                 else:
                    vardate= transdate
                    rday,rmonth,ryear = vardate.split('-')
                    vardate = str(date(int(ryear),int(rmonth),int(rday)))

                 if vardate<js or vardate> je:
                    varerr='INVALID DATE'
                    form = stockoutform()
                    return render_to_response('stock/stockissue.html',{'form':form,'varerr':varerr})

                 try:
                    stk = tblstock.objects.get(acccode=acccode,stockname=stockname)
                 except:
                    form = stockoutform()
                    varerr='INVALID STOCK'
                    return render_to_response('stock/stockissue.html',{'form':form,'varerr':varerr})

                 try:
                    stu= Student.objects.get(fullname=name,admitted_class=klass,admitted_arm=arm,admitted_session=session,gone=0)
                 except:
                    form = stockoutform()
                    varerr='INVALID STUDENT NAME'
                    return render_to_response('stock/stockissue.html',{'form':form,'varerr':varerr})

                 bal = stk.qtybal
                 bal = int(stk.qtybal)
                 if qty =='' :
                    varerr ='ENTER VALUE FOR QUANTITY'
                    form = stockoutform(request.POST)
                    return render_to_response('stock/stockissue.html',{'form':form,'varerr':varerr})
                 qty= int(qty)
                 if bal - qty > -1:
                    bal = bal - qty
                    stk = tblstock( acccode=acccode,stockname=stockname,qtybal=bal,accbal = stk.accbal,datecreated=stk.datecreated,subname=stk.subname,subcode=stk.subcode,userid=stk.userid,avgprice=stk.avgprice).save()
                    stk1 = tblstocktout(studentname =name, description=particulars,studentcode=admissionno,klass=klass,session=session,Arm =arm,stockcode=acccode,stockname=stockname,qty=qty,userid=varuser,transdate=vardate).save()
                    form = stockoutform()
                    return render_to_response('stock/stockissue.html',{'form':form,'varerr':varerr})
                 else:
                    form = stockoutform()
                    varerr= 'AVAILABLE BALANCE TOO LOW, KINDLY QUANTITY FOR THIS ITEM'
                    return render_to_response('stock/stockissue.html',{'form':form,'varerr':varerr})
        else:
            form = stockoutform()
            varerr =''
        return render_to_response('stock/stockissue.html',{'form':form,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')


def stockissuedajax(request):
    if "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                # print acccode
                admno,session = acccode.split(':')
                data = tblstocktout.objects.filter(studentcode = admno, session=session).order_by('transdate')
                return render_to_response('stock/addbillajax.html',{'data':data, 'varerr':acccode})
            else:
                gdata = ""
                return render_to_response('stock/addbillajax.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('stock/addbillajax.html',{'gdata':gdata})


def stockhistoryajax(request):
    if "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                admno,session = acccode.split(':')
                data = tblstocktout.objects.filter(studentcode = admno, session=session)
                return render_to_response('stock/historyajax.html',{'data':data, 'varerr':acccode})
            else:
                gdata = ""
                return render_to_response('stock/historyajax.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('stock/historyajax.html',{'gdata':gdata})


def testajaxstock(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   #gdata = tblaccount.objects.all()
                   gdata =[]
                   lk = ""
                   lk1 = ""
                   gdata1 = tblstock.objects.filter(acccode__startswith = acccode,subname = "MINI-STORE-BALANCE").order_by('acccode')
                   for j in gdata1:
                       lk = j.acccode,j.stockname,j.accbal
                       gdata.append(lk)
                   gdata1 = tblaccount.objects.filter(acccode__startswith = acccode,groupname = "CURRENT LIABILITIES",subgroupname ="PAYABLES").exclude(accname = "TRADE-CREDITORS").order_by('acccode')
                   for r in gdata1:
                       lk1 = r.acccode,r.accname,r.accbal
                       gdata.append(lk1)
                   gdata11 = tblaccount.objects.filter(acccode__startswith = acccode,groupname = "CURRENT ASSETS",subgroupname ="CASH AND BANK BALANCES").order_by('acccode')
                   for r in gdata11:
                       lk11 = r.acccode,r.accname,r.accbal
                       gdata.append(lk11)

                   return render_to_response('stock/testajax.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = []
                   return render_to_response('stock/testajax.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = []
              return render_to_response('stock/testajax.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def testajaxcodestock(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   gdata = tblstock.objects.filter(acccode__startswith = acccode).exclude(subname = "MINI-STORE-BALANCE").order_by('acccode')
                   #gdata = tblaccount.objects.filter(acccode__startswith = acccode,groupname = "CURRENT ASSETS",subgroupname ="RECEIVABLES").exclude(accname = "TRADE-DEBTORS")

                   return render_to_response('stock/testajax1.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = ""
                   return render_to_response('stock/testajax1.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('stock/testajax1.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def deletestock(request,invid):
    varerr =""
    if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.stockin
            if int(uenter) == 0 :
               return HttpResponseRedirect('/SchApp/account/stock/unauto/')
            varerr =""
            if request.method == 'POST':
                 accno = request.POST['hcode']#the primary key
                 seldata = tblstocktemp.objects.get(id = invid)
                 seldata.delete()
                 return HttpResponseRedirect('/SchApp/account/stock/newstock/')
            else:
               getdetails = tblstocktemp.objects.get(id = invid)
               #seldata.delete()
               return render_to_response('stock/deletestock.htm',{'getdetails':getdetails})

    else:
      return HttpResponseRedirect('/login/')

def addprocess(request):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            varyear = date.today().year
            vardate = date.today()
            if tblstocktemp.objects.filter(userid = varuser).count() == 0 :
                return HttpResponseRedirect('/SchApp/account/stock/newstock/')
            else:
                ll = []
                lk = ""
                vardata = tblstocktemp.objects.filter(userid = varuser) #all enteries made by user
                cuspart =""
                custo = 0
                for j in vardata:
                    lk = j.stockname,j.stockcode,j.particulars,j.totalprice,j.id,j.qty,j.transdate,j.unitprice
                    ll.append(lk)
                    custo = custo + j.totalprice
                    cuspart =cuspart + j.particulars + ","
                    cusno = j.vendorcode
                    cusname = j.vendorname
                    refno = j.invoiceno
                    vardate = j.transdate
                    varyear = vardate.year
                    userid = j.userid
                    qtyrm = j.qty
                    unitpm = j.unitprice
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
                #**************************************************************************#credit account
                k = cusno[0:3]
                cusno1 = cusno
                cusname1 = cusname
                if k == "304":
                #if k <> "304":
                  gdatas = tblstock.objects.get(acccode = cusno)
                  cusname = gdatas.subname
                  cusno = gdatas.subcode
                  currbal = gdatas.accbal
                  currqty = gdatas.qtybal
                  bbal1 = currqty - qtyrm
                  topr = qtyrm * unitpm
                  topr =  currbal - topr
                  dispqty = locale.format("%.2f",qtyrm,grouping=True)
                  dispbal = locale.format("%.2f",bbal1,grouping=True)
                  dispunitbal = locale.format("%.2f",unitpm,grouping=True)
                  disptotbal = locale.format("%.2f",topr,grouping=True)

                  used = tblstocktransaction(stockname = cusname1,acccode = cusno1,qty = qtyrm,stin = 0,stout = qtyrm,stbal = bbal1,transcreated = vardate,particulars = cuspart,unitprice = unitpm,totalprice = topr,userid = userid ,disqty = dispqty, disin = "0.00",disout= dispqty,disbal = dispbal,disunitprice = dispunitbal,distotalprice = disptotbal)
                  used.save()
                   #***********************************************************
                  rgdata = tblstock.objects.get(acccode = cusno1)
                  rgdata.accbal = topr
                  rgdata.qtybal = bbal1
                  rgdata.save()
                else:
                    cusno = cusno
                    cusname = cusname
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
                selsubdata.accbal = cusbal #
                selsubdata.lasttrandate = vardate
                selsubdata.save()
                #********************************************


                #**********************************
                k = range(len(ll))

                we =[]

                for h in k:

                  for m in ll[h]:
                     we.append(m)
                  accname1 = we[0]
                  acccode1 = we[1]
                  part = we[2]
                  amount = we[3]
                  rid = we[4]
                  qtyr = we[5]
                  varrdate = we[6]
                  unitp = we[7]
                  gdata = tblstock.objects.get(acccode = acccode1)
                  accname = gdata.subname
                  acccode = gdata.subcode
                  currbal = gdata.accbal
                  currqty = gdata.qtybal
                 #***************************************
                  cusdet1 =  tblaccount.objects.get(acccode = acccode)
                  bal = cusdet1.accbal
                  grp = cusdet1.groupname
                  sub = cusdet1.subgroupname
                  #here we are debiting so, take note of the assest side
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
                  #posting to the strock table

                  bbal = currqty + qtyr
                  topr = qtyr * unitp
                  topr = topr + currbal
                  avgp = topr/bbal
                  dispqty = locale.format("%.2f",qtyr,grouping=True)
                  dispbal = locale.format("%.2f",bbal,grouping=True)
                  dispunitbal = locale.format("%.2f",unitp,grouping=True)
                  disptotbal = locale.format("%.2f",topr,grouping=True)

                  used = tblstocktransaction(stockname = accname1,acccode = acccode1,qty = qtyr,stin = qtyr,stout = 0,stbal = bbal,transcreated = varrdate,particulars = part,unitprice = unitp,totalprice = topr,userid = userid ,disqty = dispqty, disin = dispqty,disout= "0.00",disbal = dispbal,disunitprice = dispunitbal,distotalprice = disptotbal)
                  used.save()
                   #***********************************************************
                  rgdata = tblstock.objects.get(acccode = acccode1)

                  rgdata.accbal = topr
                  rgdata.qtybal = bbal
                  rgdata.avgprice = avgp
                  rgdata.save()
                  #**********************************************************
                  we.remove(accname1)
                  we.remove(acccode1)
                  we.remove(part)
                  we.remove(amount)
                  we.remove(rid)
                  we.remove(qtyr)
                  we.remove(varrdate)
                  we.remove(unitp)
                  deldata = tblstocktemp.objects.filter(userid = varuser).delete()

                return render_to_response('stock/invsuccess.htm',{'varuser':varuser,'varerr':varerr,'vartransid':vartransid})

        else:
         return HttpResponseRedirect('/login/')

def outprocess(request):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            varyear = date.today().year
            vardate = date.today()
            if tblstocktempout.objects.filter(userid = varuser).count() == 0 :
                return HttpResponseRedirect('/SchApp/account/stock/outstock/')
            else:
                ll = []
                lk = ""
                vardata = tblstocktempout.objects.filter(userid = varuser)
                cuspart =""
                custo = 0
                for j in vardata:
                    lk = j.vendorname,j.vendorcode,j.qty,j.transdate,j.particulars,j.unitprice,j.totalprice,j.userid,j.stockname,j.stockcode,j.invoiceno,j.id
                    ll.append(lk)
                    vardate = j.transdate
                    varyear = vardate.year
                #**********************************
                k = range(len(ll))
                we =[]
                for h in k:
                  for m in ll[h]:
                     we.append(m)
                  accname1 = we[0]#vendor name
                  acccode1 = we[1]#vendor code
                  part = we[4] #Particular
                  rid = we[11] # rec id
                  qtyr = we[2]# qunatity
                  varrdate = we[3] # trans date
                  unitp = we[5] # unit price
                  stockname = we[8] # stock name
                  stockcode = we[9] # stock name
                  invno = we[10] # invoice no
                  #********************************************amount
                  amount = unitp * qtyr #i.e unit * quantity

                  #*******************************************************debit the the stock

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

                  #**************************************************
                  gdata = tblstock.objects.get(acccode = acccode1)
                  accname = gdata.subname
                  acccode = gdata.subcode
                  currbal = gdata.accbal
                  currqty = gdata.qtybal
                 #***************************************
                  cusdet1 =  tblaccount.objects.get(acccode = acccode)
                  bal = cusdet1.accbal
                  grp = cusdet1.groupname
                  sub = cusdet1.subgroupname
                  #here we are credit so, take note of the assest side
                  if grp == "FIXED ASSETS" or grp == "CURRENT ASSETS" or grp == "EXPENSES" or grp == "COST OF SALES":
                       cusbal1 = bal - amount
                  else:
                       cusbal1 = bal + amount

                      #***********************************************debit student

                  used = tbltransaction(accname = accname,acccode = acccode,debit = 0,credit = amount,balance = cusbal1,transid = vartransid,transdate = varrdate,particulars = part,refno = invno,groupname = grp,subname = sub ,userid = varuser, recid = varrecid )
  #                used.save()

                    #********************update
                  selsubdata1 = tblaccount.objects.get(acccode = acccode)
                  selsubdata1.accbal = cusbal1
                  selsubdata1.lasttrandate = vardate
                  selsubdata1.save()
                  #posting to the stock table
                  bbal = currqty - qtyr
                  topr = qtyr * unitp
                  topr = currbal - topr
                  avgpd = topr/bbal
                  dispqty = locale.format("%.2f",qtyr,grouping=True)
                  dispbal = locale.format("%.2f",bbal,grouping=True)
                  dispunitbal = locale.format("%.2f",unitp,grouping=True)
                  disptotbal = locale.format("%.2f",topr,grouping=True)

                  used = tblstocktransaction(stockname = accname1,acccode = acccode1,qty = qtyr,stin = 0,stout = qtyr,stbal = bbal,transcreated = varrdate,particulars = part,unitprice = unitp,totalprice = topr,userid = varuser ,disqty = dispqty, disin = "0.00",disout= dispqty,disbal = dispbal,disunitprice = dispunitbal,distotalprice = disptotbal)
                  used.save()
                   #***********************************************************
                  rgdata = tblstock.objects.get(acccode = acccode1)
                  rgdata.accbal = topr
                  rgdata.qtybal = bbal
                  rgdata.avgprice = avgpd
                  rgdata.save()
                  #********************************************************** DEBITING THE STOCK
                  k = stockcode[0:1]
                  cusno1 = stockcode
                  cusname1 = stockname
                  custo = amount
                  if k == "3":
                     gdatas = tblstock.objects.get(acccode = stockcode)
                     cusname = gdatas.subname
                     cusno = gdatas.subcode
                     currbal = gdatas.accbal
                     currqty = gdatas.qtybal
                     bbal1 = currqty + qtyr
                     topr = qtyr * unitp
                     topr =  currbal + topr
                     avgpdc = topr/bbal1
                     dispqty = locale.format("%.2f",qtyr,grouping=True)
                     dispbal = locale.format("%.2f",bbal1,grouping=True)
                     dispunitbal = locale.format("%.2f",unitp,grouping=True)
                     disptotbal = locale.format("%.2f",topr,grouping=True)

                     used = tblstocktransaction(stockname = cusname1,acccode = cusno1,qty = qtyr,stin = qtyr,stout = 0,stbal = bbal1,transcreated = varrdate,particulars = part,unitprice = unitp,totalprice = topr,userid = varuser ,disqty = dispqty, disin = dispqty,disout= "0.00",disbal = dispbal,disunitprice = dispunitbal,distotalprice = disptotbal)
                     used.save()
                    #***********************************************************
                     rgdata = tblstock.objects.get(acccode = cusno1)
                     rgdata.accbal = topr
                     rgdata.qtybal = bbal1
                     rgdata.avgprice = avgpdc
                     rgdata.save()
                  else:
                      cusno = stockcode
                      cusname = stockname
                  cusdet =  tblaccount.objects.get(acccode = cusno)
                  cusbal = cusdet.accbal
                  cusgrp = cusdet.groupname
                  cussub = cusdet.subgroupname
                  if cusgrp == "FIXED ASSETS" or cusgrp == "CURRENT ASSETS" or cusgrp == "EXPENSES" or cusgrp == "COST OF SALES":
                     cusbal = cusbal + custo
                  else:
                     cusbal = cusbal - custo
                  #***********************************************
                  used = tbltransaction(accname = cusname,acccode = cusno,debit = custo,credit = 0,balance = cusbal,transid = vartransid,transdate = varrdate,particulars = part,refno = invno,groupname = cusgrp,subname = cussub ,userid = varuser,recid = varrecid )
            #      used.save()
                  #********************
                  selsubdata = tblaccount.objects.get(acccode = cusno)
                  selsubdata.accbal = cusbal #
                  selsubdata.lasttrandate = vardate
                  selsubdata.save()
                  #***************************************************************************
                  we.remove(accname1)
                  we.remove(acccode1)
                  we.remove(part)
                  we.remove(rid)
                  we.remove(qtyr)
                  we.remove(varrdate)
                  we.remove(unitp)
                  we.remove(stockname)
                  we.remove(stockcode)
                  we.remove(invno)
                  deldata = tblstocktempout.objects.filter(userid = varuser).delete()

                return render_to_response('stock/invsuccess.htm',{'varuser':varuser,'varerr':varerr,'vartransid':vartransid})

        else:
         return HttpResponseRedirect('/login/')

def outstock(request):
     if  "userid" in request.session:

        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.stockout
        if int(uenter) == 0 :
           return HttpResponseRedirect('/SchApp/account/stock/unauto/')
        varerr =""
        getdetails = ""
        vardebit = 0
        if request.method == 'POST':
          form = stockform(request.POST) # A form bound to the POST data
          if form.is_valid():

             vendorname = form.cleaned_data['vendorname']
             vendorcode = form.cleaned_data['vendorcode']
             vendorbal =  form.cleaned_data['vendorbal']
             qty = form.cleaned_data['qty']
             caldate1 = form.cleaned_data['transdate']
             particulars = form.cleaned_data['particulars']
             unitprice = form.cleaned_data['price']
             stockname = form.cleaned_data['stockname']
             stockcode = form.cleaned_data['stockcode']
             invoiceno = form.cleaned_data['invoiceno']
             caldate2 = caldate1.split('/')
             transdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
             #**********************************************************getting the date
             if tblcalender.objects.all().count() == 0:
                 varerr = "NO START DATE"
                 #varerr ="This Month/Year Has been Process"
                 varrid1 = tblstocktempout.objects.filter(userid = varuser).aggregate(Sum('totalprice'))
                 vardebit = varrid1['totalprice__sum']
                 getdetails = tblstocktempout.objects.filter(userid = varuser).order_by('id')
                 return render_to_response('stock/outstock.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'vardebit':vardebit},context_instance = RequestContext(request))

             getdate = tblcalender.objects.all()
             stdate = datetime.date.today()
             endate = datetime.date.today()
             for g in getdate:
                 stdate = g.startmonth
                 endate = g.endtmonth
             if transdate < stdate or transdate > endate :
                 varerr = "INVALID DATE"
                 #varerr ="This Month/Year Has been Process"
                 varrid1 = tblstocktempout.objects.filter(userid = varuser).aggregate(Sum('totalprice'))
                 vardebit = varrid1['totalprice__sum']
                 getdetails = tblstocktempout.objects.filter(userid = varuser).order_by('id')
                 return render_to_response('stock/outstock.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'vardebit':vardebit},context_instance = RequestContext(request))


             tot = qty * unitprice
            # print qty, vendorbal
             if int(qty) > int(vendorbal):
                 varrid1 = tblstocktempout.objects.filter(userid = varuser).aggregate(Sum('totalprice'))
                 vardebit = varrid1['totalprice__sum']
                 varerr = "INSUFFICIENT STOCK"
                 getdetails = tblstocktempout.objects.filter(userid = varuser).order_by('id')
                 return render_to_response('stock/outstock.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'vardebit':vardebit},context_instance = RequestContext(request))
             varget = tblstocktempout.objects.filter(userid = varuser).count()
             used = tblstocktempout(vendorname = vendorname,vendorcode = vendorcode,qty = qty,transdate = transdate,particulars = particulars,unitprice = unitprice,stockname = stockname,stockcode = stockcode,invoiceno = invoiceno,totalprice = tot,userid = varuser )
             used.save()
             #*****************************
             getdetails = tblstocktempout.objects.filter(userid = varuser).order_by('id')
             return HttpResponseRedirect('/SchApp/account/stock/outstock/')
             #now i do insertion
            # return render_to_response('posting/invoice.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:

            form = stockform()
            varrid1 = tblstocktempout.objects.filter(userid = varuser).aggregate(Sum('totalprice'))
            vardebit = varrid1['totalprice__sum']
            getdetails = tblstocktempout.objects.filter(userid = varuser).order_by('id')
        return render_to_response('stock/outstock.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'vardebit':vardebit},context_instance = RequestContext(request))

        #return render_to_response('stock/newstock.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')

def testajaxstockout(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   #gdata = tblaccount.objects.all()
                   gdata = tblstock.objects.filter(acccode__startswith = acccode).order_by('acccode')

                   return render_to_response('stock/testajax1.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = []
                   return render_to_response('stock/testajax1.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = []
              return render_to_response('stock/testajax1.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def testajaxcodestockout(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   #gdata = tblaccount.objects.all()
                   gdata =[]
                   lk = ""
                   lk1 = ""
                   gdata1 = tblstock.objects.filter(acccode__startswith = acccode).order_by('acccode')
                   for j in gdata1:
                       lk = j.acccode,j.stockname,j.accbal
                       gdata.append(lk)
                   gdata1 = tblaccount.objects.filter(acccode__startswith = acccode).exclude(groupname = "INCOME").exclude(groupname = "ACCUMULATED DEPRECIATION").exclude(groupname = "FIXED ASSETS").exclude(groupname = "CAPITAL AND RESERVED").exclude(groupname = "LONG TERM LIABILITIES").order_by('acccode')
                   for r in gdata1:
                       lk1 = r.acccode,r.accname,r.accbal
                       gdata.append(lk1)

                   return render_to_response('stock/testajax.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = []
                   return render_to_response('stock/testajax.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = []
              return render_to_response('stock/testajax.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def deletestockout(request,invid):
    varerr =""
    if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.stockout
            if int(uenter) == 0 :
               return HttpResponseRedirect('/SchApp/account/stock/unauto/')
            varerr =""
            if request.method == 'POST':
                 accno = request.POST['hcode']#the primary key
                 seldata = tblstocktempout.objects.get(id = invid)
                 seldata.delete()
                 return HttpResponseRedirect('/SchApp/account/stock/outstock/')
            else:
               getdetails = tblstocktempout.objects.get(id = invid)
               #seldata.delete()
               return render_to_response('stock/deletestockout.htm',{'getdetails':getdetails})

    else:
      return HttpResponseRedirect('/login/')

def statementrep(request):
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.stockreport
        if int(uenter) == 0 :
           return HttpResponseRedirect('/SchApp/account/stock/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = statementform(request.POST) # A form bound to the POST data
          if form.is_valid():
             stockname = form.cleaned_data['stockname']
             stockcode = form.cleaned_data['stockcode']
             caldate1 = form.cleaned_data['startdate']
             caldate12 = form.cleaned_data['enddate']
             caldate2 = caldate1.split('/')
             startdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
             caldate22 = caldate12.split('/')
             enddate = date(int(caldate22[2]),int(caldate22[0]),int(caldate22[1]))
             comp = tblcompanyinfo.objects.get(id = 1)
             ll = []
             if startdate > enddate :
                 varerr = "INVALID DATE RANGE"
                 return render_to_response('stock/statement.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
             else:
                 if stockcode == '':
                     stockdata = tblstock.objects.all().order_by('acccode')
                 else:
                     stockdata = tblstock.objects.filter( acccode = stockcode ).order_by('acccode')
                 for a in stockdata:
                     stockcode = a.acccode
                     #tb = 0
                     if tblstocktransaction.objects.filter(acccode = stockcode,transcreated__lt= startdate).count() == 0:
                         varin = 0
                         varout = 0
                         opbal = 0
                     else:
                         varrid1 = tblstocktransaction.objects.filter(acccode = stockcode,transcreated__lt= startdate).aggregate(Sum('stin'),Sum('stout'))
                         varin = varrid1['stin__sum']
                         varout = varrid1['stout__sum']
                         opbal = varin - varout
                     tb = opbal
                     getdetails1 = tblstocktransaction.objects.filter(acccode = stockcode,transcreated__range=(startdate,enddate)).order_by('transcreated','id')#.exclude(accname = "TRADE-DEBTORS"),subgroupname = "STOCKS"
                     sublist = []
                     for l in getdetails1:
                         vin = l.stin
                         vout = l.stout
                         vid = l.id
                         tb = tb + vin - vout
                         dispin = locale.format("%.2f",vin,grouping=True)
                         dispout = locale.format("%.2f",vout,grouping=True)
                         disbal = locale.format("%.2f",tb,grouping=True)
                         j={'transcreated':l.transcreated,'particulars':l.particulars,'disin':dispin,'disout':dispout,'disbal':disbal}
                         sublist.append(j)
                     getdetails = {'stockcode':stockcode,'stockname':a.stockname,'opbal':locale.format("%.2f",opbal,grouping=True),'trans':sublist}#tblstocktransaction.objects.filter(acccode = stockcode,transcreated__range=(startdate,enddate) ).order_by('transcreated','id')#.exclude(accname = "TRADE-DEBTORS"),subgroupname = "STOCKS"
                     ll.append(getdetails)
                     #now i do insertion
                 if form.cleaned_data['excelfile']:
                         response = HttpResponse(mimetype="application/ms-excel")
                         response['Content-Disposition'] = 'attachment; filename=stockstatement.xls'
                         wb = xlwt.Workbook()
                         ws = wb.add_sheet('stockstatement')
                         ws.write(0, 1, comp.name)
                         ws.write(1, 1, comp.address)
                         ws.write(2, 1, 'Stock Statement' )
                         ws.write(3, 0, 'Date' )
                         ws.write(3, 1, 'Particulars' )
                         ws.write(3, 2, 'Qty In' )
                         ws.write(3, 3, 'Qty Out')
                         ws.write(3, 4, 'Qty Balance' )
                         ws.write(4, 2, stockcode)
                         ws.write(4, 3, stockname )
                         k = 5
                         for bl in getdetails:
                            ws.write(k, 0,bl.transcreated.strftime("%d-%m-%Y"))
                            ws.write(k, 1,bl.particulars)
                            ws.write(k, 2,bl.disin)
                            ws.write(k, 3,bl.disout)
                            ws.write(k, 4,bl.disbal)
                            k+=1
                         wb.save(response)
                         return response
                 else:
                         return render_to_response('stock/statement.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':ll,'comp':comp},context_instance = RequestContext(request))
        else:
            form = statementform()
        return render_to_response('stock/statement.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def ajaxcodestate(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   #gdata = tblaccount.objects.all()
                   gdata = tblstock.objects.filter(subname = acccode).order_by('acccode')

                   return render_to_response('stock/testajax1.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = []
                   return render_to_response('stock/testajax1.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = []
              return render_to_response('stock/testajax1.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def stockenter(request):#stunauto
     if  "userid" in request.session:

        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.einventory
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/welcome/')
        varerr =""
        return render_to_response('stock/stockenter.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')

def stunauto(request):#stunauto
     if  "userid" in request.session:

        varuser = request.session['userid']
        varerr =""
        return render_to_response('stock/unautorise.htm',{'varuser':varuser,'varerr':varerr})
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

def autocompletecr(request):
    term = request.GET.get('term')  # a 'GET' variable of request.POST.get
    gset = []


    """
i  removed mini store balances
    gdata1 = tblstock.objects.filter(stockname__contains = term,subname = "MINI-STORE-BALANCE").order_by('acccode')[:10]
    for j in gdata1:
        lk = {'code':j.acccode,'name':j.stockname,'bal':j.accbal}
        gset.append(lk)
"""
    gdata1 = tblaccount.objects.filter(accname__contains = term,groupname = "CURRENT LIABILITIES",subgroupname ="PAYABLES").exclude(accname = "TRADE-CREDITORS").order_by('acccode')[:10]
    for r in gdata1:
        lk1 = {'code':r.acccode,'name':r.accname,'bal':r.accbal}
        gset.append(lk1)

        """
i removed cash and bank balances
    gdata11 = tblaccount.objects.filter(accname__contains = term,groupname = "CURRENT ASSETS",subgroupname ="CASH-AND-BANK-BALANCES").order_by('acccode')[:10]
    for r in gdata11:
        lk11 = {'code':r.acccode,'name':r.accname,'bal':r.accbal}
        gset.append(lk11)
        """
    suggestions = []
    for i in gset:
        k = i['bal']
        disamt = locale.format("%.2f",k,grouping=True)
        suggestions.append({'label': '%s %s' % (i['name'],i['code']), 'acccode': i['code'],'accname': i['name'],'accbal':disamt})
    return suggestions

@json_view
def autocompletedr(request):
    term = request.GET.get('term')
#    gset = tblstock.objects.filter(stockname__contains = term).exclude(subname = "MINI-STORE-BALANCE").order_by('acccode')[:10]
    gset = tblstock.objects.filter(stockname__contains = term).order_by('acccode')[:10]
    suggestions = []
    for i in gset:
        k = i.accbal
        disamt = locale.format("%.2f",k,grouping=True)
        suggestions.append({'label': '%s %s' % (i.stockname,i.acccode), 'acccode': i.acccode,'accname': i.stockname,'accbal':disamt})
    return suggestions

@json_view
def autocompleteout(request):
    term = request.GET.get('term')
    gset = []
    gdata1 = tblstock.objects.filter(stockname__contains = term).order_by('acccode')[:10]
    for j in gdata1:
        lk = {'code':j.acccode,'name':j.stockname,'bal':j.accbal}
        #lk = j.acccode,j.stockname,j.accbal
        gset.append(lk)
    gdata1 = tblaccount.objects.filter(accname__contains = term).exclude(groupname = "INCOME").exclude(groupname = "ACCUMULATED DEPRECIATION").exclude(groupname = "FIXED ASSETS").exclude(groupname = "CAPITAL AND RESERVES").exclude(groupname = "LONG TERM LIABILITIES").exclude(groupname = "CURRENT ASSETS",subgroupname ="STOCKS").exclude(groupname = "CURRENT LIABILITIES",subgroupname = "PAYABLES",accname = "TRADE-CREDITORS").exclude(groupname = "CURRENT ASSETS",subgroupname = "MINI-STORE",accname = "MINI-STORE-BALANCE").exclude(groupname = "CURRENT ASSETS",subgroupname = "WORK-IN-PROGRESS",accname = "WORK-IN-PROGRESS-BALANCE").exclude(groupname = "CURRENT ASSETS",subgroupname = "STAFF-DEBTORS",accname = "STAFF-DEBTORS").exclude(groupname = "CURRENT ASSETS",subgroupname = "RECEIVABLES",accname = "TRADE-DEBTORS").order_by('acccode')[:10]
    for r in gdata1:
        lk1 = {'code':r.acccode,'name':r.accname,'bal':r.accbal}
        #lk1 = r.acccode,r.accname,r.accbal
        gset.append(lk1)
    suggestions = []
    for i in gset:
        k = i['bal']
        disamt = locale.format("%.2f",k,grouping=True)
        suggestions.append({'label': '%s %s' % (i['name'],i['code']), 'acccode': i['code'],'accname': i['name'],'accbal':disamt})
    return suggestions


@json_view
def autocompleteoutstock(request):
    term = request.GET.get('term')
    gset = []
    gdata1 = tblstock.objects.filter(stockname__contains = term).order_by('acccode')[:10]
    for j in gdata1:
        lk = {'code':j.acccode,'name':j.stockname,'bal':j.qtybal}
        gset.append(lk)
    suggestions = []
    for i in gset:
        k = i['bal']
        p = int(k)
     #   disamt = locale.format("%.f",k,grouping=True)
        suggestions.append({'label': '%s :%s :%s' % (i['name'],i['code'],i['bal']), 'acccode': j.acccode,'accname': i['name'],'accbal':p})
    return suggestions

@json_view
def autocompleteoutstocks(request):
    term = request.GET.get('term')
    gdata1 = tblstock.objects.filter(stockname__contains = term).order_by('acccode')[:10]

    gset = []
    for j in gdata1:
        gset.append({'label': '%s :%s :%s: ' % (j.stockname, j.qtybal ,j.acccode), 'acccode':j.accode, 'accname':j.stockname, 'accbal': int(j.qtybal)})
    return gset

@json_view
def autocompleteup(request):
    term = request.GET.get('term')
    gset = tblstock.objects.filter(stockname__contains = term).order_by('acccode')[:10]
    suggestions = []
    for i in gset:
        k = i.qtybal
        disamt = str(k)
        #disamt = locale.format("%.2f",k,grouping=True)
        suggestions.append({'label': '%s %s' % (i.stockname,i.acccode), 'acccode': i.acccode,'accname': i.stockname,'accbal':disamt,'avgprice':str(i.avgprice)})
    return suggestions

def getstockadd(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tblstocktemp.objects.get(id = acccode)
                return render_to_response('stock/deletestock.htm',{'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getstockout(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tblstocktempout.objects.get(id = acccode)
                return render_to_response('stock/deletestockout.htm',{'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')
