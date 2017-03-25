from django.conf.urls.defaults import patterns, url
urlpatterns = patterns('myproject.ruffwal.budget.views',
    # Examples:
    url(r'^enterbudget/$',"enterbudget"),
   # url(r'^unauto/$',"adminunauto"),
    url(r'^createbudget/$',"createbudget"),
    url(r'^getaccinv/$',"budgetcomplete"),
    url(r'^editbudget/(\w+)/$',"editbudget"),
    url(r'^printbudget/$',"printbudget"),
    url(r'^variancereport/$',"budgetvariance"),
    url(r'^create_budget_month/$',"createbudgetmonth"),
    url(r'^getaccinvmonth/$',"budgetcompletemonth"),
    url(r'^print_budget_monthly/$',"printbudgetmonth"),
    url(r'^budget_type/$',"budgettype"),
    url(r'^access-denied/$', "unauto"),


)
