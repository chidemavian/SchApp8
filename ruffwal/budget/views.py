# Create your views here.
from django.template import loader, Context,RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import  HttpResponseRedirect
from myproject.ruffwal.rwreport.opbal import *
from myproject.ruffwal.rwadmin.models import *
from django.db.models import Max,Sum
from myproject.ruffwal.rwreport.form import *
from myproject.ruffwal.budget.models import *
from myproject.ruffwal.budget.forms import *
from myproject.ruffwal.posting.models import *
from myproject.ruffwal.rwreport.capy import monthrange
from django.core.serializers.json import simplejson as json
import random
import locale
locale.setlocale(locale.LC_ALL,'')
import xlwt
import datetime
from datetime import date,time,timedelta
# Wrapper to make a view handle both normal and api request
def json_view(func):
    def wrap(req, *args, **kwargs):
        resp = func(req, *args, **kwargs)
        if isinstance(resp, HttpResponse):
            return resp
        return HttpResponse(json.dumps(resp), mimetype="application/json")
    return wrap

@json_view
def budgetcomplete(request):
    term = request.GET.get('term')
    gset = tblaccount.objects.filter(accname__contains = term.upper()).exclude(groupcode = "10000").exclude(groupcode = "20000").exclude(groupcode = "30000").exclude(groupcode = "40000").exclude(groupcode = "50000").exclude(groupcode = "60000").order_by('acccode')[:10]
    suggestions = []
    for i in gset:
        suggestions.append({'label': '%s %s' % (i.accname,i.acccode), 'acccode': i.acccode,'accname': i.accname,'acctype':i.groupname})
    return suggestions


@json_view
def budgetcompletemonth(request):
    getdate = tblcalender.objects.all()
    varstart = ''
    varend = ''
    for g in getdate:
        varstart = g.startmonth
        varend = g.endtmonth
    term = request.GET.get('term')
    gset = tblaccount.objects.filter(accname__contains = term.upper()).exclude(groupcode = "10000").exclude(groupcode = "20000").exclude(groupcode = "30000").exclude(groupcode = "40000").exclude(groupcode = "50000").exclude(groupcode = "60000").order_by('acccode')[:10]
    suggestions = []
    for i in gset:
        accno = i.acccode
        acc = tblaccount.objects.get(acccode = accno)
        if tblbudgetmonthly.objects.filter(acccode = acc,startmonth =  varstart,endmonth = varend):
           gacc =  tblbudgetmonthly.objects.get(acccode = acc,startmonth =  varstart,endmonth = varend)
           first = gacc.first
           second = gacc.second
           third = gacc.third
           four = gacc.four
           five = gacc.five
           six = gacc.six
           seven = gacc.seven
           eight = gacc.eight
           nine = gacc.nine
           ten = gacc.ten
           eleven = gacc.eleven
           twelve = gacc.twelve
        else:
            first = 0
            second = 0
            third = 0
            four = 0
            five = 0
            six = 0
            seven = 0
            eight = 0
            nine = 0
            ten = 0
            eleven = 0
            twelve = 0
        suggestions.append({'label': '%s %s' % (i.accname,i.acccode), 'acccode': i.acccode,'accname': i.accname,'acctype':i.groupname,'first':str(first),'second':str(second),'third':str(third),'four':str(four),'five':str(five),'six':str(six),'seven':str(seven),'eight':str(eight),'nine':str(nine),'ten':str(ten),'eleven':str(eleven),'twelve':str(twelve)})
    return suggestions

def unauto(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        return render_to_response('budget/unautorise.htm',{'varuser':varuser,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')


def enterbudget(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if int(uenter) == 0 :
            return HttpResponseRedirect('/welcome/')
        varerr =""
        vardate = date.today()
        vardate1 = vardate.strftime('%B %d,%Y')
        return render_to_response('budget/enter.htm',{'varuser':varuser,'varerr':varerr,'vardate1':vardate1})
    else:
        return HttpResponseRedirect('/login/')

def createbudget(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/budget/access-denied/')
        varerr =""
        details = ''
        getdate = tblcalender.objects.all()
        varstart = ''
        varend = ''
        for g in getdate:
            varstart = g.startmonth
            varend = g.endtmonth
        if request.method == 'POST':
            form = budgetform(request.POST) # A form bound to the POST data
            if form.is_valid():
                accname = form.cleaned_data['accname']
                acccode = form.cleaned_data['acccode']
                acctype = form.cleaned_data['acctype']
                amount = form.cleaned_data['amount']
                getacc = tblaccount.objects.get(acccode = acccode)
                if tblbudget.objects.filter(acccode = getacc,startmonth =  varstart,endmonth = varend):
                    varerr = 'Budget In Existence For The Year'
                    details = tblbudget.objects.filter(startmonth =  varstart,endmonth = varend)
                    return render_to_response('budget/budget.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':details},context_instance = RequestContext(request))
                uid = ''
                for m in range(10):
                    k = random.randint(1,199)
                    uid += str(k)
                uid +=acccode
                used = tblbudget(acccode = getacc,startmonth = varstart,endmonth = varend,userid = varuser,amount = str(amount),refcode = uid)
                used.save()
                return HttpResponseRedirect('/SchApp/account/budget/createbudget/')
            else:
                varerr ="All Fields Are Required"
                details = tblbudget.objects.filter(startmonth =  varstart,endmonth = varend)
                return render_to_response('budget/budget.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':details},context_instance = RequestContext(request))
        else:
            form = budgetform()
            if tblcalender.objects.all().count() == 0:
                varerr = "Contact Administrator to set up calendar year"
                return render_to_response('budget/budget.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
            details = tblbudget.objects.filter(startmonth =  varstart,endmonth = varend)
        return render_to_response('budget/budget.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':details},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def editbudget(request,invid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/budget/access-denied/')
        varerr =""
        if request.method == 'POST':
            getdetails = ""
            accname = request.POST['acccode'] # the amount
            acccode = request.POST['accname'] # the amount
            amount = request.POST['amount'] #the
            if acccode == '' :
                varerr ="Invalid Account"
                getdetails = tblbudget.objects.get(refcode = invid)
                return render_to_response('budget/editbudget.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            try:
               k = float(amount)
            except:
                 varerr = "INVALID AMOUNT"
                 getdetails = tblbudget.objects.get(refcode = invid)
                 return render_to_response('budget/editbudget.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            seldata = tblbudget.objects.get(refcode = invid)
            seldata.amount =str(k)
            seldata.save()
            return HttpResponseRedirect('/SchApp/account/budget/createbudget/')
        else:
             getdetails = tblbudget.objects.get(refcode = invid)
             return render_to_response('budget/editbudget.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')

def printbudget(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/budget/access-denied/')
        varerr =""
        details = ''
        if request.method == 'POST':
            form = reportform(request.POST) # A form bound to the POST data
            if form.is_valid():
                caldate1 = form.cleaned_data['varyear']
                caldate2 = caldate1.split('/')
                varstart = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                getmon = tblcalender.objects.all()
                varyear = varstart.year
                stmon1 =''
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
                vareyear = date(endyear,endmon,dday)
                details = tblbudget.objects.filter(startmonth =  varsyear,endmonth = vareyear)
                comp = tblcompanyinfo.objects.get(id = 1)
                if form.cleaned_data['excelfile']:
                    response = HttpResponse(mimetype="application/ms-excel")
                    response['Content-Disposition'] = 'attachment; filename=budgetreport.xls'
                    wb = xlwt.Workbook()
                    ws = wb.add_sheet('budget')
                    ws.write(0, 1, comp.name)
                    ws.write(1, 1, comp.address)
                    ws.write(2, 1, 'BUDGET REPORT FOR YEAR %s'% vareyear.year )
                    ws.write(3, 0, 'S/N')
                    ws.write(3, 1, 'Account Name')
                    ws.write(3, 2, 'Account Code')
                    ws.write(3, 3, 'Account Type')
                    ws.write(3, 4, 'Budget Value')
                    v = 4
                    for p,n in enumerate(details):
                        ws.write(v, 0, p+1)
                        ws.write(v, 1, n.acccode.acccode)
                        ws.write(v, 2, n.acccode.accname)
                        ws.write(v, 3, n.acccode.groupname)
                        ws.write(v, 4, locale.format("%.2f",n.amount,grouping=True))
                        v += 1
                    wb.save(response)
                    return response
                else:
                    return render_to_response('budget/printbudget.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':details,'comp':comp,'headings':'BUDGET REPORT FOR YEAR %s'% vareyear.year},context_instance = RequestContext(request))
        else:
            form = reportform()
        return render_to_response('budget/printbudget.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':details},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


def budgetvariance(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/budget/access-denied/')
        varerr =""
        details = ''
        if request.method == 'POST':
            form = dateform(request.POST) # A form bound to the POST data
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
                    return render_to_response('budget/budgetvariance.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
                #********************************************************
                if tblcalender.objects.all().count() == 0:
                    varerr = "NO START DATE"
                    #varerr = "INVALID DATE RANGE"
                    return render_to_response('budget/budgetvariance.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
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
                    return render_to_response('budget/budgetvariance.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
                    # formulating the calendar year
                castartdate = date(varstart.year,stmon,cday)
                caenddate = date(varend.year,cmon,ceday)
                ggdate = caenddate - castartdate
                difference_in_years = (ggdate.days + ggdate.seconds/86400.0)/365.2425
                #print 'the year difference :',difference_in_years
                if difference_in_years > 1:
                    varerr = "INVALID DATE RANGE"
                    return render_to_response('budget/budgetvariance.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
                #******************************************************
                if varstart > varend :
                    varerr = "INVALID DATE RANGE"
                    return render_to_response('budget/budgetvariance.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
                if tblaccount.objects.all().count() == 0:
                   varerr="NO ACCOUNT FOR TRIAL BALANCE"
                   return render_to_response('budget/budgetvariance.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
                getmon = tblcalender.objects.all()
                varyear = varend.year
                stmon1 =''
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
                vareyear = date(endyear,endmon,dday)

                #************************************treating INCOME
                getinc = tblaccount.objects.filter(groupname = 'INCOME',recreport = 'YES').order_by('acccode')
                sublist = []
                totin = 0
                for j in getinc:
                    getacc = tblaccount.objects.get(acccode = j.acccode)
                    if tblbudget.objects.filter(acccode = getacc,startmonth =  varsyear,endmonth = vareyear):
                        budget = tblbudget.objects.get(acccode = getacc,startmonth =  varsyear,endmonth = vareyear)
                    else:
                        budget = 0
                    #********************************************getting actual
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
                    totin += opbal
                    h = locale.format("%.2f",opbal,grouping=True)
                    if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS" or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                        j = {'accname':accname,'acccode':acccode,'actual':h}
                    else:
                        j = {'accname':accname,'acccode':acccode,'actual':h}
                    sublist.append(j)
                #******************************************************
                details = tblbudget.objects.filter(startmonth =  varsyear,endmonth = vareyear)
                comp = tblcompanyinfo.objects.get(id = 1)
                if form.cleaned_data['excelfile']:
                    response = HttpResponse(mimetype="application/ms-excel")
                    response['Content-Disposition'] = 'attachment; filename=budgetreport.xls'
                    wb = xlwt.Workbook()
                    ws = wb.add_sheet('budget')
                    ws.write(0, 1, comp.name)
                    ws.write(1, 1, comp.address)
                    ws.write(2, 1, 'BUDGET REPORT FOR YEAR %s'% vareyear.year )
                    ws.write(3, 0, 'S/N')
                    ws.write(3, 1, 'Account Name')
                    ws.write(3, 2, 'Account Code')
                    ws.write(3, 3, 'Account Type')
                    ws.write(3, 4, 'Budget Value')
                    v = 4
                    for p,n in enumerate(details):
                        ws.write(v, 0, p+1)
                        ws.write(v, 1, n.acccode.acccode)
                        ws.write(v, 2, n.acccode.accname)
                        ws.write(v, 3, n.acctype)
                        ws.write(v, 4, locale.format("%.2f",n.amount,grouping=True))
                        v += 1
                    wb.save(response)
                    return response
                else:
                    return render_to_response('budget/budgetvariance.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':details,'comp':comp,'headings':'BUDGET REPORT FOR YEAR %s'% vareyear.year},context_instance = RequestContext(request))
        else:
            form = dateform()
        return render_to_response('budget/budgetvariance.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':details},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


def createbudgetmonth(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/budget/access-denied/')
        varerr =""
        getdate = tblcalender.objects.all()
        varstart = ''
        varend = ''
        for g in getdate:
            varstart = g.startmonth
            varend = g.endtmonth
        details = tblbudgetmonthly.objects.filter(startmonth =  varstart,endmonth = varend)
        ll = []
        for k in details:
            tamt = float(k.first) + float(k.second) + float(k.third) + float(k.four) + float(k.five) + float(k.six) +float(k.seven) +float(k.eight) + float(k.nine) + float(k.ten) + float(k.eleven) + float(k.twelve)
            l = {'acccode':k.acccode.acccode,'accname':k.acccode.accname,'groupname':k.acccode.groupname,'first':locale.format("%.2f",float(k.first),grouping=True),'second':locale.format("%.2f",float(k.second),grouping=True),'third':locale.format("%.2f",float(k.third),grouping=True),'four':locale.format("%.2f",float(k.four),grouping=True),'five':locale.format("%.2f",float(k.five),grouping=True),'six':locale.format("%.2f",float(k.six),grouping=True),'seven':locale.format("%.2f",float(k.seven),grouping=True),'eight':locale.format("%.2f",float(k.eight),grouping=True),'nine':locale.format("%.2f",float(k.nine),grouping=True),'ten':locale.format("%.2f",float(k.ten),grouping=True),'eleven':locale.format("%.2f",float(k.eleven),grouping=True),'twelve':locale.format("%.2f",float(k.twelve),grouping=True),'total':locale.format("%.2f",tamt,grouping=True)}
            ll.append(l)
        if request.method == 'POST':
            form = budgetformmonth(request.POST) # A form bound to the POST data
            if form.is_valid():
                accname = form.cleaned_data['accname']
                acccode = form.cleaned_data['acccode']
                acctype = form.cleaned_data['acctype']
                getacc = tblaccount.objects.get(acccode = acccode)
                if tblbudgetmonthly.objects.filter(acccode = getacc,startmonth =  varstart,endmonth = varend):
                    tblbudgetmonthly.objects.filter(acccode = getacc,startmonth =  varstart,endmonth = varend).update(first = str(float(form.cleaned_data['first'])),second = str(float(form.cleaned_data['second'])),third = str(float(form.cleaned_data['third'])),four = str(float(form.cleaned_data['four'])),five = str(float(form.cleaned_data['five'])),six = str(float(form.cleaned_data['six'])),seven = str(float(form.cleaned_data['seven'])),eight = str(float(form.cleaned_data['eight'])),nine = str(float(form.cleaned_data['nine'])),ten = str(float(form.cleaned_data['ten'])),eleven = str(float(form.cleaned_data['eleven'])),twelve = str(float(form.cleaned_data['twelve'])))
                    return HttpResponseRedirect('/SchApp/account/budget/create_budget_month/')
                    #varerr = 'Budget In Existence For The Year'
                    #details = tblbudgetmonthly.objects.filter(startmonth =  varstart,endmonth = varend)
                    #return render_to_response('budget/budgetmonth.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':details},context_instance = RequestContext(request))
                uid = ''
                for m in range(10):
                    k = random.randint(1,199)
                    uid += str(k)
                uid +=acccode
                used = tblbudgetmonthly(acccode = getacc,startmonth = varstart,endmonth = varend,userid = varuser,first = str(float(form.cleaned_data['first'])),refcode = uid,second = str(float(form.cleaned_data['second'])),third = str(float(form.cleaned_data['third'])),four = str(float(form.cleaned_data['four'])),five = str(float(form.cleaned_data['five'])),six = str(float(form.cleaned_data['six'])),seven = str(float(form.cleaned_data['seven'])),eight = str(float(form.cleaned_data['eight'])),nine = str(float(form.cleaned_data['nine'])),ten = str(float(form.cleaned_data['ten'])),eleven = str(float(form.cleaned_data['eleven'])),twelve = str(float(form.cleaned_data['twelve'])))
                used.save()
                return HttpResponseRedirect('/SchApp/account/budget/create_budget_month/')
            else:
                varerr ="All Fields Are Required"
                details = ll
                return render_to_response('budget/budgetmonth.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':details},context_instance = RequestContext(request))
        else:
            form = budgetformmonth()
            comp = tblcompanyinfo.objects.get(id = 1)
            if tblcalender.objects.all().count() == 0:
                varerr = "Contact Administrator to set up calendar year"
                return render_to_response('budget/budgetmonth.htm',{'varuser':varuser,'varerr':varerr,'form':form},context_instance = RequestContext(request))
            return render_to_response('budget/budgetmonth.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':ll,'date':'FROM '+ varstart.strftime("%d-%m-%Y") + ' TO ' + varend.strftime("%d-%m-%Y"),'comp':comp},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


def printbudgetmonth(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/budget/access-denied/')
        varerr =""
        details = ''
        if request.method == 'POST':
            form = reportform(request.POST) # A form bound to the POST data
            if form.is_valid():
                caldate1 = form.cleaned_data['varyear']
                caldate2 = caldate1.split('/')
                varstart = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                getmon = tblcalender.objects.all()
                varyear = varstart.year
                stmon1 =''
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
                vareyear = date(endyear,endmon,dday)
                details = tblbudgetmonthly.objects.filter(startmonth =  varsyear,endmonth = vareyear)
                ll = []
                for k in details:
                    tamt = float(k.first) + float(k.second) + float(k.third) + float(k.four) + float(k.five) + float(k.six) +float(k.seven) +float(k.eight) + float(k.nine) + float(k.ten) + float(k.eleven) + float(k.twelve)
                    l = {'acccode':k.acccode.acccode,'accname':k.acccode.accname,'groupname':k.acccode.groupname,'first':locale.format("%.2f",float(k.first),grouping=True),'second':locale.format("%.2f",float(k.second),grouping=True),'third':locale.format("%.2f",float(k.third),grouping=True),'four':locale.format("%.2f",float(k.four),grouping=True),'five':locale.format("%.2f",float(k.five),grouping=True),'six':locale.format("%.2f",float(k.six),grouping=True),'seven':locale.format("%.2f",float(k.seven),grouping=True),'eight':locale.format("%.2f",float(k.eight),grouping=True),'nine':locale.format("%.2f",float(k.nine),grouping=True),'ten':locale.format("%.2f",float(k.ten),grouping=True),'eleven':locale.format("%.2f",float(k.eleven),grouping=True),'twelve':locale.format("%.2f",float(k.twelve),grouping=True),'total':locale.format("%.2f",tamt,grouping=True)}
                    ll.append(l)
                comp = tblcompanyinfo.objects.get(id = 1)
                if form.cleaned_data['excelfile']:
                    response = HttpResponse(mimetype="application/ms-excel")
                    response['Content-Disposition'] = 'attachment; filename=budgetreport.xls'
                    wb = xlwt.Workbook()
                    ws = wb.add_sheet('budget')
                    ws.write(0, 1, comp.name)
                    ws.write(1, 1, comp.address)
                    ws.write(2, 1, 'BUDGET REPORT FOR YEAR %s'% vareyear.year )
                    ws.write(3, 0, 'S/N')
                    ws.write(3, 1, 'Account Name')
                    ws.write(3, 2, 'Account Code')
                    ws.write(3, 3, 'Account Type')
                    ws.write(3, 4, 'First Month')
                    ws.write(3, 5, 'Second Month')
                    ws.write(3, 6, 'Third Month')
                    ws.write(3, 7, 'Fourth Month')
                    ws.write(3, 8, 'Fifth Month')
                    ws.write(3, 9, 'Sixth Month')
                    ws.write(3, 10, 'Seventh Month')
                    ws.write(3, 11, 'Eighth Month')
                    ws.write(3, 12, 'Ninth Month')
                    ws.write(3, 13, 'Ten Month')
                    ws.write(3, 14, 'Eleventh Month')
                    ws.write(3, 15, 'Twelfth Month')
                    ws.write(3, 16, 'Total')

                    v = 4
                    for p,n in enumerate(ll):
                        ws.write(v, 0, p+1)
                        ws.write(v, 1, n['accname'])
                        ws.write(v, 2, n['acccode'])
                        ws.write(v, 3, n['groupname'])
                        ws.write(v, 4, n['first'])
                        ws.write(v, 5, n['second'])
                        ws.write(v, 6, n['third'])
                        ws.write(v, 7, n['four'])
                        ws.write(v, 8, n['five'])
                        ws.write(v, 9, n['six'])
                        ws.write(v, 10, n['seven'])
                        ws.write(v, 11, n['eight'])
                        ws.write(v, 12, n['nine'])
                        ws.write(v, 13, n['ten'])
                        ws.write(v, 14, n['eleven'])
                        ws.write(v, 15, n['twelve'])
                        ws.write(v, 16, n['total'])
                        v += 1
                    wb.save(response)
                    return response
                else:
                    return render_to_response('budget/printbudgetmonth.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':ll,'comp':comp,'headings':'BUDGET REPORT FOR YEAR %s'% vareyear.year},context_instance = RequestContext(request))
        else:
            form = reportform()
            return render_to_response('budget/printbudgetmonth.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':details},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def budgettype(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/budget/access-denied/')
        varerr =""
        if tblbudgettype.objects.all():
           currbud = tblbudgettype.objects.get(id = 1).budget_type
        else:
            currbud = "NONE"
        if request.method == 'POST':
            btype = request.POST['type'] # A form bound to the POST data
            if tblbudgettype.objects.all():
               ts = tblbudgettype.objects.get(id = 1)
               ts.budget_type = btype
               ts.save()
            else:
                sa = tblbudgettype(budget_type = btype)
                sa.save()
            return HttpResponseRedirect('/SchApp/account/budget/budget_type/')
        else:
            return render_to_response('budget/budgettype.htm',{'varuser':varuser,'varerr':varerr,'curr':currbud},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


