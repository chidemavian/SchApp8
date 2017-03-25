from django.db import models

# Create your models here.
class upresentedtrans(models.Model):

    accname = models.CharField("Acc name",max_length = 150,null = False )
    acccode = models.CharField("Acc code",max_length = 150,null = False )
    debit = models.DecimalField('Debit',max_digits = 20 , decimal_places = 2, null = True )
    credit = models.DecimalField('Credit',max_digits = 20 , decimal_places = 2, null = True )
    balance = models.DecimalField('Balance',max_digits = 20 , decimal_places = 2, null = True )
    transdate = models.DateField(blank=True)
    particulars = models.CharField("Particular",max_length = 550,null = False )
    refno = models.CharField("Ref No",max_length = 50,null = False )
    userid = models.CharField("User Id",max_length = 80,null = False )
    opeaningbal = models.CharField("Opeaning Bal",max_length = 80,null = False )


    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s %s ' % (self.accname,self.acccode,self.debit,self.credit,self.balance,self.transdate,self.particulars,self.refno,self.userid,self.opeaningbal)
    class Meta:
        ordering =['transdate','id']
        verbose_name_plural = "Unpresented"

class upresentedtranstemp(models.Model):

    accname = models.CharField("Acc name",max_length = 150,null = False )
    acccode = models.CharField("Acc code",max_length = 150,null = False )
    amount = models.DecimalField('Amount',max_digits = 20 , decimal_places = 2, null = True )
    particulars = models.CharField("Particular",max_length = 550,null = False )
    refno = models.CharField("Ref No",max_length = 50,null = False )
    userid = models.CharField("User Id",max_length = 80,null = False )
    transdate = models.DateField(blank=True)


    def __unicode__(self):
        return  u'%s %s %s %s %s %s' % (self.accname,self.acccode,self.amount,self.particulars,self.refno,self.userid)
    class Meta:
        ordering =['id',]
        verbose_name_plural = "Unpresented Temp"

class uncreditedtrans(models.Model):

    accname = models.CharField("Acc name",max_length = 150,null = False )
    acccode = models.CharField("Acc code",max_length = 150,null = False )
    debit = models.DecimalField('Debit',max_digits = 20 , decimal_places = 2, null = True )
    credit = models.DecimalField('Credit',max_digits = 20 , decimal_places = 2, null = True )
    balance = models.DecimalField('Balance',max_digits = 20 , decimal_places = 2, null = True )
    transdate = models.DateField(blank=True)
    particulars = models.CharField("Particular",max_length = 550,null = False )
    refno = models.CharField("Ref No",max_length = 50,null = False )
    userid = models.CharField("User Id",max_length = 80,null = False )
    opeaningbal = models.CharField("Opeaning Bal",max_length = 80,null = False )


    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s %s  ' % (self.accname,self.acccode,self.debit,self.credit,self.balance,self.transdate,self.particulars,self.refno,self.userid,self.opeaningbal)
    class Meta:
        ordering =['id',]
        verbose_name_plural = "Uncredited Transaction"

class upcreditedtranstemp(models.Model):

    accname = models.CharField("Acc name",max_length = 150,null = False )
    acccode = models.CharField("Acc code",max_length = 150,null = False )
    amount = models.DecimalField('Amount',max_digits = 20 , decimal_places = 2, null = True )
    particulars = models.CharField("Particular",max_length = 550,null = False )
    refno = models.CharField("Ref No",max_length = 50,null = False )
    userid = models.CharField("User Id",max_length = 80,null = False )
    transdate = models.DateField(blank=True)



    def __unicode__(self):
        return  u'%s %s %s %s %s %s' % (self.accname,self.acccode,self.amount,self.particulars,self.refno,self.userid)
    class Meta:
        ordering =['id',]
        verbose_name_plural = "Uncredited  Temp"

class reconstate(models.Model):
    name = models.CharField("Name",max_length = 150,null = False )
    amount = models.CharField("Amount",max_length = 150,null = False )
    dispgr = models.CharField("Display",max_length = 550,null = False )
    transdate = models.DateField(blank=True)


    def __unicode__(self):
        return  u'%s %s %s %s' % (self.name,self.amount,self.dispgr,self.transdate)
    class Meta:
        ordering =['id',]
        verbose_name_plural = "Recon Statement"