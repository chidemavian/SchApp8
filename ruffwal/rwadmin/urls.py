from django.conf.urls.defaults import patterns, url
urlpatterns = patterns('myproject.ruffwal.rwadmin.views',
    # Examples:
    url(r'^unauto/$',"adminunauto"),
    url(r'^enteradmin/$',"enteradmin"),
    url(r'^createuser/$',"createuser"),
    url(r'^edituser/(\d+)/$',"edituser"),
    url(r'^resetuser/$',"resetuser"),
    url(r'^printuser/$',"printuser"),
    url(r'^accrollover/$',"accrollover"),
    url(r'^removetrans/$',"deletetrans"),
    url(r'^confirmaccrollover/$',"confirmaccrollover"),
    url(r'^getuseraccountrw/$',"getuseraccountrw"),
    url(r'^delete-transaction/$', "verifytransview"),
    url(r'^remove/(\w+)/$', "deletetransaction"),
    url(r'^confirm-deletion/(\w+)/$', "confirmdeletion"),
    url(r'^view-transaction/$', "transactionsview"),
    url(r'^verify_transaction/(\w+)/$',"verifyview"),


)
