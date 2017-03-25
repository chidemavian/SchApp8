# this module is to get the opening balance of any account number by supplying account number,start date,account type
from myproject.ruffwal.posting.models import tbltransaction
from myproject.ruffwal.rsetup.models import *
from django.db.models import Max,Sum
import locale
locale.setlocale(locale.LC_ALL,'')
def getopbal(acccode,varstart,groupname):
    opbal = 0
    if tbltransaction.objects.filter(acccode = acccode,transdate__lt = varstart).count() == 0:
        opbal = 0
    else:
        getdata = tbltransaction.objects.filter(acccode = acccode,transdate__lt = varstart).aggregate(Sum('debit'),Sum('credit'))
        debit = getdata['debit__sum']
        credit = getdata['credit__sum']
        if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS" or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
            opbal = debit - credit
        else:
            opbal = credit - debit
    return  opbal

def getopbalrange(acccode,varstart,varend,groupname):
    opbal = 0
    if tbltransaction.objects.filter(acccode = acccode,transdate__range=(varstart,varend)).count() == 0:
        opbal = 0
    else:
        getdata = tbltransaction.objects.filter(acccode = acccode,transdate__range=(varstart,varend)).aggregate(Sum('debit'),Sum('credit'))
        debit = getdata['debit__sum']
        credit = getdata['credit__sum']
        if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS" or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
            opbal = debit - credit
        else:
            opbal = credit - debit
    return  opbal



def getaccposition(varstart,stmon,cday,varend):#getting P & L
    totgrr2 = 0
    vardata = tblaccount.objects.filter(groupname = 'INCOME',recreport = 'YES').order_by('acccode')
    for j in vardata:
        groupname = j.groupname
        acccode = j.acccode
        accname = j.accname
        if stmon == varstart.month and cday == varstart.day:
            opbal = getopbal(acccode,varstart,groupname)#getting the opening balance
        else:
            opbal = 0
        fdata = tbltransaction.objects.filter(acccode = acccode,transdate__range=(varstart,varend)).order_by('transdate','id')
        for g in fdata:
            debit = g.debit
            credit = g.credit
            if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS"  or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                opbal = opbal + debit - credit
            else:
                opbal = opbal + credit - debit
        totgrr2 += opbal
    #getting cost of sales
    grtotalcos = 0
    vardata = tblaccount.objects.filter(groupname = 'COST OF SALES',recreport = 'YES').order_by('acccode')
    for j in vardata:
        groupname = j.groupname
        acccode = j.acccode
        accname = j.accname
        if stmon == varstart.month and cday == varstart.day:
            opbal = getopbal(acccode,varstart,groupname)#getting the opening balance
        else:
            opbal = 0
        fdata = tbltransaction.objects.filter(acccode = acccode,transdate__range=(varstart,varend)).order_by('transdate','id')
        for g in fdata:
            debit = g.debit
            credit = g.credit
            if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS"  or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                opbal = opbal + debit - credit
            else:
                opbal = opbal + credit - debit
        grtotalcos += opbal
    # getting expenses
    exptotal = 0
    vardata = tblaccount.objects.filter(groupname = 'EXPENSES',recreport = 'YES').order_by('acccode')
    for j in vardata:
        groupname = j.groupname
        acccode = j.acccode
        accname = j.accname
        if stmon == varstart.month and cday == varstart.day:
            opbal = getopbal(acccode,varstart,groupname)#getting the opening balance
        else:
            opbal = 0
        fdata = tbltransaction.objects.filter(acccode = acccode,transdate__range=(varstart,varend)).order_by('transdate','id')
        for g in fdata:
            debit = g.debit
            credit = g.credit
            if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS"  or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                opbal = opbal + debit - credit
            else:
                opbal = opbal + credit - debit
        exptotal += opbal
    totalexp = grtotalcos + exptotal
    pl = totgrr2 - totalexp
    return pl

def getopbaleq(acccode,varstart,groupname):
    opbal = 0
    if tbltransaction.objects.filter(acccode = acccode,transdate__lte = varstart).count() == 0:
        opbal = 0
    else:
        getdata = tbltransaction.objects.filter(acccode = acccode,transdate__lte = varstart).aggregate(Sum('debit'),Sum('credit'))
        debit = getdata['debit__sum']
        credit = getdata['credit__sum']
        if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS" or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
            opbal = debit - credit
        else:
            opbal = credit - debit
    return  opbal

#account balance
def accbalance(acccode):
    opbal = 0
    if tblaccount.objects.filter(acccode = acccode):
        acc = tblaccount.objects.get(acccode = acccode)
        groupname = acc.groupname
        if tbltransaction.objects.filter(acccode = acccode).count() == 0:
            opbal = 0
        else:
            getdata = tbltransaction.objects.filter(acccode = acccode).aggregate(Sum('debit'),Sum('credit'))
            debit = getdata['debit__sum']
            credit = getdata['credit__sum']
            if groupname == "FIXED ASSETS" or groupname == "NON-CURRENT ASSETS" or groupname == "CURRENT ASSETS" or groupname == "EXPENSES" or groupname == "COST OF SALES":
                opbal = debit - credit
            else:
                opbal = credit - debit
    return  opbal







