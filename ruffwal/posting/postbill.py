__author__ = 'metro'

from myproject.ruffwal.rsetup.models import tblaccount
from myproject.ruffwal.posting.models import tbltransaction
from myproject.ruffwal.rsetup.models import tblaccount
from myproject.student.models import *
import datetime

from django.db.models import Max,Sum

def postacc (transdate,draccno,cracccode,amount,particular,transid,varrecid,varuser):
#**************************************************************************DR
    if tblaccount.objects.filter(acccode = draccno):
        pass
    else:
      for j in Student.objects.filter(admissionno = draccno):
          fullname = j.fullname
      used = tblaccount(groupname = "CURRENT ASSETS",groupcode = "30000",subgroupname = "RECEIVABLES",subgroupcode="30200",datecreated = datetime.datetime.today(),userid =varuser,accname = str(fullname).upper(),acccode = draccno,accbal= 0,accstatus ="ACTIVE",recreport ="STUDENTS" )
      used.save()
    cusdet =  tblaccount.objects.get(acccode = draccno)# bank DR student
    cusbal = cusdet.accbal
    cusgrp = cusdet.groupname
    cussub = cusdet.subgroupname
    draccname = cusdet.accname
    custo = amount
    if cusgrp == "FIXED ASSETS" or cusgrp == "CURRENT ASSETS" or cusgrp == "EXPENSES" or cusgrp == "COST OF SALES" or  cusgrp == "NON-CURRENT ASSETS":
        cusbal = cusbal + custo
    else:
        cusbal = cusbal - custo
        #***********************************************
    used = tbltransaction(accname = draccname,acccode = draccno,debit = custo,credit = 0,balance = cusbal,transid = transid,transdate = transdate,particulars = particular,refno = '0000000',groupname = cusgrp,subname = cussub ,userid = varuser,recid = varrecid )
    used.save()
    #********************
    selsubdata = tblaccount.objects.get(acccode = draccno)
    selsubdata.accbal = cusbal
    selsubdata.lasttrandate = transdate
    selsubdata.save()
    #************************************************************* CR
    cusdet1 =  tblaccount.objects.get(acccode = cracccode)# bank DR Income head
    cusbal1 = cusdet1.accbal
    cusgrp1 = cusdet1.groupname
    cussub1 = cusdet1.subgroupname
    craccname = cusdet1.accname
    custo = amount
    if cusgrp1 == "FIXED ASSETS" or cusgrp1 == "CURRENT ASSETS" or cusgrp1 == "EXPENSES" or cusgrp1 == "COST OF SALES" or cusgrp1 == "NON-CURRENT ASSETS":
        cusbal1 = cusbal1 - custo
    else:
        cusbal1 = cusbal1 + custo
        #***********************************************
    used1 = tbltransaction(accname = craccname,acccode = cracccode,debit = 0,credit = custo,balance = cusbal1,transid = transid,transdate = transdate,particulars = particular,refno = '0000000',groupname = cusgrp1,subname = cussub1 ,userid = varuser,recid = varrecid )
    used1.save()
    #********************
    selsubdata1 = tblaccount.objects.get(acccode = cracccode)
    selsubdata1.accbal = cusbal1
    selsubdata1.lasttrandate = transdate
    selsubdata1.save()
    return transid


def getbalreal(acccode):#getting the account balance as at today
    groupcode = tblaccount.objects.get(acccode = acccode).groupcode
    if tbltransaction.objects.filter(acccode = acccode).count() == 0:
        opbal = 0
    else:
        getdata = tbltransaction.objects.filter(acccode = acccode).aggregate(Sum('debit'),Sum('credit'))
        debit = getdata['debit__sum']
        credit = getdata['credit__sum']
        if groupcode=='10000' or groupcode=='30000' or groupcode=='80000' or groupcode=='90000':
            opbal = debit - credit
        else:
            opbal = credit - debit
    return  opbal
