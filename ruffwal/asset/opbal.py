# this module is to get the opening balance of any account number by supplying account number,start date,account type
from myproject.ruffwal.posting.models import tbltransaction
from myproject.ruffwal.asset.models import *
from django.db.models import Max,Sum
import locale
locale.setlocale(locale.LC_ALL,'')

def getopbal1(acccode,varstart):
    opbal = 0
    if tblassetcost.objects.filter(acccode = acccode,transdate__lt = varstart).count() == 0:
        opbal = 0
    else:
        getdata = tblassetcost.objects.filter(acccode = acccode,transdate__lt = varstart).aggregate(Sum('amount'))
        debit = getdata['amount__sum']
        opbal = float(debit)
    return  opbal

def getcurrentbalance1(acccode,varstart,varend):
    opbal = 0
    if tblassetcost.objects.filter(acccode = acccode,transdate__range=(varstart,varend)).count() == 0:
        opbal = 0
    else:
        getdata = tblassetcost.objects.filter(acccode = acccode,transdate__range=(varstart,varend)).aggregate(Sum('amount'))
        debit = getdata['amount__sum']
        opbal = float(debit)
    return  opbal


def getopbal(acccode,varstart,groupname,groupcode):
    opbal = 0
    if tbltransaction.objects.filter(acccode = acccode,transdate__lt = varstart).count() == 0:
        opbal = 0
    else:
        getdata = tbltransaction.objects.filter(acccode = acccode,transdate__lt = varstart).aggregate(Sum('debit'),Sum('credit'))
        debit = getdata['debit__sum']
        credit = getdata['credit__sum']
        if groupcode=='10000' or groupcode=='80000' or groupcode=='90000':
            opbal = debit - credit
        else:
            opbal = credit - debit
    return  opbal

def getcurrentbalance(acccode,varstart,varend,groupname,groupcode):
    opbal = 0
    if tbltransaction.objects.filter(acccode = acccode,transdate__range=(varstart,varend)).count() == 0:
        opbal = 0
    else:
        getdata = tbltransaction.objects.filter(acccode = acccode,transdate__range=(varstart,varend)).aggregate(Sum('debit'),Sum('credit'))
        debit = getdata['debit__sum']
        credit = getdata['credit__sum']
        if groupcode=='10000' or groupcode=='80000' or groupcode=='90000':
            opbal = debit - credit
        else:
            opbal = credit - debit
    return  opbal

def getopendep(startyear,thisyear,acccode,deprate,groupname,groupcode):
    q = 0
    p = 0
    rate = deprate/100
    k = int(startyear)
    l = int(thisyear)
    j = 0
    if k == l:
        return  p
    while j == 0:
        opbal = 0
        if tbltransaction.objects.filter(acccode = acccode,transdate__year=k).count() == 0:
            opbal = 0
        else:
            getdata = tbltransaction.objects.filter(acccode = acccode,transdate__year=k).aggregate(Sum('debit'),Sum('credit'))
            debit = getdata['debit__sum']
            credit = getdata['credit__sum']
            if groupcode=='10000' or groupcode=='80000' or groupcode=='90000':
                opbal = debit - credit
            else:
                opbal = credit - debit
        q += opbal

        d = float(rate) * float(q)
        p += d
        k += 1
        if k == l:
            j = 1
        else:
            j = 0
    return  p

def getbal1(acccode):
    opbal = 0
    if tblassetcost.objects.filter(acccode = acccode).count() == 0:
        opbal = 0
    else:
        getdata = tblassetcost.objects.filter(acccode = acccode).aggregate(Sum('amount'))
        debit = getdata['amount__sum']
        opbal = float(debit)
    return  opbal


def getbal(acccode,groupcode):
    opbal = 0
    if tbltransaction.objects.filter(acccode = acccode).count() == 0:
        opbal = 0
    else:
        getdata = tbltransaction.objects.filter(acccode = acccode).aggregate(Sum('debit'),Sum('credit'))
        debit = getdata['debit__sum']
        credit = getdata['credit__sum']
        if groupcode=='10000' or groupcode=='80000' or groupcode=='90000':
            opbal = debit - credit
        else:
            opbal = credit - debit
    return  opbal


