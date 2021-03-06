from myproject.hrm.rcsetup.views import *
from myproject.hrm.hrm.views import *
from myproject.hrm.leave.views import *
from myproject.hrm.train.views import *
from myproject.hrm.staff.views import *
from myproject.hrm.rcwadmin.views import *
from myproject.hrm.payroll.views import *
from myproject.hrm.query.views import *
from myproject.hrm.contract.views import *
from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    ('^$',welcomecode),
    ('^login/$',index),
    ('^passwordrequest/$',passwordrequest),
    ('^unauto/$',unauto),
    ('^welcome/$',welcomecode),
    ('^changepassword/$',changepassword),
    ('^logoutuser/$',logoutuser),
    ('^entersetup/$',rentersetupcode),
    ('^setuplg/$',setuplgcode),
    ('^editlg/(\d+)/$',editlgcode),
    ('^deletelg/(\d+)/$',deletelgcode),
    ('^setupdep/$',setupdepcode),
    ('^editdep/(\d+)/$',editdepcode),
    ('^deletedep/(\d+)/$',deletedepcode),
    ('^setupdesg/$',setupdesgcode),
    ('^editdesgn/(\d+)/$',editdesgn),
    ('^deletedesgn/(\d+)/$',deletedesgn),
    ('^setuppfa/$',setuppfacode),
    ('^editpfa/(\d+)/$',editpfacode),
    ('^deletepfa/(\d+)/$',deletepfacode),
    ('^setupbank/$',setupbankcode),
    ('^editbank/(\d+)/$',editbankcode),
    ('^deletebank/(\d+)/$',deletebankcode),
    ('^setupcategory/$',setupcategorycode),
    ('^editcategory/(\d+)/$',editcategorycode),
    ('^deletecategory/(\d+)/$',deletecategorycode),
    ('^setupall/$',setupall),
    ('^ajaxall/$',allowanceajax),
    ('^editall/(\d+)/$',editall),
    ('^deleteall/(\d+)/$',deleteall),
    ('^setuspall/$',setuspall),
    ('^editspall/(\d+)/$',editspall),
    ('^deletespall/(\d+)/$',deletespall),
    ('^setupded/$',setupded),
    ('^ajaxded/$',deductionajax),
    ('^editded/(\d+)/$',editded),
    ('^deleteded/(\d+)/$',deleteded),
    ('^setupsded/$',setuspded),
    ('^editspded/(\d+)/$',editspdedded),
    ('^deletespded/(\d+)/$',deletespdedded),
    ('^statecapital/$',entersetupstate),
    ('^state/$',setupstate),
    ('^localgovt/$',setuplocalgovt),
    ('^getstate/$',getstate),
    ('^getlocal/$',getlocal),
    ('^ajaxstreetlg/$',ajaxstreetlg),
    ('^deletestate/(\d+)/$',deletestate),
    ('^deletelocalgt/(\d+)/$',deletelocalgt),
    #('^uploaddesg/$', testexcel),# to uplod design
    #('^uploadall/$', uploadall),# to uplod allowance
    ('^uploadbiodata/$', uploadbiodata),# to uplod biodata
    ('^uploadbranch/$', uploadbranch),# to uplod branch
    ('^uploadspded/$', uploadspded),# to uplod special ded
    ('^uploaddep/$', uploaddep),# to uplod depertment
    ('^uploadstaffacc/$', uploadstaffacc),# to uplod staff bank
    ('^uploadstaffedu/$', uploadstaffedu),# to uplod education
    ('^expiredate/$', controldate),# to put expiring date
    ('^genlocal/$', genlocal),# to generate local government
    ('^genstate/$', genstate),# to generate local government
    ('^uploadstate/$', uploadstate),# to uplod
    ('^uploadlocal/$', uploadlocal),# to uplod
    ('^search/$', staffsearch),#
    ('^ajaxsearchstaff/$', ajaxsearchstaff),#
    ('^hmosetup/$', setuphmo),#HMO
    ('^edithmo/(\d+)/$',edithmocode),
    ('^deletehmo/(\d+)/$',deletehmocode),
    ('^ajaxstreetlgprovider/$', ajaxstreetlgprovider),#HMO
    ('^hmosetupprovider/$', setuphmoprovider),#HMO
    ('^deletehmoprovidercode/(\d+)/$',deletehmoprovidercode),
    ('^setuplevel/$', setuplevel),
    ('^setupstep/$', setupstep),
    ('^ajaxstep/$', ajaxstep),
    ('^getnewstep/$', getnewstep),
    ('^getdescription/$', getdescription),
   # ('^get_description_special_deduction/$', getdescription1),
    ('^setupdesc/$', setupdesc),
    ('^getspdeduction/$', getspdeduction),
    ('^getspallowance/$', getspallowance),
    ('^savings/$', savings),
    ('^getsavings/$', getsavings),
    ('^editsavings/(\d+)/$',editsavings),
    ('^deletesavings/(\d+)/$',deletesavings),
    ('^loan/$', loan),
    ('^setuploandesc/$', setuploandesc),
    ('^getdescriptionloan/$', getdescriptionloan),
    ('^deleteloan/(\d+)/$',deleteloan),
    ('^getloan/$', getloan),
    ('^getpension/$', getpension),
    ('^setuppensionrate/$', setuppensionrate),
    ('^getbranch/$', getbranch),
    ('^getdepartment/$', getdepartment),
    ('^getdesignation/$', getdesignation),
    ('^getallowance/$', getallowance),
    ('^getdeduction/$', getdeduction),
    ('^getbanksetup/$', getbanksetup),
    ('^getpfa/$', getpfa),
    ('^gethmo/$', gethmo),
    ('^getsavingsname/$', getsavingsname),
    ('^setupsavingsname/$', setupsavingsname),
    ('^uploadbiodatawap/$', uploadbiodatawap),
    ('^uploadsavingswap/$', uploadsavingswap),
    ('^uploadallowancewap/$', uploadallowancewap),
    ('^uploadbankwap/$', uploadbankwap),
    ('^uploadloanwap/$', uploadloanwap),
    ('^uploaddeduction/$', uploaddeduction),


      #HRM
    ('^hrm/enterhrm/$',enterhrm),
    ('^hrm/successful/$',opsuccessfull),
    ('^hrm/unauto/$',pounauto),
    ('^hrm/ajax/$',hrmtestajax),
    ('^hrm/ajaxall/$',hrmtestajaxall),
    ('^hrm/staffdata/$',hrmstaffdata),
    ('^hrm/editstaff/$',editstaff),
    ('^hrm/ajaxstaff/$',hrmtestajaxstaff),
    ('^hrm/editstaffid/(\d+)/$',editstaffid),
    ('^hrm/staffedu/$',hrmstaffedu),
    ('^hrm/staffproff/$',hrmstaffproff),
    ('^hrm/staffnonpension/$',hrmstaffnonpension),
    ('^hrm/eduajax/$',hrmeduajax),
    ('^hrm/eduajaxall/$',hrmeduajaxall),
    ('^hrm/eduajaxallproff/$',hrmeduajaxallproff),
    ('^hrm/editstaffedu/(\d+)/$',editstaffedu),
    ('^hrm/deletestaffedu/(\d+)/$',deletestaffedu),
    ('^hrm/editstaffproff/(\d+)/$',editstaffproff),
    ('^hrm/deletestaffproff/(\d+)/$',deletestaffproff),
    ('^hrm/editstaffnonpension/(\d+)/$',editstaffnonpension),
    ('^hrm/deletestaffnonpension/(\d+)/$',deletestaffnonpension),
    ('^hrm/staffreport/$',hrmstaffreport),
    ('^hrm/staffindreport/$',hrmstaffindreport),
    ('^hrm/staffindreportall/$',hrmstaffindreportall),
    ('^hrm/lengthofservice/$',lengthofservice),
    ('^hrm/staffhmo/$',hrmstaffhmo),
    ('^hrm/eduajaxallhmo/$',hrmeduajaxallhmo),
    ('^hrm/providerajax/$',hrmproviderajaxa),
    ('^hrm/deletestaffhmo/(\d+)/$',deletestaffhmo),
    ('^hrm/staffpfa/$',hrmstaffpfa),
    ('^hrm/eduajaxallpfa/$',hrmeduajaxallpfa),
    ('^hrm/editstaffpfa/(\d+)/$',editstaffpfa),
    ('^hrm/deletestaffpfa/(\d+)/$',deletestaffpfa),
    ('^hrm/findstaff/$',autocomplete),
    ('^hrm/findstaffname/$',autocompletename),
    ('^hrm/getstaff/$',getstaff),#getstaffprofessional
    ('^hrm/getstaffeducation/$',getstaffeducation),#getstaffno
    ('^hrm/getstaffprofessional/$',getstaffprofessional),
    ('^hrm/getstaffno/$',getstaffno),
    ('^hrm/hrmstaffreportbydepartment/$',hrmstaffreportbydepartment),
    ('^hrm/hrmstaffreportbydesg/$',hrmstaffreportbydesg),
    ('^hrm/getstaffpfa/$',getstaffpfa),

      #STAFF
    ('^staff/enterstaff/$',enterstaff),
    ('^staff/successful/$',staffsuccessfull),
    ('^staff/unauto/$',staffunauto),
    ('^staff/redeployment/$',redeployment),
    ('^staff/redajax/$',redajax),
    ('^staff/redajaxall/$',redajaxall),
    ('^staff/ajaxaredeploy/$',ajaxaredeploy),
    ('^staff/ajaxstaff/$',stafftestajaxstaff),
    ('^staff/deptreport/$',deptreport),
    ('^staff/locreport/$',locreport),
    ('^staff/editredeployment/(\d+)/$',editredeployment),
    ('^staff/promotion/$',promotion),
    ('^staff/ajaxstaffpromo/$',stafftestajaxstaffpromo),
    ('^staff/editredeploymentpromo/(\d+)/$',editredeploymentpromo),
    ('^staff/ajaxaredeploypromo/$',ajaxaredeploypromo),
    ('^staff/promotionreport/$',promotionreport),
    ('^staff/resignation/$',resignation),
    ('^staff/ajaxstaffresign/$',stafftestajaxstaffresign),
    ('^staff/editredeploymentresign/(\d+)/$',editredeploymentresign),
    ('^staff/resignationreport/$',resignationreport),
    ('^staff/termination/$',termination),
    ('^staff/ajaxstaffterm/$',stafftestajaxstaffterm),
    ('^staff/editredeploymentterm/(\d+)/$',editredeploymentterm),
    ('^staff/terminationreport/$',terminationreport),
    ('^staff/retirement/$',retirement),
    ('^staff/ajaxstaffretire/$',stafftestajaxstaffretire),
    ('^staff/editredeploymentretire/(\d+)/$',editredeploymentretire),
    ('^staff/retirementreport/$',retirementreport),
    ('^staff/reinstatement/$',reinstatement),
    ('^staff/ajaxstaffreinstate/$',stafftestajaxstaffreinstate),
    ('^staff/editredeploymentreinstate/(\d+)/$',editredeploymentreinstate),
    ('^staff/getredeployment/$',getredeployment),
    ('^staff/gettermination/$',gettermination),
    ('^staff/getresignation/$',getresignation),#
    ('^staff/getretirement/$',getretirement),#
    ('^staff/getreinstatement/$',getreinstatement),#

    #TRAINING
    ('^train/unauto/$',trainunauto),
    ('^train/entertraining/$',entertraining),
    ('^train/trainingsetup/$',trainingsetup),
    ('^train/edittraining/(\d+)/$',edittrainsetup),
    ('^train/deletesetup/(\d+)/$',deletetrainsetup),
    ('^train/trainingstaff/$',stafftraining),
    ('^train/staffajax/$',trainingstaffajax),
    ('^train/editstaff/(\d+)/$',trainingeditstaff),
    ('^train/staffajaxtrain/$',trainingstaffajaxtrain),
    ('^train/deletestaff/(\d+)/$',trainingdeletestaff),
    ('^train/trainingreport/$',trainingreport),
    ('^train/yettobetrained/$',yettobetrained),#getrainsetup
    ('^train/getrainsetup/$',getrainsetup),#
     #Leave
    ('^leave/unauto/$',leaveunauto),
    ('^leave/enterleave/$',enterleave),
    ('^leave/leavesetup/$',leavesetup),
    ('^leave/leavesetup/(\d+)/$',editleavesetup),
    ('^leave/deletesetup/(\d+)/$',deleteleavesetup),
    ('^leave/leavestaff/$',staffleave),
    ('^leave/staffajax/$',leavestaffajax),
    ('^leave/editstaff/(\d+)/$',leaveeditstaff),
    ('^leave/staffajaxleave/$',leavestaffajaxleave),
    ('^leave/deletestaff/(\d+)/$',leavedeletestaff),
    ('^leave/leavereport/$',leavereport),
    ('^leave/yettobeleave/$',yettobeleave),
    ('^leave/getleave/$',getleave),


    #PAYROLL

    ('^payroll/unauto/$',pounautopayroll),
    ('^payroll/enterpayroll/$',enterpayroll),
    ('^payroll/enterworkingdays/$',enterworkingdays),
    ('^payroll/editworked/(\d+)/$',editworked),
    ('^payroll/bankdetails/$',bankdetails),
    ('^payroll/deletebank/(\d+)/$',deletebank),
    ('^payroll/editbank/(\d+)/$',editbank),
    ('^payroll/computepayroll/$',computepayroll),
    ('^payroll/printtobank/$',printtobank),
    ('^payroll/printschedule/$',printschedule),
    ('^payroll/payslip/$',printpayslip),
    ('^payroll/payslipall/$',printpayslipall),
    ('^payroll/deductionreport/$',deductionreport),
    ('^payroll/deductionajax/$',payrolldeductionajax),
    ('^payroll/printtopension/$',printtopension),
    ('^payroll/getworkedday/$',getworkedday),#bankajax
    ('^payroll/bankajax/$',bankajax),
    ('^payroll/getbank/$',getbank),
    ('^payroll/printtostate/$',printtostate),#printsavings
    ('^payroll/printloanschedule/$',printloanschedule),
    ('^payroll/printsavings/$',printsavings),
    ('^payroll/monthlyjournal/$',monthlyjournal),

    ('^query/unauto/$',queryunauto),
    ('^query/setup/$',querysetup),
    ('^query/editquery/(\d+)/$',editquerysetup),
    ('^query/deletesetup/(\d+)/$',deletequerysetup),
    ('^query/staffquery/$',staffquery),
    ('^query/successful/$',opsuccessfullquery),
    ('^query/report/$',queryreport),
    ('^query/staffajaxquery/$',staffajaxquery),
    ('^query/deletequery/(\d+)/$',deletegivenquery),
    ('^query/getquerysetup/$',getquerysetup),

    ('^contract/contractstaff/$',contractstaff),
    ('^contract/getcontract/$',getcontract),
    ('^contract/editcontract/(\d+)/$',editcontract),
    ('^contract/deletecontract/(\d+)/$',deletecontract),#contractschedule
    ('^contract/computepayrollcontract/$',computepayrollcontract),#contracttobank
    ('^contract/contractschedule/$',contractschedule),
    ('^contract/contracttobank/$',contracttobank),
     #SYSTEM ADMIN
    ('^sysadmin/unauto/$',adminunauto),
    ('^sysadmin/enteradmin/$',enteradmin),
    ('^sysadmin/createuser/$',createuser),
    ('^sysadmin/edituser/(\d+)/$',edituser),#getuseraccount
    ('^sysadmin/resetuser/$',resetuser),
    ('^sysadmin/getuseraccount/$',getuseraccount),
   # ('^sysadmin/printuser/$',printuser),
    (r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT}),
)
