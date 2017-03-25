from django.db import models
from datetime import datetime, timedelta
# Create your models here.
class tbllg(models.Model):# for branch setup
    lgname = models.CharField("LGname",max_length = 150,null = False )
    lgaddress = models.CharField("Lg Address",max_length = 450,null = False )
    datecreated = models.DateTimeField(auto_now_add=True, blank=True)
    userid = models.CharField("User Id",max_length = 150,null = False )


    def __unicode__(self):
        return  u'%s %s %s %s' % (self.lgname,self.lgaddress,self.datecreated,self.userid)
    class Meta:
        ordering =['-datecreated',]
        verbose_name_plural = "Branch Setup Table"

class tbldepartment(models.Model):
    name = models.CharField("Name",max_length = 180,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s' % (self.name,self.userid)
    class Meta:
        ordering =['name',]
        verbose_name_plural = "Department Table"


class tbldesig(models.Model):
    #desgcode = models.CharField("Code",max_length = 150,null = False )
    desc = models.CharField("Desription",max_length = 150,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s' % (self.desc,self.userid)
    class Meta:
        ordering =['desc',]
        verbose_name_plural = "DESIGNATION Table"


class tblpfa(models.Model):
    accname = models.CharField("PFA name",max_length = 350,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )


    def __unicode__(self):
        return  u'%s %s' % (self.accname,self.userid)
    class Meta:
        ordering =['accname']
        verbose_name_plural = "Pension Admin Fund Table"

class tblbank(models.Model):

    name = models.CharField("Bank name",max_length = 250,null = False )
    sortcode = models.CharField("Sort Code",max_length = 250,null = False,default="00" )
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s' % (self.name,self.userid)
    class Meta:
        ordering =['name',]
        verbose_name_plural = "Bank Table"

class tblcategory(models.Model):
    name = models.CharField("Name",max_length = 190,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s' % (self.name,self.userid)
    class Meta:
        ordering =['name',]
        verbose_name_plural = "Category Table"
class tblcompanyinfo(models.Model):
    name = models.CharField("Name",max_length = 290,null = False )
    address = models.CharField("Address",max_length = 490,null = False )
    picture = models.ImageField(upload_to = 'staff', null=True, blank=True)

    def __unicode__(self):
        return  u'%s %s %s' % (self.name,self.address,self.picture)
    class Meta:
        ordering =['name',]
        verbose_name_plural = "Company Info"

class tblallowance(models.Model):
   # desgcode = models.CharField("Code",max_length = 150,null = False )
    desc = models.CharField("Desription",max_length = 150,null = False )
    amount = models.DecimalField('Allowance',max_digits = 20 , decimal_places = 2, null = True )
    paydes = models.CharField("All. Desription",max_length = 150,null = False )#e.g basic
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s ' % (self.desc,self.amount,self.paydes,self.userid)
    class Meta:
        ordering =['id',]
        verbose_name_plural = "ALLOWANCE Table"

class tbldeduction(models.Model):
    #desgcode = models.CharField("Code",max_length = 150,null = False )
    desc = models.CharField("Desription",max_length = 150,null = False )
    amount = models.DecimalField('Deduction',max_digits = 20 , decimal_places = 2, null = True )
    paydes = models.CharField("Deduction. Desription",max_length = 150,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s ' % (self.desc,self.amount,self.paydes,self.userid)
    class Meta:
        ordering =['id',]
        verbose_name_plural = "DEDUCTION Table"

class tblspall(models.Model):
    staffid = models.CharField("staffid",max_length = 150,null = False )
    staffname = models.CharField("staffname",max_length = 350,null = False )
    amount = models.DecimalField('Allowance',max_digits = 20 , decimal_places = 2, null = True )
    paydes = models.CharField("All. Desription",max_length = 150,null = False )
    duration = models.IntegerField('Duration')
    effectivedate = models.DateField('Effective Date')
    expiredate = models.DateField('Expiring Date')
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s %s ' % (self.staffid,self.staffname,self.amount,self.paydes,self.userid,self.expiredate)
    class Meta:
        ordering =['id']
        verbose_name_plural = "SPECIAL ALLOWANCE"

class tblspecallow(models.Model): #For Special allowance
    name = models.CharField("Description",max_length = 150,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )
    
    def __unicode__(self):
        return  u'%s %s ' % (self.name,self.userid)
    class Meta:
        ordering =['name']
        verbose_name_plural = "Special Allowance Table"

class tblspded(models.Model):
    staffid = models.CharField("staffid",max_length = 150,null = False )
    staffname = models.CharField("staffname",max_length = 350,null = False )
    amount = models.DecimalField('Allowance',max_digits = 20 , decimal_places = 2, null = True )
    paydes = models.CharField("All. Desription",max_length = 150,null = False )
    duration = models.IntegerField('Duration')
    effectivedate = models.DateField('Effective Date')
    expiredate = models.DateField('Expiring Date')
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s ' % (self.staffid,self.staffname,self.amount,self.paydes,self.userid)
    class Meta:
        ordering =['id']
        verbose_name_plural = "SPECIAL DEDUCTION"

class tblcontrol(models.Model):
    datecreated = models.DateField(blank=True)
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s' % (self.datecreated,self.userid)
    class Meta:
        ordering =['id',]
        verbose_name_plural = "System Control Date"

class tblstate(models.Model):
    country = models.CharField("Country",max_length = 150,null = False )
    state = models.CharField("State",max_length = 350,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s' % (self.country,self.state,self.userid)
    class Meta:
        ordering =['country','state']
        verbose_name_plural = "State Table"

class tbllocalgovt(models.Model): #For Local Government
    country = models.CharField("Country",max_length = 150,null = False )
    state = models.CharField("State",max_length = 350,null = False )
    localgovt = models.CharField("Local Government",max_length = 350,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s' % (self.country,self.state,self.localgovt,self.userid)
    class Meta:
        ordering =['country','state']
        verbose_name_plural = "Local Government Table"

class tblhmo(models.Model): #For HMO
    name = models.CharField("Name",max_length = 150,null = False )
    address = models.CharField("Address",max_length = 380,null = False )

    def __unicode__(self):
        return  u'%s %s ' % (self.name,self.address)
    class Meta:
        ordering =['name']
        verbose_name_plural = "HMO Table"

class tblhmoprovide(models.Model): #For HMO
    hmo = models.CharField("hmo",max_length = 150,null = False )
    name = models.CharField("Name",max_length = 150,null = False )
    address = models.CharField("Address",max_length = 380,null = False )

    def __unicode__(self):
        return  u'%s %s  %s ' % (self.hmo,self.name,self.address)
    class Meta:
        ordering =['name']
        verbose_name_plural = "HMO Service Provider"

class tbllevel(models.Model): #For HMO
    level = models.IntegerField()
    userid = models.CharField("User Id",max_length = 150,null = False )
    def __unicode__(self):
        return  u'%s ' %self.level
    class Meta:
        ordering =['level']
        verbose_name_plural = "Level Table"

class tblstep(models.Model): #For HMO
    level = models.IntegerField()
    step = models.IntegerField()
    userid = models.CharField("User Id",max_length = 150,null = False )
    def __unicode__(self):
        return  u'%s %s ' %(self.level,self.step)
    class Meta:
        ordering =['level','step']
        verbose_name_plural = "Step  Table"

class tblspecialdedcode(models.Model): #For HMO
    name = models.CharField("Description",max_length = 150,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )
    class Meta:
        ordering =['name']
        verbose_name_plural = "Special Deduction Code Table"

class tblsavings(models.Model):
    staffid = models.CharField("staffid",max_length = 150,null = False )
    staffname = models.CharField("staffname",max_length = 350,null = False )
    amountbf = models.DecimalField('Allowance',max_digits = 20 , decimal_places = 2, null = True )
    contribution = models.DecimalField('Allowance',max_digits = 20 , decimal_places = 2, null = True )
    paydes = models.CharField("All. Desription",max_length = 150,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s ' % (self.staffid,self.staffname,self.amountbf,self.paydes,self.userid)
    class Meta:
        ordering =['id']
        verbose_name_plural = "SAVING TABLE"

class tblloancode(models.Model): #For HMO
    name = models.CharField("Description",max_length = 150,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )
    def __unicode__(self):
        return  u'%s %s ' % (self.name,self.userid)
    class Meta:
        ordering =['name']
        verbose_name_plural = "Loan Code Table"

class tblloan(models.Model):
    staffid = models.CharField("staffid",max_length = 150,null = False )
    staffname = models.CharField("staffname",max_length = 350,null = False )
    amount = models.DecimalField('Total Amount',max_digits = 20 , decimal_places = 2, null = True )
    paydes = models.CharField("All. Desription",max_length = 150,null = False )
    duration = models.IntegerField('Duration')
    intrate = models.IntegerField('intrate')
    effectivedate = models.DateField('Effective Date')
    expiredate = models.DateField('Expiring Date')
    monthlyepayment = models.DecimalField('Monthly Repayment',max_digits = 20 , decimal_places = 2, null = True )
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s ' % (self.staffid,self.staffname,self.amount,self.paydes,self.userid)
    class Meta:
        ordering =['id']
        verbose_name_plural = "SPECIAL DEDUCTION"

class tblpension(models.Model):
    amount = models.DecimalField('Pension Employee',max_digits = 20 , decimal_places = 2, null = True )
    employeramt = models.DecimalField('Pension Employeer',max_digits = 20 , decimal_places = 2, null = True )

    def __unicode__(self):
        return  u'Pension Rate %s, Employer Rate %s ' %(self.amount,self.employeramt)
    class Meta:
        ordering =['id']
        verbose_name_plural = "PENSION PERCENTAGE TABLE"

class tblsavingcode(models.Model):
    name = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'Savings Contribution Name %s :: '%self.name
    class Meta:
        ordering =['id']
        verbose_name_plural = "CONTRIBUTION NAME"

