from django.db import models

# Create your models here.
class redept(models.Model):
    staffid = models.CharField("staffid",max_length = 150,null = False )
    staffname = models.CharField("staffname",max_length = 350,null = False )
    sex = models.CharField("sex",max_length = 350,null = False )
    currentdept = models.CharField("current dept",max_length = 250,null = False )
    newdept = models.CharField("New Current",max_length = 250,null = False )
    recdate = models.DateField()
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s' % (self.staffid,self.staffname,self.sex,self.currentdept,self.newdept,self.recdate,self.userid)
    class Meta:
        ordering =['staffid','id']
        verbose_name_plural = "Re-Department"

class relocate(models.Model):
    staffid = models.CharField("staffid",max_length = 150,null = False )
    staffname = models.CharField("staffname",max_length = 350,null = False )
    sex = models.CharField("sex",max_length = 350,null = False )
    currentlocation = models.CharField("current dept",max_length = 250,null = False )
    newlocation = models.CharField("New Current",max_length = 250,null = False )
    recdate = models.DateField()
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s' % (self.staffid,self.staffname,self.sex,self.currentlocation,self.newlocation,self.recdate,self.userid)
    class Meta:
        ordering =['staffid','id']
        verbose_name_plural = "Re-Location"

class tblpromotion(models.Model):
    staffid = models.CharField("staffid",max_length = 150,null = False )
    staffname = models.CharField("staffname",max_length = 350,null = False )
    sex = models.CharField("sex",max_length = 350,null = False )
    olddesignation = models.CharField("current Designation",max_length = 250,null = False )
    newdesignation = models.CharField("New Designation",max_length = 250,null = False )
    oldlevel = models.CharField("current Level/Step",max_length = 250,null = False )
    newlevel = models.CharField("New Level/Step",max_length = 250,null = False )
    recdate = models.DateField()
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s' % (self.staffid,self.staffname,self.sex,self.olddesignation,self.newdesignation,self.recdate,self.userid)
    class Meta:
        ordering =['staffid','id']
        verbose_name_plural = "Promotion"

class tbltermination(models.Model):
    staffid = models.CharField("staffid",max_length = 150,null = False )
    staffname = models.CharField("staffname",max_length = 350,null = False )
    sex = models.CharField("sex",max_length = 350,null = False )
    resdate = models.DateField()
    recdate = models.DateField()
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s %s ' % (self.staffid,self.staffname,self.sex,self.resdate,self.recdate,self.userid)
    class Meta:
        ordering =['staffid','id']
        verbose_name_plural = "Termination"

class tblresignation(models.Model):
    staffid = models.CharField("staffid",max_length = 150,null = False )
    staffname = models.CharField("staffname",max_length = 350,null = False )
    sex = models.CharField("sex",max_length = 350,null = False )
    resdate = models.DateField()
    recdate = models.DateField()
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s %s ' % (self.staffid,self.staffname,self.sex,self.resdate,self.recdate,self.userid)
    class Meta:
        ordering =['staffid','id']
        verbose_name_plural = "Resignation"

class tblretirement(models.Model):
    staffid = models.CharField("staffid",max_length = 150,null = False )
    staffname = models.CharField("staffname",max_length = 350,null = False )
    sex = models.CharField("sex",max_length = 350,null = False )
    resdate = models.DateField()
    recdate = models.DateField()
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s %s ' % (self.staffid,self.staffname,self.sex,self.resdate,self.recdate,self.userid)
    class Meta:
        ordering =['staffid','id']
        verbose_name_plural = "Retirement"











