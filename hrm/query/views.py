# Create your views here.
from django.template import loader, Context,RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import  HttpResponseRedirect
from myproject.hrm.query.form import *
from myproject.hrm.query.models import *
from myproject.hrm.rcwadmin.models import *
from myproject.hrm.hrm.models import *
from myproject.hrm.rcsetup.models import *
from myproject.hrm.utils import *
import datetime
from datetime import date

def queryunauto(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        varerr =""
        return render_to_response('query/unautorise.htm',{'varuser':varuser,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def querysetup(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.addsetup
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/query/unauto/')
            varerr =""
            getdetails =""
            if request.method == 'POST':
                form = setupform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    name = form.cleaned_data['name']
                    name = name.replace(' ','-')
                    name = name.upper()
                    if tblquerysetup.objects.filter(name = name).count() == 0:
                        pass
                    else:
                        varerr = "%s in existence" % name
                        getdetails = tblquerysetup.objects.all().order_by('name')
                        return render_to_response('query/setup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                    savecon = tblquerysetup(name = name,userid = varuser)
                    savecon.save()
                    return HttpResponseRedirect('/hrm/query/setup/')
                else:
                    varerr = "All Fields Are Required/Check Inputed Picture"
                    getdetails = ""
                return render_to_response('query/setup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
            else:
                form = setupform()
                getdetails = tblquerysetup.objects.all().order_by('name')
            return render_to_response('query/setup.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def editquerysetup(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.addsetup
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/train/unauto/')
        varerr =""
        getdetails =''
        if request.method == 'POST':
            getdetails = ""
            name = request.POST['name']
            name = name.replace(' ','-')
            name = name.upper()
            if  tblquerysetup.objects.filter(name = name).exclude(id = invid).count() == 0 :
                pass
            else:
                varerr = "%s In Existence" % name
                getdetails = tblquerysetup.objects.get(id = invid)
                return render_to_response('query/edittraining.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})

            if  name == "" :
                varerr = "ALL FIELDS ARE REQUIRED"
                getdetails = tblquerysetup.objects.get(id = invid)
                return render_to_response('query/edittraining.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})
            seldata = tblquerysetup.objects.get(id = invid)
            seldata.name = name
            seldata.save()
            return HttpResponseRedirect('/hrm/query/setup/')
        else:
            try:
                getdetails = tblquerysetup.objects.get(id = invid)#.order_by('acccode')#tblaccount_acccode
                return render_to_response('query/edittraining.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,'desg':desg,'gpfa':gpfa,'gbank':gbank,'gdept':gdept,'glocal':glocal})
            except:
                varerr = ""
            return render_to_response('query/edittraining.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails})

    else:
        return HttpResponseRedirect('/login/')

def deletequerysetup(request,invid):
    varerr =""
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.addsetup
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/query/unauto/')
        varerr =""
        try:
            uacc = tblquerysetup.objects.get(id = invid)
            uacc.delete()
            return HttpResponseRedirect('/hrm/query/setup/')
        except :
            return HttpResponseRedirect('/hrm/query/setup/')
    else:
        return HttpResponseRedirect('/login/')

def staffquery(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.addsetup
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/query/unauto/')
            varerr =""
            getdetails =""
            if request.method == 'POST':
                form = querytostaff(request.POST) # A form bound to the POST data
                if form.is_valid():
                    staffid = form.cleaned_data['staffid']
                    staffname = form.cleaned_data['staffname']
                    querytype = form.cleaned_data['querytype']
                    querydate = form.cleaned_data['querydate']
                    linemanager = form.cleaned_data['linemanager']
                    reason = form.cleaned_data['reason']
                    action = form.cleaned_data['action']
                    getissuer = str(linemanager)
                    if getissuer.find('&&') <= 0:
                       varerr = "Invalid Query Issuer"
                       getdetails = ''
                       return render_to_response('query/staffquery.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))

                    giverid,givername = linemanager.split('&&')
                    j = str(giverid)
                    j = j.replace(" ","-")
                    dmon,dday,dyear, = querydate.split('/')
                    sdate = date(int(dyear),int(dmon),int(dday))

                    if staffrec.objects.filter(staffid = giverid).count() == 0:
                        varerr = "%s  not in existence" % giverid
                        getdetails = ''
                        return render_to_response('query/staffquery.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
                    else:
                        pass
                    if staffrec.objects.get(staffid = staffid):
                       getstaff = staffrec.objects.get(staffid = staffid)
                       getissu =  staffrec.objects.get(staffid = giverid)
                       savecon = tblstaffquery(staffid = staffid,staffname = staffname,designation = getstaff.designation,department = getstaff.department,querytype = querytype,querydate = sdate,querygiver = getissu.name,querygiverid = giverid,reasonforquery = reason,actiontaken = action,userid = varuser)
                       savecon.save()
                       return HttpResponseRedirect('/hrm/query/successful/')
                else:
                    varerr = "All Fields Are Required/Check Inputed Picture"
                    getdetails = ""
                return render_to_response('query/staffquery.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
            else:
                form = querytostaff()
                getdetails = tblquerysetup.objects.all().order_by('name')
            return render_to_response('query/staffquery.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')
def opsuccessfullquery(request):
    if  "userid" in request.session:
        varuser = request.session['userid']
        user = tbluseracc.objects.get(username = varuser)
        uenter = user.receipt
        if uenter == "False" :
            return HttpResponseRedirect('/hrm/query/unauto/')
        varerr =""
        #form = editstaform()
        return render_to_response('query/opsuccessful.htm',{'varuser':varuser,'varerr':varerr})
    else:
        return HttpResponseRedirect('/login/')

def queryreport(request):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.addsetup
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/query/unauto/')
            varerr =""
            getdetails =""
            if request.method == 'POST':
                form = queryreportform(request.POST) # A form bound to the POST data
                if form.is_valid():
                    querytype = form.cleaned_data['querytype']
                    queryyear = form.cleaned_data['queryyear']
                    comp = tblcompanyinfo.objects.get(id = 1)
                    staff_list = tblstaffquery.objects.filter(querytype = querytype,querydate__year = queryyear ).order_by('querydate')
                    return render_to_response('query/queryreport.htm',{'varuser':varuser,'varerr':varerr,'form':form,'staff_list':staff_list,'comp':comp,'querytype':querytype,'printdate':gettime()},context_instance = RequestContext(request))

                else:
                    varerr = "All Fields Are Required"
                    getdetails = ""
                return render_to_response('query/queryreport.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
            else:
                form = queryreportform()
                getdetails = ''#tblquerysetup.objects.all().order_by('name')
            return render_to_response('query/queryreport.htm',{'varuser':varuser,'varerr':varerr,'form':form,'getdetails':getdetails},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


def staffajaxquery(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                #print acccode
                staff_list = tblstaffquery.objects.filter(staffid = acccode).order_by('-querydate')

                return render_to_response('query/textajax51.htm',{'staff_list':staff_list})
            else:
                #gdata = tblaccount.objects.all()
                gdata = ""
                return render_to_response('query/textajax51.htm',{'gdata':gdata})
        else:
            #gdata = tblaccount.objects.all()
            gdata = ""
            return render_to_response('query/textajax51.htm',{'gdata':gdata})

    else:
        return HttpResponseRedirect('/login/')

def deletegivenquery(request,qid):
    varerr =""
    if  "userid" in request.session:
        if  "userid" in request.session:
            varuser = request.session['userid']
            user = tbluseracc.objects.get(username = varuser)
            uenter = user.addsetup
            if uenter == "False" :
                return HttpResponseRedirect('/hrm/query/unauto/')
            varerr =""
            details =""
            if request.method == 'POST':
                reason = request.POST['reason']
                if reason =='':
                   varerr = "You must have reason for deleting this query"
                   details = tblstaffquery.objects.get(id = qid)
                   return render_to_response('query/deletequery.htm',{'varuser':varuser,'varerr':varerr,'details':details},context_instance = RequestContext(request))
                staffdata = tblstaffquery.objects.get(id = qid)
                savecon = tblstaffquerydeleted(staffid = staffdata.staffid,staffname = staffdata.staffname,designation = staffdata.designation,department = staffdata.department,querytype = staffdata.querytype,querydate = staffdata.querydate,querygiver = staffdata.querygiver,querygiverid = staffdata.querygiverid,reasonforquery = staffdata.reasonforquery,actiontaken = staffdata.actiontaken,userid = varuser,reasonfordeletion = reason)
                savecon.save()
                staffdata.delete()
                return HttpResponseRedirect('/hrm/query/successful/')
            else:
                 details = tblstaffquery.objects.get(id = qid)
            return render_to_response('query/deletequery.htm',{'varuser':varuser,'varerr':varerr,'details':details},context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')

def getquerysetup(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                getdetails = tblquerysetup.objects.get(id = acccode)#.order_by('acccode')#tblaccount_acccode
                return render_to_response('query/edittraining.htm',{'varuser':varuser,'varerr':varerr,'getdetails':getdetails,})
            else:
                gdata = ""
                return render_to_response('rsetup/index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('rsetup/getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')



