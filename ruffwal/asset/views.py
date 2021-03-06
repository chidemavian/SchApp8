# Create your views here.
from django.template import loader, Context,RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import  HttpResponseRedirect
from django.contrib.sessions.models import Session
import datetime
from datetime import date
from myproject.ruffwal.rwadmin.models import *
from myproject.ruffwal.asset.form import *
from myproject.ruffwal.asset.models import *
from myproject.ruffwal.rsetup.models import *
from myproject.ruffwal.posting.models import *
from myproject.ruffwal.asset.opbal import *
import random
import locale
import xlwt
locale.setlocale(locale.LC_ALL,'')

def unauto(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        return render_to_response('asset/unautorise.htm',{'varuser':varuser,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def enterasset(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if int(uenter) == 0 :
            return HttpResponseRedirect('/welcome/')
        varerr =""
        vardate = date.today()
        vardate1 = vardate.strftime('%B %d,%Y')
        return render_to_response('asset/enter.htm',{'varuser':varuser,'varerr':varerr,'vardate1':vardate1})
    else:
        return HttpResponseRedirect('/login/')

#************************************************Treating The Stock *********************
def assetregister(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/assets/access-denied/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
            form = inventoryform(request.POST) # A form bound to the POST data
            if form.is_valid():
                subgrname = form.cleaned_data['subgrname']
                accname = form.cleaned_data['accname']
                caldate1 = form.cleaned_data['recdate']
                deprate = form.cleaned_data['deprate']
                department = form.cleaned_data['department']
                span = form.cleaned_data['span']
                opdepn = form.cleaned_data['opdepn']
                accnameupp = accname.upper()
                caldate2 = caldate1.split('/')
                recdate = date(int(caldate2[2]),int(caldate2[1]),int(caldate2[0]))
                accnameupp = accnameupp.replace('&', 'AND')
                if tblasset.objects.filter(name = accnameupp,subname = subgrname):
                    varerr ="Asset In Existence"
                    getdetails = ""
                    return render_to_response('asset/assetsetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                else:
                    varsubcode = tblaccount.objects.get(accname = subgrname,groupcode = '10000')#account level
                    vgsubcode = varsubcode.subgroupcode
                    grname = varsubcode.groupname
                    vcount = tblasset.objects.filter(subname = subgrname ).count()
                    vcount += 1
                    srealsubcode = str(varsubcode.acccode) + str(vcount)
                    uid = ''
                    for m in range(25):
                        k = random.randint(1,999)
                        uid += str(k)
                    uid += srealsubcode
                    #CREATING THE ASSET ACCOUNT
                    #used = tblaccount(groupname = grname,groupcode = varsubcode.groupcode,subgroupname = varsubcode.accname,subgroupcode=varsubcode.acccode,datecreated = date.today(),userid =varuser,accname = accnameupp,acccode = srealsubcode.upper(),accbal= 0,accstatus ="ACTIVE",recreport ="NO")
                    #used.save()
                    used = tblasset(name = accnameupp,acccode = srealsubcode,deprate = deprate,datepurchase = recdate,userid =varuser,subname = varsubcode.accname,subcode = varsubcode.acccode,department = department,span = span,refcode = uid,opdepn = str(opdepn))
                    used.save()
                    #*****************************
                    return HttpResponseRedirect('/SchApp/account/assets/asset-creation/')
            else:
                getdetails = tblasset.objects.all()
                varerr = "All Fields Are Required"
                return render_to_response('asset/assetsetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = inventoryform()
            getdetails = tblasset.objects.all()
            return render_to_response('asset/assetsetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def editasset(request,refcode):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/assets/access-denied/')
        varerr =""
        getdetails = tblasset.objects.get(refcode = refcode)
        if request.method == 'POST':
            subgrname = request.POST['subgrname']
            accname = request.POST['accname']
            caldate1 = request.POST['recdate']
            deprate = request.POST['deprate']
            department = request.POST['department']
            span = request.POST['span']
            opdepn = request.POST['opdepn']

            if subgrname == "" or accname == "" or caldate1 == "" or deprate == "" or department == "" or span == "" or opdepn =="":
                varerr = "All Fields Are Required"
                dept = tblassetdepartment.objects.all()
                return render_to_response('asset/editasset.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'dept':dept})
            accnameupp = accname.upper()
            caldate2 = caldate1.split('/')
            recdate = date(int(caldate2[2]),int(caldate2[1]),int(caldate2[0]))
            accnameupp = accnameupp.replace('&', 'AND')
            try:
                krate = float(deprate)
            except :
                varerr = "Invalid Depreciation Rate"
                dept = tblassetdepartment.objects.all()
                return render_to_response('asset/editasset.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'dept':dept})
            try:
                kspan = float(span)
            except :
                varerr = "Invalid Asset Span"
                dept = tblassetdepartment.objects.all()
                return render_to_response('asset/editasset.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'dept':dept})

            try:
                kopdepn = float(opdepn)
            except :
                varerr = "Invalid Opening DEPN."
                dept = tblassetdepartment.objects.all()
                return render_to_response('asset/editasset.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'dept':dept})

            if tblasset.objects.filter(name = accnameupp,subname = subgrname).exclude(refcode = refcode).count() == 0:
                #tblaccount.objects.filter(acccode = getdetails.acccode).update(accname = accnameupp)
                #tbltransaction.objects.filter(acccode = getdetails.acccode).update(accname = accnameupp)
                #tbltemp.objects.filter(acccode = getdetails.acccode).update(accname = accnameupp)
                #tbltempreceipt.objects.filter(acccode = getdetails.acccode).update(accname = accnameupp)
                #tbltemppayment.objects.filter(acccode = getdetails.acccode).update(accname = accnameupp)
                #tbljournal.objects.filter(acccode = getdetails.acccode).update(accname = accnameupp)
                #tblstandard.objects.filter(acccode = getdetails.acccode).update(accname = accnameupp)
                getdetails.name = accnameupp
                getdetails.deprate = str(krate)
                getdetails.datepurchase = recdate
                getdetails.department = department
                getdetails.span = str(kspan)
                getdetails.userid = varuser
                getdetails.opdepn = str(opdepn)
                getdetails.save()
                return HttpResponseRedirect('/SchApp/account/assets/asset-creation/')
            else:
                varerr ="Asset In Existence"
                return render_to_response('asset/editasset.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
        else:
            dept = tblassetdepartment.objects.all()
            return render_to_response('asset/editasset.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'dept':dept})

    else:
        return HttpResponseRedirect('/login/')

def assetdept(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/assets/access-denied/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
            form = assetdeptform(request.POST) # A form bound to the POST data
            if form.is_valid():
                name = form.cleaned_data['name']
                accnameupp = name.upper()
                if tblassetdepartment.objects.filter(name = accnameupp):
                    varerr ="Name In Existence"
                    getdetails = ""
                    return render_to_response('asset/assetdept.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                else:
                    used = tblassetdepartment(name = accnameupp,userid =varuser)
                    used.save()
                    #*****************************
                    return HttpResponseRedirect('/SchApp/account/assets/asset-department/')
            else:
                varerr = "Invalid Entry"
                return render_to_response('asset/assetdept.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = assetdeptform()
            getdetails = tblassetdepartment.objects.all()
            return render_to_response('asset/assetdept.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def deleteasset(request,refcode):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/assets/access-denied/')
        varerr =""
        getdetails = tblaccount.objects.get(refcode = refcode)
        acc = getdetails.acccode
        subname = getdetails.subgroupname
        grname = getdetails.groupname
        if tbltransaction.objects.filter(groupname = grname,subname = subname,acccode = acc):
            varerr = "This Assets Can Not Be Deleted"
            return render_to_response('asset/assetdept.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            tblaccount.objects.filter(refcode = refcode).delete()
            tblasset.objects.filter(refcode = refcode).delete()
        return HttpResponseRedirect('/SchApp/account/assets/asset-creation/')
    else:
        return HttpResponseRedirect('/SchApp/account/profile/login/')

def assetlist(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/assets/access-denied/')
        varerr =""
        getdetails =""
        comp = tblcompanyinfo.objects.all()
        logo = ''
        address = ''
        compname = ''
        for k in comp:
            logo = k.picture
            address = k.address
            compname = k.name
        if request.method == 'POST':
            form = assetlistform(request.POST) # A form bound to the POST data
            if form.is_valid():
                subgrname = form.cleaned_data['subgrname']
                all =[]
                if form.cleaned_data['allasset']:
                    allassets = tblsubgroup.objects.filter(groupcode ='10000').order_by('subgroupcode')
                    for j in allassets:
                        getdetails = tblasset.objects.filter(subname = j.subgroupname)
                        k ={'sub':j.subgroupname,'getdetails':getdetails}
                        all.append(k)
                    return render_to_response('asset/assetlist.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'comp':compname,'address':address,'logo':logo,'asset':str(subgrname).title(),'all':all},context_instance = RequestContext(request))
                else:
                    getdetails = tblasset.objects.filter(subname = subgrname)
                    k ={'sub':subgrname,'getdetails':getdetails}
                    all.append(k)
                    return render_to_response('asset/assetlist.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'comp':compname,'address':address,'logo':logo,'asset':str(subgrname).title(),'all':all},context_instance = RequestContext(request))
            else:
                varerr = "Invalid Assets"
                return render_to_response('asset/assetlist.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

        else:
            form = assetlistform()
            getdetails = ""
            return render_to_response('asset/assetlist.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def assetschedule(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/assets/access-denied/')
        varerr =""
        getdetails =""
        comp = tblcompanyinfo.objects.all()
        logo = ''
        address = ''
        compname = ''
        for k in comp:
            logo = k.picture
            address = k.address
            compname = k.name
        if request.method == 'POST':
            form = dateform(request.POST) # A form bound to the POST data
            if form.is_valid():
                subgrname = form.cleaned_data['subgrname']
                caldate11 = form.cleaned_data['enddate']
                try:
                    vyear = int(caldate11)
                except :
                    varerr ="Invalid Year "
                    return render_to_response('asset/schedule.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

                getdate = tblcalender.objects.all()
                stmon1 = date.today()
                endmon1 = date.today()
                for g in getdate:
                   stmon1 = g.startmonth
                   endmon1 = g.endtmonth
                calyear = stmon1.year
                calendyear = endmon1.year
                #varstart = stmon1
                #varend = endmon1
                if calyear == calendyear:
                    varstart = date(int(vyear),int(stmon1.month),int(stmon1.day))
                    varend = date(int(vyear),int(endmon1.month),int(endmon1.day))
                else:
                    varstart = date(int(vyear-1),int(stmon1.month),int(stmon1.day))
                    varend = date(int(vyear),int(endmon1.month),int(endmon1.day))
                mmdate = date(vyear,12,31)
                if tblasset.objects.filter(datepurchase__lte= mmdate):
                    pass
                else:
                    varerr ="No Asset Found "
                    return render_to_response('asset/schedule.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                all =[]
                depyear = 0
                if tblresidualvalue.objects.all():
                    residualval = tblresidualvalue.objects.get(id = 1).deprate
                else:
                    residualval = 100
                allassets = tblsubgroup.objects.filter(groupcode ='10000',subgroupname = subgrname)
                #print 'The Calendar :',varstart,varend
                for j in allassets:
                    ass =[]
                    totaldepn = 0
                    totalamount = 0
                    totaladdition = 0
                    ftotalamount = 0
                    totalopendep = 0
                    totalyear = 0
                    totalnbv = 0
                    getdetails = tblasset.objects.filter(subname = subgrname)
                    for p in getdetails:
                        sub = p.subcode
                        acc = tblaccount.objects.get(acccode = sub)
                        amount = getopbal1(p.acccode,varstart)
                        addition = getcurrentbalance1(p.acccode,varstart,varend)
                        total = float(amount) + float(addition)
                        opendepold = p.opdepn
                        #y = 0
                        #if tbltransaction.objects.filter(acccode = p.acccode).count() == 0:
                         #   pass
                        #else:
                        #    trans = tbltransaction.objects.filter(acccode = p.acccode).order_by('id')[:1]
                        #    for jj in trans:
                        #        y = jj.transdate.year
                        #if y > vyear:
                        #    pass
                        #else:
                        opendep = getopendep(p.datepurchase.year,vyear,p.acccode,p.deprate,acc.groupname,acc.groupcode)
                        opendep += float(opendepold)
                        totamt = float(amount)+float(addition)
                        rate = p.deprate/100
                        if totamt > opendep:
                           depyear = totamt * float(rate)
                           totdep = depyear + float(opendep)
                           if totdep >= totamt:
                               depyear = totamt - float(opendep) - float(residualval)
                        else:
                            opendep = totamt - float(residualval)
                            depyear = 0
                        totdep = depyear + float(opendep)
                        nbv = totamt - totdep
                        if totamt == 0:
                            pass
                        else:
                           k ={'name':p.name,'acccode':p.acccode,'datepurchase':p.datepurchase,'deprate':p.deprate,'amount':locale.format("%.2f",amount,grouping=True),'additional':locale.format("%.2f",addition,grouping=True),'totamt':locale.format("%.2f",totamt,grouping=True),'opendep':locale.format("%.2f",opendep,grouping=True),'depyear':locale.format("%.2f",depyear,grouping=True),'totdep':locale.format("%.2f",totdep,grouping=True),'nbv':locale.format("%.2f",nbv,grouping=True)}
                           ass.append(k)
                        totaldepn += totdep #total depreciation
                        totalamount += amount #total Amount
                        totaladdition += addition#total addition
                        ftotalamount += totamt # full total amount
                        totalopendep += opendep #total depreciation
                        totalyear += depyear # total depn for the year
                        totalnbv += nbv #total net book value
                    m = {'sub':j.subgroupname,'getdetails':ass,'totaldepn':locale.format("%.2f",totaldepn,grouping=True),'totalamount':locale.format("%.2f",totalamount,grouping=True),'totaladdition':locale.format("%.2f",totaladdition,grouping=True),'ftotal':locale.format("%.2f",ftotalamount,grouping=True),'totalopendepn':locale.format("%.2f",totalopendep,grouping=True),'totalyear':locale.format("%.2f",totalyear,grouping=True),'totalnbv':locale.format("%.2f",totalnbv,grouping=True)}
                    all.append(m)
                comp = tblcompanyinfo.objects.get(id = 1)
                if form.cleaned_data['excelfile']:
                    response = HttpResponse(mimetype="application/ms-excel")
                    response['Content-Disposition'] = 'attachment; filename=assetschedule.xls'
                    wb = xlwt.Workbook()
                    ws = wb.add_sheet('assetschedule')
                    ws.write(0, 1, comp.name)
                    ws.write(1, 1, comp.address)
                    ws.write(2, 1, 'ASSET SCHEDULE FOR YEAR %s'% vyear )
                    ws.write(3, 0, 'S/N')
                    ws.write(3, 1, 'Account Name')
                    ws.write(3, 2, 'Date Of Purchase')
                    ws.write(3, 3, 'Depn Rate')
                    ws.write(3, 4, 'Amount')
                    ws.write(3, 5, 'Add. Amount')
                    ws.write(3, 6, 'Total Amount')
                    ws.write(3, 7, 'Open Depn')
                    ws.write(3, 8, 'Current Depn.')
                    ws.write(3, 9, 'Total Depn')
                    ws.write(3, 10, 'NBV')
                    v = 4
                    for n in all:
                        ws.write(v, 0, n['sub'])
                        v += 1
                        for p,a in enumerate(n['getdetails']):
                            ws.write(v, 0, p+1)
                            ws.write(v, 1, a['name'])
                            ws.write(v, 2, str(a['datepurchase'].day) +'/'+ str(a['datepurchase'].month) +'/'+str(a['datepurchase'].year))
                            ws.write(v, 3, a['deprate'])
                            ws.write(v, 4, a['amount'])
                            ws.write(v, 5, a['additional'])
                            ws.write(v, 6, a['totamt'])
                            ws.write(v, 7, a['opendep'])
                            ws.write(v, 8, a['depyear'])
                            ws.write(v, 9, a['totdep'])
                            ws.write(v, 10, a['nbv'])
                            v += 1
                        ws.write(v, 3, 'Total DEPN.')
                        ws.write(v, 4, n['totalamount'])
                        ws.write(v, 5, n['totaladdition'])
                        ws.write(v, 6, n['ftotal'])
                        ws.write(v, 7, n['totalopendepn'])
                        ws.write(v, 8, n['totalyear'])
                        ws.write(v, 9, n['totaldepn'])
                        ws.write(v, 10, n['totalnbv'])
                        v += 1
                    wb.save(response)
                    return response
                    #return render_to_response('asset/schedule.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'comp':compname,'address':address,'logo':logo,'all':all},context_instance = RequestContext(request))
                else:
                    return render_to_response('asset/schedule.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'comp':compname,'address':address,'logo':logo,'all':all,'year':vyear},context_instance = RequestContext(request))
            else:
                varerr ="Invalid Entry"
                return render_to_response('asset/schedule.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = dateform()
            getdetails = ""
            return render_to_response('asset/schedule.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


def residual(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/assets/access-denied/')
        varerr =""
        getdetails =""
        if tblresidualvalue.objects.all():
            residualval = tblresidualvalue.objects.get(id = 1).deprate
        else:
            residualval = 100
        if request.method == 'POST':
            value = request.POST['value']
            if value == "":
                varerr ="Invalid Value "
                return render_to_response('asset/residualvalue.htm',{'varuser':varuser,'varerr':varerr,'data':residualval},context_instance = RequestContext(request))
            try:
                rvalue = float(value)
            except :
                varerr ="Invalid Value "
                return render_to_response('asset/residualvalue.htm',{'varuser':varuser,'varerr':varerr,'data':residualval},context_instance = RequestContext(request))
            if tblresidualvalue.objects.filter(id = 1):
               get = tblresidualvalue.objects.get(id = 1)
               get.deprate = str(rvalue)
               get.save()
            else:
                sa = tblresidualvalue(deprate = str(rvalue),userid = varuser)
                sa.save()
            return HttpResponseRedirect('/SchApp/account/assets/asset-operation-successful/')
        else:
            return render_to_response('asset/residualvalue.htm',{'varuser':varuser,'varerr':varerr,'data':residualval},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def successful(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        return render_to_response('asset/invsuccess.htm',{'varuser':varuser,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def assetsummary(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/assets/access-denied/')
        varerr =""
        getdetails =""
        comp = tblcompanyinfo.objects.all()
        logo = ''
        address = ''
        compname = ''
        for k in comp:
            logo = k.picture
            address = k.address
            compname = k.name
        if request.method == 'POST':
            form = assetlistform(request.POST) # A form bound to the POST data
            if form.is_valid():
                subgrname = form.cleaned_data['subgrname']
                all =[]
                if form.cleaned_data['allasset']:
                    allassets = tblsubgroup.objects.filter(groupcode ='10000')
                    for j in allassets:
                        getdetails = tblasset.objects.filter(subname = j.subgroupname)
                        ass = []
                        for p in getdetails:
                            accbal = getbal1(p.acccode)
                            k ={'name':p.name,'acccode':p.acccode,'datepurchase':p.datepurchase,'span':p.span,'amount':locale.format("%.2f",accbal,grouping=True)}
                            ass.append(k)
                        k ={'sub':j.subgroupname,'getdetails':ass}
                        all.append(k)
                    return render_to_response('asset/assetsummary.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'comp':compname,'address':address,'logo':logo,'asset':str(subgrname).title(),'all':all},context_instance = RequestContext(request))
                else:
                    getdetails = tblasset.objects.filter(subname = subgrname)
                    ass = []
                    for p in getdetails:
                        accbal = getbal1(p.acccode)
                        k ={'name':p.name,'acccode':p.acccode,'datepurchase':p.datepurchase,'span':p.span,'amount':locale.format("%.2f",accbal,grouping=True)}
                        ass.append(k)
                    k ={'sub':subgrname,'getdetails':ass}
                    all.append(k)
                    return render_to_response('asset/assetsummary.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'comp':compname,'address':address,'logo':logo,'asset':str(subgrname).title(),'all':all},context_instance = RequestContext(request))
            else:
                varerr = "Invalid Entry"
                return render_to_response('asset/assetsummary.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = assetlistform()
            getdetails = ""
            return render_to_response('asset/assetsummary.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

#********************creating the asset Cost ********************
def assetcost(request,refcode):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/assets/access-denied/')
        varerr =""
        getdetails = tblasset.objects.get(refcode = refcode)
        data = tblassetcost.objects.filter(acccode = getdetails.acccode)
        if request.method == 'POST':
            form = costform(request.POST) # A form bound to the POST data
            if form.is_valid():
                caldate1 = form.cleaned_data['transdate']
                value = form.cleaned_data['value']
                caldate2 = caldate1.split('/')
                transdate = date(int(caldate2[2]),int(caldate2[1]),int(caldate2[0]))
                getdate = tblcalender.objects.all()
                stmon1 = date.today()
                endmon1 = date.today()
                for g in getdate:
                    stmon1 = g.startmonth
                    endmon1 = g.endtmonth
                if transdate < stmon1 or transdate > endmon1 :
                    varerr = "Invalid Date Entry "
                    return render_to_response('asset/assetcost.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'data':data},context_instance = RequestContext(request))
                uid = ''
                for m in range(25):
                    k = random.randint(1,999)
                    uid += str(k)
                vsave = tblassetcost(acccode =  getdetails.acccode,transdate = transdate,userid = varuser,amount = value,refcode =uid)
                vsave.save()
                return HttpResponseRedirect('/SchApp/account/assets/asset-cost/%s/'%refcode)
            else:
                varerr = "Invalid Entry"
                return render_to_response('asset/assetcost.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'data':data},context_instance = RequestContext(request))
        else:
            form = costform()
            return render_to_response('asset/assetcost.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails,'data':data},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

#remove Cost
def remove_cost(request,refcode):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        ass = tblassetcost.objects.get(refcode = refcode)
        getdetails = tblasset.objects.get(acccode = ass.acccode)
        uenter = user.unpresented
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/assets/access-denied/')
        tblassetcost.objects.filter(refcode = refcode).delete()
        return HttpResponseRedirect('/SchApp/account/assets/asset-cost/%s/'%getdetails.refcode)
    else:
        return HttpResponseRedirect('/login/')








