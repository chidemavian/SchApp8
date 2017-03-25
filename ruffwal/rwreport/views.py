from django.template import loader, Context,RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import  HttpResponseRedirect
from myproject.ruffwal.utils import *
from myproject.ruffwal.rwreport.opbal import *
from myproject.ruffwal.posting.models import *
from myproject.ruffwal.rwreport.models import *
from myproject.ruffwal.rwadmin.models import *
from django.db.models import Max,Sum
from myproject.ruffwal.rwreport.reports import *
from myproject.ruffwal.rwreport.form import *
from myproject.ruffwal.stock.models import *
from myproject.ruffwal.rwreport.capy import monthrange
from myproject.sysadmin.models import *
from myproject.student.models import *
from django.core.serializers.json import simplejson as json
import locale
locale.setlocale(locale.LC_ALL,'')
import xlwt
import datetime
from datetime import date,time,timedelta

currse = currentsession.objects.get(id = 1)
vvtoday= datetime.date.today

def reportunauto(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        return render_to_response('report/unautorise.htm',{'varuser':varuser,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def enterreport(request):
     if  "userid" in request.session:

        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.ereport
        if int(uenter) == 0 :
            return HttpResponseRedirect('/welcome/')
        varerr =""
        return render_to_response('report/report.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')

def chartofaccrep(request):
     if  "userid" in request.session:

        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.statutory
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/report/unauto/')
        varerr =""
        return render_to_response('report/chartofacc.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')

def chatreport(request):
     if  "userid" in request.session:
         varuser = request.session['userid']
         user = tbluseracc.objects.get(username = varuser)
         uenter = user.statutory
         if int(uenter) == 0 :
             return HttpResponseRedirect('/SchApp/account/report/unauto/')
         varerr =""
         if request.method == 'POST':
             #deldata = tblstatement.objects.all().delete()
             form = chartform(request.POST) # A form bound to the POST data
             if form.is_valid():
                     #************************
                 gacc = tblgroup.objects.all().order_by('groupcode')
                 ll = []
                 da ={}
                 for ap in gacc:
                     da ={}
                     vade = tblaccount.objects.filter(groupcode = ap.groupcode,recreport ="YES").order_by('groupcode', 'acccode')
                     da = {'grname':ap.groupname,'grcode':ap.groupcode,'gracc':vade}
                     ll.append(da)
                 comp = tblcompanyinfo.objects.get(id = 1)
                 if form.cleaned_data['excelfile']:
                     response = HttpResponse(mimetype="application/ms-excel")
                     response['Content-Disposition'] = 'attachment; filename=chartofacc.xls'
                     wb = xlwt.Workbook()
                     ws = wb.add_sheet('chartofacc')
                     ws.write(0, 1, comp.name)
                     ws.write(1, 1, comp.address)
                     ws.write(2, 1, 'CHART OF ACCOUNT REPORT')
                     k = 3
                     v = 4
                     for m in ll:
                         ws.write(k, 1,m['grcode'])
                         ws.write(k, 2, m['grname'])
                         for n in m['gracc']:
                             ws.write(v, 2, n.acccode)
                             ws.write(v, 3, n.accname)
                             v += 1
                         k = v + 1
                         v = k + 1
                     wb.save(response)
                     return response
                 else:
                     return render_to_response('report/chartofacc.htm',{'varuser':varuser,'varerr':varerr,'form':form,'ll':ll,'comp':comp},context_instance = RequestContext(request))

         else:
            form = chartform()
         return render_to_response('report/chartofacc.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
        # if tblaccount.objects.filter(recreport ="YES").count() == 0:
         #    varerr =""
          #   return render_to_response('report/notfound.htm',{'varuser':varuser,'varerr':varerr})

         #resp = HttpResponse(mimetype='application/pdf')
         #chartofacc = tblaccount.objects.filter(recreport ="YES").order_by('groupcode', 'acccode')
         #report = Reportchartofacc(queryset=chartofacc)
         #report.generate_by(PDFGenerator, filename=resp)
         #return resp
     else:
       return HttpResponseRedirect('/login/')


def receivablesrep(request):
    if  "userid" in request.session:
        #getting the data
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.statutory
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/report/unauto/')
        varerr =""
        ll = []
        if request.method == 'POST':
            form = studentForm(request.POST) # A form bound to the POST data
            if form.is_valid():
               admitted_class = form.cleaned_data['admitted_class']
               admitted_arm = form.cleaned_data['admitted_arm']

               #caldate1 = form.cleaned_data['enddate']
               #caldate2 = caldate1.split('/')
               #varend = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
               tbal = 0
               comp = tblcompanyinfo.objects.get(id = 1)
               if form.cleaned_data['excelfile']:
                   llp = tblaccount.objects.filter(groupname ="CURRENT ASSETS",subgroupname = "RECEIVABLES", recreport = 'STUDENTS',accstatus = 'ACTIVE').exclude(accname = "TRADE-DEBTORS").order_by('accname')#tblreceiavables.objects.all().order_by('groupname','acccode')
                   for h in llp:
                    opbal = accbalance(h.acccode)
                    opbal1 = locale.format("%.2f",opbal,grouping=True)
                    tbal += opbal
                    accdic = {'acc':h,'pid':h.id,'pos':opbal1}
                    ll.append(accdic)
               else:
                   llp = Student.objects.filter(admitted_class =admitted_class,admitted_session =currse, admitted_arm =admitted_arm ).order_by('fullname')
                   for h in llp:
                        opbal = accbalance(h.admissionno)
                        opbal1 = locale.format("%.2f",opbal,grouping=True)
                        tbal += opbal
                        if tblaccount.objects.filter(acccode = h.admissionno):
                           acc = tblaccount.objects.get(acccode = h.admissionno)
                        else:
                            acc = {}
                        accdic = {'acc':acc,'pid':h.id,'pos':opbal1}
                        ll.append(accdic)
               totbal = locale.format("%.2f",tbal,grouping=True)
               if form.cleaned_data['excelfile1']:
                   response = HttpResponse(mimetype="application/ms-excel")
                   response['Content-Disposition'] = 'attachment; filename=receivables.xls'
                   wb = xlwt.Workbook()
                   ws = wb.add_sheet('receivables')
                   ws.write(0, 1, comp.name)
                   ws.write(1, 1, comp.address)
                   ws.write(2, 1, 'STUDENT ACCOUNT BALANCE')
                   ws.write(3, 1, 'Account Code')
                   ws.write(3, 2, 'Account Name')
                   #ws.write(3, 3, 'Last Transaction Date')
                   ws.write(3, 3, 'Account Balance')
                   k = 4
                   for d,m in enumerate(ll):
                       ws.write(k, 0,d+1)
                       ws.write(k, 1,m['acc'].acccode)
                       ws.write(k, 2, m['acc'].accname)
                       #ws.write(k, 3, m['acc'].lasttrandate.strftime("%d-%m-%Y"))
                       ws.write(k, 3, m['pos'])
                       k += 1
                   ws.write(k, 2, 'Total')
                   ws.write(k, 4, totbal)
                   wb.save(response)
                   return response
               else:
                   return render_to_response('report/receivables.htm',{'vvtoday':vvtoday,'currse':currse,'varuser':varuser,'varerr':varerr,'form':form,'ll':ll,'comp':comp,'totbal':totbal,'admitted_class':admitted_class},context_instance = RequestContext(request))
        else:
            form = studentForm()
        return render_to_response('report/receivables.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))

    else:
       return HttpResponseRedirect('/login/')



def stockrep(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.statutory
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/report/unauto/')
        if request.method == 'POST':
         form = dateform(request.POST) # A form bound to the POST data
         if form.is_valid():
            caldate1 = form.cleaned_data['enddate']
            caldate2 = caldate1.split('/')
            varend = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
            tbal = 0
            tblstockrep.objects.all().delete()
            comp = tblcompanyinfo.objects.get(id = 1)
            p = tblstock.objects.all().exclude(subname ="MINI-STORE-BALANCE").order_by('acccode')
            sublist = []
            totbal = 0
            totqty = 0
            for j in p:
                totbalance = 0
                qty = 0
                avgpr = 0

                if tblstocktransaction.objects.filter(acccode = j.acccode,transcreated__lte = varend).count() == 0:
                   qty = 0
                   avgpr = 0
                   totbalance = 0
                else:
                    getdata = tblstocktransaction.objects.filter(acccode = j.acccode,transcreated__lte = varend).order_by('transcreated','id')
                    for u in getdata:
                        inout = u.stin - u.stout
                        unitpr = u.unitprice
                        tb = inout * unitpr
                        qty += inout
                        totbalance += tb
                    avgpr = float(totbalance) / float(qty)
                j = {'stockname':j.stockname,'acccode':j.acccode,'qtybal':qty,'avgprice':locale.format("%.2f",avgpr,grouping=True),'accbal':locale.format("%.2f",totbalance,grouping=True)}
                sublist.append(j)
                totbal += totbalance
                totqty += qty
            totbal = locale.format("%.2f",totbal,grouping=True)
            totqty = locale.format("%.2f",totqty,grouping=True)
            ll = sublist#tblstock.objects.all().exclude(subname ="MINI-STORE-BALANCE").order_by('acccode')

            if form.cleaned_data['excelfile']:
                    response = HttpResponse(mimetype="application/ms-excel")
                    response['Content-Disposition'] = 'attachment; filename=inventory.xls'
                    wb = xlwt.Workbook()
                    ws = wb.add_sheet('inventory')
                    ws.write(0, 1, comp.name)
                    ws.write(1, 1, comp.address)
                    ws.write(2, 1, 'INVENTORY REPORT')
                    ws.write(3, 1, 'Stock Code')
                    ws.write(3, 2, 'Stock Name')
                    ws.write(3, 3, 'Quantity In Store')
                    ws.write(3, 4, 'Average Price')
                    ws.write(3, 5, 'Account Balance')
                    k = 4
                    for m in ll:
                        ws.write(k, 1,m.acccode)
                        ws.write(k, 2, m.stockname)
                        ws.write(k, 3, m.qtybal)
                        ws.write(k, 4, m.avgprice)
                        ws.write(k, 5, m.accbal)
                        k += 1
                    ws.write(k, 2, 'Total')
                    ws.write(k, 3, totqty)
                    ws.write(k, 5, totbal)
                    wb.save(response)
                    return response
            else:
                    return render_to_response('report/stock.htm',{'form':form,'ll':ll,'comp':comp,'totbal':totbal,'totqty':totqty},context_instance = RequestContext(request))
        else:
           form = dateform()
        return render_to_response('report/stock.htm',{'form':form},context_instance = RequestContext(request))
    else:
       return HttpResponseRedirect('/login/')


def payablerep(request):
     if  "userid" in request.session:
     #getting the data
         #varuser = request.session['userid']
         varuser = request.session['userid']
         user = tbluseracc.objects.get(username = varuser)
         uenter = user.statutory
         if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/report/unauto/')
         varerr =""
         ll = []
         if request.method == 'POST':
             #deldata = tblstatement.objects.all().delete()
             form = dateform(request.POST) # A form bound to the POST data
             if form.is_valid():
                 caldate1 = form.cleaned_data['enddate']
                 caldate2 = caldate1.split('/')
                 varend = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                 tbal = 0
                 tblpayable.objects.all().delete()
                 comp = tblcompanyinfo.objects.get(id = 1)
                 llp = tblaccount.objects.filter(groupname ="CURRENT LIABILITIES",subgroupname = "PAYABLES").exclude(accname = "TRADE-CREDITORS").order_by('acccode')#tblreceiavables.objects.all().order_by('groupname','acccode')
                 for h in llp:
                      if payables.objects.filter(acccode = h.acccode).count() == 0:
                          pass
                      else:
                          opbal = getopbaleq(h.acccode,varend,h.groupname)
                          opbal1 = locale.format("%.2f",opbal,grouping=True)
                          tbal += opbal
                          km = payables.objects.get(acccode = h.acccode)
                          accdic = {'acc':h,'pid':km.id,'pos':opbal1}
                          ll.append(accdic)
                 totbal = locale.format("%.2f",tbal,grouping=True)
                 if form.cleaned_data['excelfile']:
                    response = HttpResponse(mimetype="application/ms-excel")
                    response['Content-Disposition'] = 'attachment; filename=payables.xls'
                    wb = xlwt.Workbook()
                    ws = wb.add_sheet('payables')
                    ws.write(0, 1, comp.name)
                    ws.write(1, 1, comp.address)
                    ws.write(2, 1, 'ACCOUNT PAYABLE REPORT')
                    ws.write(3, 1, 'Account Code')
                    ws.write(3, 2, 'Account Name')
                    ws.write(3, 3, 'Last Transaction Date')
                    ws.write(3, 4, 'Account Balance')
                    k = 4
                    for m in ll:
                       ws.write(k, 1,m['acc'].acccode)
                       ws.write(k, 2, m['acc'].accname)
                       ws.write(k, 3, m['acc'].lasttrandate)
                       ws.write(k, 4, m['acc'].accbal)
                       k += 1
                    wb.save(response)
                    return response
                 else:
                    return render_to_response('report/payables.htm',{'varuser':varuser,'varerr':varerr,'form':form,'ll':ll,'comp':comp,'totbal':totbal},context_instance = RequestContext(request))
         else:
            form = dateform()
         return render_to_response('report/payables.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')


def ministorerep(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.statutory
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/report/unauto/')
        if request.method == 'POST':

          form = dateform(request.POST) # A form bound to the POST data
          if form.is_valid():
            caldate1 = form.cleaned_data['enddate']
            caldate2 = caldate1.split('/')
            varend = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
            tbal = 0
            tblstockrep.objects.all().delete()
            comp = tblcompanyinfo.objects.get(id = 1)
            p = tblstock.objects.filter(subname ="MINI-STORE-BALANCE").order_by('acccode')
            sublist = []
            totbal = 0
            totqty = 0
            for j in p:
                totbalance = 0
                qty = 0
                avgpr = 0

                if tblstocktransaction.objects.filter(acccode = j.acccode,transcreated__lte = varend).count() == 0:
                    qty = 0
                    avgpr = 0
                    totbalance = 0
                else:
                    getdata = tblstocktransaction.objects.filter(acccode = j.acccode,transcreated__lte = varend).order_by('transcreated','id')
                    for u in getdata:
                        inout = u.stin - u.stout
                        unitpr = u.unitprice
                        tb = inout * unitpr
                        qty += inout
                        totbalance += tb
                    avgpr = float(totbalance) / float(qty)
                j = {'stockname':j.stockname,'acccode':j.acccode,'qtybal':qty,'avgprice':locale.format("%.2f",avgpr,grouping=True),'accbal':locale.format("%.2f",totbalance,grouping=True)}
                sublist.append(j)
                totbal += totbalance
                totqty += qty
            totbal = locale.format("%.2f",totbal,grouping=True)
            totqty = locale.format("%.2f",totqty,grouping=True)
            ll = sublist#tblstock.objects.all().exclude(subname ="MINI-STORE-BALANCE").order_by('acccode')
            if form.cleaned_data['excelfile']:
                response = HttpResponse(mimetype="application/ms-excel")
                response['Content-Disposition'] = 'attachment; filename=ministore.xls'
                wb = xlwt.Workbook()
                ws = wb.add_sheet('ministore')
                ws.write(0, 1, comp.name)
                ws.write(1, 1, comp.address)
                ws.write(2, 1, 'MINI-STROE REPORT')
                ws.write(3, 1, 'Stock Code')
                ws.write(3, 2, 'Stock Name')
                ws.write(3, 3, 'Quantity In Store')
                ws.write(3, 4, 'Average Price')
                ws.write(3, 5, 'Account Balance')
                k = 4
                for m in ll:
                    ws.write(k, 1,m.acccode)
                    ws.write(k, 2, m.stockname)
                    ws.write(k, 3, m.qtybal)
                    ws.write(k, 4, m.avgprice)
                    ws.write(k, 5, m.accbal)
                    k += 1
                ws.write(k, 2, 'Total')
                ws.write(k, 3, totqty)
                ws.write(k, 5, totbal)
                wb.save(response)
                return response
            else:
                return render_to_response('report/ministore.htm',{'form':form,'ll':ll,'comp':comp,'totbal':totbal,'totqty':totqty},context_instance = RequestContext(request))
        else:
            form = dateform()
        return render_to_response('report/ministore.htm',{'form':form},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


def trialbalancerep(request):
     if  "userid" in request.session:

        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.statutory
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/report/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
              tbltrialbalance.objects.all().delete()
              form = dateformpl(request.POST) # A form bound to the POST data
              if form.is_valid():
                 varstart2 = form.cleaned_data['startdate']
                 caldate1 = form.cleaned_data['enddate']
                 caldate2 = caldate1.split('/')
                 varend = datetime.date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                 varyear = varend.year
                 varstart1 = varstart2.split('/')
                 varstart = datetime.date(int(varstart1[2]),int(varstart1[0]),int(varstart1[1]))
                 stmon1 = ''
                 endmon1 = ''
                 #********************************************************
                 if varstart > varend :
                     varerr = "INVALID DATE RANGE"
                     return render_to_response('report/trialbalance.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))

                 if tblcalender.objects.all().count() == 0:
                     varerr = "PLEASE SET CALENDAR YEAR FOR THIS COMPANY"
                     return render_to_response('report/trialbalance.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
                 #GETTING THE CALENDAR YEAR
                 getdate = tblcalender.objects.all()
                 for g in getdate:
                     stmon1 = g.startmonth
                     endmon1 = g.endtmonth
                 stmon = stmon1.month# calendarstart month
                 cday = stmon1.day # calendar start day
                 cmon = endmon1.month
                 ceday = endmon1.day
                 endmon = varend.month
                 #make the date a year
                 varstartt =  varend - varstart
                 difference_in_years = (varstartt.days + varstartt.seconds/86400.0)/365.2425
                 #print 'the year difference :',difference_in_years
                 if difference_in_years > 1:
                    varerr = "INVALID DATE RANGE"
                    return render_to_response('report/trialbalance.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
                 # formulating the calendar year
                 castartdate = date(varstart.year,stmon,cday)
                 caenddate = date(varend.year,cmon,ceday)
                 ggdate = caenddate - castartdate
                 difference_in_years = (ggdate.days + ggdate.seconds/86400.0)/365.2425
                 #print 'the year difference :',difference_in_years
                 if difference_in_years > 1:
                     varerr = "INVALID DATE RANGE"
                     return render_to_response('report/trialbalance.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
                 varryear = varend.year
                 varrmonth =  varend.month
                 varrday =  varend.day
                 varrdate = str(varrday) + '/' + str(varrmonth) + '/' + str(varryear)
                 if tblaccount.objects.all().count() == 0:
                     varerr="NO ACCOUNT FOR TRIAL BALANCE"
                     return render_to_response('report/trialbalance.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
                 ll = []
                 lk = ""
                 grdic = {}
                 acclist = []
                 getgrp = tblgroup.objects.all().order_by('groupcode')
                 comp = tblcompanyinfo.objects.get(id = 1)
                 totdeb = 0
                 totcr = 0
                 totdeb1 =''
                 totcr1 = ''
                 for gr in getgrp :
                     sublist = []
                     subdic = {}
                     grtotal = 0
                     #taking care of control account
                     if tblaccount.objects.filter(groupcode = gr.groupcode,recreport = 'YES').exclude(groupname='CURRENT ASSETS',subgroupname = 'STAFF-DEBTORS',accname = 'STAFF-DEBTORS').exclude(groupname='CURRENT ASSETS',subgroupname = 'RECEIVABLES', accname = 'TRADE-DEBTORS').exclude(groupname='CURRENT ASSETS',subgroupname = 'STUDENT DEBTORS', accname = 'ACCOUNT RECEIVEABLE - STUDENT DEBTORS').exclude(groupname='CURRENT LIABILITIES',subgroupname = 'PAYABLES',  accname = 'TRADE-CREDITORS').count() == 0:
                         pass
                     else:
                         vardata = tblaccount.objects.filter(groupcode = gr.groupcode,recreport = 'YES').exclude(groupname='CURRENT ASSETS',subgroupname = 'STAFF-DEBTORS',accname = 'STAFF-DEBTORS').exclude(groupname='CURRENT ASSETS',subgroupname = 'RECEIVABLES', accname = 'TRADE-DEBTORS').exclude(groupname='CURRENT LIABILITIES',subgroupname = 'PAYABLES',  accname = 'TRADE-CREDITORS').exclude(groupname='CURRENT ASSETS',subgroupname = 'STUDENT DEBTORS', accname = 'ACCOUNT RECEIVEABLE - STUDENT DEBTORS').order_by('acccode')
                         cuspart =""
                         custo = 0
                         for j in vardata:
                             groupname = j.groupname
                             acccode = j.acccode
                             accname = j.accname
                             if stmon == varstart.month and cday == varstart.day:
                                opbal = getopbal(acccode,varstart,groupname)#getting the opening balance
                             else:
                                 opbal = 0
                             #opbal = getopbal(acccode,varstart,groupname)#getting the opening balance
                             accbal = getopbalrange(acccode,varstart,varend,groupname)
                             opbal += accbal
                             h = locale.format("%.2f",opbal,grouping=True)
                             if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS" or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                                 j = {'accname':accname,'acccode':acccode,'debit':h,'credit':'0.00','pid':j.id}
                             else:
                                 j = {'accname':accname,'acccode':acccode,'debit':'0.00','credit':h,'pid':j.id}
                             sublist.append(j)
                             grtotal += opbal
                     if gr.groupname == 'CURRENT ASSETS':
                         totgrr = 0
                         stdebtor = tblaccount.objects.filter(groupname = gr.groupname,subgroupname = 'STAFF-DEBTORS').exclude(accname = 'STAFF-DEBTORS')
                         for t in stdebtor:
                             acode = t.acccode
                             grname = t.groupname
                             acname = t.accname
                             if stmon == varstart.month and cday == varstart.day:
                                 opbal = getopbal(acode,varstart,grname)#getting the opening balance
                             else:
                                 opbal = 0
                             #opbal = getopbal(acode,varstart,grname)#getting the opening balance
                             accbal = getopbalrange(acode,varstart,varend,t.groupname)
                             opbal += accbal
                             totgrr += opbal
                         totgrr1 = locale.format("%.2f",totgrr,grouping=True)
                         j = {'accname':'STAFF-DEBTORS','acccode':'30601','debit':totgrr1,'credit':'0.00'}
                         sublist.append(j)
                         grtotal += totgrr
                         trdebtor = tblaccount.objects.filter(groupname = gr.groupname,subgroupname = 'RECEIVABLES').exclude(accname = 'TRADE-DEBTORS')
                         trtotal = 0
                         for t in trdebtor:
                             acode = t.acccode
                             grname = t.groupname
                             acname = t.accname
                             #print 'The Account :',t.accname
                             if stmon == varstart.month and cday == varstart.day:
                                 opbal = getopbal(acode,varstart,grname)#getting the opening balance
                             else:
                                 opbal = 0
                             #opbal = getopbal(acode,varstart,grname)#getting the opening balance
                             accbal = getopbalrange(acode,varstart,varend,t.groupname)
                             opbal += accbal
                             trtotal += opbal
                         trtotal1 = locale.format("%.2f",trtotal,grouping=True)
                         j = {'accname':'ACCOUNT RECEIVEABLE - STUDENT DEBTORS','acccode':'30301','debit':trtotal1,'credit':'0.00'}
                         sublist.append(j)
                         grtotal += trtotal
                     if gr.groupname == 'CURRENT LIABILITIES':
                         totgrr2 = 0
                         stdebtor = tblaccount.objects.filter(groupname = gr.groupname,subgroupname = 'PAYABLES').exclude(recreport = 'YES')
                         for t in stdebtor:
                             acode = t.acccode
                             grname = t.groupname
                             acname = t.accname
                             if stmon == varstart.month and cday == varstart.day:
                                 opbal = getopbal(acode,varstart,t.groupname)#getting the opening balance
                             else:
                                 opbal = 0
                             #opbal = getopbal(acode,varstart,grname)#getting the opening balance
                             accbal = getopbalrange(acode,varstart,varend,t.groupname)
                             opbal += accbal
                             totgrr2 += opbal
                         totgrr13 = locale.format("%.2f",totgrr2,grouping=True)
                         j = {'accname':'TRADE-CREDITORS','acccode':'40101','debit':'0.00','credit':totgrr13}
                         sublist.append(j)
                         grtotal += totgrr2

                     grtotal1 = locale.format("%.2f",grtotal,grouping=True)
                     if gr.groupname == "FIXED ASSETS" or gr.groupname == "NON-CURRENT ASSETS"  or gr.groupname == "CURRENT ASSETS" or gr.groupname == "EXPENSES" or gr.groupname == "COST OF SALES":
                         tdr = grtotal1
                         tcr = '0.00'
                         totdeb  +=  grtotal
                     else:
                         tdr = '0.00'
                         tcr = grtotal1
                         totcr += grtotal
                     grdic = {'groupname':gr.groupname,'grdetails':sublist,'grdeb':tdr,'grcr':tcr}
                     acclist.append(grdic)
                     totdeb1 = locale.format("%.2f",totdeb,grouping=True)
                     totcr1 = locale.format("%.2f",totcr,grouping=True)

                 if form.cleaned_data['excelfile']:
                     response = HttpResponse(mimetype="application/ms-excel")
                     response['Content-Disposition'] = 'attachment; filename=trialbalance.xls'
                     wb = xlwt.Workbook()
                     ws = wb.add_sheet('trialbalance')
                     ws.write(0, 1, comp.name)
                     ws.write(1, 1, comp.address)
                     ws.write(2, 1, 'TRIAL BALANCE - %s TO %s' %(varstart.strftime("%d-%m-%Y"),varend.strftime("%d-%m-%Y")))
                     ws.write(3, 1, 'Account Name')
                     ws.write(3, 2, 'Account Code')
                     ws.write(3, 3, 'Debit')
                     ws.write(3, 4, 'Credit')
                     k = 4
                     for n in acclist:
                         ws.write(k, 1, n['groupname'])
                         k += 1
                         for j in n['grdetails']:
                             ws.write(k, 1, j['accname'].title())
                             ws.write(k, 2, j['acccode'])
                             ws.write(k, 3, j['debit'])
                             ws.write(k, 4, j['credit'])
                             k += 1

                         ws.write(k, 2, 'SUB TOTAL')
                         ws.write(k, 3, n['grdeb'])
                         ws.write(k, 4, n['grcr'])
                         k += 1
                     ws.write(k, 2, 'GRAND TOTAL')
                     ws.write(k, 3, totdeb1)
                     ws.write(k, 4, totcr1)
                     wb.save(response)
                     return response
                 else:

                     return render_to_response('report/trialbalance.htm',{'varuser':varuser,'varerr':varerr,'form':form,'ll':acclist,'comp':comp,'varstart':varstart,'varend':varend,'totaldebit':totdeb1,'totalcredit':totcr1,'printdate':gettime()},context_instance = RequestContext(request))

        else:
            form = dateformpl()
            #varerr ="Invalid Date"
        return render_to_response('report/trialbalance.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def profitlossrep(request):
     if  "userid" in request.session:

        #varuser = request.session['userid']
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.statutory
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/report/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          deldata = tbltrialbalance.objects.all().delete()
          deldata2 = tblprofitloss.objects.all().delete()
          form = dateformpl(request.POST) # A form bound to the POST data
          if form.is_valid():
             caldate1 = form.cleaned_data['startdate']
             caldate11 = form.cleaned_data['enddate']
             caldate2 = caldate1.split('/')
             varstart = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
             caldate22 = caldate11.split('/')
             varend = date(int(caldate22[2]),int(caldate22[0]),int(caldate22[1]))

             #varstart = date(vartyear,01,01)
             stmon = ''

             edmon = varend.month  # i.e r
             if varstart > varend :
                 varerr = "INVALID DATE RANGE"
                 return render_to_response('report/profitloss.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
             #********************************************************
             if tblcalender.objects.all().count() == 0:
                 varerr = "NO START DATE"
                 #varerr = "INVALID DATE RANGE"
                 return render_to_response('report/profitloss.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))

             getdate = tblcalender.objects.all()
             stmon1 = 0
             endmon1 = 0
             for g in getdate:
                 stmon1 = g.startmonth
                 endmon1 = g.endtmonth
             stmon = stmon1.month# calendarstart month
             cday = stmon1.day # calendar start day
             cmon = endmon1.month
             ceday = endmon1.day
             endmon = varend.month
             #make the date a year
             varstartt =  varend - varstart
             difference_in_years = (varstartt.days + varstartt.seconds/86400.0)/365.2425
             #print 'the year difference :',difference_in_years
             if difference_in_years > 1:
                 varerr = "INVALID DATE RANGE"
                 return render_to_response('report/profitloss.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
                 # formulating the calendar year
             castartdate = date(varstart.year,stmon,cday)
             caenddate = date(varend.year,cmon,ceday)
             ggdate = caenddate - castartdate
             difference_in_years = (ggdate.days + ggdate.seconds/86400.0)/365.2425
             #print 'the year difference :',difference_in_years
             if difference_in_years > 1:
                 varerr = "INVALID DATE RANGE"
                 return render_to_response('report/profitloss.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))

             #******************************************************

             if varstart > varend :
                 varerr = "INVALID DATE RANGE"
                 return render_to_response('report/profitloss.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))

             if tblaccount.objects.all().count() == 0:
                  varerr="NO ACCOUNT FOR TRIAL BALANCE"
                  return render_to_response('report/profitloss.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
             ll = []
             lk = ""
             grdic = {}
             acclist = []
             #*******************************************************treating income
             sublist = []
             totgrr2 = 0
             grtotal = 0
             vardata = tblaccount.objects.filter(groupname = 'INCOME',recreport = 'YES').order_by('acccode')
             for j in vardata:
                 groupname = j.groupname
                 acccode = j.acccode
                 accname = j.accname
                 if stmon == varstart.month and cday == varstart.day:
                     opbal = getopbal(acccode,varstart,groupname)#getting the opening balance
                 else:
                     opbal = 0
                 fdata = tbltransaction.objects.filter(acccode = acccode,transdate__range=(varstart,varend)).order_by('transdate','id')

                 for g in fdata:
                     debit = g.debit
                     credit = g.credit
                     if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS"  or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                         opbal = opbal + debit - credit
                     else:
                         opbal = opbal + credit - debit
                 totgrr2 += opbal
                 h = locale.format("%.2f",opbal,grouping=True)
                 if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS" or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                     j = {'accname':accname,'acccode':acccode,'debit':h,'credit':'','pid':j.id}
                 else:
                     j = {'accname':accname,'acccode':acccode,'debit':'','credit':h,'pid':j.id}
                 sublist.append(j)
             grtotal1 = locale.format("%.2f",totgrr2,grouping=True)
             tdr = ''
             tcr = grtotal1
             #totcr += grtotal
             j = {'accname':'','acccode':'','debit':'','credit':tcr}
             sublist.append(j)
             grdic = {'groupname':'INCOME','grdetails':sublist,'grdeb':tdr,'grcr':tcr}
             acclist.append(grdic)
             #************************************************************treating the costof sales
             sublist = []
             grtotalcos = 0
             vardata = tblaccount.objects.filter(groupname = 'COST OF SALES',recreport = 'YES').order_by('acccode')
             for j in vardata:
                 groupname = j.groupname
                 acccode = j.acccode
                 accname = j.accname
                 if stmon == varstart.month and cday == varstart.day:
                     opbal = getopbal(acccode,varstart,groupname)#getting the opening balance
                 else:
                     opbal = 0
                 fdata = tbltransaction.objects.filter(acccode = acccode,transdate__range=(varstart,varend)).order_by('transdate','id')
                 for g in fdata:
                     debit = g.debit
                     credit = g.credit
                     if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS"  or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                         opbal = opbal + debit - credit
                     else:
                         opbal = opbal + credit - debit
                 grtotalcos += opbal
                 h = locale.format("%.2f",opbal,grouping=True)
                 if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS" or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                     j = {'accname':accname,'acccode':acccode,'debit':h,'credit':'','pid':j.id}
                 else:
                     j = {'accname':accname,'acccode':acccode,'debit':'','credit':h,'pid':j.id}
                 sublist.append(j)
             grtotalcos1 = locale.format("%.2f",grtotalcos,grouping=True)
             tdr = grtotalcos1
             tcr = ''
             #totcr += grtotal
             j = {'accname':'','acccode':'','debit':tdr,'credit':tdr}
             sublist.append(j)
             grdic = {'groupname':'COST OF SALES','grdetails':sublist,'grdeb':tdr,'grcr':tcr}
             acclist.append(grdic)
             diffinc = totgrr2 - grtotalcos
             #*********************************************************************GROSS PROFIT
             sublist = []
             j = {'accname':'','acccode':'','debit':'','credit':locale.format("%.2f",diffinc,grouping=True)}
             sublist.append(j)
             grdic = {'groupname':'GROSS PROFIT','grdetails':sublist,'grdeb':tdr,'grcr':tcr}
             acclist.append(grdic)
             #************************************************************
             sublist = []
             exptotal = 0
             vardata = tblaccount.objects.filter(groupname = 'EXPENSES',recreport = 'YES').order_by('acccode')
             for j in vardata:
                 groupname = j.groupname
                 acccode = j.acccode
                 accname = j.accname
                 if stmon == varstart.month and cday == varstart.day:
                     opbal = getopbal(acccode,varstart,groupname)#getting the opening balance
                 else:
                     opbal = 0
                 fdata = tbltransaction.objects.filter(acccode = acccode,transdate__range=(varstart,varend)).order_by('transdate','id')
                 for g in fdata:
                     debit = g.debit
                     credit = g.credit
                     if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS"  or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                         opbal = opbal + debit - credit
                     else:
                         opbal = opbal + credit - debit
                 exptotal += opbal
                 h = locale.format("%.2f",opbal,grouping=True)
                 if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS" or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                     j = {'accname':accname,'acccode':acccode,'debit':h,'credit':'','pid':j.id}
                 else:
                     j = {'accname':accname,'acccode':acccode,'debit':'','credit':h,'pid':j.id}
                 sublist.append(j)
             grtotalcos1 = locale.format("%.2f",exptotal,grouping=True)
             tdr = grtotalcos1
             tcr = ''
             #totcr += grtotal
             j = {'accname':'','acccode':'','debit':tdr,'credit':tdr}
             sublist.append(j)
             grdic = {'groupname':'EXPENSES','grdetails':sublist,'grdeb':tdr,'grcr':tcr}
             acclist.append(grdic)
             #***************************************************************
             netprofit = diffinc -exptotal #totcr-totdeb#NET PAY
             stdebtor = tblaccount.objects.filter(acccode = '80301')#TAX aCCOUNT
             taxamt = 0
             taxname = 'TAX-EXPENSES'
             for t in stdebtor:
                 acode = t.acccode
                 grname = t.groupname
                 acname = t.accname
                 if stmon == varstart.month and cday == varstart.day:
                     opbal = getopbal(acode,varstart,grname)#getting the opening balance
                 else:
                     opbal = 0
                     # opbal = getopbal(acode,varstart,grname)#getting the opening balance
                 fdata = tbltransaction.objects.filter(acccode = acode,transdate__range=(varstart,varend)).order_by('transdate','id')
                 for g in fdata:
                     debit = g.debit
                     credit = g.credit
                     if grname == "FIXED ASSETS" or grname == "NON-CURRENT ASSETS"  or grname == "CURRENT ASSETS" or grname == "EXPENSES" or grname == "COST OF SALES":
                         opbal = opbal + debit - credit
                     else:
                         opbal = opbal + credit - debit
                     taxamt = opbal
                     taxname = acname
             #kk = {'taxname':acname,}
             proaftertax = netprofit - taxamt
           #********************************************************************
             comp = tblcompanyinfo.objects.get(id = 1)
             if form.cleaned_data['excelfile']:
                 response = HttpResponse(mimetype="application/ms-excel")
                 response['Content-Disposition'] = 'attachment; filename=profitloss.xls'
                 wb = xlwt.Workbook()
                 ws = wb.add_sheet('pl')
                 ws.write(0, 1, comp.name)
                 ws.write(1, 1, comp.address)
                 ws.write(2, 1, 'PROFIT/LOSS - %s TO %s' %(varstart.strftime("%d-%m-%Y"),varend.strftime("%d-%m-%Y")))
                 ws.write(3, 1, 'Account Name')
                 ws.write(3, 2, 'Account Code')
                 ws.write(3, 3, '=N=')
                 ws.write(3, 4, '=N=')
                 k = 4
                 for n in acclist:
                     ws.write(k, 1, n['groupname'])
                     k += 1
                     for j in n['grdetails']:

                         ws.write(k, 1, j['accname'].title())
                         ws.write(k, 2, j['acccode'])
                         ws.write(k, 3, j['debit'])
                         ws.write(k, 4, j['credit'])
                         k += 1
                 k += 1
                 #ws.write(k, 2, 'TOTAL')
                 ws.write(k, 2, 'NET PROFIT')
                 ws.write(k, 4, locale.format("%.2f",netprofit,grouping=True))
                 #k += 1
                 #ws.write(k, 2, 'TOTAL')
                 #ws.write(k, 2, taxname)
                 #ws.write(k, 4, locale.format("%.2f",taxamt,grouping=True))
                 #k += 1
                 #ws.write(k, 2, 'TOTAL')
                 #ws.write(k, 2, 'NET PROFIT AFTER TAX')
                 #ws.write(k, 4, locale.format("%.2f",proaftertax,grouping=True))

                 wb.save(response)
                 return response
             else:
                 return render_to_response('report/profitloss.htm',{'varuser':varuser,'varerr':varerr,'form':form,'ll':acclist,'comp':comp,'varstart':varstart,'varend':varend,'printdate':gettime(),'netprofit':locale.format("%.2f",netprofit,grouping=True),'taxname':taxname,'taxamt':locale.format("%.2f",taxamt,grouping=True),'profitaftertax':locale.format("%.2f",proaftertax,grouping=True),'beforetax':'NET PROFIT ','aftertax':'NET PROFIT AFTER TAX'},context_instance = RequestContext(request))
              #*******************
        else:

            form = dateformpl()
            #return render_to_response('report/profitloss.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))

            #getdetails = tbltemp.objects.filter(userid = varuser).order_by('transdate')
        return render_to_response('report/profitloss.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')
def balancesheetrep(request):
    if  "userid" in request.session:

        #varuser = request.session['userid']
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.statutory
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/report/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          tbltrialbalance.objects.all().delete()#tblbalancesheet
          tblbalancesheet.objects.all().delete()
          form = dateform(request.POST) # A form bound to the POST data
          if form.is_valid():
             #varstart = form.cleaned_data['enddate']
             caldate1 = form.cleaned_data['enddate']
             caldate2 = caldate1.split('/')
             varend = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
             vartyear = varend.year
             varyear = varend.year
             stmon1 = 1
             #********************************************************
             if tblcalender.objects.all().count() == 0:
                 varerr = "NO START DATE"
                 #varerr = "INVALID DATE RANGE"
                 return render_to_response('report/trialbalance.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
             getdate = tblcalender.objects.all()
             for g in getdate:
                 stmon1 = g.startmonth
                 endmon1 = g.endtmonth
             stmon = stmon1.month
             endmon = varend.month
             cday = stmon1.day # calendar start day
             rvaryear = int(varyear)
             if int(stmon) > int(endmon):
                 startyear = rvaryear - 1
                 endyear = rvaryear
             else:
                 startyear = rvaryear
                 endyear = rvaryear
             varstart = date(startyear,stmon,1)
             if varstart > varend :
                 varerr = "INVALID DATE RANGE"
                 return render_to_response('report/balancesheet.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))

             if tblaccount.objects.all().count() == 0:
                  varerr="NO ACCOUNT FOR BALANCE SHEET"
                  return render_to_response('report/balancesheet.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
             ll = []
             lk = ""
             grdic = {}
             acclist = []
             #*******************************************************treating income
             sublist = []
             totgrr2 = 0
             grtotal = 0
             vardata = tblaccount.objects.filter(groupname = 'FIXED ASSETS',recreport = 'YES').order_by('acccode')
             for j in vardata:
                 groupname = j.groupname
                 acccode = j.acccode
                 accname = j.accname
                 #if stmon == varstart.month and cday == varstart.day:
                  #   opbal = getopbal(acccode,varstart,groupname)#getting the opening balance
                 #else:
                  #   opbal = 0
                 opbal = getopbal(acccode,varstart,groupname)#getting the opening balance
                 fdata = tbltransaction.objects.filter(acccode = acccode,transdate__range=(varstart,varend)).order_by('transdate','id')
                 for g in fdata:
                     debit = g.debit
                     credit = g.credit
                     if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS"  or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                         opbal = opbal + debit - credit
                     else:
                         opbal = opbal + credit - debit
                 totgrr2 += opbal
                 h = locale.format("%.2f",opbal,grouping=True)
                 if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS" or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                     j = {'accname':accname,'acccode':acccode,'debit':'','credit':h,'pid':j.id}
                 else:
                     j = {'accname':accname,'acccode':acccode,'debit':'','credit':h,'pid':j.id}
                 sublist.append(j)
             grtotal1 = locale.format("%.2f",totgrr2,grouping=True)
             tdr = ''
             tcr = grtotal1
             #totcr += grtotal
             j = {'accname':'','acccode':'','debit':'','credit':tcr}
             sublist.append(j)
             grdic = {'groupname':'FIXED ASSETS','grdetails':sublist,'grdeb':tdr,'grcr':tcr}
             acclist.append(grdic)
             #************************************************************treating accumulation depreciation
             sublist = []
             grtotalcos = 0
             vardata = tblaccount.objects.filter(groupname = 'ACCUMULATED DEPRECIATION',recreport = 'YES').order_by('acccode')
             for j in vardata:
                 groupname = j.groupname
                 acccode = j.acccode
                 accname = j.accname
                 #if stmon == varstart.month and cday == varstart.day:
                  #   opbal = getopbal(acccode,varstart,groupname)#getting the opening balance
                 #else:
                  #   opbal = 0
                 opbal = getopbal(acccode,varstart,groupname)#getting the opening balance
                 fdata = tbltransaction.objects.filter(acccode = acccode,transdate__range=(varstart,varend)).order_by('transdate','id')
                 for g in fdata:
                     debit = g.debit
                     credit = g.credit
                     if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS"  or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                         opbal = opbal + debit - credit
                     else:
                         opbal = opbal + credit - debit
                 grtotalcos += opbal
                 h = locale.format("%.2f",opbal,grouping=True)
                 if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS" or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                     j = {'accname':accname,'acccode':acccode,'debit':'','credit':h,'pid':j.id}
                 else:
                     j = {'accname':accname,'acccode':acccode,'debit':h,'credit':'','pid':j.id}
                 sublist.append(j)
             grtotalcos1 = locale.format("%.2f",grtotalcos,grouping=True)
             tdr = grtotalcos1
             tcr = ''
             #totcr += grtotal
             j = {'accname':'','acccode':'','debit':tdr,'credit':''}
             sublist.append(j)
             grdic = {'groupname':'ACCUMULATED DEPRECIATION','grdetails':sublist,'grdeb':tdr,'grcr':tcr}
             acclist.append(grdic)
             diffinc = totgrr2 - grtotalcos
             #************************************************************
             sublist = []
             j = {'accname':'','acccode':'','debit':'','credit':locale.format("%.2f",diffinc,grouping=True)}
             sublist.append(j)
             grdic = {'groupname':'NET FIXED ASSET','grdetails':sublist,'grdeb':tdr,'grcr':tcr}
             acclist.append(grdic)
             #*********************************************TREATING CURRENT ASSETS
             sublist = []
             grtotalcurr = 0
             vardata = tblaccount.objects.filter(groupname = 'CURRENT ASSETS',recreport = 'YES').exclude(groupname='CURRENT ASSETS',subgroupname = 'STAFF-DEBTORS',accname = 'STAFF-DEBTORS').exclude(groupname='CURRENT ASSETS',subgroupname = 'RECEIVABLES', accname = 'TRADE-DEBTORS').order_by('acccode')
             for j in vardata:
                 groupname = j.groupname
                 acccode = j.acccode
                 accname = j.accname
                # if stmon == varstart.month and cday == varstart.day:
                 #    opbal = getopbal(acccode,varstart,groupname)#getting the opening balance
                 #else:
                  #   opbal = 0
                 opbal = getopbal(acccode,varstart,groupname)#getting the opening balance
                 fdata = tbltransaction.objects.filter(acccode = acccode,transdate__range=(varstart,varend)).order_by('transdate','id')
                 for g in fdata:
                     debit = g.debit
                     credit = g.credit
                     if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS"  or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                         opbal = opbal + debit - credit
                     else:
                         opbal = opbal + credit - debit
                 grtotalcurr += opbal
                 h = locale.format("%.2f",opbal,grouping=True)
                 if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS" or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                     j = {'accname':accname,'acccode':acccode,'debit':h,'credit':'','pid':j.id}
                 else:
                     j = {'accname':accname,'acccode':acccode,'debit':'','credit':h,'pid':j.id}
                 sublist.append(j)
             #treating staff debtor
             totgrr = 0
             stdebtor = tblaccount.objects.filter(groupname = 'CURRENT ASSETS',subgroupname = 'STAFF-DEBTORS').exclude(accname = 'STAFF-DEBTORS')
             for t in stdebtor:
                 acode = t.acccode
                 grname = t.groupname
                 acname = t.accname
                 #if stmon == varstart.month and cday == varstart.day:
                  #   opbal = getopbal(acode,varstart,grname)#getting the opening balance
                 #else:
                  #   opbal = 0
                 opbal = getopbal(acode,varstart,grname)#getting the opening balance
                 fdata = tbltransaction.objects.filter(acccode = acode,transdate__range=(varstart,varend)).order_by('transdate','id')
                 for g in fdata:
                     debit = g.debit
                     credit = g.credit
                     if grname == "FIXED ASSETS" or grname == "NON-CURRENT ASSETS"  or grname == "CURRENT ASSETS" or grname == "EXPENSES" or grname == "COST OF SALES":
                         opbal = opbal + debit - credit
                     else:
                         opbal = opbal + credit - debit
                 totgrr += opbal
             j = {'accname':'STAFF-DEBTORS','acccode':'30601','credit':'','debit':locale.format("%.2f",totgrr,grouping=True)}
             sublist.append(j)
             grtotalcurr += totgrr
             #getting trade-debtors
             trdebtor = tblaccount.objects.filter(groupname = "CURRENT ASSETS",subgroupname = 'RECEIVABLES').exclude(accname = 'TRADE-DEBTORS').exclude(groupname='CURRENT ASSETS',subgroupname = 'STUDENT DEBTORS', accname = 'ACCOUNT RECEIVEABLE - STUDENT DEBTORS')
             trtotal = 0
             for t in trdebtor:
                 acode = t.acccode
                 grname = t.groupname
                 acname = t.accname
                 #print 'The Account :',t.accname
                # if stmon == varstart.month and cday == varstart.day:
                 #    opbal = getopbal(acode,varstart,grname)#getting the opening balance
                 #else:
                  #   opbal = 0
                 opbal = getopbal(acode,varstart,grname)#getting the opening balance
                 fdata = tbltransaction.objects.filter(acccode = acode,transdate__range=(varstart,varend)).order_by('transdate','id')
                 for g in fdata:
                     debit = g.debit
                     credit = g.credit
                     if grname == "FIXED ASSETS" or grname == "NON-CURRENT ASSETS"  or grname == "CURRENT ASSETS" or grname == "EXPENSES" or grname == "COST OF SALES":
                         opbal = opbal + debit - credit
                     else:
                         opbal = opbal + credit - debit
                 trtotal += opbal
             trtotal1 = locale.format("%.2f",trtotal,grouping=True)
             j = {'accname':'ACCOUNT RECEIVEABLE - STUDENT DEBTORS','acccode':'30301','debit':trtotal1,'credit':''}
             sublist.append(j)
             grtotalcurr += trtotal
             #****************************************
             grtotalcos1 = locale.format("%.2f",grtotalcurr,grouping=True)
             tdr = grtotalcos1
             tcr = ''
             #totcr += grtotal
             j = {'accname':'','acccode':'','debit':tdr,'credit':''}
             sublist.append(j)
             grdic = {'groupname':'CURRENT ASSETS','grdetails':sublist,'grdeb':tdr,'grcr':tcr}
             acclist.append(grdic)
             #******************************************************************************treating current liabilities
             sublist = []
             grtotallib = 0
             vardata = tblaccount.objects.filter(groupname = 'CURRENT LIABILITIES',recreport = 'YES').exclude(groupname='CURRENT LIABILITIES',subgroupname = 'PAYABLES',  accname = 'TRADE-CREDITORS').order_by('acccode')
             for j in vardata:
                 groupname = j.groupname
                 acccode = j.acccode
                 accname = j.accname
                 #if stmon == varstart.month and cday == varstart.day:
                  #   opbal = getopbal(acccode,varstart,groupname)#getting the opening balance
                 #else:
                  #   opbal = 0
                 opbal = getopbal(acccode,varstart,groupname)#getting the opening balance
                 fdata = tbltransaction.objects.filter(acccode = acccode,transdate__range=(varstart,varend)).order_by('transdate','id')
                 for g in fdata:
                     debit = g.debit
                     credit = g.credit
                     if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS"  or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                         opbal = opbal + debit - credit
                     else:
                         opbal = opbal + credit - debit
                 grtotallib += opbal
                 h = locale.format("%.2f",opbal,grouping=True)
                 if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS" or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                     j = {'accname':accname,'acccode':acccode,'debit':'','credit':h,'pid':j.id}
                 else:
                     j = {'accname':accname,'acccode':acccode,'debit':h,'credit':'','pid':j.id}
                 sublist.append(j)
             #treating trade-creditor
             totgrr2 = 0
             stdebtor = tblaccount.objects.filter(groupname = "CURRENT LIABILITIES",subgroupname = 'PAYABLES').exclude(recreport = 'YES')
             for t in stdebtor:
                 acode = t.acccode
                 grname = t.groupname
                 acname = t.accname
                 #if stmon == varstart.month and cday == varstart.day:
                  #   opbal = getopbal(acode,varstart,grname)#getting the opening balance
                 #else:
                  #   opbal = 0
                 opbal = getopbal(acode,varstart,grname)#getting the opening balance
                     # opbal = getopbal(acode,varstart,grname)#getting the opening balance
                 fdata = tbltransaction.objects.filter(acccode = acode,transdate__range=(varstart,varend)).order_by('transdate','id')
                 for g in fdata:
                     debit = g.debit
                     credit = g.credit
                     if grname == "FIXED ASSETS" or grname == "NON-CURRENT ASSETS"  or grname == "CURRENT ASSETS" or grname == "EXPENSES" or grname == "COST OF SALES":
                         opbal = opbal + debit - credit
                     else:
                         opbal = opbal + credit - debit
                 totgrr2 += opbal
             totgrr13 = locale.format("%.2f",totgrr2,grouping=True)
             j = {'accname':'TRADE-CREDITORS','acccode':'40101','debit':totgrr13,'credit':''}
             sublist.append(j)
             grtotallib += totgrr2
             #****************************************
             grtotalcos1 = locale.format("%.2f",grtotallib,grouping=True)
             tdr = grtotalcos1
             tcr = ''
             j = {'accname':'','acccode':'','debit':tdr,'credit':''}
             sublist.append(j)
             grdic = {'groupname':'CURRENT LIABILITIES','grdetails':sublist,'grdeb':tdr,'grcr':tcr}
             acclist.append(grdic)
             #*******************************************************************************
             sublist =[]
             liadiff = grtotalcurr - grtotallib
             net = locale.format("%.2f",liadiff,grouping=True)
             j = {'accname':'','acccode':'','debit':'','credit':locale.format("%.2f",liadiff,grouping=True)}
             sublist.append(j)
             grdic = {'groupname':'NET CURRENT ASSETS','grdetails':sublist,'grdeb':tdr,'grcr':tcr}
             acclist.append(grdic)

             #************************************************************
             wokcap = grtotalcurr - grtotallib + diffinc
             sublist = []
             j = {'accname':'','acccode':'','debit':'','credit':locale.format("%.2f",wokcap,grouping=True)}
             sublist.append(j)
             grdic = {'groupname':'WORKING CAPITAL','grdetails':sublist,'grdeb':tdr,'grcr':tcr}
             acclist.append(grdic)
             #*********************************************capital and reseves
             sublist = []
             grtotalcapres = 0
             vardata = tblaccount.objects.filter(groupname = 'CAPITAL AND RESERVES',recreport = 'YES').exclude(groupname='CAPITAL AND RESERVES',subgroupname = 'SHAREHOLDERS FUND',  accname = 'CURRENT-YEAR-P/L').order_by('acccode')
             for j in vardata:
                 groupname = j.groupname
                 acccode = j.acccode
                 accname = j.accname
                 #if stmon == varstart.month and cday == varstart.day:
                  #   opbal = getopbal(acccode,varstart,groupname)#getting the opening balance
                 #else:
                  #   opbal = 0
                 opbal = getopbal(acccode,varstart,groupname)#getting the opening balance
                 fdata = tbltransaction.objects.filter(acccode = acccode,transdate__range=(varstart,varend)).order_by('transdate','id')
                 for g in fdata:
                     debit = g.debit
                     credit = g.credit
                     if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS"  or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                         opbal = opbal + debit - credit
                     else:
                         opbal = opbal + credit - debit
                 grtotalcapres += opbal
                 h = locale.format("%.2f",opbal,grouping=True)
                 if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS" or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                     j = {'accname':accname,'acccode':acccode,'debit':'','credit':h,'pid':j.id}
                 else:
                     j = {'accname':accname,'acccode':acccode,'debit':h,'credit':'','pid':j.id}
                 sublist.append(j)
             #getting p & L
             p = getaccposition(varstart,stmon,cday,varend)
             j = {'accname':'CURRENT-YEAR-P/L','acccode':'60104','debit':locale.format("%.2f",p,grouping=True),'credit':''}
             sublist.append(j)
             grtotalcapres += p
             grtotalcos1 = locale.format("%.2f",grtotalcapres,grouping=True)
             tdr = grtotalcos1
             tcr = ''
             #totcr += grtotal
             j = {'accname':'','acccode':'','debit':tdr,'credit':''}
             sublist.append(j)
             grdic = {'groupname':'CAPITAL AND RESERVES','grdetails':sublist,'grdeb':tdr,'grcr':tcr}
             acclist.append(grdic)
             #******************************************************************************getting long term liablities
             sublist = []
             grtotallia = 0
             vardata = tblaccount.objects.filter(groupname = 'LONG TERM LIABILITIES',recreport = 'YES').order_by('acccode')
             for j in vardata:
                 groupname = j.groupname
                 acccode = j.acccode
                 accname = j.accname
                 #if stmon == varstart.month and cday == varstart.day:
                  #   opbal = getopbal(acccode,varstart,groupname)#getting the opening balance
                 #else:
                  #   opbal = 0
                 opbal = getopbal(acccode,varstart,groupname)#getting the opening balance
                 fdata = tbltransaction.objects.filter(acccode = acccode,transdate__range=(varstart,varend)).order_by('transdate','id')
                 for g in fdata:
                     debit = g.debit
                     credit = g.credit
                     if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS"  or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                         opbal = opbal + debit - credit
                     else:
                         opbal = opbal + credit - debit
                 grtotallia += opbal
                 h = locale.format("%.2f",opbal,grouping=True)
                 if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS" or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                     j = {'accname':accname,'acccode':acccode,'debit':'','credit':h,'pid':j.id}
                 else:
                     j = {'accname':accname,'acccode':acccode,'debit':h,'credit':'','pid':j.id}
                 sublist.append(j)
             grtotalcos1 = locale.format("%.2f",grtotallia,grouping=True)
             tdr = grtotalcos1
             tcr = ''
             #totcr += grtotal
             j = {'accname':'','acccode':'','debit':tdr,'credit':''}
             sublist.append(j)
             grdic = {'groupname':'LONG TERM LIABILITIES','grdetails':sublist,'grdeb':tdr,'grcr':tcr}
             acclist.append(grdic)
             #*************************************************
             balancesheet = grtotalcapres + grtotallia
             sublist = []
             j = {'accname':'','acccode':'','debit':'','credit':locale.format("%.2f",balancesheet,grouping=True)}
             sublist.append(j)
             grdic = {'groupname':'','grdetails':sublist,'grdeb':tdr,'grcr':tcr}
             acclist.append(grdic)
             #*******************************************************************
             #print 'start date :',varstart
             comp = tblcompanyinfo.objects.get(id = 1)
             if form.cleaned_data['excelfile']:
                 response = HttpResponse(mimetype="application/ms-excel")
                 response['Content-Disposition'] = 'attachment; filename=balancesheet.xls'
                 wb = xlwt.Workbook()
                 ws = wb.add_sheet('balancesheet')
                 ws.write(0, 1, comp.name)
                 ws.write(1, 1, comp.address)
                 ws.write(2, 1, 'BALANCE SHEET AS AT - %s' %(varend.strftime("%d-%m-%Y")))
                 ws.write(3, 1, 'Account Name')
                 ws.write(3, 2, 'Account Code')
                 ws.write(3, 3, '=N=')
                 ws.write(3, 4, '=N=')
                 k = 4
                 for n in acclist:
                     ws.write(k, 1, n['groupname'])
                     k += 1
                     for j in n['grdetails']:
                         ws.write(k, 1, j['accname'].title())
                         ws.write(k, 2, j['acccode'])
                         ws.write(k, 3, j['debit'])
                         ws.write(k, 4, j['credit'])
                         k += 1
                 wb.save(response)
                 return response
             else:

                 return render_to_response('report/balancesheet.htm',{'varuser':varuser,'varerr':varerr,'form':form,'ll':acclist,'comp':comp,'varstart':varstart,'varend':varend,'printdate':gettime()},context_instance = RequestContext(request))
        else:
            form = dateform()
        return render_to_response('report/balancesheet.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
    else:
       return HttpResponseRedirect('/login/')

def statementreprep(request):
    if  "userid" in request.session:

        #varuser = request.session['userid']
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.statutory
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/report/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
            tblstatement.objects.all().delete()
            form = staterep(request.POST) # A form bound to the POST data
            if form.is_valid():

                grpname = form.cleaned_data['grpname']
                subgrname = form.cleaned_data['subgrname']
                caldate1 = form.cleaned_data['startdate']
                caldate11 = form.cleaned_data['enddate']
                caldate2 = caldate1.split('/')
                varstart = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                caldate22 = caldate11.split('/')
                varend = date(int(caldate22[2]),int(caldate22[0]),int(caldate22[1]))
                accno = ''
                #******************************************
                varryear = varstart.year
                varrmonth =  varstart.month
                varrday =  varstart.day
                varstartdate = str(varrday) + "-" + str(varrmonth) + "-" + str(varryear)
                varstartdate2 = date(varryear,varrmonth,varrday)
                #****************************************************
                varryear1 = varend.year
                varrmonth1 =  varend.month
                varrday1 =  varend.day
                varenddate = str(varrday1) + "-" + str(varrmonth1) + "-" + str(varryear1)
                opbal = 0
                #**********************************************

                grdis = 'ACCOUNT STATEMENT FROM - ' + varstartdate +" TO " + varenddate
                if varstart > varend :
                    varerr = "INVALID DATE RANGE"
                    return render_to_response('report/statement.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))

                varacc = tblaccount.objects.filter(groupname = grpname,subgroupname = subgrname).order_by('acccode')
                ld =[]
                dd ={}
                tblstatement.objects.all().delete()
                for na in varacc:
                    accno = na.acccode
                    getdata = tbltransaction.objects.filter(acccode = accno,transdate__range=(varstart,varend)).order_by('transdate','id')
                    bal = 0
                    dd ={}
                    getdetails =""
                    opbal = getopbal(accno,varstart,na.groupname)
                    bal = opbal
                    sublist = []
                    for jd in getdata:
                        groupname = jd.groupname
                        debit =jd.debit
                        credit = jd.credit
                        particulars = jd.particulars
                        refno =jd.refno
                        transdate = jd.transdate
                        accname =  jd.accname
                        acccode =  jd.acccode
                        transid = jd.transid

                        if groupname == "FIXED ASSETS" or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                            bal = bal + debit - credit
                        else:
                            bal = bal - debit + credit
                        disdebit = locale.format("%.2f",debit,grouping=True)
                        discredit = locale.format("%.2f",credit,grouping=True)
                        disbal = locale.format("%.2f",bal,grouping=True)
                        disop = locale.format("%.2f",opbal,grouping=True)
                        grdis = acccode + "-" + accname + ' FROM   ' + varstartdate +" TO " + varenddate + '    OPENING BALANCE  = ' + disop
                        #used = tblstatement(accname = accname,acccode = acccode,debit = debit,credit = credit,balance = bal,transdate = transdate,particulars = particulars,refno = refno,groupname = groupname,disdebit = disdebit,discredit = discredit,disbal = disbal,disgrp = grdis)
                        #used.save()
                        j = {'accname' : accname,'acccode' : acccode,'debit' : debit,'credit' : credit,'balance': bal,'transdate' : transdate,'particulars': particulars,'refno': refno,'groupname': groupname,'disdebit': disdebit,'discredit': discredit,'disbal': disbal,'disgrp': grdis,'transid':transid}
                        sublist.append(j)
                    dd ={'varco':na.acccode,'varna':na.accname,'vardat':na.lasttrandate,'opbal':opbal,'trans': sublist}
                    ld.append(dd)

                    #************************
                comp = tblcompanyinfo.objects.get(id = 1)
                if form.cleaned_data['excelfile']:
                    response = HttpResponse(mimetype="application/ms-excel")
                    response['Content-Disposition'] = 'attachment; filename=accstatementall.xls'
                    wb = xlwt.Workbook()
                    for jd in ld:
                        ws = wb.add_sheet(jd['varco'])
                        ws.write(0, 1, comp.name)
                        ws.write(1, 1, comp.address)
                        ws.write(2, 1, 'ACCOUNT STATEMENT')
                        ws.write(2, 2, varstart.strftime('%d-%m-%Y'))
                        ws.write(2, 3, varend.strftime('%d-%m-%Y'))
                        ws.write(3, 0,jd['varco'])
                        ws.write(3, 1, jd['varna'])
                        ws.write(3, 2,'LAST TRANS DATE %s' %(jd['vardat'].strftime('%d-%m-%Y')))
                        ws.write(3, 3, 'OPENING BALANCE %s' %jd['opbal'])
                        ws.write(4, 0,'Transdate')
                        ws.write(4, 1, 'Particulars')
                        ws.write(4, 2,'Ref. No')
                        ws.write(4, 3, 'Debit')
                        ws.write(4, 4, 'Credit')
                        ws.write(4, 5, 'Balance')
                        v = 5
                        for n in jd['trans']:
                            ws.write(v, 0, n['transdate'].strftime('%d-%m-%Y'))
                            ws.write(v, 1, n['particulars'])
                            ws.write(v, 2, n['refno'])
                            ws.write(v, 3, n['disdebit'])
                            ws.write(v, 4, n['discredit'])
                            ws.write(v, 5, n['disbal'])
                            v += 1
                    wb.save(response)
                    return response
                else:
                    return render_to_response('report/statement.htm',{'varuser':varuser,'varerr':varerr,'form':form,'ld':ld,'comp':comp,'varstart':varstart,'varend':varend},context_instance = RequestContext(request))

        else:
            form = staterep()
        return render_to_response('report/statement.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def valueadded(request):
     if  "userid" in request.session:

        #varuser = request.session['userid']
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.statutory
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/report/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          deldata = tblstatement.objects.all().delete()
          form = valueform(request.POST) # A form bound to the POST data
          if form.is_valid():
             caldate1 = form.cleaned_data['varyear']
             caldate2 = caldate1.split('/')
             varstart = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
             getmon = tblcalender.objects.all()
             varyear = varstart.year
             #print getmon
             stmon1 = ''
             endmon1 = ''
             for y in getmon:
               stmon1 = y.startmonth
               endmon1 = y.endtmonth
             stmon = stmon1.month
             endmon = endmon1.month

             rvaryear = int(varyear)
             if endmon == 12:
                 startyear = rvaryear
                 endyear = rvaryear
             else:
                 startyear = rvaryear - 1
                 endyear = rvaryear
             varsyear = date(startyear,stmon,1)
             dday = int(monthrange(endyear,endmon)[1])
             #if endmon in [1,3,5,7,8,10,12]:
              #   dday =  31
             #elif endmon in [4,6,9,11]:
              #   dday =  30
             #else:
              #   dday =  28
             vareyear = date(endyear,endmon,dday)
             delet = tblvalue.objects.all().delete()
           #*******************
             if tbltransaction.objects.filter(groupname ="INCOME",transdate__range = (varsyear,vareyear)).exclude(particulars = 'OPENING BALANCE',refno = '00000000').count() == 0:
                    tottran = 0
             else:
                   varrid1 = tbltransaction.objects.filter(groupname ="INCOME",transdate__range = (varsyear,vareyear)).exclude(particulars = 'OPENING BALANCE',refno = '00000000').aggregate(Sum('debit'),Sum('credit'))
                   debit = varrid1['debit__sum']
                   credit = varrid1['credit__sum']
                   tottran = credit - debit

             fbal = locale.format("%.2f",tottran,grouping=True)

             used = tblvalue(name = "Turnover",recamount = fbal,perc = "",disgrp = "EARNINGS",transdate = vareyear,disgrp1 = "" )
             used.save()
             #treating cost of sales
             if tbltransaction.objects.filter(groupname ="COST OF SALES",transdate__range = (varsyear,vareyear)).exclude(particulars = 'OPENING BALANCE',refno = '00000000').count() == 0:
                    tottranc = 0
             else:
                   varrid1 = tbltransaction.objects.filter(groupname ="COST OF SALES",transdate__range = (varsyear,vareyear)).exclude(particulars = 'OPENING BALANCE',refno = '00000000').aggregate(Sum('debit'),Sum('credit'))
                   debit = varrid1['debit__sum']
                   credit = varrid1['credit__sum']
                   tottranc = debit - credit
             #fbalc = locale.format("%.2f",tottranc,grouping=True)
             #treating other expenses

             if tbltransaction.objects.filter(groupname ="EXPENSES",transdate__range = (varsyear,vareyear)).exclude(subname = "TAX LIABILITIES").exclude(subname = "SALARIES AND WAGES").exclude(subname = "FINANCE EXPENSES").exclude(subname = "DEPRECIATION EXPENSES").exclude(particulars = 'OPENING BALANCE',refno = '00000000').count() == 0:
                    tottranco = 0
             else:
                   varrid11 = tbltransaction.objects.filter(groupname ="EXPENSES",transdate__range = (varsyear,vareyear)).exclude(subname = "TAX LIABILITIES").exclude(subname = "SALARIES AND WAGES").exclude(subname = "FINANCE EXPENSES").exclude(subname = "DEPRECIATION EXPENSES").exclude(particulars = 'OPENING BALANCE',refno = '00000000').aggregate(Sum('debit'),Sum('credit'))
                   debit = varrid11['debit__sum']
                   credit = varrid11['credit__sum']
                   tottranco = debit - credit
             tfbalco = tottranco + tottranc
             fbalco = locale.format("%.2f",tfbalco,grouping=True)
             used = tblvalue(name = "Bought in Materials and Services",recamount = fbalco,perc = "",disgrp = "EARNINGS",transdate = vareyear,disgrp1 = "" )
             used.save()
             #value added
             ttottran = tottran - tfbalco
             fbalcorr = locale.format("%.2f",ttottran,grouping=True)
             used = tblvalue(name = "Value Added",recamount = fbalcorr,perc = "100%",disgrp = "EARNINGS",transdate = vareyear,disgrp1 = "" )
             used.save()
             #treating other expenses
             if tbltransaction.objects.filter(groupname ="EXPENSES",subname = "SALARIES AND WAGES",transdate__range = (varsyear,vareyear)).exclude(particulars = 'OPENING BALANCE',refno = '00000000').count() == 0:
                    tottrancos = 0
             else:
                   varrid11 = tbltransaction.objects.filter(groupname ="EXPENSES",subname = "SALARIES AND WAGES",transdate__range = (varsyear,vareyear)).exclude(particulars = 'OPENING BALANCE',refno = '00000000').aggregate(Sum('debit'),Sum('credit'))
                   debit = varrid11['debit__sum']
                   credit = varrid11['credit__sum']
                   tottrancos = debit - credit
             #GETTING PERCENTAGE
             if ttottran == 0:
                 perc1 = 0
             else:
                 perc1 = (tottrancos/ ttottran) * 100
             perc1d = locale.format("%.0f",perc1,grouping=True) + "%"
             fbalcos = locale.format("%.2f",tottrancos,grouping=True)
             used = tblvalue(name = "Salaries and Benefit",recamount = fbalcos,perc = perc1d,disgrp = "DISTRIBUTION",transdate = vareyear,disgrp1 = "Employees" )
             used.save()
             #treating other expenses
             if tbltransaction.objects.filter(groupname ="EXPENSES",subname = "FINANCE EXPENSES",transdate__range = (varsyear,vareyear)).exclude(particulars = 'OPENING BALANCE',refno = '00000000').count() == 0:
                    tottrancosf = 0
             else:
                   varrid11 = tbltransaction.objects.filter(groupname ="EXPENSES",subname = "FINANCE EXPENSES",transdate__range = (varsyear,vareyear)).exclude(particulars = 'OPENING BALANCE',refno = '00000000').aggregate(Sum('debit'),Sum('credit'))
                   debit = varrid11['debit__sum']
                   credit = varrid11['credit__sum']
                   tottrancosf = debit - credit
             #GETTING PERCENTAGE
             if ttottran == 0:
                 perc11 = 0
             else:
                 perc11 = (tottrancosf/ ttottran) * 100
             perc11d = locale.format("%.0f",perc11,grouping=True) + "%"
             fbalcosf = locale.format("%.2f",tottrancosf,grouping=True)
             used = tblvalue(name = "Interest/Dividend",recamount = fbalcosf,perc = perc11d,disgrp = "DISTRIBUTION",transdate = vareyear,disgrp1 = "Provider of funds" )
             used.save()
             #treating other taxation
             if tbltransaction.objects.filter(groupname ="EXPENSES",subname = "TAX LIABILITIES",transdate__range = (varsyear,vareyear)).exclude(particulars = 'OPENING BALANCE',refno = '00000000').count() == 0:
                    tottrancosft = 0
             else:
                   varrid11 = tbltransaction.objects.filter(groupname ="EXPENSES",subname = "TAX LIABILITIES",transdate__range = (varsyear,vareyear)).exclude(particulars = 'OPENING BALANCE',refno = '00000000').aggregate(Sum('debit'),Sum('credit'))
                   debit = varrid11['debit__sum']
                   credit = varrid11['credit__sum']
                   tottrancosft = debit - credit
             #GETTING PERCENTAGE
             if ttottran == 0:
                 perc11 = 0
             else:
                perc11 = (tottrancosft/ ttottran) * 100
             perc11d = locale.format("%.0f",perc11,grouping=True) + "%"
             fbalcosft = locale.format("%.2f",tottrancosft,grouping=True)
             used = tblvalue(name = "Taxation",recamount = fbalcosft,perc = perc11d,disgrp = "DISTRIBUTION",transdate = vareyear,disgrp1 = "Government" )
             used.save()
             #treating other Depreciation
             if tbltransaction.objects.filter(groupname ="EXPENSES",subname = "DEPRECIATION EXPENSES",transdate__range = (varsyear,vareyear)).exclude(particulars = 'OPENING BALANCE',refno = '00000000').count() == 0:
                    tottrancosftd = 0
             else:
                   varrid11 = tbltransaction.objects.filter(groupname ="EXPENSES",subname = "DEPRECIATION EXPENSES",transdate__range = (varsyear,vareyear)).exclude(particulars = 'OPENING BALANCE',refno = '00000000').aggregate(Sum('debit'),Sum('credit'))
                   debit = varrid11['debit__sum']
                   credit = varrid11['credit__sum']
                   tottrancosftd = debit - credit
             #GETTING PERCENTAGE
             if ttottran == 0:
                 perc11 = 0
             else:
                 perc11 = (tottrancosftd/ ttottran) * 100
             perc11d = locale.format("%.0f",perc11,grouping=True) + "%"
             fbalcosftd = locale.format("%.2f",tottrancosftd,grouping=True)
             used = tblvalue(name = "Depreciation",recamount = fbalcosftd,perc = perc11d,disgrp = "DISTRIBUTION",transdate = vareyear,disgrp1 = "The Future" )
             used.save()
             #retained profit/loss
             k = tottrancosftd +  tottrancosft + tottrancosf + tottrancos
             kk = ttottran - k
             if ttottran == 0:
                 perc11 = 0
             else:
                 perc11 = (kk/ ttottran) * 100
             perc11d = locale.format("%.0f",perc11,grouping=True)+ "%"
             kkk = locale.format("%.2f",kk,grouping=True)
             used = tblvalue(name = "Retured Profit/Loss for the year",recamount = kkk,perc = perc11d,disgrp = "DISTRIBUTION",transdate = vareyear,disgrp1 = "" )
             used.save()
             #getting the total
             used = tblvalue(name = "",recamount = fbalcorr,perc = "100%",disgrp = "DISTRIBUTION",transdate = vareyear,disgrp1 = "" )
             used.save()
             ll =[]
             getdetails = tblvalue.objects.filter(disgrp ='EARNINGS').order_by('id')
             dea = {'name':'EARNINGS','endyear':vareyear,'data':getdetails}
             ll.append(dea)
             getdetails2 = tblvalue.objects.filter(disgrp ='DISTRIBUTION').order_by('id')
             dea2 = {'name':'DISTRIBUTION','endyear':vareyear,'data':getdetails2}
             ll.append(dea2)
             v = 0
             comp = tblcompanyinfo.objects.get(id = 1)
             if form.cleaned_data['excelfile']:
                 response = HttpResponse(mimetype="application/ms-excel")
                 response['Content-Disposition'] = 'attachment; filename=valueadded.xls'
                 wb = xlwt.Workbook()
                 ws = wb.add_sheet('valueadded')
                 ws.write(0, 1, comp.name)
                 ws.write(1, 1, comp.address)
                 ws.write(2, 1, 'VALUE ADDED STATEMENT FOR THE YEAR ENDED %s'% vareyear.strftime('%b,%Y') )
                 k4 = 3
                 v = 4
                 for jd in ll:
                     ws.write(k4, 1, jd['name'])
                     for n in jd['data']:
                         ws.write(v, 2, n.name)
                         ws.write(v, 3, n.recamount)
                         ws.write(v, 4, n.perc)
                         v += 1
                     k4 = v + 1
                     v = k4 + 1
                 wb.save(response)
                 return response
             else:
                 return render_to_response('report/valueadded.htm',{'varuser':varuser,'varerr':varerr,'form':form,'ll':ll,'comp':comp,'endyear':vareyear},context_instance = RequestContext(request))
            # if tblvalue.objects.all().count() == 0:
             #   varerr =""
              #  return render_to_response('report/notfound.htm',{'varuser':varuser,'varerr':varerr})
             #resp = HttpResponse(mimetype='application/pdf')
             #getdetails = tblvalue.objects.all().order_by('id')
             #report = valueaddedreport(queryset=getdetails)
             #report.generate_by(PDFGenerator, filename=resp)
             #return resp
        else:#not
            form = valueform()
        return render_to_response('report/valueadded.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')

def statementreprepall(request):
    if  "userid" in request.session:
        #varuser = request.session['userid']
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.statutory
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/report/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
            deldata = tblstatement.objects.all().delete()
            form = staterepall(request.POST) # A form bound to the POST data
            if form.is_valid():
                #varstart = form.cleaned_data['enddate']
                #accno = form.cleaned_data['accno']
                acccode = form.cleaned_data['acccode']
                caldate1 = form.cleaned_data['startdate']
                caldate11 = form.cleaned_data['enddate']
                caldate2 = caldate1.split('/')
                varstart = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                caldate22 = caldate11.split('/')
                varend = date(int(caldate22[2]),int(caldate22[0]),int(caldate22[1]))
                opbal = 0
                #**********************************************
                if varstart > varend :
                    varerr = "INVALID DATE RANGE"
                    return render_to_response('report/statementall.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
                if acccode == "":
                    varacc = tblaccount.objects.all().exclude(groupname = "CURRENT ASSETS",subgroupname ="STOCKS").exclude(groupname = "CAPITAL AND RESERVES",subgroupname ="SHAREHOLDERS FUND",accname = "CURRENT-YEAR-P/L").exclude(groupname = "CURRENT LIABILITIES",subgroupname = "PAYABLES",accname = "TRADE-CREDITORS").exclude(groupname = "CURRENT ASSETS",subgroupname = "MINI-STORE",accname = "MINI-STORE-BALANCE").exclude(groupname = "CURRENT ASSETS",subgroupname = "WORK-IN-PROGRESS",accname = "WORK-IN-PROGRESS-BALANCE").exclude(groupname = "CURRENT ASSETS",subgroupname = "STAFF-DEBTORS",accname = "STAFF-DEBTORS").exclude(groupname = "CURRENT ASSETS",subgroupname = "RECEIVABLES",accname = "TRADE-DEBTORS").order_by('acccode')

                else:
                    varacc = tblaccount.objects.filter(acccode = acccode)
                ld =[]
                dd ={}
                tblstatement.objects.all().delete()
                for na in varacc:
                    accno = na.acccode
                    getdata = tbltransaction.objects.filter(acccode = accno,transdate__range=(varstart,varend)).order_by('transdate','id')
                    bal = 0
                    dd ={}
                    getdetails =""
                    opbal = getopbal(accno,varstart,na.groupname)
                    bal = opbal
                    sublist = []
                    for jd in getdata:
                        groupname = jd.groupname
                        debit =jd.debit
                        credit = jd.credit
                        particulars = jd.particulars
                        refno =jd.refno
                        transdate = jd.transdate
                        accname =  jd.accname
                        acccode =  jd.acccode
                        transid = jd.transid
                        if groupname == "FIXED ASSETS" or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                           bal = bal + debit - credit
                        else:
                           bal = bal - debit + credit
                        disdebit = locale.format("%.2f",debit,grouping=True)
                        discredit = locale.format("%.2f",credit,grouping=True)
                        disbal = locale.format("%.2f",bal,grouping=True)
                        #opbal = getopbal(acccode,varstart,groupname)
                        disop = locale.format("%.2f",opbal,grouping=True)
                        grdis = acccode + "-" + accname + ' FROM   ' + varstart.strftime("%d-%m-%Y") +" TO " + varend.strftime("%d-%m-%Y") + '    OPENING BALANCE  = ' + disop
                        #used = tblstatement(accname = accname,acccode = acccode,debit = debit,credit = credit,balance = bal,transdate = transdate,particulars = particulars,refno = refno,groupname = groupname,disdebit = disdebit,discredit = discredit,disbal = disbal,disgrp = grdis)
                        #used.save()
                        j = {'accname' : accname,'acccode' : acccode,'debit' : debit,'credit' : credit,'balance': bal,'transdate' : transdate,'particulars': particulars,'refno': refno,'groupname': groupname,'disdebit': disdebit,'discredit': discredit,'disbal': disbal,'disgrp': grdis,'transid':transid}
                        sublist.append(j)
                    dd ={'varco':na.acccode,'varna':na.accname,'vardat':na.lasttrandate,'opbal':opbal,'trans':sublist,'varname':na.accname}
                    ld.append(dd)

                    #************************
                comp = tblcompanyinfo.objects.get(id = 1)
                if form.cleaned_data['excelfile']:
                    response = HttpResponse(mimetype="application/ms-excel")
                    response['Content-Disposition'] = 'attachment; filename=accstatementall.xls'
                    wb = xlwt.Workbook()
                    for jd in ld:
                        ws = wb.add_sheet(str(jd['varco']).replace(' ','-')[:30])
                        ws.write(0, 1, comp.name)
                        ws.write(1, 1, comp.address)
                        ws.write(2, 1, 'ACCOUNT STATEMENT')
                        ws.write(2, 2, varstart.strftime('%d-%m-%Y'))
                        ws.write(2, 3, varend.strftime('%d-%m-%Y'))
                        ws.write(3, 0,jd['varco'])
                        ws.write(3, 1, jd['varna'])
                        ws.write(3, 2,'LAST TRANS DATE %s' %(jd['vardat'].strftime('%d-%m-%Y')))
                        ws.write(3, 3, 'OPENING BALANCE %s' %jd['opbal'])
                        ws.write(4, 0,'Transdate')
                        ws.write(4, 1, 'Particulars')
                        ws.write(4, 2,'Ref. No')
                        ws.write(4, 3, 'Debit')
                        ws.write(4, 4, 'Credit')
                        ws.write(4, 5, 'Balance')
                        v = 5
                        for n in jd['trans']:
                            ws.write(v, 0, n['transdate'].strftime('%d-%m-%Y'))
                            ws.write(v, 1, n['particulars'])
                            ws.write(v, 2, n['refno'])
                            ws.write(v, 3, n['disdebit'])
                            ws.write(v, 4, n['discredit'])
                            ws.write(v, 5, n['disbal'])
                            v += 1
                    wb.save(response)
                    return response
                else:
                    return render_to_response('report/statementall.htm',{'varuser':varuser,'varerr':varerr,'form':form,'ld':ld,'comp':comp,'varstart':varstart,'varend':varend},context_instance = RequestContext(request))

        else:
            form = staterepall()
        return render_to_response('report/statementall.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
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
def autocompletebankallreport(request):
    term = request.GET.get('term')
    gset = tblaccount.objects.filter(accname__contains = term).exclude(groupname = "CURRENT ASSETS",subgroupname ="STOCKS").exclude(groupname = "CAPITAL AND RESERVES",subgroupname ="SHAREHOLDERS FUND",accname = "CURRENT-YEAR-P/L").exclude(groupname = "CURRENT LIABILITIES",subgroupname = "PAYABLES",accname = "TRADE-CREDITORS").exclude(groupname = "CURRENT ASSETS",subgroupname = "MINI-STORE",accname = "MINI-STORE-BALANCE").exclude(groupname = "CURRENT ASSETS",subgroupname = "WORK-IN-PROGRESS",accname = "WORK-IN-PROGRESS-BALANCE").exclude(groupname = "CURRENT ASSETS",subgroupname = "STAFF-DEBTORS",accname = "STAFF-DEBTORS").exclude(groupname = "CURRENT ASSETS",subgroupname = "RECEIVABLES",accname = "TRADE-DEBTORS").order_by('acccode')[:10]
    suggestions = []
    for i in gset:
        k = i.accbal
        disamt = locale.format("%.2f",k,grouping=True)
        suggestions.append({'label': '%s %s' % (i.accname,i.acccode), 'acccode': i.acccode,'accname': i.accname,'accbal':disamt})
    return suggestions

def getministatement(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode1 = post['userid']
                acccode,vdate = acccode1.split(':')
                #print 'acc no and date :',acccode,vdate
                getdate = tblcalender.objects.all()
                opbal = 0
                caldate22 = vdate.split('/')
                varend = date(int(caldate22[2]),int(caldate22[0]),int(caldate22[1]))
                vartyear = varend.year
                varyear = varend.year
                #**********************************************
                stmon1 = datetime.date.today()
                for g in getdate:
                    stmon1 = g.startmonth
                    endmon1 = g.endtmonth
                stmon = stmon1.month
                endmon = varend.month
                cday = stmon1.day # calendar start day
                rvaryear = int(varyear)
                if int(stmon) > int(endmon):
                   startyear = rvaryear - 1
                   endyear = rvaryear
                else:
                   startyear = rvaryear
                   endyear = rvaryear
                varstart = date(startyear,stmon,1)
                km = tblaccount.objects.get(id = acccode)
                varacc = tblaccount.objects.filter(id = acccode)
                ld =[]  #empty list
                dd ={}   #empty dict
                tblstatement.objects.all().delete()
                for na in varacc:
                    accno = na.acccode
                    getdata = tbltransaction.objects.filter(acccode = accno,transdate__range=(varstart,varend)).order_by('transdate','id')
                    opbal = getopbal(accno,varstart,na.groupname)
                    bal = opbal
                    sublist = []
                    for jd in getdata:
                        groupname = jd.groupname
                        debit =jd.debit
                        credit = jd.credit
                        particulars = jd.particulars
                        refno =jd.refno
                        transdate = jd.transdate
                        accname =  jd.accname
                        acccode =  jd.acccode
                        transid = jd.transid
                        if groupname == "FIXED ASSETS" or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                            bal = bal + debit - credit
                        else:
                            bal = bal - debit + credit
                        disdebit = locale.format("%.2f",debit,grouping=True)
                        discredit = locale.format("%.2f",credit,grouping=True)
                        disbal = locale.format("%.2f",bal,grouping=True)
                        #opbal = 0
                        disop = locale.format("%.2f",opbal,grouping=True)
                        #grdis = acccode + "-" + accname + ' FROM   ' + str(stdate) +" TO " + str(endate) + '    OPENING BALANCE  = ' + disop
                        #used = tblstatement(accname = accname,acccode = acccode,debit = debit,credit = credit,balance = bal,transdate = transdate,particulars = particulars,refno = refno,groupname = groupname,disdebit = disdebit,discredit = discredit,disbal = disbal,disgrp = grdis)
                        #used.save()
                        j = {'accname' : accname,'acccode' : acccode,'debit' : debit,'credit' : credit,'balance': bal,'transdate' : transdate,'particulars': particulars,'refno': refno,'groupname': groupname,'disdebit': disdebit,'discredit': discredit,'disbal': disbal,'transid':transid}
                        sublist.append(j)
                    dd ={'varco':na.acccode,'varna':na.accname,'vardat':na.lasttrandate,'opbal':opbal,'trans':sublist}
                    ld.append(dd)

                    #************************
                comp = tblcompanyinfo.objects.get(id = 1)
                return render_to_response('report/ministatement.htm',{'varuser':varuser,'varerr':varerr,'ld':ld,'comp':comp,'varstart':varstart,'varend':varend},context_instance = RequestContext(request))
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getministatementpayable(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode1 = post['userid']
                acccode,vdate = acccode1.split(':')
                #print 'acc no and date :',acccode,vdate
                opbal = 0
                caldate22 = vdate.split('/')
                varend = date(int(caldate22[2]),int(caldate22[0]),int(caldate22[1]))
                vartyear = varend.year
                varyear = varend.year
                stmon1 = datetime.date.today()
                getdate = tblcalender.objects.all()
                for g in getdate:
                    stmon1 = g.startmonth
                    endmon1 = g.endtmonth
                opbal = 0
                stmon = stmon1.month
                endmon = varend.month
                cday = stmon1.day # calendar start day
                rvaryear = int(varyear)
                if int(stmon) > int(endmon):
                    startyear = rvaryear - 1
                    endyear = rvaryear
                else:
                    startyear = rvaryear
                    endyear = rvaryear
                varstart = date(startyear,stmon,1)
                #**********************************************
                km = payables.objects.get(id = acccode)
                varacc = tblaccount.objects.filter(acccode = km.acccode)
                ld =[]
                dd ={}
                tblstatement.objects.all().delete()
                for na in varacc:
                    accno = na.acccode
                    getdata = tbltransaction.objects.filter(acccode = accno,transdate__range=(varstart,varend)).order_by('transdate','id')
                    opbal = getopbal(accno,varstart,na.groupname)
                    bal = opbal
                    dd ={}
                    getdetails =""
                    sublist = []
                    for jd in getdata:
                        groupname = jd.groupname
                        debit =jd.debit
                        credit = jd.credit
                        particulars = jd.particulars
                        refno =jd.refno
                        transdate = jd.transdate
                        accname =  jd.accname
                        acccode =  jd.acccode
                        if groupname == "FIXED ASSETS" or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                            bal = bal + debit - credit
                        else:
                            bal = bal - debit + credit
                        disdebit = locale.format("%.2f",debit,grouping=True)
                        discredit = locale.format("%.2f",credit,grouping=True)
                        disbal = locale.format("%.2f",bal,grouping=True)
                        opbal = 0
                        disop = locale.format("%.2f",opbal,grouping=True)
                        #grdis = acccode + "-" + accname + ' FROM   ' + str(stdate) +" TO " + str(endate) + '    OPENING BALANCE  = ' + disop
                        #used = tblstatement(accname = accname,acccode = acccode,debit = debit,credit = credit,balance = bal,transdate = transdate,particulars = particulars,refno = refno,groupname = groupname,disdebit = disdebit,discredit = discredit,disbal = disbal,disgrp = grdis)
                        #used.save()
                        j = {'accname' : accname,'acccode' : acccode,'debit' : debit,'credit' : credit,'balance': bal,'transdate' : transdate,'particulars': particulars,'refno': refno,'groupname': groupname,'disdebit': disdebit,'discredit': discredit,'disbal': disbal}
                        sublist.append(j)
                    dd ={'varco':na.acccode,'varna':na.accname,'vardat':na.lasttrandate,'opbal':opbal,'trans':sublist}
                    ld.append(dd)

                    #************************
                comp = tblcompanyinfo.objects.get(id = 1)
                return render_to_response('report/ministatement.htm',{'varuser':varuser,'varerr':varerr,'ld':ld,'comp':comp,'varstart':varstart,'varend':varend},context_instance = RequestContext(request))
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')



def getsubaccountaccreport(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                state = acccode
                kk = []
                sdic = {}
                data = tblsubgroup.objects.filter(groupname = state).order_by('subgroupcode')
                for p in data:
                    kk.append(p.subgroupname)
                return HttpResponse(json.dumps(kk), mimetype='application/json')
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')
