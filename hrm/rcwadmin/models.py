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
    staffname = models.CharField("Staff Name",max_length = 250,null = False )
    createacc = models.CharField("Create Account",max_length = 50,null = False,default= 'False')
    inventory = models.CharField("Create Inventory",max_length = 50,null = False,default= 'False')
    payables = models.CharField("Create Payables",max_length = 50,null = False,default= 'False')
    receivables = models.CharField("Create Payables",max_length = 50,null = False,default= 'False')
    #posting
    invoice = models.CharField("Invoice",max_length = 50,null = False,default= 'False')
    receipt = models.CharField("Receipt",max_length = 50,null = False,default= 'False')
    payment = models.CharField("Payment",max_length = 50,null = False,default= 'False')
    genledger = models.CharField("General Ledger",max_length = 50,null = False,default= 'False')
    standardledger = models.CharField("Standard Ledger",max_length = 50,null = False,default= 'False')
     #Inventory
    stockin = models.CharField("Stock In",max_length = 50,null = False,default= 'False')
    stockout = models.CharField("Stock Out",max_length = 50,null = False,default= 'False')
    stockreport = models.CharField("Stock Report",max_length = 50,null = False,default= 'False')
    #Work in progess
    jobsetup = models.CharField("Job Setup",max_length = 50,null = False,default= 'False')
    addsetup = models.CharField("Additional Setup",max_length = 50,null = False,default= 'False')
    jobcosting = models.CharField("Create Payables",max_length = 50,null = False,default= 'False')
    returnmat = models.CharField("Return Item",max_length = 50,null = False,default= 'False')
    wipinvoice = models.CharField("Invoice",max_length = 50,null = False,default= 'False')
    wipreport = models.CharField("Report",max_length = 50,null = False,default= 'False')
     #Reconciliation
    unpresented = models.CharField("Unpresented",max_length = 50,null = False,default= 'False')
     #Report
    statutory = models.CharField("Statutory Report",max_length = 50,null = False,default= 'False')
      #System Admin
    createuser = models.CharField("Create User",max_length = 50,null = False,default= 'False')
    resetuser = models.CharField("Reset User",max_length = 50,null = False,default= 'False')
    userreport = models.CharField("User Report",max_length = 50,null = False,default= 'False')
    rollover = models.CharField("RollOver",max_length = 50,null = False,default= 'False')
    #welcome page
    esetup = models.CharField( "Setup",max_length = 50,null = False,default= 'False')
    eposting = models.CharField("Posting",max_length = 50,null = False,default= 'False')
    einventory = models.CharField("Inventory",max_length = 50,null = False,default= 'False')
    ewip = models.CharField("WIP",max_length = 50,null = False,default= 'False')
    ereonciliation = models.CharField("Reconciliation",max_length = 50,null = False,default= 'False')
    ereport = models.CharField("Report",max_length = 50,null = False,default= 'False')
    eadmin = models.CharField("Admin",max_length = 50,null = False,default= 'False')
    #
    status = models.CharField("Status",max_length = 50,null = False,default= 'ACTIVE')
    userid = models.CharField("User Id",max_length = 80,null = False,default= 'Admin' )

    def __unicode__(self):
        return  u'%s %s %s %s' % (self.username,self.password,self.recdate,self.staffname)
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

