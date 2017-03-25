from django.db import models
from datetime import datetime, timedelta


class tblrollover(models.Model):

    recyear = models.IntegerField()
    recamount = models.DecimalField('Credit',max_digits = 20 , decimal_places = 2, null = True )
    recdate = models.DateField(blank=True)
    userid = models.CharField("User Id",max_length = 80,null = False )


    def __unicode__(self):
        return  u'%s %s %s %s ' % (self.recyear,self.recamount,self.recdate,self.userid)
    class Meta:
        ordering =['recyear',]
        verbose_name_plural = "Roll Over"

class tbluseracc(models.Model):
    username = models.CharField("Username",max_length = 160,null = False )
    password = models.CharField("Password",max_length = 50,null = False )
    recdate = models.DateTimeField(auto_now_add=True, blank=True)
    expiredate = models.DateTimeField()
    staffname = models.CharField("Staff Name",max_length = 250,null = False,default= '0')
    createacc = models.CharField("Create Account",max_length = 50,null = False,default= '0')
    inventory = models.CharField("Create Inventory",max_length = 50,null = False,default= '0')
    payables = models.CharField("Create Payables",max_length = 50,null = False,default= '0')
    receivables = models.CharField("Create Payables",max_length = 50,null = False,default= '0')
    #posting
    invoice = models.CharField("Invoice",max_length = 50,null = False,default= '0')
    receipt = models.CharField("Receipt",max_length = 50,null = False,default= '0')
    payment = models.CharField("Payment",max_length = 50,null = False,default= '0')
    genledger = models.CharField("General Ledger",max_length = 50,null = False,default= '0')
    standardledger = models.CharField("Standard Ledger",max_length = 50,null = False,default= '0')
     #Inventory
    stockin = models.CharField("Stock In",max_length = 50,null = False,default= '0')
    stockout = models.CharField("Stock Out",max_length = 50,null = False,default= '0')
    stockreport = models.CharField("Stock Report",max_length = 50,null = False,default= '0')
    #Work in progess
    jobsetup = models.CharField("Job Setup",max_length = 50,null = False,default= '0')
    addsetup = models.CharField("Additional Setup",max_length = 50,null = False,default= '0')
    jobcosting = models.CharField("Create Payables",max_length = 50,null = False,default= '0')
    returnmat = models.CharField("Return Item",max_length = 50,null = False,default= '0')
    wipinvoice = models.CharField("Invoice",max_length = 50,null = False,default= '0')
    wipreport = models.CharField("Report",max_length = 50,null = False,default= '0')
     #Reconciliation
    unpresented = models.CharField("Unpresented",max_length = 50,null = False,default= '0')
     #Report
    statutory = models.CharField("Statutory Report",max_length = 50,null = False,default= '0')
      #System Admin
    createuser = models.CharField("Create User",max_length = 50,null = False,default= '0')
    resetuser = models.CharField("Reset User",max_length = 50,null = False,default= '0')
    userreport = models.CharField("User Report",max_length = 50,null = False,default= '0')
    rollover = models.CharField("RollOver",max_length = 50,null = False,default= '0')
    #welcome page
    esetup = models.CharField( "Setup",max_length = 50,null = False,default= '0')
    eposting = models.CharField("Posting",max_length = 50,null = False,default= '0')
    einventory = models.CharField("Inventory",max_length = 50,null = False,default= '0')
    ewip = models.CharField("WIP",max_length = 50,null = False,default='0')
    ereonciliation = models.CharField("Reconciliation",max_length = 50,null = False,default= '0')
    ereport = models.CharField("Report",max_length = 50,null = False,default='0')
    eadmin = models.CharField("Admin",max_length = 50,null = False,default='0')
    #
    status = models.CharField("Status",max_length = 50,null = False,default= '0')
    userid = models.CharField("User Id",max_length = 80,null = False ,default='0')


    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s %s' % (self.username,self.password,self.recdate,self.staffname,self.esetup,self.eposting,self.einventory,self.ereonciliation,self.ereport,self.eadmin)
    class Meta:
        ordering =['-recdate',]
        verbose_name_plural = "User Account"

class tblcalender(models.Model):
    startmonth = models.DateField('Start Year')
    endtmonth = models.DateField('End Year')


    def __unicode__(self):
        return  u'%s %s' % (self.startmonth,self.endtmonth)
    class Meta:
        ordering =['id',]
        verbose_name_plural = "Company Calender"

class tblcontrol(models.Model):
    acccode = models.CharField("Account Code",max_length = 80,null = False )

    def __unicode__(self):
        return  u'%s' % (self.acccode)
    class Meta:
        ordering =['id',]
        verbose_name_plural = "Control Account"