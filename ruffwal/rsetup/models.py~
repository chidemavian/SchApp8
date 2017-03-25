from django.db import models
from datetime import datetime, timedelta
# Create your models here.
class tblgroup(models.Model):
    #ACC_CHOICES =( (u'Personal',u'Personal'),(u'Business',u'Business'),)
    groupname = models.CharField("Groupname",max_length = 150,null = False )
    groupcode = models.CharField("Groupcode",max_length = 150,primary_key= True,null = False )
    datecreated = models.DateTimeField(auto_now_add=True, blank=True)


    def __unicode__(self):
        return  u'%s %s %s' % (self.groupname,self.groupcode,self.datecreated)
    class Meta:
        ordering =['-datecreated',]
        verbose_name_plural = "Group Table"
class tblsubgroup(models.Model):
    #ACC_CHOICES =( (u'Personal',u'Personal'),(u'Business',u'Business'),)
    groupname = models.CharField("Groupname",max_length = 150,null = False )
    groupcode = models.CharField("Groupcode",max_length = 150,null = False )
    datecreated = models.DateTimeField(auto_now_add=True, blank=True)
    subgroupname = models.CharField("Subgroupname",max_length = 300,null = False )
    subgroupcode = models.CharField("Subgroupcode",max_length = 150,primary_key= True,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s %s' % (self.groupname,self.groupcode,self.datecreated,self.subgroupname,self.subgroupcode,self.userid)
    class Meta:
        ordering =['-datecreated',]
        verbose_name_plural = "SubGroup Table"

class tblaccount(models.Model):
    accname = models.CharField("Acc name",max_length = 350,null = False )
    acccode = models.CharField("Acc code",max_length = 150,null = False )
    accbal = models.DecimalField('Acc Bal',max_digits = 20 , decimal_places = 2, null = False )
    groupname = models.CharField("Groupname",max_length = 150,null = False )
    groupcode = models.CharField("Groupcode",max_length = 150,null = False )
    datecreated = models.DateTimeField(auto_now_add=True, blank=True)
    subgroupname = models.CharField("Subgroupname",max_length = 150,null = False )
    subgroupcode = models.CharField("Subgroupcode",max_length = 150,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )
    accstatus = models.CharField("Acc Status",max_length = 70,null = False )
    recreport = models.CharField("Report Acc",max_length = 50,null = False )
    lasttrandate = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s' % (self.accname,self.acccode,self.accbal,self.groupname,self.groupcode,self.datecreated,self.subgroupname,self.subgroupcode,self.userid)
    class Meta:
        ordering =['groupcode','acccode']
        verbose_name_plural = "Account Table"

class tblstock(models.Model):
    stockname = models.CharField("Stock name",max_length = 350,null = False )
    acccode = models.CharField("Acc code",max_length = 150,primary_key= True,null = False )
    accbal = models.DecimalField('Acc Bal',max_digits = 20 , decimal_places = 2, null = True )
    datecreated = models.DateTimeField(auto_now_add=True, blank=True)
    subname = models.CharField("Subgroupname",max_length = 150,null = False )
    subcode = models.CharField("Subgroupcode",max_length = 150,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )
    qtybal = models.DecimalField('Qty Bal',max_digits = 20 , decimal_places = 2, null = True )
    avgprice = models.DecimalField('Average Price',max_digits = 20 , decimal_places = 2, null = True )


    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s' % (self.stockname,self.acccode,self.accbal,self.datecreated,self.subname,self.subcode,self.userid,self.qtybal,self.avgprice)
    class Meta:
        ordering =['-datecreated',]
        verbose_name_plural = "Stock Table"



class receivables(models.Model):
    accname = models.CharField("Account Name",max_length = 350,null = False )
    acccode = models.CharField("Acc code",max_length = 150,null = False )
    address = models.CharField("Address",max_length = 350,null = False )
    phoneno = models.CharField("Phone No",max_length = 150,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s' % (self.accname,self.acccode,self.address,self.phoneno,self.userid)
    class Meta:
        ordering =['acccode',]
        verbose_name_plural = "Receivables Table"

class payables(models.Model):
    accname = models.CharField("Account Name",max_length = 350,null = False )
    acccode = models.CharField("Acc code",max_length = 150,null = False )
    address = models.CharField("Address",max_length = 350,null = False )
    phoneno = models.CharField("Phone No",max_length = 150,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s' % (self.accname,self.acccode,self.address,self.phoneno,self.userid)
    class Meta:
        ordering =['acccode',]
        verbose_name_plural = "Payables Table"


class tblcompanyinfo(models.Model):
    name = models.CharField("Name",max_length = 290,null = False )
    address = models.CharField("Address",max_length = 490,null = False )
    picture = models.ImageField(upload_to = 'staff', null=True, blank=True)
    phonenumber = models.CharField('Telephone', max_length=65,null=True,blank=True)
    email = models.EmailField('Email', max_length=75,null=True,blank=True)
    website = models.CharField('Website', max_length=200,null=True,blank=True)

    def __unicode__(self):
        return  u'%s %s %s %s %s %s' % (self.name,self.address,self.picture,self.phonenumber,self.email,self.website)
    class Meta:
        ordering =['name',]
        verbose_name_plural = "Company Info"

class staffonloan(models.Model):
    accname = models.CharField("Account Name",max_length = 350,null = False )
    acccode = models.CharField("Acc code",max_length = 150,null = False )
    address = models.CharField("Address",max_length = 350,null = False )
    phoneno = models.CharField("Phone No",max_length = 150,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s' % (self.accname,self.acccode,self.address,self.phoneno,self.userid)
    class Meta:
        ordering =['acccode',]
        verbose_name_plural = "Staff On Loan Table"







