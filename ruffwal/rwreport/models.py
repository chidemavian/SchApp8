from django.db import models
from datetime import datetime, timedelta
#from ruffwal import settings

class tbltrialbalance(models.Model):

    accname = models.CharField("Acc name",max_length = 150,null = False )
    acccode = models.CharField("Acc code",max_length = 150,null = False )
    debit = models.DecimalField('Debit',max_digits = 20 , decimal_places = 2, null = True )
    credit = models.DecimalField('Credit',max_digits = 20 , decimal_places = 2, null = True )
    startdate = models.DateField(blank=True)
    enddate = models.DateField(blank=True)
    groupcode = models.CharField("Group Code",max_length = 50,null = False )
    groupname = models.CharField("Group Name",max_length = 80,null = False )
    subname = models.CharField("Sub Name",max_length = 150,null = False )
    subcode = models.CharField("Sub Code",max_length = 550,null = False )
    userid = models.CharField("User Id",max_length = 80,null = False )
    recreport = models.CharField("Report Acc",max_length = 80,null = False )
    disamt = models.CharField("Display Amount DEBIT",max_length = 180,null = False )
    disamt2 = models.CharField("Display Amount CREDIT",max_length = 180,null = False )
    disgrp = models.CharField("Display Group",max_length = 280,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.accname,self.acccode,self.debit,self.credit,self.startdate,self.enddate,self.groupcode,self.groupname,self.subcode,self.subname,self.recreport,self.userid,self.disamt,self.disgrp)
    class Meta:
        ordering =['groupcode',]
        verbose_name_plural = "Trialbalance"

class tblprofitloss(models.Model):

    sortid = models.IntegerField("Sort Code",max_length = 150,null = False )
    accname = models.CharField("Acc code",max_length = 150,null = False )
    amount = models.DecimalField('Amount',max_digits = 20 , decimal_places = 2, null = True )
    groupname = models.CharField("Group Name",max_length = 80,null = False )
    userid = models.CharField("User Id",max_length = 80,null = False )
    startdate = models.DateField(blank=True)
    enddate = models.DateField(blank=True)
    disamt = models.CharField("Display Amount",max_length = 180,null = False )
    disgrp = models.CharField("Display Group",max_length = 280,null = False )



    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s' % (self.sortid,self.accname,self.amount,self.groupname,self.userid,self.startdate,self.enddate,self.disamt,self.disgrp)
    class Meta:
        ordering =['sortid','groupname']
        verbose_name_plural = "Profit And Loss"

class tblbalancesheet(models.Model):

    sortid = models.IntegerField("Sort Code",max_length = 150,null = False )
    accname = models.CharField("Acc code",max_length = 150,null = False )
    amount = models.DecimalField('Amount',max_digits = 20 , decimal_places = 2, null = True )
    amount2 = models.DecimalField('Amount2',max_digits = 20 , decimal_places = 2, null = True )
    groupname = models.CharField("Group Name",max_length = 80,null = False )
    userid = models.CharField("User Id",max_length = 80,null = False )
    startdate = models.DateField(blank=True)
    enddate = models.DateField(blank=True)
    disamt = models.CharField("Display Amount",max_length = 80,null = False )#comma separated value
    disamt2 = models.CharField("Display2 Amount",max_length = 80,null = False )#comma separated value
    disgrp = models.CharField("Display Group",max_length = 180,null = False )#comma separated value


    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s %s %s' % (self.sortid,self.accname,self.amount,self.amount2,self.groupname,self.userid,self.startdate,self.enddate,self.disamt,self.disamt2,self.disgrp)
    class Meta:
        ordering =['sortid','groupname']
        verbose_name_plural = "Balance Sheet"

class tblreceiavables(models.Model):

    accname = models.CharField("Acc name",max_length = 350,null = False )
    acccode = models.CharField("Acc code",max_length = 150,primary_key= True,null = False )
    accbal = models.DecimalField('Acc Bal',max_digits = 20 , decimal_places = 2, null = False )
    groupname = models.CharField("Groupname",max_length = 150,null = False )
    groupcode = models.CharField("Groupcode",max_length = 150,null = False )
    datecreated = models.DateTimeField()
    subgroupname = models.CharField("Subgroupname",max_length = 150,null = False )
    subgroupcode = models.CharField("Subgroupcode",max_length = 150,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )
    accstatus = models.CharField("Acc Status",max_length = 70,null = False )
    recreport = models.CharField("Report Acc",max_length = 50,null = False )
    lasttrandate = models.CharField("Last Trans Date",max_length = 150,null = False )
    disamt = models.CharField("Display Amount",max_length = 80,null = False )#comma separated value
    disgrp = models.CharField("Display Group",max_length = 280,null = False )#comma separated value




    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s %s %s' % (self.accname,self.acccode,self.accbal,self.groupname,self.groupcode,self.datecreated,self.subgroupname,self.subgroupcode,self.userid,self.disamt,self.disgrp)
    class Meta:
        ordering =['groupcode','acccode',]
        verbose_name_plural = "Receivables"

class tblpayable(models.Model):

    accname = models.CharField("Acc name",max_length = 350,null = False )
    acccode = models.CharField("Acc code",max_length = 150,primary_key= True,null = False )
    accbal = models.DecimalField('Acc Bal',max_digits = 20 , decimal_places = 2, null = False )
    groupname = models.CharField("Groupname",max_length = 150,null = False )
    groupcode = models.CharField("Groupcode",max_length = 150,null = False )
    datecreated = models.DateTimeField()
    subgroupname = models.CharField("Subgroupname",max_length = 150,null = False )
    subgroupcode = models.CharField("Subgroupcode",max_length = 150,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )
    accstatus = models.CharField("Acc Status",max_length = 70,null = False )
    recreport = models.CharField("Report Acc",max_length = 50,null = False )
    lasttrandate = models.CharField("Last Trans Date",max_length = 150,null = False )
    disamt = models.CharField("Display Amount",max_length = 80,null = False )#comma separated value
    disgrp = models.CharField("Display Group",max_length = 280,null = False )#comma separated value

    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s %s %s' % (self.accname,self.acccode,self.accbal,self.groupname,self.groupcode,self.datecreated,self.subgroupname,self.subgroupcode,self.userid,self.disamt,self.disgrp)
    class Meta:
        ordering =['groupcode','acccode',]
        verbose_name_plural = "Payables"

class tblstockrep(models.Model):

    stockname = models.CharField("Stock name",max_length = 350,null = False )
    acccode = models.CharField("Acc code",max_length = 150,primary_key= True,null = False )
    accbal = models.DecimalField('Acc Bal',max_digits = 20 , decimal_places = 2, null = True )
    datecreated = models.DateTimeField(auto_now_add=True, blank=True)
    subname = models.CharField("Subgroupname",max_length = 150,null = False )
    subcode = models.CharField("Subgroupcode",max_length = 150,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )
    qtybal = models.DecimalField('Qty Bal',max_digits = 20 , decimal_places = 2, null = True )
    disbal = models.CharField("Display Balance",max_length = 150,null = False )
    disqty = models.CharField("Display Quantity",max_length = 150,null = False )
    disgrp = models.CharField("Display Group",max_length = 280,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s %s %s' % (self.stockname,self.acccode,self.accbal,self.datecreated,self.subname,self.subcode,self.userid,self.qtybal,self.disbal,self.disqty,self.disgrp)
    class Meta:
        ordering =['acccode',]
        verbose_name_plural = "Stock Report"

class tblstatement(models.Model):

    accname = models.CharField("Acc name",max_length = 150,null = False )
    acccode = models.CharField("Acc code",max_length = 150,null = False )
    debit = models.DecimalField('Debit',max_digits = 20 , decimal_places = 2, null = True )
    credit = models.DecimalField('Credit',max_digits = 20 , decimal_places = 2, null = True )
    balance = models.DecimalField('Balance',max_digits = 20 , decimal_places = 2, null = True )
    transdate = models.DateField(blank=True)
    particulars = models.CharField("Particular",max_length = 550,null = False )
    refno = models.CharField("Ref No",max_length = 50,null = False )
    groupname = models.CharField("Group Name",max_length = 80,null = False )
    disdebit = models.CharField("Display Debit",max_length = 150,null = False )
    discredit = models.CharField("Display Credit",max_length = 180,null = False )
    disbal = models.CharField("Display Balance",max_length = 180,null = False )
    disgrp = models.CharField("Display Balance",max_length = 180,null = False )
    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.accname,self.acccode,self.debit,self.credit,self.balance,self.transdate,self.particulars,self.refno,self.groupname,self.disdebit,self.discredit,self.disbal,self.disgrp)
    class Meta:
        ordering =['id',]
        verbose_name_plural = "Statement Of Account"

class tblvalue(models.Model):

    name = models.CharField("Name",max_length = 250,null = False )
    recamount = models.CharField("Amount",max_length = 150,null = False )
    perc = models.CharField("Percentage",max_length = 50,null = False )
    disgrp = models.CharField("Display Balance",max_length = 180,null = False )
    transdate = models.DateField(blank=True)
    disgrp1 = models.CharField("Display Group",max_length = 180,null = False )


    def __unicode__(self):
        return  u'%s %s %s %s %s %s '% (self.name,self.recamount,self.perc,self.disgrp,self.transdate,self.disgrp1)
    class Meta:
        ordering =['id',]
        verbose_name_plural = "Statement Of Value Added"