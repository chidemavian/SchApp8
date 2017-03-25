from django.db import models

# Create your models here.
class tblasset(models.Model):
    name = models.CharField("Asset name",max_length = 350,null = False )
    acccode = models.CharField("Asset code",max_length = 150,null = False )
    deprate = models.DecimalField('Dep Rate',max_digits = 20 , decimal_places = 5, null = True )
    datepurchase = models.DateField()
    subname = models.CharField("Subgroupname",max_length = 150,null = False )
    subcode = models.CharField("Subgroupcode",max_length = 150,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )
    department = models.CharField("Department",max_length = 150,null = False )
    span = models.DecimalField('Average Price',max_digits = 20 , decimal_places = 2, null = True )
    refcode = models.CharField('Reference Code',max_length=550)
    opdepn = models.DecimalField('Opening Depn',max_digits = 20 , decimal_places = 2, null = True,default=0 )

    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s' % (self.name,self.acccode,self.deprate,self.datepurchase,self.subname,self.subcode,self.userid,self.department,self.span)
    class Meta:
        ordering =['acccode',]
        verbose_name_plural = "Assets Register Table"

class tblassetdepartment(models.Model):
    name = models.CharField("Asset name",max_length = 350,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )
    def __unicode__(self):
        return  u'%s %s' % (self.name,self.userid)
    class Meta:
        ordering =['name',]
        verbose_name_plural = "Assets Department  Table"

class tblresidualvalue(models.Model):
    deprate = models.DecimalField('Dep Rate',max_digits = 20 , decimal_places = 2, null = True )
    userid = models.CharField("User Id",max_length = 150,null = False )
    def __unicode__(self):
        return  u'%s %s' % (self.deprate,self.userid)
    class Meta:
        ordering =['id',]
        verbose_name_plural = "Assets Residual Value"

class tblassetcost(models.Model):
    acccode = models.CharField("Asset code",max_length = 150,null = False )
    transdate = models.DateField()
    userid = models.CharField("User Id",max_length = 150,null = False )
    amount = models.DecimalField('Cost Amount',max_digits = 20 , decimal_places = 2, null = True )
    refcode = models.CharField('Reference Code',max_length=550)
    def __unicode__(self):
        return  u'%s %s %s %s ' % (self.acccode,self.userid,self.transdate,self.amount)
    class Meta:
        ordering =['acccode','transdate']
        verbose_name_plural = "Assets Cost Table"

