# Create your views here.
from django.template import loader, Context,RequestContext
from django.shortcuts import render_to_response
from django.http import  HttpResponseRedirect
from myproject.hrm.rcsetup.models import *
from myproject.hrm.rcwadmin.models import *
from myproject.hrm.rcwadmin.form import *
import datetime
from datetime import date,time
from django.core.mail import send_mail

def enteradmin(request):#adminunauto
     if  "userid" in request.session:

        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.eadmin
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/welcome/')
        varerr =""
        return render_to_response('sysadmin/enteradmin.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')

def createuser(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.createuser
        if uenter == "False" :
           return HttpResponseRedirect('/hrm/sysadmin/unauto/')
        varerr =""
        getdetails =""
        esetup = 'False'
        eposting  = 'False'
        einventory = 'False'
        ewip = 'False'
        ereonciliation = 'False'
        ereport = 'False'
        eadmin = 'False'
        addsetup ='False'
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
                 esetup = 'True'
             if form.cleaned_data['invoice'] or form.cleaned_data['receipt'] or form.cleaned_data['payment'] or form.cleaned_data['genledger'] or form.cleaned_data['standardledger']:
                 eposting = 'True'
             if form.cleaned_data['stockin'] or form.cleaned_data['stockout'] or form.cleaned_data['stockreport']:
                 einventory = 'True'
             if form.cleaned_data['jobsetup'] or form.cleaned_data['addsetup'] or form.cleaned_data['jobcosting'] or form.cleaned_data['returnmat'] or form.cleaned_data['wipinvoice'] or form.cleaned_data['wipreport']:
                 ewip = 'True'
             if form.cleaned_data['unpresented']:
                 ereonciliation = 'True'
                 unpresented = 'True'
             else:
                 unpresented = 'False'
             if form.cleaned_data['statutory']:
                 ereport = 'True'
                 statutory = 'True'
             else:
                 statutory = 'False'

             if form.cleaned_data['createuser'] or form.cleaned_data['resetuser'] or form.cleaned_data['userreport'] or form.cleaned_data['rollover']:
                 eadmin = 'True'
             #pull into the sub table
             if form.cleaned_data['createuser']:
                 createuser = 'True'
             else:
                 createuser = 'False'
             if form.cleaned_data['resetuser']:
                 resetuser = 'True'
             else:
                 resetuser = 'False'
             if form.cleaned_data['userreport']:
                 userreport = 'True'
             else:
                 userreport = 'False'
             if form.cleaned_data['rollover']:
                 rollover = 'True'
             else:
                 rollover = 'False'
             if form.cleaned_data['jobsetup']:
                 jobsetup = 'True'
             else:
                 jobsetup = 'False'
             if form.cleaned_data['addsetup']:
                 addsetup = 'True'
             else:
                 addsetup = 'False'
             if form.cleaned_data['jobcosting']:
                 jobcosting = 'True'
             else:
                 jobcosting = 'False'
             if form.cleaned_data['returnmat']:
                 returnmat = 'True'
             else:
                 returnmat = 'False'
             if form.cleaned_data['wipinvoice']:
                 wipinvoice = 'True'
             else:
                 wipinvoice = 'False'
             if form.cleaned_data['wipreport']:
                 wipreport = 'True'
             else:
                 wipreport = 'False'
             if form.cleaned_data['stockin']:
                 stockin = 'True'
             else:
                 stockin = 'False'
             if form.cleaned_data['stockout']:
                 stockout = 'True'
             else:
                 stockout = 'False'
             if form.cleaned_data['stockreport']:
                 stockreport = 'True'
             else:
                 stockreport = 'False'
             if form.cleaned_data['invoice']:
                 invoice = 'True'
             else:
                 invoice = 'False'
             if form.cleaned_data['receipt']:
                 receipt = 'True'
             else:
                 receipt = 'False'
             if form.cleaned_data['payment']:
                 payment = 'True'
             else:
                 payment = 'False'
             if form.cleaned_data['genledger']:
                 genledger = 'True'
             else:
                 genledger = 'False'
             if form.cleaned_data['standardledger']:
                 standardledger = 'True'
             else:
                 standardledger = 'False'
             if form.cleaned_data['createacc']:
                 createacc = 'True'
             else:
                 createacc = 'False'
             if form.cleaned_data['inventory']:
                 inventory = 'True'
             else:
                 inventory = 'False'
             if form.cleaned_data['payables']:
                 payables = 'True'
             else:
                  payables = 'False'
             if form.cleaned_data['receivables']:
                 receivables = 'True'
             else:
                 receivables = 'False'
             try:
                 varvali = tbluseracc.objects.get(username__iexact = uuname)
                 varerr ="User With This UserName In Existence"
                 return render_to_response('sysadmin/createuser.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             except:
                 used = tbluseracc(username = uuname,password = "12345",recdate = datetime.datetime.today(),expiredate=expiredate,staffname = staffname,userid =varuser,createacc = createacc,inventory = inventory,payables = payables ,receivables = receivables,invoice = invoice,receipt = receipt,payment = payment,genledger = genledger,standardledger = standardledger,stockin = stockin,stockout = stockout,stockreport = stockreport,jobsetup = jobsetup,addsetup = addsetup,jobcosting = jobcosting,returnmat = returnmat,wipinvoice = wipinvoice,wipreport = wipreport,unpresented = unpresented,statutory = statutory,createuser = createuser,resetuser = resetuser,userreport = userreport,rollover = rollover,status = "ACTIVE",esetup = esetup,eposting = eposting, einventory = einventory,ewip = ewip, ereonciliation = ereonciliation, ereport =  ereport, eadmin = eadmin)
                 used.save()
                 return HttpResponseRedirect('/hrm/sysadmin/createuser/')
                 #*****************************
        else:
            form = userform()
            getdetails = tbluseracc.objects.all().order_by('username')
        return render_to_response('sysadmin/createuser.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')

def edituser(request,ind):
     varerr ='False'
     createacc = 'False'
     inventory= 'False'
     payables= 'False'
     receivables = 'False'
     invoice = 'False'
     receipt = 'False'
     payment = 'False'
     genledger = 'False'
     standardledger = 'False'
     stockin = 'False'
     stockout = 'False'
     stockreport = 'False'
     jobsetup = 'False'
     addsetup = 'False'
     jobcosting = 'False'
     returnmat = 'False'
     wipinvoice = 'False'
     wipreport = 'False'
     unpresented = 'False'
     statutory = 'False'
     createuser = 'False'
     resetuser = 'False'
     userreport = 'False'
     rollover = 'False'
     if  "userid" in request.session:
        varuser = request.session['userid']
        #user = tbluseracc.objects.get(username = varuser)
        #uenter = user.createuser
        #if uenter == "False" :
         #  return HttpResponseRedirect('/hrm/sysadmin/unauto/')
        varerr =""
        getdetails =""
        if request.method == 'POST':
          username = request.POST["username"]
          staffname = request.POST["staffname"]
          #expdate = request.POST["expiredate"]
         # createacc = request.POST["createacc"]#invoice
          uname = str(username)
          uname = uname.lower()
          uname = uname.replace(' ','-')
          #********************************************
          #****************************************************
          if "createacc" in request.POST:
              createacc = 'True'

          else:
              createacc = 'False'

          if "inventory" in request.POST:
              inventory = 'True'

          else:
              inventory = 'False'

          if "payables" in request.POST:
              payables = 'True'

          else:
              payables = 'False'

          if "receivables" in request.POST:
              receivables = 'True'

          else:
              receivables = 'False'

          #***************************************************
          if receivables == 'True' or payables == 'True' or inventory == 'True' or createacc == 'True':
              esetup = 'True'
          else:
              esetup = 'False'
          if "invoice" in request.POST:
              invoice = 'True'
          else:
              invoice = 'False'
          if "receipt" in request.POST:
              receipt = 'True'
          else:
              receipt = 'False'
          if "payment" in request.POST:
              payment = 'True'
          else:
              payment = 'False'
          if "genledger" in request.POST:
              genledger = 'True'
          else:
              genledger = 'False'
          if "standardledger" in request.POST:
              standardledger = 'True'
          else:
              standardledger = 'False'
         #**********************************************
          if standardledger == 'True' or genledger == 'True' or payment == 'True' or receipt == 'True' or invoice == 'True':
              eposting = 'True'
          else:
              eposting = 'False'
          #************************
          if "stockin" in request.POST:
              stockin = 'True'

          else:
              stockin = 'False'
          if "stockout" in request.POST:
              stockout = 'True'
          else:
              stockout = 'False'
          if "stockreport" in request.POST:
              stockreport = 'True'
          else:
              stockreport = 'False'
          if stockreport == 'True' or stockout == 'True' or stockin == 'True':
              einventory = 'True'
          else:
              einventory = 'False'
          if "jobsetup" in request.POST:
              jobsetup = 'True'
          else:
              jobsetup = 'False'
          if "addsetup" in request.POST:
              addsetup = 'True'
          else:
              addsetup = 'False'
          if "jobcosting" in request.POST:
              jobcosting = 'True'
          else:
              jobcosting = 'False'
          if "returnmat" in request.POST:
              returnmat = 'True'
          else:
              returnmat = 'False'
          if "wipinvoice" in request.POST:
              wipinvoice = 'True'
          else:
              wipinvoice = 'False'
          if "wipreport" in request.POST:
              wipreport = 'True'
          else:
              wipreport = 'False'
          if wipreport == 'True' or wipinvoice == 'True' or returnmat == 'True' or returnmat == 'True' or addsetup == 'True' or jobcosting == 'True' or jobsetup == 'True':
              ewip = 'True'
          else:
              ewip = 'False'
          #**********************************
          if "unpresented" in request.POST:
              unpresented = 'True'
              ereonciliation = 'True'
          else:
              unpresented = 'False'
              ereonciliation = 'False'
          if "statutory" in request.POST:
              statutory = 'True'
              ereport = 'True'
          else:
              statutory = 'False'
              ereport = 'False'
          if "createuser" in request.POST:
              createuser = 'True'
          else:
              createuser = 'False'
          if "resetuser" in request.POST:
              resetuser = 'True'
          else:
              resetuser = 'False'
          if "userreport" in request.POST:
              userreport = 'True'
          else:
              userreport = 'False'
          if "rollover" in request.POST:
              rollover = 'True'
          else:
              rollover = 'False'
          #*************************************************
          if rollover == 'True' or userreport == 'True' or resetuser == 'True'or createuser == 'True' :#or addsetup == 1 or jobcosting == 1 or jobsetup == 1:
              eadmin = 'True'
          else:
              eadmin = 'False'
          #*********************************************
          #if username == "" or staffname == "":
           #   varerr = "NO RECORD FOUND"
            #  getdetails = ""
            #  return HttpResponseRedirect('/hrm/sysadmin/createuser/')
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
            if createacc == 'True':
                createacc ="checked"
            else:
                createacc ="unchecked"
            inventory = getdetails.inventory
            if inventory == 'True':
                inventory ="checked"
            else:
                inventory ="unchecked"
            payables = getdetails.payables
            if payables == 'True':
                payables ="checked"
            else:
                payables ="unchecked"
            receivables = getdetails.receivables
            if receivables == 'True':
                receivables ="checked"
            else:
                receivables ="unchecked"
            invoice = getdetails.invoice
            if invoice == 'True':
                invoice ="checked"
            else:
                invoice ="unchecked"

            receipt = getdetails.receipt
            if receipt == 'True':
                receipt ="checked"
            else:
                receipt ="unchecked"
            payment = getdetails.payment
            if payment == 'True':
                payment ="checked"
            else:
                payment ="unchecked"

            genledger = getdetails.genledger
            if genledger == 'True':
                genledger ="checked"
            else:
                genledger ="unchecked"
            standardledger = getdetails.standardledger
            if standardledger == 'True':
                standardledger ="checked"
            else:
                standardledger ="unchecked"
            stockin = getdetails.stockin
            if stockin == 'True':
                stockin ="checked"
            else:
                stockin ="unchecked"
            stockout = getdetails.stockout
            if stockout == 'True':
                stockout ="checked"
            else:
                stockout ="unchecked"
            stockreport = getdetails.stockreport
            if stockreport == 'True':
                stockreport ="checked"
            else:
                stockreport ="unchecked"
            jobsetup = getdetails.jobsetup
            if jobsetup == 'True':
                jobsetup ="checked"
            else:
                jobsetup ="unchecked"
            addsetup = getdetails.addsetup
            if addsetup == 'True':
                addsetup ="checked"
            else:
                addsetup ="unchecked"
            jobcosting = getdetails.jobcosting
            if jobcosting == 'True':
                jobcosting ="checked"
            else:
                jobcosting ="unchecked"
            returnmat = getdetails.returnmat
            if returnmat == 'True':
                returnmat ="checked"
            else:
                returnmat ="unchecked"
            wipinvoice = getdetails.wipinvoice
            if wipinvoice == 'True':
                wipinvoice ="checked"
            else:
                wipinvoice ="unchecked"
            wipreport = getdetails.wipreport
            if wipreport == 'True':
                wipreport ="checked"
            else:
                wipreport ="unchecked"
            unpresented = getdetails.unpresented
            if unpresented == 'True':
                unpresented ="checked"
            else:
                unpresented ="unchecked"
            statutory = getdetails.statutory
            if statutory == 'True':
                statutory ="checked"
            else:
                statutory ="unchecked"
            createuser = getdetails.createuser
            if createuser == 'True':
                createuser ="checked"
            else:
                createuser ="unchecked"
            resetuser = getdetails.resetuser
            if resetuser == 'True':
                resetuser ="checked"
            else:
                resetuser ="unchecked"
            userreport = getdetails.userreport
            if userreport == 'True':
                userreport ="checked"
            else:
                userreport ="unchecked"
            rollover = getdetails.rollover
            if rollover == 'True':
                rollover ="checked"
            else:
                rollover ="unchecked"
        return render_to_response('sysadmin/edituser.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'createacc':createacc,'inventory':inventory,'payables':payables,'receivables':receivables,'invoice':invoice,'receipt':receipt,'payment':payment,'genledger':genledger,'standardledger':standardledger,'stockin':stockin,'stockout':stockout,'stockreport':stockreport,'jobsetup':jobsetup,'addsetup':addsetup,'jobcosting':jobcosting,'returnmat':returnmat,'wipinvoice':wipinvoice,'wipreport':wipreport,'unpresented':unpresented,'statutory':statutory,'createuser':createuser,'resetuser':resetuser,'userreport':userreport,'rollover':rollover},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')

def adminunauto(request):
     if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        return render_to_response('sysadmin/unautorise.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')


def resetuser(request):
     varerr =""
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.resetuser
        if uenter == "False" :
           return HttpResponseRedirect('/hrm/sysadmin/unauto/')
        varerr =""
        getdetails =""

        if request.method == 'POST':
          form = resetuserform(request.POST) # A form bound to the POST data
          if form.is_valid():
             username = form.cleaned_data['username']#username
             if username == "":
                 varerr ="Invalid User Name"
                 return render_to_response('sysadmin/resetuser.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             #pull into the sub table
             try:
                 varvali = tbluseracc.objects.get(username__iexact = username)
                 varvali.password = "12345"
                 varvali.save()
                 varerr ="Account Reset Successfull"
                 return render_to_response('sysadmin/resetuser.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             except:
                 varerr ="Invalid User Name"
                 return render_to_response('sysadmin/resetuser.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
             #pull into the sub table
                 #*****************************
        else:
            form = resetuserform()
            getdetails = tbluseracc.objects.all().order_by('username')
        return render_to_response('sysadmin/resetuser.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

     else:
       return HttpResponseRedirect('/login/')




def index(request):
    varerr = ""
    varerr2 = ''
    a = tblcontrol.objects.all()
    for p in a:
        vdate = p.datecreated
   # print vdate
    vtoday = datetime.date.today()
   # print vtoday
    form = useraccform()
   # if vtoday >= vdate:
     #   varerr = "Software Expires,Call 08062916005 or 08033204305"
      #  return render_to_response('login.htm',{'form':form,'varerr':varerr})
   # else:
    #    pass
    form2 = userloginform()
    if request.method == 'POST':
       form = useraccform(request.POST) # A form bound to the POST data
       if form.is_valid():
           username1 = form.cleaned_data['username']
           password1 = form.cleaned_data['password']
           username = username1.lower()
           password = password1.lower()
           try:
               user = tbluseracc.objects.get(username = username,password=password,status = "ACTIVE")
               if user.password == password :
                        request.session['userid'] = user.username
                        return HttpResponseRedirect('/hrm/welcome/')
           except:
               varerr = "Invalid User"
               return render_to_response('rsetup/login.htm',{'form':form,'form2':form2,'varerr':varerr})
    else:
         form = useraccform()

    return render_to_response('rsetup/login.htm',{'form':form,'form2':form2,'varerr':varerr,'varerr2':varerr2})
def welcomecode(request):
     if  "userid" in request.session:

        varuser = request.session['userid']
        varerr =""
        user = tbluseracc.objects.get(username = varuser)
        if str(user.esetup) == 'True' or str(user.eposting) ==  'True'  or str(user.einventory) ==  'True' or str(user.ereonciliation) ==  'True' or str(user.ereport) ==  'True' or str(user.eadmin) ==  'True':
            pass
        else:
            return HttpResponseRedirect('/welcome/')
        return render_to_response('rsetup/welcome.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')


def logoutuser(request):
    try:
        del request.session['userid']
    except KeyError:
        pass
    return HttpResponseRedirect('/login/')

def changepassword(request):
     if  "userid" in request.session:
        varuser = request.session['userid']

        varerr = ""
        if request.method == 'POST':
           form = changepassform(request.POST) # A form bound to the POST data
           if form.is_valid():
             oldpassword = form.cleaned_data['oldpassword']
             password = form.cleaned_data['password']
             password2 = form.cleaned_data['password2']
             if password == password2:
               try:
                   user = tbluseracc.objects.get(username = varuser,password=oldpassword)
                   #user = tbluseracc.objects.get(username = varuser)
                   user.password = password.lower()
                   user.save()
                   return HttpResponseRedirect('/hrm/logoutuser/')
               except:
                  varerr = "Invalid User"
                  return render_to_response('rsetup/changepass.htm',{'form':form,'varerr':varerr,'varuser':varuser})

             else:
                varerr = "Re-confirm password"
                return render_to_response('rsetup/changepass.htm',{'form':form,'varerr':varerr,'varuser':varuser})

        else:
                  form = changepassform()
        return render_to_response('rsetup/changepass.htm',{'form':form,'varerr':varerr,'varuser':varuser})

     else:
       return HttpResponseRedirect('/login/')

def passwordrequest(request):
    varerr = ""
    varerr2 = ""

    form = useraccform()

    if request.method == 'POST':
        form2 = userloginform(request.POST) # A form bound to the POST data
        if form2.is_valid():
            emailm = form2.cleaned_data['email']

            try:
                body ='Your Username : demo223 \n\n Password : passworddemo \n\n\n Support Team \n +2348033204305,+2348062916005'
                send_mail('Demo Password',body, 'support@ruffwal.com',[emailm],fail_silently=False)
                send_mail('Demo Password',emailm, 'support@ruffwal.com',['support@ruffwal.com'],fail_silently=False)
                varerr2 = "You can check your email for your login details"
                return render_to_response('rsetup/login.htm',{'varerr2':varerr2,'form':form,'form2':form2},context_instance = RequestContext(request))
            except :
                varerr2 = "Error occurred, Please Check your connection"
                return render_to_response('rsetup/login.htm',{'varerr2':varerr2,'form':form,'form2':form2},context_instance = RequestContext(request))
    else:
        form = useraccform()
        form2 = userloginform()

    return render_to_response('rsetup/login.htm',{'form':form,'form2':form2,'varerr':varerr})

def getuseraccount(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tbluseracc.objects.get(id = acccode)
                createacc = getdetails.createacc
                if createacc == 'True':
                   createacc ="checked"
                else:
                   createacc ="unchecked"
                inventory = getdetails.inventory
                if inventory == 'True':
                   inventory ="checked"
                else:
                   inventory ="unchecked"
                payables = getdetails.payables
                if payables == 'True':
                   payables ="checked"
                else:
                   payables ="unchecked"
                receivables = getdetails.receivables
                if receivables == 'True':
                   receivables ="checked"
                else:
                   receivables ="unchecked"
                invoice = getdetails.invoice
                if invoice == 'True':
                   invoice ="checked"
                else:
                   invoice ="unchecked"

                receipt = getdetails.receipt
                if receipt == 'True':
                   receipt ="checked"
                else:
                   receipt ="unchecked"
                payment = getdetails.payment
                if payment == 'True':
                   payment ="checked"
                else:
                   payment ="unchecked"

                genledger = getdetails.genledger
                if genledger == 'True':
                   genledger ="checked"
                else:
                   genledger ="unchecked"
                standardledger = getdetails.standardledger
                if standardledger == 'True':
                   standardledger ="checked"
                else:
                   standardledger ="unchecked"
                stockin = getdetails.stockin
                if stockin == 'True':
                   stockin ="checked"
                else:
                   stockin ="unchecked"
                stockout = getdetails.stockout
                if stockout == 'True':
                   stockout ="checked"
                else:
                   stockout ="unchecked"
                stockreport = getdetails.stockreport
                if stockreport == 'True':
                   stockreport ="checked"
                else:
                   stockreport ="unchecked"
                jobsetup = getdetails.jobsetup
                if jobsetup == 'True':
                   jobsetup ="checked"
                else:
                   jobsetup ="unchecked"
                addsetup = getdetails.addsetup
                if addsetup == 'True':
                   addsetup ="checked"
                else:
                   addsetup ="unchecked"
                jobcosting = getdetails.jobcosting
                if jobcosting == 'True':
                   jobcosting ="checked"
                else:
                   jobcosting ="unchecked"
                returnmat = getdetails.returnmat
                if returnmat == 'True':
                   returnmat ="checked"
                else:
                   returnmat ="unchecked"
                wipinvoice = getdetails.wipinvoice
                if wipinvoice == 'True':
                   wipinvoice ="checked"
                else:
                   wipinvoice ="unchecked"
                wipreport = getdetails.wipreport
                if wipreport == 'True':
                  wipreport ="checked"
                else:
                  wipreport ="unchecked"
                unpresented = getdetails.unpresented
                if unpresented == 'True':
                   unpresented ="checked"
                else:
                   unpresented ="unchecked"
                statutory = getdetails.statutory
                if statutory == 'True':
                   statutory ="checked"
                else:
                  statutory ="unchecked"
                createuser = getdetails.createuser
                if createuser == 'True':
                   createuser ="checked"
                else:
                   createuser ="unchecked"
                resetuser = getdetails.resetuser
                if resetuser == 'True':
                   resetuser ="checked"
                else:
                   resetuser ="unchecked"
                userreport = getdetails.userreport
                if userreport == 'True':
                   userreport ="checked"
                else:
                  userreport ="unchecked"
                rollover = getdetails.rollover
                if rollover == 'True':
                   rollover ="checked"
                else:
                   rollover ="unchecked"
                return render_to_response('rcadmin/edituser.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'createacc':createacc,'inventory':inventory,'payables':payables,'receivables':receivables,'invoice':invoice,'receipt':receipt,'payment':payment,'genledger':genledger,'standardledger':standardledger,'stockin':stockin,'stockout':stockout,'stockreport':stockreport,'jobsetup':jobsetup,'addsetup':addsetup,'jobcosting':jobcosting,'returnmat':returnmat,'wipinvoice':wipinvoice,'wipreport':wipreport,'unpresented':unpresented,'statutory':statutory,'createuser':createuser,'resetuser':resetuser,'userreport':userreport,'rollover':rollover},context_instance = RequestContext(request))
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

