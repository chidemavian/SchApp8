# Create your views here.
from django.template import loader, Context,RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import  HttpResponseRedirect
from myproject.ruffwal.rwreport.opbal import *
from myproject.ruffwal.rwadmin.models import *
from myproject.ruffwal.posting.models import *
from myproject.ruffwal.newyear.models import *
from myproject.ruffwal.rwadmin.form import *
from myproject.ruffwal.rwreport.reports import *
from myproject.utilities.views import *
from django.contrib.sessions.models import Session
from myproject.ruffwal.rwadmin.capy import monthrange
from django.db.models import Max,Sum
import datetime
import datetime
from datetime import date,time
import xlwt

def enteradmin(request):#adminunauto
     if  "userid" in request.session:

        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.eadmin
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/welcome/')
        varerr =""
        return render_to_response('rwadmin/enteradmin.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')

def createuser(request):

     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createuser
        if int(uenter) == 0 :
           return HttpResponseRedirect('/SchApp/account/sysadmin/unauto/')
        varerr =""
        getdetails =""
        esetup = 0
        eposting  = 0
        einventory = 0
        ewip = 0
        ereonciliation = 0
        ereport = 0
        eadmin = 0
        varerr = ""
        createacc = 0
        inventory= 0
        payables=0
        receivables=0
        invoice=0
        receipt = 0
        payment = 0
        genledger = 0
        standardledger = 0
        stockin = 0
        stockout = 0
        stockreport = 0
        jobsetup = 0
        addsetup =0
        jobcosting = 0
        returnmat = 0
        wipinvoice = 0
        wipreport = 0
        unpresented = 0
        statutory = 0
        createuser = 0
        resetuser = 0
        userreport = 0
        rollover = 0
        if request.method == 'POST':
          form = userform(request.POST) # A form bound to the POST data
          if form.is_valid():
             username = form.cleaned_data['username']#username
             staffname = form.cleaned_data['staffname'] # staff name
             caldate1 = form.cleaned_data['expiredate'] #expiry date
             caldate2 = caldate1.split('/')
             expiredate = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
             uname = str(username)
             uname = uname.lower()
             uuname = uname.replace(' ','-')
             if form.cleaned_data['createacc'] or form.cleaned_data['inventory'] or form.cleaned_data['payables'] or form.cleaned_data['receivables']:
                 esetup = 1
             if form.cleaned_data['invoice'] or form.cleaned_data['receipt'] or form.cleaned_data['payment'] or form.cleaned_data['genledger'] or form.cleaned_data['standardledger']:
                 eposting = 1
             if form.cleaned_data['stockin'] or form.cleaned_data['stockout'] or form.cleaned_data['stockreport']:
                 einventory = 1
             if form.cleaned_data['jobsetup'] or form.cleaned_data['addsetup'] or form.cleaned_data['jobcosting'] or form.cleaned_data['returnmat'] or form.cleaned_data['wipinvoice'] or form.cleaned_data['wipreport']:
                 ewip = 1
             if form.cleaned_data['unpresented']:
                 ereonciliation = 1
             if form.cleaned_data['statutory']:
                 ereport = 1
             if form.cleaned_data['createuser'] or form.cleaned_data['resetuser'] or form.cleaned_data['userreport'] or form.cleaned_data['rollover']:
                 eadmin = 1
             #pull into the sub table
             if form.cleaned_data['createacc'] :
                 createacc = 1
             else:
                createacc = 0
             if form.cleaned_data['inventory']:
                 inventory = 1
             else:
                 inventory = 0
             if form.cleaned_data['payables']:
                 payables = 1
             else:
                 payables = 0
             if form.cleaned_data['receivables']:
                 receivables = 1
             else:
                 receivables = 0
             if form.cleaned_data['invoice']:
                  invoice = 1
             else:
                 invoice = 0
             if form.cleaned_data['receipt']:
                 receipt = 1
             else:
                 receipt = 0
             if form.cleaned_data['payment']:
                payment = 1
             else:
                 payment = 0
             if form.cleaned_data['genledger']:
                 genledger = 1
             else:
                 genledger = 0
             if form.cleaned_data['standardledger']:
                 standardledger = 1
             else:
                 standardledger = 0
             if form.cleaned_data['stockin']:
                 stockin = 1
             else:
                 stockin = 0
             if form.cleaned_data['stockout']:
                 stockout = 1
             else:
                 stockout = 0
             if form.cleaned_data['stockreport']:
                 stockreport = 1
             else:
                 stockreport = 0
             if form.cleaned_data['jobsetup']:
                 jobsetup = 1
             else:
                 jobsetup = 0

             if form.cleaned_data['addsetup']:
                 addsetup = 1
             else:
                 addsetup = 0

             if form.cleaned_data['jobcosting']:
                 jobcosting = 1
             else:
                 jobcosting = 0

             if form.cleaned_data['returnmat']:
                 returnmat = 1
             else:
                 returnmat = 0
             if form.cleaned_data['wipinvoice']:
                 wipinvoice = 1
             else:
                 wipinvoice = 0
             if form.cleaned_data['wipreport']:
                 wipreport = 1
             else:
                 wipreport = 0
             if form.cleaned_data['unpresented']:
                 unpresented = 1
             else:
                 unpresented = 0
             if form.cleaned_data['statutory']:
                 statutory = 1
             else:
                 statutory = 0
             if form.cleaned_data['createuser']:
                 createuser = 1
             else:
                 createuser = 0
             if form.cleaned_data['resetuser']:
                 resetuser = 1
             else:
                 resetuser = 0
             if form.cleaned_data['userreport']:
                 userreport = 1
             else:
                 userreport = 0
             if form.cleaned_data['rollover']:
                 rollover = 1
             else:
                 rollover = 0
             try:
                 varvali = tbluseracc.objects.get(username__iexact = uuname)
                 varerr ="User With This UserName In Existence"
                 return render_to_response('rwadmin/createuser.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             except:
                 used = tbluseracc(username = username,password = "12345",recdate = datetime.datetime.today(),expiredate=expiredate,staffname = staffname,userid =varuser,createacc = createacc,inventory = inventory,payables = payables ,receivables = receivables,invoice = invoice,receipt = receipt,payment = payment,genledger = genledger,standardledger = standardledger,stockin = stockin,stockout = stockout,stockreport = stockreport,jobsetup = jobsetup,addsetup = addsetup,jobcosting = jobcosting,returnmat = returnmat,wipinvoice = wipinvoice,wipreport = wipreport,unpresented = unpresented,statutory = statutory,createuser = createuser,resetuser = resetuser,userreport = userreport,rollover = rollover,status = "ACTIVE",esetup = esetup,eposting = eposting, einventory = einventory,ewip = ewip, ereonciliation = ereonciliation, ereport =  ereport, eadmin = eadmin)
                 used.save()
                 return HttpResponseRedirect('/SchApp/account/sysadmin/createuser/')
                 #*****************************
        else:
            form = userform()
            getdetails = tbluseracc.objects.all().order_by('username')
        return render_to_response('rwadmin/createuser.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')

def edituser(request,ind):
     varerr =0
     createacc = 0
     inventory= 0
     payables=0
     receivables=0
     invoice=0
     receipt = 0
     payment = 0
     genledger = 0
     standardledger = 0
     stockin = 0
     stockout = 0
     stockreport = 0
     jobsetup = 0
     addsetup =0
     jobcosting = 0
     returnmat = 0
     wipinvoice = 0
     wipreport = 0
     unpresented = 0
     statutory = 0
     createuser = 0
     resetuser = 0
     userreport = 0
     rollover = 0
     if  "userid" in request.session:
        varuser = request.session['userid']
        #user = tbluseracc.objects.get(username = varuser)
        #uenter = user.createuser
        #if int(uenter) == 0 :
         #  return HttpResponseRedirect('/SchApp/account/sysadmin/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          username = request.POST["username"]
          staffname = request.POST["staffname"]
         # expdate = request.POST["expiredate"]
         # createacc = request.POST["createacc"]#invoice
          uname = str(username)
          uname = uname.lower()
          uuname = uname.replace(' ','-')
          #********************************************
          #****************************************************
          if "createacc" in request.POST:
              createacc = 1

          else:
              createacc = 0

          if "inventory" in request.POST:
              inventory = 1

          else:
              inventory = 0

          if "payables" in request.POST:
              payables = 1

          else:
              payables = 0

          if "receivables" in request.POST:
              receivables = 1

          else:
              receivables = 0

          #***************************************************
          if receivables == 1 or payables == 1 or inventory == 1 or createacc == 1:
              esetup = 1
          else:
              esetup = 0
          if "invoice" in request.POST:
              invoice = 1

          else:
              invoice = 0

          if "receipt" in request.POST:
              receipt = 1

          else:
              receipt = 0

          if "payment" in request.POST:
              payment = 1

          else:
              payment = 0

          if "genledger" in request.POST:
              genledger = 1

          else:
              genledger = 0

          if "standardledger" in request.POST:
              standardledger = 1

          else:
              standardledger = 0


         #**********************************************
          if standardledger == 1 or genledger == 1 or payment == 1 or receipt == 1 or invoice == 1:
              eposting = 1
          else:
              eposting = 0
          #************************

          if "stockin" in request.POST:
              stockin = 1

          else:
              stockin = 0

          if "stockout" in request.POST:
              stockout = 1

          else:
              stockout = 0

          if "stockreport" in request.POST:
              stockreport = 1

          else:
              stockreport = 0

          if stockreport == 1 or stockout == 1 or stockin == 1:
              einventory = 1
          else:
              einventory = 0
          if "jobsetup" in request.POST:
              jobsetup = 1

          else:
              jobsetup = 0

          if "addsetup" in request.POST:
              addsetup = 1

          else:
              addsetup = 0

          if "jobcosting" in request.POST:
              jobcosting = 1

          else:
              jobcosting = 0

          if "returnmat" in request.POST:
              returnmat = 1

          else:
              returnmat = 0

          if "wipinvoice" in request.POST:
              wipinvoice = 1

          else:
              wipinvoice = 0

          if "wipreport" in request.POST:
              wipreport = 1

          else:
              wipreport = 0
          if wipreport == 1 or wipinvoice == 1 or returnmat == 1 or returnmat == 1 or addsetup == 1 or jobcosting == 1 or jobsetup == 1:
              ewip = 1
          else:
              ewip = 0
          #**********************************
          if "unpresented" in request.POST:
              unpresented = 1
              ereonciliation = 1
          else:
              unpresented = 0
              ereonciliation = 0
          if "statutory" in request.POST:
              statutory = 1
              ereport = 1
          else:
              statutory = 0
              ereport = 0
          if "createuser" in request.POST:
              createuser = 1
          else:
              createuser = 0
          if "resetuser" in request.POST:
              resetuser = 1
          else:
              resetuser = 0
          if "userreport" in request.POST:
              userreport = 1
          else:
              userreport = 0
          if "rollover" in request.POST:
              rollover = 1
          else:
              rollover = 0
          #*************************************************
          if rollover == 1 or userreport == 1 or resetuser == 1 or createuser == 1 :#or addsetup == 1 or jobcosting == 1 or jobsetup == 1:
              eadmin = 1
          else:
              eadmin = 0
          #*********************************************
          #if username == "" or staffname == "" or expdate == "":
           #   varerr = "NO RECORD FOUND"
            #  getdetails = ""
             # return HttpResponseRedirect('/SchApp/account/sysadmin/createuser/')
              #return render_to_response('wip/notfound.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
           #***********GETTING THE DATE
          #vyear = str(expdate)
          #vk = vyear[0:4]
          #if vk.isdigit() == True :
                 #print 'digit value'
           #   vdate = date(int(vyear[0:4]),int(vyear[5:7]),int(vyear[8:10]))
          #else:
                  #print 'not digit'
           #  vdate = date(int(vyear[6:10]),int(vyear[0:2]),int(vyear[3:5]))
          try:
                    getdetails = tbluseracc.objects.get(id = ind)
                    getdetails.eposting = eposting
                    getdetails.esetup = esetup
                    getdetails.einventory = einventory
                    getdetails.ereonciliation = ereonciliation
                    getdetails.ewip = ewip
                    getdetails.ereport = ereport
                    getdetails.eadmin = eadmin
                    getdetails.createacc = createacc
                    getdetails.inventory =  inventory
                    getdetails.payables = payables
                    getdetails.receivables = receivables
                    getdetails.invoice = invoice
                    getdetails.receipt = receipt
                    getdetails.payment =  payment
                    getdetails.genledger = genledger
                    getdetails.standardledger =  standardledger
                    getdetails.stockin = stockin
                    getdetails.stockout = stockout
                    getdetails.stockreport = stockreport
                    getdetails.jobsetup = jobsetup
                    getdetails.addsetup = addsetup
                    getdetails.jobcosting =  jobcosting
                    getdetails.returnmat = returnmat
                    getdetails.wipinvoice = wipinvoice
                    getdetails.wipreport = wipreport
                    getdetails.unpresented = unpresented
                    getdetails.statutory = statutory
                    getdetails.createuser = createuser
                    getdetails.resetuser = resetuser
                    getdetails.userreport = userreport
                    getdetails.rollover = rollover
                    #username
                    #getdetails.username = uuname
                    #getdetails.staffname = staffname
                    #getdetails.expiredate = vdate
                    #getdetails.status = request.POST["status"]
                    getdetails.userid = varuser
                    getdetails.save()
                    return HttpResponseRedirect('/sysadmin/createuser/')
          except:
                 return HttpResponseRedirect('/sysadmin/createuser/')
                 #*****************************
        else:

            getdetails = tbluseracc.objects.get(id = ind)
            createacc = getdetails.createacc
            if int(createacc) == 1:
                createacc ="checked"
            else:
                createacc ="unchecked"
            inventory = getdetails.inventory
            if int(inventory) == 1:
                inventory ="checked"
            else:
                inventory ="unchecked"
            payables = getdetails.payables
            if int(payables) == 1:
                payables ="checked"
            else:
                payables ="unchecked"
            receivables = getdetails.receivables
            if int(receivables) == 1:
                receivables ="checked"
            else:
                receivables ="unchecked"
            invoice = getdetails.invoice
            if int(invoice) == 1:
                invoice ="checked"
            else:
                invoice ="unchecked"

            receipt = getdetails.receipt
            if int(receipt) == 1:
                receipt ="checked"
            else:
                receipt ="unchecked"
            payment = getdetails.payment
            if int(payment) == 1:
                payment ="checked"
            else:
                payment ="unchecked"

            genledger = getdetails.genledger
            if int(genledger) == 1:
                genledger ="checked"
            else:
                genledger ="unchecked"
            standardledger = getdetails.standardledger
            if int(standardledger) == 1:
                standardledger ="checked"
            else:
                standardledger ="unchecked"
            stockin = getdetails.stockin
            if int(stockin) == 1:
                stockin ="checked"
            else:
                stockin ="unchecked"
            stockout = getdetails.stockout
            if int(stockout) == 1:
                stockout ="checked"
            else:
                stockout ="unchecked"
            stockreport = getdetails.stockreport
            if int(stockreport) == 1:
                stockreport ="checked"
            else:
                stockreport ="unchecked"
            jobsetup = getdetails.jobsetup
            if int(jobsetup) == 1:
                jobsetup ="checked"
            else:
                jobsetup ="unchecked"
            addsetup = getdetails.addsetup
            if int(addsetup) == 1:
                addsetup ="checked"
            else:
                addsetup ="unchecked"
            jobcosting = getdetails.jobcosting
            if int(jobcosting) == 1:
                jobcosting ="checked"
            else:
                jobcosting ="unchecked"
            returnmat = getdetails.returnmat
            if int(returnmat) == 1:
                returnmat ="checked"
            else:
                returnmat ="unchecked"
            wipinvoice = getdetails.wipinvoice
            if int(wipinvoice) == 1:
                wipinvoice ="checked"
            else:
                wipinvoice ="unchecked"
            wipreport = getdetails.wipreport
            if int(wipreport) == 1:
                wipreport ="checked"
            else:
                wipreport ="unchecked"
            unpresented = getdetails.unpresented
            if int(unpresented) == 1:
                unpresented ="checked"
            else:
                unpresented ="unchecked"
            statutory = getdetails.statutory
            if int(statutory) == 1:
                statutory ="checked"
            else:
                statutory ="unchecked"
            createuser = getdetails.createuser
            if int(createuser) == 1:
                createuser ="checked"
            else:
                createuser ="unchecked"
            resetuser = getdetails.resetuser
            if int(resetuser) == 1:
                resetuser ="checked"
            else:
                resetuser ="unchecked"
            userreport = getdetails.userreport
            if int(userreport) == 1:
                userreport ="checked"
            else:
                userreport ="unchecked"
            rollover = getdetails.rollover
            if int(rollover) == 1:
                rollover ="checked"
            else:
                rollover ="unchecked"
        return render_to_response('rwadmin/edituser.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'createacc':createacc,'inventory':inventory,'payables':payables,'receivables':receivables,'invoice':invoice,'receipt':receipt,'payment':payment,'genledger':genledger,'standardledger':standardledger,'stockin':stockin,'stockout':stockout,'stockreport':stockreport,'jobsetup':jobsetup,'addsetup':addsetup,'jobcosting':jobcosting,'returnmat':returnmat,'wipinvoice':wipinvoice,'wipreport':wipreport,'unpresented':unpresented,'statutory':statutory,'createuser':createuser,'resetuser':resetuser,'userreport':userreport,'rollover':rollover},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')

def adminunauto(request):
     if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        return render_to_response('rwadmin/unautorise.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')


def resetuser(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.resetuser
        if int(uenter) == 0 :
           return HttpResponseRedirect('/SchApp/account/sysadmin/unauto/')
        varerr =""
        getdetails =""

        if request.method == 'POST':
          form = resetuserform(request.POST) # A form bound to the POST data
          if form.is_valid():
             username = form.cleaned_data['username']#username
             if username == "":
                 varerr ="Invalid User Name"
                 return render_to_response('rwadmin/resetuser.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             #pull into the sub table
             try:
                 varvali = tbluseracc.objects.get(username__iexact = username)
                 varvali.password = "12345"
                 varvali.save()
                 varerr ="Account Reset Successfull"
                 return render_to_response('rwadmin/resetuser.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             except:
                 varerr ="Invalid User Name"
                 return render_to_response('rwadmin/resetuser.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             #pull into the sub table
                 #*****************************
        else:
            form = resetuserform()
            getdetails = tbluseracc.objects.all().order_by('username')
        return render_to_response('rwadmin/resetuser.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')

def printuserold(request):
     if  "userid" in request.session:
         varuser = request.session['userid']
         user = tbluseracc.objects.get(username = varuser)
         uenter = user.userreport
         if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/sysadmin/unauto/')
         if tbluseracc.objects.all().count() == 0:
             varerr =""
             return render_to_response('rwadmin/notfound.htm',{'varuser':varuser,'varerr':varerr})

         #resp = HttpResponse(mimetype='application/pdf')
         #chartofacc = tbluseracc.objects.all().order_by('username')
         #report = useraccountrep(queryset=chartofacc)
         #report.generate_by(PDFGenerator, filename=resp)
         #return resp
     else:
       return HttpResponseRedirect('/login/')

def printuser(request):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.resetuser
        if int(uenter) == 0 :
           return HttpResponseRedirect('/SchApp/account/sysadmin/unauto/')
        varerr =""
        getdetails = tbluseracc.objects.all().order_by('username')
        return render_to_response('rwadmin/printuser.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails},context_instance = RequestContext(request))

    else:
       return HttpResponseRedirect('/login/')

def accrollover(request):
     if  "userid" in request.session:
         varerr =""
         varuser = request.session['userid']
         user = tbluseracc.objects.get(username = varuser)
         uenter = user.rollover
         if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/sysadmin/unauto/')
         if tblcalender.objects.all().count() == 0:
               varerr = "NO YEAR TO ROLL OVER"
               return render_to_response('rwadmin/rollover.htm',{'varuser':varuser,'varerr':varerr},context_instance = RequestContext(request))

         getdate = tblcalender.objects.all()
         for g in getdate:
             stdate = g.startmonth
             endate = g.endtmonth

         return render_to_response('rwadmin/rollover.htm',{'varuser':varuser,'varerr':varerr,'stdate':stdate,'endate':endate},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')

def confirmaccrollover(request):
     if  "userid" in request.session:
         varerr =""
         varuser = request.session['userid']
         userid = varuser
         user = tbluseracc.objects.get(username = varuser)
         uenter = user.rollover
         if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/sysadmin/unauto/')
         if tblcalender.objects.all().count() == 0:
               varerr = "NO YEAR TO ROLL OVER"
               return render_to_response('rwadmin/conrollover.htm',{'varuser':varuser,'varerr':varerr},context_instance = RequestContext(request))
         stdate = datetime.date.today()
         endate = datetime.date.today()
         getdate = tblcalender.objects.all()
         for g in getdate:
             stdate = g.startmonth
             endate = g.endtmonth
         varstart = stdate
         varend = endate
         stmon = stdate.month# calendarstart month
         cday = stdate.day # calendar start day
         varyear = varstart.year + 1
         varsmon = varstart.month
         newstdate = date(varyear,varsmon,1) # getting the new start year
         varemon = varend.month
         vareday = varend.day
         varendyear = varend.year + 1
         kp = monthrange(varendyear,varemon)[1]
         #print kp
         vmd = int(kp)
         newedate =  date(varendyear,varemon,vmd)#getting the new end year
         if request.method == 'POST':
             ll = []
             lk = ""
             if tblaccount.objects.all().count()== 0:
                 varerr = "NO ACCOUNT TO ROLL OVER"
                 return render_to_response('rwadmin/conrollover.htm',{'varuser':varuser,'varerr':varerr,'stdate':stdate,'endate':endate},context_instance = RequestContext(request))
                 #**********************************************************************
             if tbltransaction.objects.filter(transdate__year = varyear).count() == 0 :
                 varrid = 1
             else:
                 varrid1 = tbltransaction.objects.filter(transdate__year = varyear).aggregate(Max('recid'))
                 varrid = varrid1['recid__max']
                 varrid +=  1
             vyear =  str(varyear)
             vayear = vyear[2]+ vyear[3]
             vartransid = str(vayear)+ str(varrid) #trans id
             varrecid = varrid # my recid

             #***********************************************************
             vardata = tblaccount.objects.all().exclude(groupname = "FIXED ASSETS" ).exclude(groupname = "NON-CURRENT ASSETS" ).exclude(groupname = "ACCUMULATED DEPRECIATION" ).exclude(groupname = "CURRENT LIABILITIES").exclude(groupname = "LONG TERM LIABILITIES").exclude(groupname = "CAPITAL AND RESERVES").exclude(groupname = "CURRENT ASSETS").order_by('acccode')
             for j in vardata:
                 acccode = j.acccode
                 groupname = j.groupname
                 accname = j.accname
                 subname = j.subgroupname
                 if stmon == varstart.month and cday == varstart.day:
                     opbal = getopbal(acccode,varstart,groupname)#getting the opening balance
                 else:
                     opbal = 0
                 fdata = tbltransaction.objects.filter(acccode = acccode,transdate__range=(varstart,varend)).order_by('transdate','id')
                 #getting the opeaning balance
                 for g in fdata:
                     debit = g.debit
                     credit = g.credit
                     if groupname == "FIXED ASSETS" or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                         opbal = opbal + debit - credit
                     else:
                         opbal = opbal + credit - debit
                 acc = tblaccount.objects.get(acccode = "60103")
                 fbal = acc.accbal
                 if groupname == "FIXED ASSETS" or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                     used = tbltransaction(accname = accname,acccode = acccode,debit = 0,credit = opbal,balance = 0,transid = vartransid,transdate = newstdate,particulars = "OPENING BALANCE",refno = "00000000",groupname = groupname,subname = subname ,userid = userid,recid = varrecid )
                     used.save()
                     used1 = tbltransaction(accname = "RETAINED-PROFIT/LOSS",acccode = "60103",debit = opbal,credit = 0,balance = fbal - opbal,transid = vartransid,transdate = newstdate,particulars = "Retained profit for the year ended %s" %endate.strftime("%d-%m-%Y"),refno = "00000000",groupname = "CAPITAL AND RESERVED",subname = "SHAREHOLDERS FUND" ,userid = userid,recid = varrecid )
                     used1.save()
                     acc.accbal = fbal - opbal
                     acc.save()
                 else:
                     used = tbltransaction(accname = accname,acccode = acccode,debit = opbal,credit = 0,balance = 0,transid = vartransid,transdate = newstdate,particulars = "OPENING BALANCE",refno = "00000000",groupname = groupname,subname = subname ,userid = userid,recid = varrecid )
                     used.save()
                     used1 = tbltransaction(accname = "RETAINED-PROFIT/LOSS",acccode = "60103",debit = 0,credit = opbal,balance = fbal + opbal,transid = vartransid,transdate = newstdate,particulars = "Retained profit for the year ended %s" %endate.strftime("%d-%m-%Y"),refno = "00000000",groupname = "CAPITAL AND RESERVED",subname = "SHAREHOLDERS FUND" ,userid = userid,recid = varrecid )
                     used1.save()
                     acc.accbal = fbal + opbal
                     acc.save()
                     #********************
                 selsubdata = tblaccount.objects.get(acccode = acccode)
                 selsubdata.accbal = opbal
                 selsubdata.lasttrandate = newstdate
                 selsubdata.save()
                 #ending zerorising income,cost of sales,expenses

             #treating cost of sales
             tblaccount.objects.filter(groupname = "COST OF SALES").update(accbal = 0,lasttrandate = newstdate )

             #treating cost of expenses
             tblaccount.objects.filter(groupname = "EXPENSES").update(accbal = 0,lasttrandate = newstdate )

             #treating cost of income
             tblaccount.objects.filter(groupname = "INCOME").update(accbal = 0,lasttrandate = newstdate )
             #updating calender table
             upd = tblcalender.objects.all().aggregate(Max('id'))
             varrid3 = upd['id__max']
             gup = tblcalender.objects.get(id = varrid3)
             gup.startmonth = newstdate
             gup.endtmonth = newedate
             gup.save()
             #moving from the temporary table
             if tbltransactiontemp.objects.all().count() == 0 :
                 pass
             else:
                 varpost = tbltransactiontemp.objects.all().order_by('recid')
                 for t in varpost:
                     accname =  t.accname
                     acccode =  t.acccode
                     debit =  t.debit
                     credit =  t.credit
                     balance =  t.balance
                     transid =  t.transid
                     transdate =  t.transdate
                     particulars =  t.particulars
                     refno =  t.refno
                     groupname =  t.groupname
                     subname =  t.subname
                     userid =  t.userid
                     recid =  t.recid
                     #inserting into table
                     used = tbltransaction(accname = accname,acccode = acccode,debit = debit,credit = credit,balance = balance,transid = transid,transdate = transdate,particulars = particulars,refno = refno,groupname = groupname,subname = subname ,userid = userid,recid = recid )
                     used.save()
             tbltransactiontemp.objects.all().delete()

             #*********************************************************************CLOSING ACCOUNT BALANCING
             return render_to_response('rwadmin/success.htm',{'varuser':varuser,'varerr':varerr,'stdate':stdate,'endate':endate},context_instance = RequestContext(request))

                # varerr = "ERROR FOUND IN YOUR REQUEST PLEASE CONTACT YOUR ADMINISTRATOR"
                # return render_to_response('sysadmin/conrollover.htm',{'varuser':varuser,'varerr':varerr,'stdate':stdate,'endate':endate},context_instance = RequestContext(request))
         else:
             return render_to_response('rwadmin/conrollover.htm',{'varuser':varuser,'varerr':varerr,'stdate':stdate,'endate':endate},context_instance = RequestContext(request))

         return render_to_response('rwadmin/conrollover.htm',{'varuser':varuser,'varerr':varerr,'stdate':stdate,'endate':endate},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')


def deletetrans(request):
    if  "userid" in request.session:
        varerr =""
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.rollover
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/sysadmin/unauto/')
        if request.method == 'POST':
            succ =""
            form = resetuserform(request.POST)
            if form.is_valid():
                transid = form.cleaned_data['username']
                if tbltransaction.objects.filter(transid = transid):
                    pass
                else:
                    succ = 'No Transaction Found '
                    return render_to_response('rwadmin/deletetrans.htm',{'form': form,'succ':succ})
                #********************Checking if the trans date is within
                vdate = datetime.datetime.today()
                trans = tbltransaction.objects.filter(transid = transid)
                for j in trans:
                    vdate = j.transdate
                stdate = datetime.datetime.today()
                endate = datetime.datetime.today()
                getdate = tblcalender.objects.all()
                for g in getdate:
                    stdate = g.startmonth
                    endate = g.endtmonth
                if vdate < stdate or vdate > endate :
                    succ = 'You Cannot delete this transaction '
                    return render_to_response('rwadmin/deletetrans.htm',{'form': form,'succ':succ})

                #****************************************************
                tbltransaction.objects.filter(transid = transid).delete()
                succ = 'OPERATION SUCCESSFUL'
                return render_to_response('rwadmin/deletetrans.htm',{'form': form,'succ':succ})
        else:
            form = resetuserform()
            return render_to_response('rwadmin/deletetrans.htm', {'form': form})

        #return render_to_response('rwadmin/rollover.htm',{'varuser':varuser,'varerr':varerr,'stdate':stdate,'endate':endate},context_instance = RequestContext(request))

    else:
        return HttpResponseRedirect('/login/')



def getuseraccountrw(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tbluseracc.objects.get(id = acccode)
                createacc = getdetails.createacc
                if int(createacc) == 1:
                   createacc ="checked"
                else:
                   createacc ="unchecked"
                inventory = getdetails.inventory
                if int(inventory) == 1:
                   inventory ="checked"
                else:
                   inventory ="unchecked"
                payables = getdetails.payables
                if int(payables) == 1:
                   payables ="checked"
                else:
                   payables ="unchecked"
                receivables = getdetails.receivables
                if int(receivables) == 1:
                   receivables ="checked"
                else:
                   receivables ="unchecked"
                invoice = getdetails.invoice
                if int(invoice) == 1:
                   invoice ="checked"
                else:
                   invoice ="unchecked"

                receipt = getdetails.receipt
                if int(receipt) == 1:
                   receipt ="checked"
                else:
                   receipt ="unchecked"
                payment = getdetails.payment
                if int(payment) == 1:
                   payment ="checked"
                else:
                   payment ="unchecked"
                genledger = getdetails.genledger
                if int(genledger) == 1:
                   genledger ="checked"
                else:
                   genledger ="unchecked"
                standardledger = getdetails.standardledger
                if int(standardledger) == 1:
                   standardledger ="checked"
                else:
                   standardledger ="unchecked"
                stockin = getdetails.stockin
                if int(stockin) == 1:
                   stockin ="checked"
                else:
                   stockin ="unchecked"
                stockout = getdetails.stockout
                if int(stockout) == 1:
                   stockout ="checked"
                else:
                   stockout ="unchecked"
                stockreport = getdetails.stockreport
                if int(stockreport) == 1:
                    stockreport ="checked"
                else:
                    stockreport ="unchecked"
                jobsetup = getdetails.jobsetup
                if int(jobsetup) == 1:
                   jobsetup ="checked"
                else:
                   jobsetup ="unchecked"
                addsetup = getdetails.addsetup
                if int(addsetup) == 1:
                   addsetup ="checked"
                else:
                   addsetup ="unchecked"
                jobcosting = getdetails.jobcosting
                if int(jobcosting) == 1:
                   jobcosting ="checked"
                else:
                   jobcosting ="unchecked"
                returnmat = getdetails.returnmat
                if int(returnmat) == 1:
                   returnmat ="checked"
                else:
                   returnmat ="unchecked"
                wipinvoice = getdetails.wipinvoice
                if int(wipinvoice) == 1:
                   wipinvoice ="checked"
                else:
                   wipinvoice ="unchecked"
                wipreport = getdetails.wipreport
                if int(wipreport) == 1:
                   wipreport ="checked"
                else:
                   wipreport ="unchecked"
                unpresented = getdetails.unpresented
                if int(unpresented) == 1:
                   unpresented ="checked"
                else:
                  unpresented ="unchecked"
                statutory = getdetails.statutory
                if int(statutory) == 1:
                   statutory ="checked"
                else:
                   statutory ="unchecked"
                createuser = getdetails.createuser
                if int(createuser) == 1:
                   createuser ="checked"
                else:
                  createuser ="unchecked"
                resetuser = getdetails.resetuser
                if int(resetuser) == 1:
                  resetuser ="checked"
                else:
                  resetuser ="unchecked"
                userreport = getdetails.userreport
                if int(userreport) == 1:
                  userreport ="checked"
                else:
                 userreport ="unchecked"
                rollover = getdetails.rollover
                if int(rollover) == 1:
                  rollover ="checked"
                else:
                  rollover ="unchecked"
                return render_to_response('rwadmin/edituser.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'createacc':createacc,'inventory':inventory,'payables':payables,'receivables':receivables,'invoice':invoice,'receipt':receipt,'payment':payment,'genledger':genledger,'standardledger':standardledger,'stockin':stockin,'stockout':stockout,'stockreport':stockreport,'jobsetup':jobsetup,'addsetup':addsetup,'jobcosting':jobcosting,'returnmat':returnmat,'wipinvoice':wipinvoice,'wipreport':wipreport,'unpresented':unpresented,'statutory':statutory,'createuser':createuser,'resetuser':resetuser,'userreport':userreport,'rollover':rollover},context_instance = RequestContext(request))
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

#****************************************************
def verifytransview(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.rollover
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/sysadmin/unauto/')
        varerr = ""
        if request.method == 'POST':
            form = verifytransform(request.POST)
            if form.is_valid():
                transid = form.cleaned_data['transid']
                trans = verifyposting(str(transid).upper())
                return render_to_response('rwadmin/verify.htm',{'data':trans,'form':form,'varerr':varerr,'varuser':varuser,'transid':str(transid).upper()})
            else:
                varerr = 'All Fields are required'
                return render_to_response('rwadmin/verify.htm',{'form':form,'varerr':varerr,'varuser':varuser})
        else:
            form = verifytransform()
        return render_to_response('rwadmin/verify.htm',{'form':form,'varerr':varerr,'varuser':varuser})
    else:
        return HttpResponseRedirect('/login/')

def deletetransaction(request,transid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.rollover
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/sysadmin/unauto/')
        tbltransaction.objects.filter(transid = str(transid).upper()).delete()
        #tblstocktransaction.objects.filter(distotalprice = str(transid).upper()).delete()
        #tblmotovehicle.objects.filter(transid = str(transid).upper()).delete()
        #tblpromo.objects.filter(transid = str(transid).upper()).delete()
        return HttpResponseRedirect('/SchApp/account/sysadmin/delete-transaction/')
    else:
        return HttpResponseRedirect('/login/')

def confirmdeletion(request,transid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.rollover
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/sysadmin/unauto/')
        getdate = tblcalender.objects.all()
        stdate = date.today()
        endate = date.today()
        for g in getdate:
            stdate = g.startmonth
            endate = g.endtmonth
        p = tbltransaction.objects.filter(transid =  str(transid).upper())
        tdate = date.today()
        for h in p:
            tdate = h.transdate
        #if tblendofmonth.objects.filter(endday__month = tdate.month):
        #    varerr ="Transaction with trans-id %s Can Not be Deleted !!!"%str(transid).upper()
        #    return render_to_response('sysadmin/confirmdeletion.htm',{'data':'','varerr':varerr,'varuser':str(varuser).upper(),'transid':str(transid).upper()})
        if tdate < stdate or tdate > endate :
            varerr ="Transaction with trans-id %s Can Not be Deleted !!!"%str(transid).upper()
            return render_to_response('rwadmin/confirmdeletion.htm',{'data':'','varerr':varerr,'varuser':str(varuser).upper(),'transid':str(transid).upper()})
        else:
            trans = verifyposting(str(transid).upper())
            return render_to_response('rwadmin/confirmdeletion.htm',{'data':trans,'varerr':'','varuser':str(varuser).upper(),'transid':str(transid).upper()})
    else:
        return HttpResponseRedirect('/login/')

def transactionsview(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.rollover
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/sysadmin/unauto/')
        if request.method == 'POST':
            succ =""
            form = dateform(request.POST)
            if form.is_valid():
                caldate1 = form.cleaned_data['startdate']
                caldate11 = form.cleaned_data['enddate']
                caldate2 = caldate1.split('/')
                varstart = date(int(caldate2[2]),int(caldate2[0]),int(caldate2[1]))
                caldate22 = caldate11.split('/')
                kp = monthrange(int(caldate22[2]),int(caldate22[0]))[1]
                vmd = int(kp)
                varend = date(int(caldate22[2]),int(caldate22[0]),int(caldate22[1]))
                if varstart > varend :
                    succ = "Invalid Date"
                    return render_to_response('rwadmin/trans.htm', {'form': form,'succ':succ})
                trans = tbltransaction.objects.filter(transdate__range=(varstart,varend)).order_by('transdate','id')
                sdic = {}
                for h in trans:
                    sdic.update({h.transid:h.transid})
                mlist = sdic.keys()
                data = []
                if tbltransaction.objects.filter(transdate__range=(varstart,varend)):
                    for n in mlist:
                        getdata1 = tbltransaction.objects.filter(transid = n,transdate__range=(varstart,varend)).aggregate(Sum('debit'),Sum('credit'))
                        debit1 = getdata1['debit__sum']
                        credit1 = getdata1['credit__sum']
                        f = {'transid':n,'debit':locale.format("%.2f",float(debit1),grouping=True),'credit':locale.format("%.2f",float(credit1),grouping=True),'diff':locale.format("%.2f",float(debit1-credit1),grouping=True)}
                        data.append(f)
                    getdata = tbltransaction.objects.filter(transdate__range=(varstart,varend)).aggregate(Sum('debit'),Sum('credit'))
                    debit = getdata['debit__sum']
                    credit = getdata['credit__sum']
                else:
                    debit = 0
                    credit = 0
                return render_to_response('rwadmin/trans.htm',{'form': form,'acc':data,'debit':locale.format("%.2f",float(debit),grouping=True),'credit':locale.format("%.2f",float(credit),grouping=True)})
            else:
                succ = 'Invaid Form'
                return render_to_response('rwadmin/trans.htm', {'form': form,'succ':succ})
        else:
            form = dateform()
            return render_to_response('rwadmin/trans.htm', {'form': form})
    else:
        return HttpResponseRedirect('/login/')
#*********************************************************************************************
def verifyview(request,transid):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.rollover
        if int(uenter) == 0 :
            return HttpResponseRedirect('/SchApp/account/sysadmin/unauto/')
        varerr = ""
        getdetails = tbltransaction.objects.filter(transid = transid)
        tdebit = 0
        tcredit = 0
        userid = ''
        for h in getdetails:
            userid = h.userid
            tdebit += h.debit
            tcredit += h.credit
        comp = tblcompanyinfo.objects.get(id = 1)
        return render_to_response('rwadmin/verifyposting.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'school':comp,'userid':str(userid),'tdebit':locale.format("%.2f",float(tdebit),grouping=True),'tcredit':locale.format("%.2f",float(tcredit),grouping=True),'transid':str(transid)},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')





