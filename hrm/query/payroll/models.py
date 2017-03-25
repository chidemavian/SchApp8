from django.db import models

# Create your models here.
class tblbankdetails(models.Model):
    staffid = models.CharField("staffid",max_length = 150,null = False )
    staffname = models.CharField("staffname",max_length = 350,null = False )
    bankname = models.CharField("bank name",max_length = 350,null = False )
    accountno = models.CharField("account no",max_length = 250,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u' %s %s %s %s %s' % (self.staffid,self.staffname,self.bankname,self.accountno,self.userid)
    class Meta:
        ordering =['staffid']
        verbose_name_plural = "STAFF BANK DETAILS"

class tblpayroll(models.Model):
    staffid = models.CharField("staffid",max_length = 150,null = False )
    staffname = models.CharField("staffname",max_length = 450,null = False )
    designation = models.CharField("Designation",max_length = 450,null = False )
    allamount = models.DecimalField('Allowance',max_digits = 20 , decimal_places = 2, null = True )
    alldes = models.CharField("All. Desription",max_length = 150,null = False )
    dedamount = models.DecimalField('Deduction',max_digits = 20 , decimal_places = 2, null = True )
    deddes = models.CharField("Ded.. Desription",max_length = 150,null = False )
    schamount = models.DecimalField('Allowance',max_digits = 20 , decimal_places = 2, null = True )
    schdes = models.CharField("All. Desription",max_length = 150,null = False )
    outbal = models.DecimalField('Oustanding Balance',max_digits = 20 , decimal_places = 2, null = True )
    wokingday = models.IntegerField(max_length = 3)#working days
    recday = models.IntegerField(max_length = 3)
    recmonth = models.IntegerField(max_length = 3)
    recyear = models.IntegerField(max_length = 4)
    recdate = models.DateField()
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u' %s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.staffid,self.staffname,self.allamount,self.alldes,self.dedamount,self.deddes,self.schamount,self.schdes,self.wokingday,self.recday,self.recmonth,self.recyear,self.recdate)
    class Meta:
        ordering =['id']
        verbose_name_plural = "PAYROLL"

class tblpayrollpension(models.Model):
    staffid = models.CharField("staffid",max_length = 150,null = False )
    employeeamount = models.DecimalField('Employee Contribution',max_digits = 20 , decimal_places = 2, null = True )
    employeramount = models.DecimalField('Employer Contribution',max_digits = 20 , decimal_places = 2, null = True )
    recdate = models.DateField()
    recday = models.IntegerField(max_length = 3)
    recmonth = models.IntegerField(max_length = 3)
    recyear = models.IntegerField(max_length = 4)

    def __unicode__(self):
        return  u' %s %s %s %s' % (self.staffid,self.employeeamount,self.employeramount,self.recdate)
    class Meta:
        ordering =['id']
        verbose_name_plural = "Payroll Pension"
