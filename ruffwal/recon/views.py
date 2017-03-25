from django.template import loader, Context,RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import  HttpResponseRedirect
from myproject.ruffwal.recon.form import *
from myproject.ruffwal.recon.models import *
from myproject.ruffwal.posting.models import *
from myproject.ruffwal.rwadmin.models import *
from myproject.ruffwal.rsetup.models import *
from myproject.ruffwal.posting.models import *
from myproject.ruffwal.rwreport.reports import *
from django.db.models import Max,Sum
from django.contrib.sessions.models import Session
import datetime
from datetime import date,time
import xlwt
from django.core.serializers.json import simplejson as json
import locale
locale.setlocale(locale.LC_ALL,'')

def reconunauto(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        return render_to_response('recon/unautorise.htm',{'varuser':varuser,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def reconstatement(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/recon/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = reconstatementform(request.POST) # A form bound to the POST data
          if form.is_valid():
             caldate1 = form.cleaned_data['transdate']
             #year = form.cleaned_data['year']
             bankname = form.cleaned_data['bankname']
             caldate2 = caldate1.split('/')
             transdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
             reconlist = []
             #********************************************************************
             opbal = 0
             debit = 0
             credit = 0
             getacc = tblaccount.objects.get(accname = bankname,groupname ="CURRENT ASSETS",subgroupname = "CASH-AND-BANK-BALANCES")
             groupname = getacc.groupname
             acccode = getacc.acccode
             if tbltransaction.objects.filter(acccode = acccode,transdate__lt = transdate).count() == 0:
                opbal = 0
             else:
                getdata = tbltransaction.objects.filter(acccode = acccode,transdate__lt = transdate).aggregate(Sum('debit'),Sum('credit'))
                debit = getdata['debit__sum']
                credit = getdata['credit__sum']
             if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS" or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                 opbal = debit - credit
             else:
                 opbal = credit - debit
             fbal = locale.format("%.2f",opbal,grouping=True)
             j = {'name':"Balance as per CashBook",'amount':fbal,'dispgr':bankname,'transdate':transdate}
             reconlist.append(j)
             #*************************************************
             if upresentedtrans.objects.filter(transdate__lte = transdate,acccode = acccode).count() == 0:
                 tottran1 = 0
             else:
                 varrid11 = upresentedtrans.objects.filter(transdate__lte = transdate,acccode = acccode).aggregate(Sum('debit'),Sum('credit'))
                 debit = varrid11['debit__sum']
                 credit = varrid11['credit__sum']
                 tottran1 = debit - credit
             fbal1 = locale.format("%.2f",tottran1,grouping=True)
             j = {'name':"Add Unpresented Cheques",'amount':fbal1,'dispgr':bankname,'transdate':transdate}
             reconlist.append(j)
             #****************************
             gtt = opbal + tottran1
             rrt = locale.format("%.2f",gtt,grouping=True)
             j = {'name':"",'amount':rrt,'dispgr':bankname,'transdate':transdate}
             reconlist.append(j)
             #*************************************************
             if uncreditedtrans.objects.filter(transdate__lte = transdate,acccode = acccode).count() == 0:
                 tottran12 = 0
             else:
                 varrid11 = uncreditedtrans.objects.filter(transdate__lte = transdate,acccode = acccode).aggregate(Sum('debit'),Sum('credit'))
                 debit = varrid11['debit__sum']
                 credit = varrid11['credit__sum']
                 tottran12 = debit - credit
             fbal12 = locale.format("%.2f",tottran12,grouping=True)
             j = {'name':"Less Uncredited Lodgements",'amount':fbal12,'dispgr':bankname,'transdate':transdate}
             reconlist.append(j)
             #****************************
             fbb = gtt - tottran12
             ff = locale.format("%.2f",fbb,grouping=True)
             j = {'name':"Balance as per Bank Statement",'amount':ff,'dispgr':bankname,'transdate':transdate}
             reconlist.append(j)
             hhead = bankname
             kk = transdate.strftime('%b,%Y')
             comp = tblcompanyinfo.objects.get(id = 1)
             if form.cleaned_data['excelfile']:
                 response = HttpResponse(mimetype="application/ms-excel")
                 response['Content-Disposition'] = 'attachment; filename=bankreconciliation.xls'
                 wb = xlwt.Workbook()
                 ws = wb.add_sheet('reconciliation')
                 ws.write(0, 1, comp.name)
                 ws.write(1, 1, comp.address)
                 ws.write(2, 1, hhead)
                 ws.write(2, 2, kk)
                 k = 3
                 for jd in reconlist:
                     ws.write(k, 2, jd.name)
                     ws.write(k, 3, jd.amount)
                     k += 1
                 wb.save(response)
                 return response
             else:
                 return render_to_response('recon/statement.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':reconlist,'hhead':hhead,'kk':kk,'comp':comp},context_instance = RequestContext(request))
        else:

            form = reconstatementform()
            getdetails = ""
        return render_to_response('recon/statement.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')

def unpresented(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/recon/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = unpresentedform(request.POST) # A form bound to the POST data
          if form.is_valid():

             acccode = form.cleaned_data['acccode']
             accname = form.cleaned_data['accname'] #customer code
             accbal = form.cleaned_data['accbal']
             transamount = form.cleaned_data['transamount']
             caldate1 = form.cleaned_data['transdate']
             particulars = form.cleaned_data['particulars']
             refno = form.cleaned_data['refno']
             caldate2 = caldate1.split('/')
             transdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
             #***************************************************
             if tblcalender.objects.all().count() == 0:
                 varerr = "NO START DATE"
                 getdetails = upresentedtranstemp.objects.all()
                 return render_to_response('recon/unpresented.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

             getdate = tblcalender.objects.all()
             for g in getdate:
                 stdate = g.startmonth
                 endate = g.endtmonth
             if transdate < stdate or transdate > endate :
                 varerr = "INVALID DATE"
                 getdetails = upresentedtranstemp.objects.all()
                 return render_to_response('recon/unpresented.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             varget = upresentedtrans.objects.filter(acccode = acccode).count()
             if varget == 0 :
                used = upresentedtrans(accname = accname,acccode = acccode,debit = transamount,credit = 0,balance = transamount,transdate = transdate,particulars = particulars,userid = varuser,refno = refno, opeaningbal = "OPENING BAL : 0")
                used.save()
                used1 = upresentedtranstemp(accname = accname,acccode = acccode,amount = transamount,particulars = particulars,userid = varuser,refno = refno,transdate = transdate, )
                used1.save()
                return HttpResponseRedirect('/SchApp/account/recon/unpresented/')
             else:
                    vargetnew = upresentedtrans.objects.filter(refno = refno,acccode = acccode).count()
                    if vargetnew == 0:
                        varrid1 = upresentedtrans.objects.filter(acccode = acccode).aggregate(Max('id'))
                        varrid = varrid1['id__max']

                        getda = upresentedtrans.objects.get(id = varrid)
                        currbal1 = getda.balance
                        currbal = currbal1 + transamount

                        varopen = "OPENING BAL : " + locale.format("%.2f",currbal1,grouping=True)
                        used = upresentedtrans(accname = accname,acccode = acccode,debit = transamount,credit = 0,balance = currbal,transdate = transdate,particulars = particulars,userid = varuser,refno = refno,opeaningbal = varopen )
                        used.save()
                        used1 = upresentedtranstemp(accname = accname,acccode = acccode,amount = transamount,particulars = particulars,userid = varuser,refno = refno,transdate = transdate, )
                        used1.save()
                        #************************balance the account
                        vcbal = 0
                        varbalacc = upresentedtrans.objects.filter(acccode = acccode).order_by('transdate','id')
                        for j in varbalacc:
                            debit = j.debit
                            #print debit
                            credit = j.credit
                            vid = j.id
                            vopbal = "OPENING BAL : " + locale.format("%.2f",vcbal,grouping=True)
                            vcbal = vcbal + debit - credit
                            # print vcbal, vid
                            getdau = upresentedtrans.objects.get(id = vid)
                            getdau.balance = vcbal
                            getdau.opeaningbal = vopbal
                            getdau.save()
                        return HttpResponseRedirect('/SchApp/account/recon/unpresented/')
                    else:
                        varerr = "INVALID CHEQUE NO"
                        getdetails = ""
                        return render_to_response('recon/unpresented.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

          else:
              varerr = "INVALID FORM ENTRY"
              getdetails = upresentedtranstemp.objects.all()
              return render_to_response('recon/unpresented.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

        else:

            form = unpresentedform()
            getdetails = upresentedtranstemp.objects.all()
        return render_to_response('recon/unpresented.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')

def recontestajax(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   #gdata = tblaccount.objects.all()
                   gdata = tblaccount.objects.filter(acccode__startswith = acccode,groupname = "CURRENT ASSETS",subgroupname ="CASH-AND-BANK-BALANCES").order_by('acccode')

                   return render_to_response('recon/testajax.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = ""
                   return render_to_response('recon/testajax.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('recon/testajax.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def recontestajaxall(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   #gdata = tblaccount.objects.all()
                   gdata = upresentedtranstemp.objects.filter(acccode = acccode).order_by('id')

                   return render_to_response('recon/testajax1.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = ""
                   return render_to_response('recon/testajax1.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('recon/testajax1.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def editunpresented(request,invid):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            getdetails = upresentedtranstemp.objects.get(id = invid)
            if request.method == 'POST':
                getdetails = ""
                accno = request.POST['hcode']#the primary key
                acccode =  request.POST['acccode']
                accname =  request.POST['accname']
                amount =  request.POST['amount']
                part =  request.POST['part']
                refno =  request.POST['refno']
                pdate =  request.POST['pdate']
                #getdetails = tblwiptemp.objects.get(id = invid).delete()
                vyear = str(pdate)
                if vyear == "":
                   varerr = "All Fields are required"
                   getdetails = upresentedtranstemp.objects.get(id = invid)
                   return render_to_response('recon/editunpresented.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})

                vk = vyear[0:4]
                if vk.isdigit() == True :
                    #print 'digit value'
                    vdate = date(int(vyear[0:4]),int(vyear[5:7]),int(vyear[8:10]))
                else:
                    #print 'not digit'
                    vdate = date(int(vyear[6:10]),int(vyear[0:2]),int(vyear[3:5]))
                #*******************************************************************************
                 #***************************************************
                if tblcalender.objects.all().count() == 0:
                   varerr = "NO START DATE"
                   getdetails = upresentedtranstemp.objects.get(id = invid)
                   return render_to_response('recon/editunpresented.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})

                getdate = tblcalender.objects.all()
                for g in getdate:
                    stdate = g.startmonth
                    endate = g.endtmonth
                if vdate < stdate or vdate > endate :
                    varerr = "INVALID DATE"
                    getdetails = upresentedtranstemp.objects.get(id = invid)
                    return render_to_response('recon/editunpresented.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})

                getdetails = upresentedtranstemp.objects.get(id = invid)
                tdate = getdetails.transdate
                if vdate < tdate :
                    return HttpResponseRedirect('/SchApp/account/recon/unpresented/')

                #*******************
                varrid1 = upresentedtrans.objects.filter(acccode = acccode).aggregate(Max('id'))
                varrid = varrid1['id__max']
                k = float(amount)
                #print k *2

                getda = upresentedtrans.objects.get(id = varrid)
                currbal = getda.balance
                currbal = currbal #- amount
                h =  float(currbal)
                gf =  h - k
                #print gf
                kk = str(gf)
                used = upresentedtrans(accname = accname,acccode = acccode,debit = 0,credit = amount,balance = kk,transdate = vdate,particulars = part,userid = varuser,refno = refno )
                used.save()
                upresentedtranstemp.objects.get(id = accno).delete()
                return HttpResponseRedirect('/SchApp/account/recon/unpresented/')

            else:
                try:
                  getdetails = upresentedtranstemp.objects.get(id = invid)
                  return render_to_response('recon/editunpresented.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                except:
                    varerr = "Account Not Exist"
                    return render_to_response('recon/editunpresented.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
        else:
         return HttpResponseRedirect('/login/')

def uncredited(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.unpresented
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/recon/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          form = unpresentedform(request.POST) # A form bound to the POST data
          if form.is_valid():

             acccode = form.cleaned_data['acccode']
             accname = form.cleaned_data['accname'] #customer code
             accbal = form.cleaned_data['accbal']
             transamount = form.cleaned_data['transamount']
             caldate1 = form.cleaned_data['transdate']
             particulars = form.cleaned_data['particulars']
             refno = form.cleaned_data['refno']
             caldate2 = caldate1.split('/')
             transdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
              #***************************************************
             if tblcalender.objects.all().count() == 0:
                 varerr = "NO START DATE"
                 getdetails = upcreditedtranstemp.objects.all()
                 return render_to_response('recon/uncredited.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

             getdate = tblcalender.objects.all()
             for g in getdate:
                 stdate = g.startmonth
                 endate = g.endtmonth
             if transdate < stdate or transdate > endate :
                 varerr = "INVALID DATE"
                 getdetails = upcreditedtranstemp.objects.all()
                 return render_to_response('recon/uncredited.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

             varget = uncreditedtrans.objects.filter(acccode = acccode).count()
             if varget == 0 :
                used = uncreditedtrans(accname = accname,acccode = acccode,debit = transamount,credit = 0,balance = transamount,transdate = transdate,particulars = particulars,userid = varuser,refno = refno, opeaningbal = "OPENING BAL : 0" )
                used.save()
                used1 = upcreditedtranstemp(accname = accname,acccode = acccode,amount = transamount,particulars = particulars,userid = varuser,refno = refno,transdate = transdate, )
                used1.save()
                return HttpResponseRedirect('/SchApp/account/recon/uncredited/')
             else:
                    vargetnew = uncreditedtrans.objects.filter(refno = refno,acccode = acccode).count()
                    if vargetnew == 0:
                        varrid1 = uncreditedtrans.objects.filter(acccode = acccode).aggregate(Max('id'))
                        varrid = varrid1['id__max']
                        getda = uncreditedtrans.objects.get(id = varrid)
                        currbal1 = getda.balance
                        varopen = "OPENING BAL : " + str(currbal1)
                        currbal = currbal1 + transamount
                        used = uncreditedtrans(accname = accname,acccode = acccode,debit = transamount,credit = 0,balance = currbal,transdate = transdate,particulars = particulars,userid = varuser,refno = refno,opeaningbal = varopen )
                        used.save()
                        used1 = upcreditedtranstemp(accname = accname,acccode = acccode,amount = transamount,particulars = particulars,userid = varuser,refno = refno,transdate = transdate, )
                        used1.save()
                        vcbal = 0
                        varbalacc = uncreditedtrans.objects.filter(acccode = acccode).order_by('transdate','id')
                        for j in varbalacc:
                            debit = j.debit
                            #print debit
                            credit = j.credit
                            vid = j.id
                            vopbal = "OPENING BAL : " + str(vcbal)
                            vcbal = vcbal + debit - credit
                            #print vcbal, vid
                            getdau = uncreditedtrans.objects.get(id = vid)
                            getdau.balance = vcbal
                            getdau.opeaningbal = vopbal
                            getdau.save()
                        return HttpResponseRedirect('/SchApp/account/recon/uncredited/')
                    else:
                        varerr = "INVALID CHEQUE NO"
                        getdetails = ""
                        return render_to_response('recon/uncredited.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

          else:
              varerr = "INVALID FORM ENTRY"
              getdetails = upcreditedtranstemp.objects.all()
              return render_to_response('recon/uncredited.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

        else:

            form = unpresentedform()
            getdetails = upcreditedtranstemp.objects.all()
        return render_to_response('recon/uncredited.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')

def ajaxalluncr(request):
     if  "userid" in request.session:
         if request.is_ajax():
             if request.method == 'POST':
                   varuser = request.session['userid']
                   varerr =""
                   post = request.POST.copy()
                   acccode = post['userid']
                   #print acccode
                   #gdata = tblaccount.objects.all()
                   gdata = upcreditedtranstemp.objects.filter(acccode = acccode).order_by('id')

                   return render_to_response('recon/testajax2.htm',{'gdata':gdata,'post':post})
             else:
                   #gdata = tblaccount.objects.all()
                   gdata = ""
                   return render_to_response('recon/testajax2.htm',{'gdata':gdata})
         else:
              #gdata = tblaccount.objects.all()
              gdata = ""
              return render_to_response('recon/testajax2.htm',{'gdata':gdata})

     else:
       return HttpResponseRedirect('/login/')

def edituncredited(request,invid):
        varerr =""
        if  "userid" in request.session:
            varuser = request.session['userid']
            varerr =""
            getdetails = upcreditedtranstemp.objects.get(id = invid)
            if request.method == 'POST':
                getdetails = ""
                accno = request.POST['hcode']#the primary key
                acccode =  request.POST['acccode']
                accname =  request.POST['accname']
                amount =  request.POST['amount']
                part =  request.POST['part']
                refno =  request.POST['refno']
                pdate =  request.POST['pdate']
                #getdetails = tblwiptemp.objects.get(id = invid).delete()
                vyear = str(pdate)
                if vyear == "" :
                   varerr = "All Fields Are Required"
                   getdetails = upcreditedtranstemp.objects.get(id = invid)
                   return render_to_response('recon/edituncredited.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})

                vk = vyear[0:4]
                if vk.isdigit() == True :
                    #print 'digit value'
                    vdate = date(int(vyear[0:4]),int(vyear[5:7]),int(vyear[8:10]))
                else:
                    #print 'not digit'
                    vdate = date(int(vyear[6:10]),int(vyear[0:2]),int(vyear[3:5]))
                #*******************************************************************************
                stdate = ''
                endate =''
                #***************************************************
                if tblcalender.objects.all().count() == 0:
                   varerr = "NO START DATE"
                   getdetails = upcreditedtranstemp.objects.get(id = invid)
                   return render_to_response('recon/edituncredited.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                getdate = tblcalender.objects.all()
                for g in getdate:
                   stdate = g.startmonth
                   endate = g.endtmonth
                if vdate < stdate or vdate > endate :
                    varerr = "INVALID DATE"
                    getdetails = upcreditedtranstemp.objects.get(id = invid)
                    return render_to_response('recon/edituncredited.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                varrid1 = uncreditedtrans.objects.filter(acccode = acccode).aggregate(Max('id'))
                varrid = varrid1['id__max']
                k = float(amount)
                getdetails = upcreditedtranstemp.objects.get(id = invid)
                tdate = getdetails.transdate
                if vdate < tdate :
                    return HttpResponseRedirect('/SchApp/account/recon/uncredited/')
                getda = uncreditedtrans.objects.get(id = varrid)
                currbal = getda.balance
                currbal = currbal #- amount
                h =  float(currbal)
                gf =  h - k
                #print gf
                kk = str(gf)
                used = uncreditedtrans(accname = accname,acccode = acccode,debit = 0,credit = amount,balance = kk,transdate = vdate,particulars = part,userid = varuser,refno = refno )
                used.save()
                upcreditedtranstemp.objects.get(id = accno).delete()
                return HttpResponseRedirect('/SchApp/account/recon/uncredited/')
            else:
                try:
                  getdetails = upcreditedtranstemp.objects.get(id = invid)
                  return render_to_response('recon/edituncredited.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
                except:
                    varerr = "Account Not Exist"
                    return render_to_response('recon/edituncredited.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
        else:
         return HttpResponseRedirect('/login/')

def unpresentedsta(request):
    if  "userid" in request.session:
          varuser = request.session['userid']
          user = tbluseracc.objects.get(username = varuser)
          uenter = user.unpresented
          if int(uenter) == 0 :
             return HttpResponseRedirect('/SchApp/account/recon/unauto/')
          varerr =""
          getdetails = ""
          if request.method == 'POST':
                form = daterangeform(request.POST) # A form bound to the POST data
                if form.is_valid():
                     acccode = form.cleaned_data['acccode']
                     caldate1 = form.cleaned_data['startdate']
                     caldate11 = form.cleaned_data['enddate']
                     caldate2 = caldate1.split('/')
                     stratdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                     caldate22 = caldate11.split('/')
                     enddate = date(int(caldate22[2]),int(caldate22[0]),int(caldate22[1]))
                     ll = []
                     dacc = {}
                     vobal =''
                     if enddate >= stratdate:
                         comp = tblcompanyinfo.objects.get(id = 1)
                         if acccode == '':
                            varacc = tblaccount.objects.filter(groupname = "CURRENT ASSETS",subgroupname = "CASH-AND-BANK-BALANCES").order_by('acccode')
                         else:
                            varacc = tblaccount.objects.filter(acccode = acccode)
                         for m in varacc:
                             dacc = {}
                             if upresentedtrans.objects.filter(transdate__range = (stratdate,enddate),acccode = m.acccode).count() == 0:
                                 pass
                             else:
                                 varop = upresentedtrans.objects.filter(transdate__range = (stratdate,enddate),acccode = m.acccode).order_by('acccode','transdate')[:1]
                                 for op in varop:
                                    vobal = op.opeaningbal
                                    #print vobal
                                 dacc = {'acccode':m.acccode,'accname':m.accname,'trans':upresentedtrans.objects.filter(transdate__range = (stratdate,enddate),acccode = m.acccode).order_by('acccode','transdate'),'opbal':vobal}
                                 ll.append(dacc)
                         if form.cleaned_data['excelfile']:
                            response = HttpResponse(mimetype="application/ms-excel")
                            response['Content-Disposition'] = 'attachment; filename=unpresentedstm.xls'
                            wb = xlwt.Workbook()
                            ws = wb.add_sheet('unpresented')
                            ws.write(0, 1, comp.name)
                            ws.write(1, 1, comp.address)
                            ws.write(2, 1, 'UNPRESENTED STATEMENT')
                            ws.write(2, 2, stratdate.strftime('%d-%m-%Y'))
                            ws.write(2, 3, enddate.strftime('%d-%m-%Y'))
                            ws.write(3, 0,'Transdate')
                            ws.write(3, 1, 'Particulars')
                            ws.write(3, 2,'Ref. No')
                            ws.write(3, 3, 'Debit')
                            ws.write(3, 4, 'Credit')
                            ws.write(3, 5, 'Balance')
                            k = 4
                            for jd in ll:
                                ws.write(k, 2, jd['acccode'])
                                ws.write(k, 3, jd['accname'])
                                ws.write(k, 4, jd['opbal'])
                                v = k + 1
                                for n in jd['trans']:
                                    ws.write(v, 0, n.transdate.strftime('%d-%m-%Y'))
                                    ws.write(v, 1, n.particulars)
                                    ws.write(v, 2, n.refno)
                                    ws.write(v, 3, n.debit)
                                    ws.write(v, 4, n.credit)
                                    ws.write(v, 5, n.balance)
                                    v += 1

                                k = v + 1
                            wb.save(response)
                            return response
                         else:
                            return render_to_response('recon/unpresentedrep.htm',{'varuser':varuser,'varerr':varerr,'form':form,'comp':comp,'ll':ll,'stratdate':stratdate,'enddate':enddate},context_instance = RequestContext(request))


                         #if upresentedtrans.objects.filter(transdate__range = (stratdate,enddate)).count() == 0:
                          #   varerr = "NO RECORD FOUND"
                           #  getdetails = ""
                            # return render_to_response('recon/notfound.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                         #else:
                          #   resp = HttpResponse(mimetype='application/pdf')
                           #  getdetails = upresentedtrans.objects.filter(transdate__range = (stratdate,enddate)).order_by('acccode','transdate')
                            # report = unpresentedreport(queryset=getdetails)
                            # report.generate_by(PDFGenerator, filename=resp)
                            # return resp
                else:
                     #varerr = "All Fields Are Required"
                     getdetails = ""
                return render_to_response('recon/unpresentedrep.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

          else:

                form = daterangeform()
                getdetails = ""
          return render_to_response('recon/unpresentedrep.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))


    else:
       return HttpResponseRedirect('/login/')

def uncreditedsta(request):
    if  "userid" in request.session:
          varuser = request.session['userid']
          user = tbluseracc.objects.get(username = varuser)
          uenter = user.unpresented
          if int(uenter) == 0 :
              return HttpResponseRedirect('/SchApp/account/recon/unauto/')
          varerr =""
          getdetails = ""
          if request.method == 'POST':
                form = daterangeform(request.POST) # A form bound to the POST data
                if form.is_valid():
                     acccode = form.cleaned_data['acccode']
                     caldate1 = form.cleaned_data['startdate']
                     caldate11 = form.cleaned_data['enddate']
                     caldate2 = caldate1.split('/')
                     stratdate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                     caldate22 = caldate11.split('/')
                     enddate = date(int(caldate22[2]),int(caldate22[0]),int(caldate22[1]))
                     ll = []
                     dacc = {}
                     vobal =''
                     if enddate >= stratdate:
                         comp = tblcompanyinfo.objects.get(id = 1)
                         if acccode == '':
                             varacc = tblaccount.objects.filter(groupname = "CURRENT ASSETS",subgroupname = "CASH-AND-BANK-BALANCES").order_by('acccode')
                         else:
                             varacc = tblaccount.objects.filter(acccode = acccode)
                         for m in varacc:
                             dacc = {}
                             if uncreditedtrans.objects.filter(transdate__range = (stratdate,enddate),acccode = m.acccode).count() == 0:
                                pass
                             else:
                                varop = uncreditedtrans.objects.filter(transdate__range = (stratdate,enddate),acccode = m.acccode).order_by('acccode','transdate')[:1]
                                for op in varop:
                                    vobal = op.opeaningbal
                                 #print vobal
                                dacc = {'acccode':m.acccode,'accname':m.accname,'trans':uncreditedtrans.objects.filter(transdate__range = (stratdate,enddate),acccode = m.acccode).order_by('acccode','transdate'),'opbal':vobal}
                                ll.append(dacc)
                         if form.cleaned_data['excelfile']:
                            response = HttpResponse(mimetype="application/ms-excel")
                            response['Content-Disposition'] = 'attachment; filename=uncreditedstm.xls'
                            wb = xlwt.Workbook()
                            ws = wb.add_sheet('uncredited')
                            ws.write(0, 1, comp.name)
                            ws.write(1, 1, comp.address)
                            ws.write(2, 1, 'UNCREDITED LODGEMENT')
                            ws.write(2, 2, stratdate.strftime('%d-%m-%Y'))
                            ws.write(2, 3, enddate.strftime('%d-%m-%Y'))
                            ws.write(3, 0,'Transdate')
                            ws.write(3, 1, 'Particulars')
                            ws.write(3, 2,'Ref. No')
                            ws.write(3, 3, 'Debit')
                            ws.write(3, 4, 'Credit')
                            ws.write(3, 5, 'Balance')
                            k = 4
                            for jd in ll:
                              ws.write(k, 2, jd['acccode'])
                              ws.write(k, 3, jd['accname'])
                              ws.write(k, 4, jd['opbal'])
                              v = k + 1
                              for n in jd['trans']:
                                 ws.write(v, 0, n.transdate.strftime('%d-%m-%Y'))
                                 ws.write(v, 1, n.particulars)
                                 ws.write(v, 2, n.refno)
                                 ws.write(v, 3, n.debit)
                                 ws.write(v, 4, n.credit)
                                 ws.write(v, 5, n.balance)
                                 v += 1
                              k = v + 1
                              wb.save(response)
                              return response
                         else:
                            #print ll
                            return render_to_response('recon/uncreditedsta.htm',{'varuser':varuser,'varerr':varerr,'form':form,'comp':comp,'ll':ll,'stratdate':stratdate,'enddate':enddate},context_instance = RequestContext(request))
                         #if uncreditedtrans.objects.filter(transdate__range = (stratdate,enddate)).count() == 0:
                          #   varerr = "NO RECORD FOUND"
                           #  getdetails = ""
                            # return render_to_response('recon/notfound.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                        # else:
                         #    resp = HttpResponse(mimetype='application/pdf')
                          #   getdetails = uncreditedtrans.objects.filter(transdate__range = (stratdate,enddate)).order_by('acccode','transdate')
                           #  report = uncreditedreport(queryset=getdetails)
                           #  report.generate_by(PDFGenerator, filename=resp)
                            # return resp
                else:
                    # varerr = "All Fields Are Required"
                     getdetails = ""
                return render_to_response('recon/uncreditedsta.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

          else:

                form = daterangeform()
                getdetails = ""
          return render_to_response('recon/uncreditedsta.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))


    else:
       return HttpResponseRedirect('/login/')

def enterrec(request):
     if  "userid" in request.session:

        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.ereonciliation
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/welcome/')
        varerr =""
        return render_to_response('recon/enterrecon.htm',{'varuser':varuser,'varerr':varerr})
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
def autocompleterecon(request):
    term = request.GET.get('term')
    gset = tblaccount.objects.filter(accname__contains = term,groupname = "CURRENT ASSETS",subgroupname = "CASH-AND-BANK-BALANCES").exclude(accname = "TRADE-DEBTORS").order_by('acccode')[:10]
    suggestions = []
    for i in gset:
        k = i.accbal
        disamt = locale.format("%.2f",k,grouping=True)
        suggestions.append({'label': '%s %s' % (i.accname,i.acccode), 'acccode': i.acccode,'accname': i.accname,'accbal':disamt})
    return suggestions


def getpresented(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = upresentedtranstemp.objects.get(id = acccode)
                return render_to_response('recon/editunpresented.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def getcredited(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = upcreditedtranstemp.objects.get(id = acccode)
                return render_to_response('recon/edituncredited.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')
