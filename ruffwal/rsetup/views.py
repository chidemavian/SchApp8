from django.template import loader, Context,RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import  HttpResponseRedirect
from myproject.ruffwal.raccount.form import useraccform
from django.core.serializers.json import simplejson as json
from myproject.ruffwal.rsetup.form import *
from myproject.ruffwal.stock.models import *
from myproject.ruffwal.rsetup.models import *
from myproject.ruffwal.posting.models import *
from myproject.ruffwal.rwadmin.models import *
import datetime

def entersetupcode(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = groupform(request.POST) # A form bound to the POST data
          if form.is_valid():
             gname = form.cleaned_data['frgroup']
             sgname = form.cleaned_data['subname']
             sgnamety =  sgname.upper()
             sgnamety = sgnamety.replace(' ', '-')
             #pull into the sub table
             try:
                 varvali = tblsubgroup.objects.get(subgroupname__iexact = sgnamety)
                 varerr ="Sub Name In Existence"
                 #if varvali = sgna
                 return render_to_response('setup/entersetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             except:
                 varcode = tblgroup.objects.get(groupname = gname)
                 vgcode = varcode.groupcode
                 #print vgcode count
                 vcount = tblsubgroup.objects.filter(groupname = gname).count()
                 vcount = vcount + 1
                 k = str(vcount)
                 pk = len(k)
                 if pk == 1:
                     vcount =  vcount * 100
                     vgcodetu = vgcode[0:2]
                 elif pk == 2:
                     vcount = vcount *100
                     vgcodetu = vgcode[0:1]
                 else:
                     return render_to_response('setup/entersetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))   #the three digits from the subgroup code
                 # the first two digits from the group code
                 srealsubcode = str(vgcodetu) + str(vcount)
                 #print srealsubcode
                 used = tblsubgroup(groupname = gname,groupcode = vgcode,subgroupname = sgnamety,subgroupcode=srealsubcode,datecreated = datetime.datetime.today(),userid =varuser )
                 used.save()
                 #*****************************
                 getdetails = tblsubgroup.objects.filter(groupname = gname).order_by('subgroupcode')
                 #now i do insertion
                 return render_to_response('setup/entersetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = groupform()
            getdetails = tblsubgroup.objects.all().order_by('subgroupcode')
        return render_to_response('setup/entersetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
     else:
       return HttpResponseRedirect('/login/')


def entersetupcodedet(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = groupformdetails(request.POST) # A form bound to the POST data
          if form.is_valid():
             gname = form.cleaned_data['frgroup']
                 #*****************************
             getdetails = tblsubgroup.objects.filter(groupname = gname).order_by('subgroupcode')
             return render_to_response('setup/groupdetails.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = groupform()
            getdetails = tblsubgroup.objects.all().order_by('subgroupcode')
        return render_to_response('setup/groupdetails.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
    else:
       return HttpResponseRedirect('/login/')

def createacccode(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = accountform(request.POST) # A form bound to the POST data
          if form.is_valid():
             gname = form.cleaned_data['grpname']
             subgrname = form.cleaned_data['subgrname']
             accname = form.cleaned_data['accname']
             accnameupp = accname.upper()
             accnameupp = accnameupp.replace(' ', '-')
             try:
                 varvali = tblaccount.objects.get(accname__iexact = accnameupp,subgroupname__iexact = subgrname,groupname__iexact = gname )
                 varerr ="Account Name In Existence"
                 #if varvali = sgna
                 return render_to_response('setup/createacc.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             except:
                 varcode = tblgroup.objects.get(groupname = gname)
                 vgcode = varcode.groupcode
                 varsubcode = tblsubgroup.objects.get(subgroupname__iexact = subgrname,groupname__iexact = gname)
                 vgsubcode = varsubcode.subgroupcode
                 #print vgcode count
                 vcount = tblaccount.objects.filter(groupname = gname,subgroupname =subgrname ).count()
                 vcount = vcount + 1
                 k = str(vcount)
                 pk = len(k)
                 if pk == 1:
                     vcount =  vcount
                     vgcodetu = vgsubcode[0:4]
                 elif pk == 2:
                     vcount = vcount
                     vgcodetu = vgsubcode[0:3]
                 else:
                     return render_to_response('setup/createacc.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))   #the three digits from the subgroup code
                 # the first two digits from the group code
                 srealsubcode = str(vgcodetu) + str(vcount)
                 #print srealsubcode
                 used = tblaccount(groupname = gname,groupcode = vgcode,subgroupname = subgrname,subgroupcode=vgsubcode,datecreated = datetime.datetime.today(),userid =varuser,accname = accnameupp,acccode = srealsubcode,accbal= 0,accstatus ="ACTIVE",recreport ="YES" )
                 used.save()
                 #*****************************
                 getdetails = tblaccount.objects.filter(groupname = gname,subgroupname = subgrname,recreport ="YES" ).order_by('acccode')
                 #now i do insertion
                 return render_to_response('setup/createacc.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                 #*****************************
                 getdetails = tblaccount.objects.filter(groupname = gname,subgroupname = subgrname,recreport ="YES" ).order_by('acccode')
             return render_to_response('setup/createacc.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = accountform()
            getdetails = tblaccount.objects.filter(recreport ="YES").order_by('acccode')
        return render_to_response('setup/createacc.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
    else:
       return HttpResponseRedirect('/login/')

def getdataccode(request):
     if request.is_ajax() and request.method == 'POST':
        auto_type = tblsubgroup.objects.filter(groupname=request.POST.get('grpname', ''))
        colors = auto_type.subgroupname.all() # get all the colors for this type of auto.
     return render_to_response('setup/createacc.htm', locals())
    #  return render_to_response('getdata.htm')

def getsubaccountacc(request):
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
                data = tblsubgroup.objects.filter(groupname = state).exclude(groupname = "CURRENT ASSETS",subgroupname ="STAFF-DEBTORS").exclude(groupname = "CURRENT ASSETS",subgroupname ="STUDENT DEBTORS").exclude(groupname = "CURRENT ASSETS",subgroupname ="MINI-STORE").exclude(groupname = "CURRENT ASSETS",subgroupname ="WORK-IN-PROGRESS").exclude(groupname = "CURRENT LIABILITIES",subgroupname ="PAYABLES").exclude(groupname = "EXPENSES",subgroupname ="TAX LIABILITIES").order_by('subgroupcode')
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

def getaccountdetails(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                grname,subgrp = acccode.split(':')
                getdetails = tblaccount.objects.filter(recreport ="YES",groupname = grname,subgroupname = subgrp).exclude(groupname = "CAPITAL AND RESERVES",subgroupname ="SHAREHOLDERS FUND",accname = "CURRENT-YEAR-P/L").order_by('acccode')
                return render_to_response('setup/accountdetails.html',{'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def editacc(request,acccode):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/unauto/')
        varerr =""
        if request.method == 'POST':
            getdetails = ""
            acname = request.POST['accname']
            accno = request.POST['hcode']
            subname = request.POST['hsubname']
            grpname = request.POST['hgrpname']
            acname = acname.replace(' ', '-')
            acname = acname.upper()
            telen =  len(acname)
            if telen == 0:
                return HttpResponseRedirect('/SchApp/account/createacc/')
            if tblaccount.objects.filter(accname = acname.upper(),subgroupname = subname,groupname = grpname ).exclude(acccode = acccode).count() == 0:
                seldata = tblaccount.objects.get(acccode = accno)
                seldata.accname = acname
                seldata.save()
                tbltransaction.objects.filter(acccode = accno).update(accname = acname )
                tblstock.objects.filter(subcode = accno).update(subname = acname )
                tblstocktransaction.objects.filter(acccode = accno).update(stockname = acname)
                return HttpResponseRedirect('/SchApp/account/createacc/')
            else:
                return HttpResponseRedirect('/SchApp/account/createacc/')
        else:
            try:
              getdetails = tblaccount.objects.get(acccode = acccode)#.order_by('acccode')#tblaccount_acccode
              return render_to_response('setup/editacc.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                varerr = "Account Not Exist"
                return render_to_response('setup/editacc.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})

    else:
       return HttpResponseRedirect('/login/')

def getsubaccount(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tblaccount.objects.get(acccode = acccode)
                return render_to_response('setup/editacc.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')
def editsubacc(request,acccode):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/unauto/')
        varerr =""
        if request.method == 'POST':
            getdetails = ""
            acname = request.POST['accname']
            accno = request.POST['hcode']
            grpname = request.POST['hgrpname']
            acname = acname.replace(' ', '-')
            acname = acname.upper()
            telen =  len(acname)
            if telen == 0:
                 varerr ="Invalid Name"
                 getdetails = tblsubgroup.objects.get(acccode = accno)#.order_by('acccode')#tblaccount_acccode
                 return render_to_response('setup/editsubacc.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            try:
                 varvali = tblsubgroup.objects.get(accname__iexact = acname.upper(),groupname__iexact = grpname )
                 varerr ="Sub Name In Existence"
                 getdetails = tblsubgroup.objects.get(acccode = accno)#.order_by('acccode')#tblaccount_acccode
                 return render_to_response('setup/editsubacc.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                #update the request
                if acname == "STOCKS":
                    varerr = "The Name Can not be changed"
                    getdetails = tblsubgroup.objects.get(subgroupcode = acccode)
                    return render_to_response('setup/editsubacc.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                else:
                    seldata = tblsubgroup.objects.get(subgroupcode = accno)
                    seldata.subgroupname = acname
                    seldata.save()
                    selsubdata = tblaccount.objects.filter(subgroupcode = accno).update(subgroupname =acname )
                    #selsubdata.subgroupname = acname
                    #selsubdata.update()
                   # print acname,accno
                    #return render_to_response('editacc.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'acname':acname})
                    return HttpResponseRedirect('/SchApp/account/entersetup/')
        else:
            try:
              getdetails = tblsubgroup.objects.get(subgroupcode = acccode)#.order_by('acccode')#tblaccount_acccode
              return render_to_response('setup/editsubacc.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                varerr = "Account Not Exist"
                return render_to_response('setup/editsubacc.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
    else:
       return HttpResponseRedirect('/login/')


def stock(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = inventoryform(request.POST) # A form bound to the POST data
          if form.is_valid():
             subgrname = form.cleaned_data['subgrname']
             accname = form.cleaned_data['accname']
             accnameupp = accname.upper()
             accnameupp = accnameupp.replace(' ', '-')
             try:
                 varvali = tblstock.objects.get(stockname__iexact = accnameupp,subname__iexact = subgrname)
                 varerr ="Stock Name In Existence"
                 getdetails = ""
                 return render_to_response('setup/stocksetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             except:
                 varsubcode = tblaccount.objects.get(accname__iexact = subgrname)
                 vgsubcode = varsubcode.acccode
                 #print vgcode count
                 vcount = tblstock.objects.filter(subname = subgrname ).count()
                 vcount = vcount + 1
                 srealsubcode = str(vgsubcode) + str(vcount)
                 #print srealsubcode
                 used = tblstock(stockname = accnameupp,acccode = srealsubcode,accbal = 0,datecreated = datetime.datetime.today(),userid =varuser,subname = subgrname,subcode = vgsubcode,qtybal = 0,avgprice = 0)
                 used.save()
                 #*****************************
                 getdetails = tblstock.objects.all().exclude(subname = "MINI-STORE-BALANCE").order_by('acccode')
                 #now i do insertion
                 return render_to_response('setup/stocksetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = inventoryform()
            getdetails = tblstock.objects.all().exclude(subname = "MINI-STORE-BALANCE").order_by('acccode')
        return render_to_response('setup/stocksetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
    else:
       return HttpResponseRedirect('/login/')
def getstock(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails =  tblstock.objects.get(acccode = acccode)
                return render_to_response('setup/editstock.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')
def editstock(request,acccode):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/unauto/')
        varerr =""
        if request.method == 'POST':
            getdetails = ""
            acname = request.POST['accname']
            accno = request.POST['hcode']
            grpname = request.POST['hgrpname']
            acname = acname.replace(' ', '-')
            acname = acname.upper()
            telen =  len(acname)
           # print 'acc name :', acname,'acc no :',accno,'sub group :',grpname
            if telen == 0:
                return HttpResponseRedirect('/SchApp/account/inventory/')
            if tblstock.objects.filter(stockname = acname.upper(),subname = grpname).exclude(acccode = accno).count() == 0:
                seldata = tblstock.objects.get(acccode = accno)
                seldata.stockname = acname
                seldata.save()
                tblstocktransaction.objects.filter(acccode = accno).update(stockname = acname)
                return HttpResponseRedirect('/SchApp/account/inventory/')
            else:
                return HttpResponseRedirect('/SchApp/account/inventory/')
        else:
            try:
              getdetails = tblstock.objects.get(acccode = acccode)#.order_by('acccode')#tblaccount_acccode
              return render_to_response('setup/editstock.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                varerr = "Account Not Exist"
                return render_to_response('setup/editstock.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
    else:
       return HttpResponseRedirect('/login/')

def debtors(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.receivables
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = debtorsform(request.POST) # A form bound to the POST data
          if form.is_valid():
             accname = form.cleaned_data['accname']
             accnameupp = accname.upper()
             address1 = form.cleaned_data['address']
             phoneno1 = form.cleaned_data['phoneno']
             accnameupp = accnameupp.replace(' ', '-')
             try:
                 varvali = tblaccount.objects.get(accname__iexact = accnameupp,subgroupname__iexact = "RECEIVABLES",groupname__iexact ="CURRENT ASSETS")
                 varerr ="Debtors Name In Existence"
                 getdetails = receivables.objects.filter().order_by('id')
                 return render_to_response('setup/debtorssetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             except:
                 vcount = tblaccount.objects.filter(subgroupname = "RECEIVABLES",groupname ="CURRENT ASSETS" ).exclude(accname = "TRADE-DEBTORS").count()
                 vcount = vcount + 1
                 #print vcount
                 varaccno = "1" + str(vcount)
                 #print varaccno
                 used = tblaccount(groupname = "CURRENT ASSETS",groupcode = "30000",subgroupname = "RECEIVABLES",subgroupcode="30200",datecreated = datetime.datetime.today(),userid =varuser,accname = accnameupp,acccode = varaccno,accbal= 0,accstatus ="ACTIVE",recreport ="NO" )
                 used.save()
                 used1 = receivables(accname = accnameupp,acccode = varaccno,address = address1,phoneno=phoneno1,userid = varuser )
                 used1.save()
                 #*****************************
                 getdetails = receivables.objects.filter().order_by('id')
                 return HttpResponseRedirect('/SchApp/account/receivables/')
                 #getdetails = tblaccount.objects.filter(groupname ="CURRENT ASSETS",subgroupname = "RECEIVABLES").exclude(accname = "TRADE-DEBTORS").order_by('acccode')
                 #now i do insertion
                # return render_to_response('setup/debtorssetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = debtorsform()
            getdetails =  receivables.objects.filter().order_by('id')
            #getdetails = tblaccount.objects.filter(groupname ="CURRENT ASSETS",subgroupname = "RECEIVABLES").exclude(accname = "TRADE-DEBTORS").order_by('acccode')
        return render_to_response('setup/debtorssetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

    else:
       return HttpResponseRedirect('/login/')

def getdebtordia(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails =  receivables.objects.get(id = acccode)
               # print getdetails
                return render_to_response('setup/editdebtors.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def editdebtors(request,acccode):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.receivables
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/unauto/')
        varerr =""
        if request.method == 'POST':
            getdetails = ""
            acname = request.POST['accname']
            accno = request.POST['hcode']
            subname = request.POST['subname']
            grpname = request.POST['grpname']
            acname = acname.replace(' ', '-')
            acname = acname.upper()
            telen1 =  len(subname)
            telen2 =  len(grpname)

            telen =  len(acname)
            if telen == 0 :
                return HttpResponseRedirect('/SchApp/account/receivables/')
            if receivables.objects.filter(accname = acname.upper(),address = subname,phoneno = grpname ).exclude(acccode = accno).count()== 0:
                #update the request  replace
                seldata = tblaccount.objects.get(acccode = accno)
                seldata.accname = acname
                seldata.save()
                seldata1 = tbltransaction.objects.filter(acccode = accno).update(accname = acname)
                seldata2 = receivables.objects.get(acccode = accno)
                seldata2.accname = acname
                seldata2.address = subname
                seldata2.phoneno = grpname
                seldata2.save()
                return HttpResponseRedirect('/SchApp/account/receivables/')
            else:
                return HttpResponseRedirect('/SchApp/account/receivables/')
        else:
            try:
              getdetails = receivables.objects.get(acccode = acccode)
              return render_to_response('setup/editdebtors.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                varerr = "Debtor Does Not Exist"
                getdetails = receivables.objects.get(acccode = acccode)
                return render_to_response('setup/editdebtors.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})

    else:
       return HttpResponseRedirect('/login/')

def creditors(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.payables
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = creditorsform(request.POST) # A form bound to the POST data
          if form.is_valid():
             accname = form.cleaned_data['accname']
             address1 = form.cleaned_data['address']
             phoneno1 = form.cleaned_data['phoneno']
             accnameupp = accname.upper()
             accnameupp = accnameupp.replace(' ', '-')
             su = tblsubgroup.objects.get(subgroupname = "PAYABLES",groupname ="CURRENT LIABILITIES")
             try:
                 varvali = tblaccount.objects.get(accname__iexact = accnameupp,subgroupname__iexact = "PAYABLES",groupname__iexact ="CURRENT LIABILITIES")
                 varerr ="Creditors Name In Existence"
                 getdetails = ""
                 return render_to_response('setup/creditorsetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

             except:

                 vcount = tblaccount.objects.filter(subgroupname = "PAYABLES",groupname ="CURRENT LIABILITIES" ).exclude(accname = "TRADE-CREDITORS").count()
                 vcount = vcount + 1
                 #print vcount
                 varaccno = "2" + str(vcount)
                 #print varaccno
                 used = tblaccount(groupname = su.groupname,groupcode = su.groupcode,subgroupname = su.subgroupname,subgroupcode=su.subgroupcode,datecreated = datetime.datetime.today(),userid =varuser,accname = accnameupp,acccode = varaccno,accbal= 0,accstatus ="ACTIVE",recreport ="NO" )
                 used.save()
                 used1 = payables(accname = accnameupp,acccode = varaccno,address = address1,phoneno=phoneno1,userid = varuser )
                 used1.save()
                 #*****************************
                 getdetails = tblaccount.objects.filter(groupname ="CURRENT LIABILITIES",subgroupname = "PAYABLES").exclude(accname = "TRADE-CREDITORS").order_by('acccode')
                 #now i do insertion
                 return HttpResponseRedirect('/SchApp/account/payables/')
                 #return render_to_response('setup/creditorsetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = creditorsform()
            getdetails = payables.objects.all().order_by('acccode')
            #getdetails = tblaccount.objects.filter(groupname ="CURRENT LIABILITIES",subgroupname = "PAYABLES").exclude(accname = "TRADE-CREDITORS").order_by('acccode')
        return render_to_response('setup/creditorsetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

    else:
       return HttpResponseRedirect('/login/')

def getcreditor(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails =  payables.objects.get(id = acccode)
                return render_to_response('setup/editcreditor.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')
def editcreditors(request,acccode):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.payables
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/unauto/')
        varerr =""
        if request.method == 'POST':
            getdetails = ""
            acname = request.POST['accname']
            accno = request.POST['hcode']
            subname = request.POST['subname']
            #print subname
            grpname = request.POST['grpname']
            acname = acname.replace(' ', '-')
            acname = acname.upper()
            telen =  len(acname)
            telen1 =  len(subname)
            telen2 =  len(grpname)
            if telen == 0 :
                return HttpResponseRedirect('/SchApp/account/payables/')

            if  payables.objects.filter(accname = acname.upper(),address = subname,phoneno = grpname).exclude(acccode = accno).count() == 0:
                #update the request  replace(' ', '-')
                seldata = tblaccount.objects.get(acccode = accno)
                seldata.accname = acname
                seldata.save()
                seldata1 = tbltransaction.objects.filter(acccode = accno).update(accname = acname)
                seldata2 = payables.objects.get(acccode = accno)
                seldata2.accname = acname
                seldata2.address = subname
                seldata2.phoneno = grpname
                seldata2.save()#payables update
                # print acname,accno
                return HttpResponseRedirect('/SchApp/account/payables/')
            else:
                return HttpResponseRedirect('/SchApp/account/payables/')
        else:
            try:
              getdetails = payables.objects.get(acccode = acccode)
              return render_to_response('setup/editcreditor.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                varerr = "Creditor Does Not Exist"
                getdetails = payables.objects.get(acccode = acccode)
                return render_to_response('setup/editcreditor.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})

    else:
       return HttpResponseRedirect('/login/')


def ministorecode(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = ministoreform(request.POST) # A form bound to the POST data
          if form.is_valid():
             #subgrname = form.cleaned_data['subgrname']
             accname = form.cleaned_data['accname']
             accnameupp = accname.upper()
             accnameupp = accnameupp.replace(' ', '-')
             try:
                 varvali = tblstock.objects.get(stockname__iexact = accnameupp,subname__iexact = "MINI-STORE-BALANCE")
                 varerr ="Name In Existence"
                 getdetails = ""
                 return render_to_response('setup/minstoresetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             except:
                 varsubcode = tblaccount.objects.get(accname__iexact = "MINI-STORE-BALANCE")
                 vgsubcode = varsubcode.acccode
                 #print vgcode count
                 vcount = tblstock.objects.filter(subname = "MINI-STORE-BALANCE").count()
                 vcount = vcount + 1
                 srealsubcode = '3' + str(vcount)
                 #print srealsubcode
                 used = tblstock(stockname = accnameupp,acccode = srealsubcode,accbal = 0,datecreated = datetime.datetime.today(),userid =varuser,subname = "MINI-STORE-BALANCE",subcode = vgsubcode,qtybal = 0,avgprice = 0)
                 used.save()
#                 ****************** my addition***********************
#                 used1 = tblaccount(accname='', acccode = srealsubcode,accbal=0,groupname= 'CURRENT ASSETS',groupcode=30000,datecreated=datetime.datetime.today(),subgroupname=,subgroupcode,userid,accstatus='ACTIVE',recreport='YES',lasttrandate='')
#                 used1.save()

                 #*****************************
                 getdetails = tblstock.objects.filter(subname = "MINI-STORE-BALANCE").order_by('acccode')
                 #now i do insertion
                 return render_to_response('setup/minstoresetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = ministoreform()
            getdetails = tblstock.objects.filter(subname = "MINI-STORE-BALANCE").order_by('acccode')
        return render_to_response('setup/minstoresetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

    else:
       return HttpResponseRedirect('/login/')

def getministore(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails =  tblstock.objects.get(acccode = acccode)
                return render_to_response('setup/editministore.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')
def editministore(request,acccode):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createacc
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/unauto/')
        varerr =""
        if request.method == 'POST':
            getdetails = ""
            acname = request.POST['accname']
            accno = request.POST['hcode']
            grpname = request.POST['hgrpname']
            acname = acname.replace(' ', '-')
            acname = acname.upper()
            telen =  len(acname)
            if telen == 0:
                 varerr ="Invalid Name"
                 getdetails = tblstock.objects.get(acccode = accno)#.order_by('acccode')#tblaccount_acccode
                 return render_to_response('setup/editministore.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            if tblstock.objects.filter(stockname__iexact = acname.upper(),subname__iexact = grpname ).exclude(acccode = acccode).count()==0:
                seldata = tblstock.objects.get(acccode = accno)
                seldata.stockname = acname
                seldata.save()
                selsubdata = tblstocktransaction.objects.filter(acccode = accno).update(stockname =acname )
                return HttpResponseRedirect('/SchApp/account/ministore/')
            else:
                varerr ="Sub Name In Existence"
                getdetails = tblstock.objects.get(acccode = acccode)
                return render_to_response('setup/editministore.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
        else:
            try:
              getdetails = tblstock.objects.get(acccode = acccode)#.order_by('acccode')#tblaccount_acccode
              return render_to_response('setup/editministore.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                varerr = "Account Not Exist"
                return render_to_response('setup/editministore.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})

    else:
       return HttpResponseRedirect('/login/')


def accajaxcode(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   gdata = tblsubgroup.objects.filter(groupname = acccode).exclude(subgroupname = "RECEIVABLES").exclude(subgroupname = "PAYABLES").exclude(subgroupname = "MINI STORE").order_by('groupcode')#exclude(subgroupname = "STOCKS").
                   return render_to_response('setup/getdata.htm',{'gdata':gdata,'post':post})
             else:
                   gdata = tblsubgroup.objects.all()
                   #gdata = ""
                   return render_to_response('setup/getdata.htm',{'gdata':gdata})
         else:
              gdata = tblsubgroup.objects.all()
              #gdata = ""
              return render_to_response('setup/getdata.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def rentersetupcode(request):#unauto
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.esetup
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/welcome/')
        varerr =""
        return render_to_response('setup/renter.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')

def unauto(request):
     if  "userid" in request.session:
        varuser = request.session['userid']

        varerr =""
        return render_to_response('setup/unautorise.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')

def debtorssch(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.receivables
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
            form = studentaccform(request.POST) # A form bound to the POST data
            if form.is_valid():
                accname = form.cleaned_data['accname']
                accnameupp = accname.upper()
                varaccno1 = form.cleaned_data['accno']
                #phoneno1 = form.cleaned_data['phoneno']
                #accnameupp = accnameupp.replace(' ', '-')
                varaccno = varaccno1.upper()
                try:
                    varvali = tblaccount.objects.get(acccode__iexact = varaccno,subgroupname__iexact = "RECEIVABLES",groupname__iexact ="CURRENT ASSETS")
                    varerr ="Student Account In Existence"
                    getdetails = ""
                    return render_to_response('setup/stdentacc.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                except:
                    #vcount = tblaccount.objects.filter(subgroupname = "RECEIVABLES",groupname ="CURRENT ASSETS" ).exclude(accname = "TRADE-DEBTORS").count()
                    #vcount = vcount + 1
                    #print vcount
                    #varaccno = "%.6d" %vcount
                    #print varaccno
                    used = tblaccount(groupname = "CURRENT ASSETS",groupcode = "30000",subgroupname = "RECEIVABLES",subgroupcode="30200",datecreated = datetime.datetime.today(),userid =varuser,accname = accnameupp,acccode = varaccno,accbal= 0,accstatus ="ACTIVE",recreport ="NO" )
                    used.save()
                    used1 = receivables(accname = accnameupp,acccode = varaccno,address = 'Nil',phoneno='Nil',userid = varuser )
                    used1.save()
                    #*****************************
                    getdetails = tblaccount.objects.filter(groupname ="CURRENT ASSETS",subgroupname = "RECEIVABLES").exclude(accname = "TRADE-DEBTORS").order_by('acccode')
                    #now i do insertion
                    return render_to_response('setup/stdentacc.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = studentaccform()
            getdetails = tblaccount.objects.filter(groupname ="CURRENT ASSETS",subgroupname = "RECEIVABLES").exclude(accname = "TRADE-DEBTORS").order_by('acccode')
        return render_to_response('setup/stdentacc.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')

def editdebtorssch(request,acccode):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.receivables
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/unauto/')
        varerr =""
        if request.method == 'POST':
            accstatus = request.POST['status']
            data = tblaccount.objects.get(id = acccode)
            data.accstatus = accstatus
            data.save()
            return HttpResponseRedirect('/SchApp/account/receivables/')
        else:
            try:
                getdetails = tblaccount.objects.get(id = acccode)
                return render_to_response('setup/editstuacc.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                varerr = "Debtor Does Not Exist"
                getdetails = tblaccount.objects.get(id = acccode)
                return render_to_response('setup/editstuacc.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
    else:
        return HttpResponseRedirect('/login/')
def staffonloancode(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.receivables
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
            form = debtorsform(request.POST) # A form bound to the POST data
            if form.is_valid():
                accname = form.cleaned_data['accname']
                accnameupp = accname.upper()
                address1 = form.cleaned_data['address']
                phoneno1 = form.cleaned_data['phoneno']
                accnameupp = accnameupp.replace(' ', '-')
                try:
                    varvali = tblaccount.objects.get(accname__iexact = accnameupp,subgroupname__iexact = "RECEIVABLES",groupname__iexact ="CURRENT ASSETS",accname = "STAFF-DEBTORS")
                    varerr ="Staff Name In Existence"
                    getdetails = staffonloan.objects.filter().order_by('id')
                    return render_to_response('setup/staffonloan.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                except:
                    vcount = tblaccount.objects.filter(subgroupname = "STAFF-DEBTORS",groupname ="CURRENT ASSETS" ).exclude(accname = "STAFF-DEBTORS").count()
                    vcount = vcount + 1
                    #print vcount
                    varaccno = "4" + str(vcount)
                    #print varaccno
                    used = tblaccount(groupname = "CURRENT ASSETS",groupcode = "30000",subgroupname = "STAFF-DEBTORS",subgroupcode="30600",datecreated = datetime.datetime.today(),userid =varuser,accname = accnameupp,acccode = varaccno,accbal= 0,accstatus ="ACTIVE",recreport ="NO" )
                    used.save()
                    used1 = staffonloan(accname = accnameupp,acccode = varaccno,address = address1,phoneno=phoneno1,userid = varuser)
                    used1.save()
                    #*****************************
                    getdetails = staffonloan.objects.filter().order_by('accname')
                    return HttpResponseRedirect('/SchApp/account/staffonloan/')
                    #getdetails = tblaccount.objects.filter(groupname ="CURRENT ASSETS",subgroupname = "RECEIVABLES").exclude(accname = "TRADE-DEBTORS").order_by('acccode')
                    #now i do insertion
                    # return render_to_response('setup/debtorssetup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
        else:
            form = debtorsform()
            getdetails =  staffonloan.objects.filter().order_by('id')
            #getdetails = tblaccount.objects.filter(groupname ="CURRENT ASSETS",subgroupname = "RECEIVABLES").exclude(accname = "TRADE-DEBTORS").order_by('acccode')
        return render_to_response('setup/staffonloan.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')

def getstaffonloan(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails =  staffonloan.objects.get(id = acccode)
                # print getdetails
                return render_to_response('setup/editstaffonloan.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def editstaffonloan(request,acccode):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.receivables
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/unauto/')
        varerr =""
        if request.method == 'POST':
            getdetails = ""
            acname = request.POST['accname']
            accno = request.POST['hcode']
            subname = request.POST['subname']
            grpname = request.POST['grpname']
            acname = acname.replace(' ', '-')
            acname = acname.upper()
            telen1 =  len(subname)
            telen2 =  len(grpname)

            telen =  len(acname)
            if telen == 0 :
                return HttpResponseRedirect('/SchApp/account/staffonloan/')
            if staffonloan.objects.filter(accname = acname.upper(),address = subname,phoneno = grpname ).exclude(acccode = accno).count()== 0:
                #update the request  replace
                seldata = tblaccount.objects.get(acccode = accno)
                seldata.accname = acname
                seldata.save()
                seldata1 = tbltransaction.objects.filter(acccode = accno).update(accname = acname)
                seldata2 = staffonloan.objects.get(acccode = accno)
                seldata2.accname = acname
                seldata2.address = subname
                seldata2.phoneno = grpname
                seldata2.save()
                return HttpResponseRedirect('/SchApp/account/staffonloan/')
            else:
                return HttpResponseRedirect('/SchApp/account/staffonloan/')
        else:
            try:
                getdetails = staffonloan.objects.get(acccode = acccode)
                return render_to_response('setup/editstaffonloan.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            except:
                varerr = "Staff Does Not Exist"
                getdetails = staffonloan.objects.get(acccode = acccode)
                return render_to_response('setup/editstaffonloan.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})

    else:
        return HttpResponseRedirect('/login/')

def receivablesstatus(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.receivables
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/unauto/')
        varerr =""
        getdetails =""
        getdata = tblaccount.objects.filter(subgroupname = "RECEIVABLES",groupname ="CURRENT ASSETS").order_by('accname')
        return render_to_response('setup/stdentacc.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdata},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')



