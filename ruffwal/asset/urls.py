from django.conf.urls.defaults import patterns, url
urlpatterns = patterns('myproject.ruffwal.asset.views',
    # Examples:
    url(r'^welcome/$', "enterasset"),
    url(r'^asset-creation/$', "assetregister"),
    url(r'^asset-department/$', "assetdept"),
    url(r'^edit-asset/(\w+)/$', "editasset"),
    url(r'^deleteasset/(\w+)/$', "deleteasset"),
    url(r'^asset-list/$', "assetlist"),
    url(r'^asset-schedule/$', "assetschedule"),
    url(r'^asset-residual-value/$', "residual"),
    url(r'^asset-operation-successful/$', "successful"),
    url(r'^asset-summary/$', "assetsummary"),
    url(r'^access-denied/$', "unauto"),
    url(r'^asset-cost/(\w+)/$', "assetcost"),
    url(r'^remove-cost/(\w+)/$', "remove_cost"),

)
