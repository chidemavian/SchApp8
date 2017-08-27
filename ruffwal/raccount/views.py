
from myproject.ruffwal.raccount.form import *
from myproject.ruffwal.rwadmin.models import *
from myproject.utilities.views import *
import datetime

def index(request):
    varerr = ""
    if request.method == 'POST':
       form = useraccform(request.POST) # A form bound to the POST data
       if form.is_valid():
           username = form.cleaned_data['username']
           password = form.cleaned_data['password']
           try:
               user = tbluseracc.objects.get(username = username,password=password,status = "ACTIVE")
               if user.password == password :
                        request.session['userid'] = user.username
                        return HttpResponseRedirect('/SchApp/account/welcome/')
           except:
               varerr = "Invalid Login Credentials"
               return render_to_response('setup/login.htm',{'form':form,'varerr':varerr})
    else:
         form = useraccform()
    return render_to_response('setup/login.htm',{'form':form,'varerr':varerr})
def welcomecode(request):
     if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        if int(user.esetup) == 1 or int(user.eposting) == 1  or int(user.einventory) == 1 or int(user.ereonciliation) == 1 or int(user.ereport) == 1 or int(user.eadmin) == 1:
            pass
        else:
            return HttpResponseRedirect('/welcome/')

        varerr =""
        #verifying payments*************************
        tday = datetime.date.today()
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
        return render_to_response('setup/welcome.htm',{'varuser':varuser,'varerr':varerr})
     else:
       return HttpResponseRedirect('/login/')


def logoutuser(request):
    try:
        del request.session['userid']
    except KeyError:
        pass
    return HttpResponseRedirect('/login/')

def header(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        useracc = tbluseracc.objects.get(username = varuser)
        #schinfo = School.objects.get(id = 1)
        return render_to_response('setup/header.html',{'useracc':useracc})
    else:
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
                   user.password = password
                   user.save()
                   return HttpResponseRedirect('/logoutuser/')
               except:
                  varerr = "Invalid User"
                  return render_to_response('setup/changepass.htm',{'form':form,'varerr':varerr,'varuser':varuser})

             else:
                varerr = "Re-confirm password"
                return render_to_response('setup/changepass.htm',{'form':form,'varerr':varerr,'varuser':varuser})

        else:
                  form = changepassform()
        return render_to_response('setup/changepass.htm',{'form':form,'varerr':varerr,'varuser':varuser})

     else:
       return HttpResponseRedirect('/login/')

