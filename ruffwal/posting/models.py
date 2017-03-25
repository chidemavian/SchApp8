from django.db import models
from datetime import datetime, timedelta
#from ruffwal import settings
# Create your models here.
class tbltemp(models.Model):
    cusname = models.CharField("Cus name",max_length = 350,null = False )
    cuscode = models.CharField("Cus code",max_length = 150,null = False )
    amount = models.DecimalField('Amount',max_digits = 20 , decimal_places = 2, null = True )
    particular = models.CharField("Particular",max_length = 450,null = False )
    transdate = models.DateField(blank=True)
    accname = models.CharField("Acc Name",max_length = 350,null = False )
    acccode = models.CharField("Acc Code",max_length = 150,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )
    drcr = models.CharField("DrCr",max_length = 50,null = False )
    invoiceno = models.CharField("Invoice No",max_length = 50,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s' % (self.cusname,self.cuscode,self.amount,self.particular,self.transdate,self.accname,self.acccode,self.userid,self.drcr)
    class Meta:
        ordering =['-transdate',]
        verbose_name_plural = "Temporary Posting Table"
class tbltransaction(models.Model):
    accname = models.CharField("Acc name",max_length = 150,null = False )
    acccode = models.CharField("Acc code",max_length = 150,null = False )
    debit = models.DecimalField('Debit',max_digits = 20 , decimal_places = 2, null = True )
    credit = models.DecimalField('Credit',max_digits = 20 , decimal_places = 2, null = True )
    balance = models.DecimalField('Balance',max_digits = 20 , decimal_places = 2, null = True )
    transid = models.CharField('Trans Id',max_length = 150,null = False)
    transdate = models.DateField(blank=True)
    particulars = models.CharField("Particular",max_length = 550,null = False )
    refno = models.CharField("Ref No",max_length = 50,null = False )
    groupname = models.CharField("Group Name",max_length = 80,null = False )
    subname = models.CharField("Sub Name",max_length = 150,null = False )
    userid = models.CharField("User Id",max_length = 80,null = False )
    recid = models.IntegerField()

    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.accname,self.acccode,self.debit,self.credit,self.balance,self.transid,self.transdate,self.particulars,self.refno,self.groupname,self.subname,self.userid,self.recid)
    class Meta:
        ordering =['transdate','id']
        verbose_name_plural = "Transaction Table"

class tbltempreceipt(models.Model):
    cusname = models.CharField("Cus name",max_length = 350,null = False )
    cuscode = models.CharField("Cus code",max_length = 150,null = False )
    amount = models.DecimalField('Amount',max_digits = 20 , decimal_places = 2, null = True )
    particular = models.CharField("Particular",max_length = 450,null = False )
    transdate = models.DateField(blank=True)#auto_now_add=True,
    accname = models.CharField("Acc Name",max_length = 350,null = False )
    acccode = models.CharField("Acc Code",max_length = 150,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )
    drcr = models.CharField("DrCr",max_length = 50,null = False )
    invoiceno = models.CharField("Invoice No",max_length = 50,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s' % (self.cusname,self.cuscode,self.amount,self.particular,self.transdate,self.accname,self.acccode,self.userid,self.drcr)
    class Meta:
        ordering =['-transdate',]
        verbose_name_plural = "Temporary Receipt Table"

class tbltemppayment(models.Model):
    cusname = models.CharField("Cus name",max_length = 350,null = False )
    cuscode = models.CharField("Cus code",max_length = 150,null = False )
    amount = models.DecimalField('Amount',max_digits = 20 , decimal_places = 2, null = True )
    particular = models.CharField("Particular",max_length = 450,null = False )
    transdate = models.DateField(blank=True)#auto_now_add=True,
    accname = models.CharField("Acc Name",max_length = 350,null = False )
    acccode = models.CharField("Acc Code",max_length = 150,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )
    drcr = models.CharField("DrCr",max_length = 50,null = False )
    invoiceno = models.CharField("Invoice No",max_length = 50,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s' % (self.cusname,self.cuscode,self.amount,self.particular,self.transdate,self.accname,self.acccode,self.userid,self.drcr)
    class Meta:
        ordering =['-transdate',]
        verbose_name_plural = "Temporary Payment Table"

class tbljournal(models.Model):
    accname = models.CharField("Cus name",max_length = 350,null = False )
    acccode = models.CharField("Cus code",max_length = 150,null = False )
    particular = models.CharField("Particular",max_length = 450,null = False )
    transdate = models.DateField(blank=True)#auto_now_add=True,
    dr = models.DecimalField('Amount',max_digits = 20 , decimal_places = 2, null = False )
    cr = models.DecimalField('Amount',max_digits = 20 , decimal_places = 2, null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )
    refno = models.CharField("Invoice No",max_length = 50,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s ' % (self.accname,self.acccode,self.particular,self.transdate,self.dr,self.cr,self.refno,self.userid)
    class Meta:
        ordering =['-transdate',]
        verbose_name_plural = "Temporary Journal Table"

class tblstandard(models.Model):
    accname = models.CharField("Acc name",max_length = 350,null = False )
    acccode = models.CharField("Acc code",max_length = 150,null = False )
    particular = models.CharField("Particular",max_length = 450,null = False )
    amount = models.DecimalField('Amount',max_digits = 20 , decimal_places = 2, null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )
    refno = models.CharField("Invoice No",max_length = 50,null = False )
    craccname = models.CharField("Cus name",max_length = 350,null = False )
    cracccode = models.CharField("Cus code",max_length = 150,null = False )
    duration = models.IntegerField(max_length = 11)


    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s' % (self.accname,self.acccode,self.particular,self.amount,self.userid,self.refno,self.craccname,self.cracccode,self.duration)
    class Meta:
        ordering =['acccode',]
        verbose_name_plural = "Temporary Standard Journal Table"

class tblstandarddate(models.Model):
    transdate = models.DateField(blank=True)
    userid = models.CharField("User Id",max_length = 150,null = False )



    def __unicode__(self):
        return  u'%s %s' % (self.transdate,self.userid)
    class Meta:
        ordering =['-id',]
        verbose_name_plural = "Standard Posted"

class tbltemppocket(models.Model):
    cusname = models.CharField("Cus name",max_length = 350,null = False )
    cuscode = models.CharField("Cus code",max_length = 150,null = False )
    amount = models.DecimalField('Amount',max_digits = 20 , decimal_places = 2, null = True )
    particular = models.CharField("Particular",max_length = 450,null = False )
    transdate = models.DateField(blank=True)#auto_now_add=True,
    accname = models.CharField("Acc Name",max_length = 350,null = False )
    acccode = models.CharField("Acc Code",max_length = 150,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )
    drcr = models.CharField("DrCr",max_length = 50,null = False )
    invoiceno = models.CharField("Invoice No",max_length = 50,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s' % (self.cusname,self.cuscode,self.amount,self.particular,self.transdate,self.accname,self.acccode,self.userid,self.drcr)
    class Meta:
        ordering =['-transdate',]
        verbose_name_plural = "Temporary Pocket Money Table"

