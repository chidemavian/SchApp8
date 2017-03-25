from django.db import models

# Create your models here.

class tblcontractstaff(models.Model):
    staffname = models.CharField("Staff Name",max_length = 350,null = False )
    address = models.CharField("Address",max_length = 450,null = False )
    phoneno = models.CharField("Phone no",max_length = 250,null = False )
    nextofkin = models.CharField("Next of kin",max_length = 350,null = False )
    nextofkinphone = models.CharField("Next Of Kin Phone",max_length = 310,null = False )
    accname = models.CharField("Account Name",max_length = 30,null = False )
    accno = models.CharField("Account Number",max_length = 30,null = False )
    allowance = models.DecimalField('Allowance',max_digits = 20 , decimal_places = 2, null = True )
    deduction = models.DecimalField('Deduction',max_digits = 20 , decimal_places = 2, null = True )
    overtime = models.DecimalField('Overtime',max_digits = 20 , decimal_places = 2, null = True )
    userid = models.CharField("User Id",max_length = 150,null = False )
    def __unicode__(self):
        return  u'%s %s %s %s %s %s ' % (self.staffname,self.address,self.phoneno,self.nextofkin,self.nextofkinphone,self.userid)
    class Meta:
        ordering =['staffname','id']
        verbose_name_plural = "CONTRACT STAFF "

class tblcontractpayroll(models.Model):
    staffname = models.CharField("Staff Name",max_length = 350,null = False )
    accname = models.CharField("Account Name",max_length = 30,null = False )
    accno = models.CharField("Account Number",max_length = 30,null = False )
    allowance = models.DecimalField('Allowance',max_digits = 20 , decimal_places = 2, null = True )
    deduction = models.DecimalField('Deduction',max_digits = 20 , decimal_places = 2, null = True )
    overtime = models.DecimalField('Overtime',max_digits = 20 , decimal_places = 2, null = True )
    recday = models.IntegerField(max_length = 3)
    recmonth = models.IntegerField(max_length = 3)
    recyear = models.IntegerField(max_length = 4)
    recdate = models.DateField()
    userid = models.CharField("User Id",max_length = 150,null = False )
    def __unicode__(self):
        return  u'%s %s %s %s %s %s ' % (self.staffname,self.accname,self.accno,self.recdate,self.allowance,self.deduction)
    class Meta:
        ordering =['staffname','id']
        verbose_name_plural = "CONTRACT STAFF PAYROLL "




