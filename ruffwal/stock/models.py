from django.db import models
from datetime import datetime, timedelta

# Create your models here.
class tblstocktransaction(models.Model):
    stockname = models.CharField("Stock name",max_length = 350,null = False )
    acccode = models.CharField("Acc code",max_length = 150,null = False )
    qty = models.DecimalField('Qty',max_digits = 20 , decimal_places = 2, null = True )
    stin = models.DecimalField('Stock In',max_digits = 20 , decimal_places = 2, null = True )
    stout = models.DecimalField('Stock Out',max_digits = 20 , decimal_places = 2, null = True )
    stbal = models.DecimalField('Stock Bal',max_digits = 20 , decimal_places = 2, null = True )
    transcreated = models.DateField()
    particulars = models.CharField("Particulars",max_length = 150,null = False )
    unitprice = models.DecimalField('Unit Price',max_digits = 20 , decimal_places = 2, null = True )
    totalprice = models.DecimalField('Total Price',max_digits = 20 , decimal_places = 2, null = True )
    userid = models.CharField("User Id",max_length = 150,null = False )
    disqty = models.CharField("Quantity Display",max_length = 150,null = False )#comma separated value
    disin = models.CharField("In Display",max_length = 150,null = False )#comma separated value
    disout = models.CharField("Out Display",max_length = 150,null = False )#comma separated value
    disbal = models.CharField("Balance Display",max_length = 150,null = False )#comma separated value
    disunitprice = models.CharField("Unit Price",max_length = 150,null = False )#comma separated value
    distotalprice = models.CharField("Total Price",max_length = 150,null = False )#comma separated value



    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.stockname,self.acccode,self.qty,self.stin,self.stout,self.stbal,self.transcreated,self.particulars,self.unitprice,self.totalprice,self.userid,self.disbal,self.disin,self.disout,self.disqty,self.distotalprice,self.disunitprice)
    class Meta:
        ordering =['userid',]
        verbose_name_plural = "Stock Transaction Table"

class tblstocktemp(models.Model):
    vendorname = models.CharField("Vendor name",max_length = 350,null = False )
    vendorcode = models.CharField("Vendor code",max_length = 150,null = False )
    qty = models.DecimalField('Qty',max_digits = 20 , decimal_places = 2, null = True )
    transdate = models.DateField()
    particulars = models.CharField("Particulars",max_length = 150,null = False )
    unitprice = models.DecimalField('Unit Bal',max_digits = 20 , decimal_places = 2, null = True )
    totalprice = models.DecimalField('Total Bal',max_digits = 20 , decimal_places = 2, null = True )
    userid = models.CharField("User Id",max_length = 150,null = False )
    stockname = models.CharField("Stock Name",max_length = 150,null = False )#comma separated value
    stockcode = models.CharField("Stock Code",max_length = 150,null = False )#comma separated value
    invoiceno = models.CharField("Invoice No",max_length = 150,null = False )#comma separated value


    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s %s %s' % (self.vendorname,self.vendorcode,self.qty,self.transdate,self.particulars,self.unitprice,self.totalprice,self.userid,self.stockname,self.stockcode,self.invoiceno)
    class Meta:
        ordering =['userid',]
        verbose_name_plural = "Stock Temp"

class tblstocktempout(models.Model):
    vendorname = models.CharField("Vendor name",max_length = 350,null = False )
    vendorcode = models.CharField("Vendor code",max_length = 150,null = False )
    qty = models.DecimalField('Qty',max_digits = 20 , decimal_places = 2, null = True )
    transdate = models.DateField()
    particulars = models.CharField("Particulars",max_length = 150,null = False )
    unitprice = models.DecimalField('Unit Bal',max_digits = 20 , decimal_places = 2, null = True )
    totalprice = models.DecimalField('Total Bal',max_digits = 20 , decimal_places = 2, null = True )
    userid = models.CharField("User Id",max_length = 150,null = False )
    stockname = models.CharField("Stock Name",max_length = 150,null = False )#comma separated value
    stockcode = models.CharField("Stock Code",max_length = 150,null = False )#comma separated value
    invoiceno = models.CharField("Invoice No",max_length = 150,null = False )#comma separated value


    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s %s %s' % (self.vendorname,self.vendorcode,self.qty,self.transdate,self.particulars,self.unitprice,self.totalprice,self.userid,self.stockname,self.stockcode,self.invoiceno)
    class Meta:
        ordering =['userid',]
        verbose_name_plural = "Stock Temp Out"

class tblstocktout(models.Model):
    studentname = models.CharField("Student name",max_length = 350,null = False )
    studentcode = models.CharField("Reg No",max_length = 150,null = False )
    klass = models.CharField("Class",max_length = 150,null = False )
    session = models.CharField("Session",max_length = 150,null = False )
    Arm = models.CharField("Arm",max_length = 150,null = False )
    stockcode = models.CharField("Stock Code",max_length = 150,null = False )
    stockname = models.CharField("Stock Name",max_length = 150,null = False )
    qty = models.DecimalField('Qty',max_digits = 20 , decimal_places = 2, null = True )
    userid = models.CharField("userid",max_length = 350,null = False )
    transdate = models.DateField()
    description = models.CharField("userid",max_length = 350,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s %s %s' % (self.studentname,self.studentcode,self.klass,self.session,self.arm,self.stockcode,self.stockname,self.qty,self.userid,self.transdate,self.description)
    class Meta:
        ordering =['userid',]
        verbose_name_plural = "Stock Out"