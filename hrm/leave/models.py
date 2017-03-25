from django.db import models

class tblleavesetup(models.Model):
    name = models.CharField("staffname",max_length = 350,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s' % (self.name,self.userid)
    class Meta:
        ordering =['name']
        verbose_name_plural = "SETUP Leave"

class tblleave(models.Model):
    staffid = models.CharField("Staff Id",max_length = 150,null = False )
    staffname = models.CharField("staffname",max_length = 350,null = False )
    sex = models.CharField("sex",max_length = 50,null = False )
    designation = models.CharField("Designation",max_length = 350,null = False )
    department = models.CharField("Department",max_length = 350,null = False )
    traintype = models.CharField("Training Type",max_length = 350,null = False )
    description = models.CharField("Description",max_length = 350,null = False )
    duration = models.CharField("Duration",max_length = 350,null = False )
    commdate = models.DateField()
    enddate = models.DateField()
    recyear = models.IntegerField()
    recendyear = models.IntegerField()
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s %s %s %s' % (self.staffid,self.staffname,self.sex,self.designation,self.department,self.traintype,self.description,self.duration,self.commdate,self.userid,self.recyear,self.enddate)
    class Meta:
        ordering =['staffid','id']
        verbose_name_plural = "Staff Leave"


