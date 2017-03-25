from django.db import models

# Create your models here.
class tblquerysetup(models.Model):
    name = models.CharField("Query Name",max_length = 350,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s' % (self.name,self.userid)
    class Meta:
        ordering =['name']
        verbose_name_plural = "SETUP QUERY"

class tblstaffquery(models.Model):
    staffid = models.CharField("Staff Id",max_length = 150,null = False )
    staffname = models.CharField("staffname",max_length = 350,null = False )
    designation = models.CharField("Designation",max_length = 350,null = False )
    department = models.CharField("Department",max_length = 350,null = False )
    querytype = models.CharField("Query Type",max_length = 350,null = False )
    querydate = models.DateField("Query Date")
    querygiver = models.CharField("Query Issuer",max_length=400)
    querygiverid = models.CharField("Query Issuer Id" ,max_length=20)
    reasonforquery = models.TextField("Reason for query",max_length=1200)
    actiontaken = models.TextField("Action Taken on the query",max_length=1200)
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s %s ' % (self.staffid,self.staffname,self.designation,self.department,self.querytype,self.querydate,self.querygiver,self.reasonforquery,self.userid,self.actiontaken)
    class Meta:
        ordering =['staffid','id']
        verbose_name_plural = "QUERY FOR STAFF"

class tblstaffquerydeleted(models.Model):
    staffid = models.CharField("Staff Id",max_length = 150,null = False )
    staffname = models.CharField("staffname",max_length = 350,null = False )
    designation = models.CharField("Designation",max_length = 350,null = False )
    department = models.CharField("Department",max_length = 350,null = False )
    querytype = models.CharField("Query Type",max_length = 350,null = False )
    querydate = models.DateField("Query Date")
    querygiver = models.CharField("Query Issuer",max_length=400)
    querygiverid = models.CharField("Query Issuer Id" ,max_length=20)
    reasonforquery = models.TextField("Reason for query",max_length=1200)
    actiontaken = models.TextField("Action Taken on the query",max_length=1200)
    userid = models.CharField("User Id",max_length = 150,null = False )
    reasonfordeletion = models.CharField("Reason for deletion",max_length=300)
    deleted_date = models.DateTimeField('Date Deleted', auto_now_add=True)

    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s %s ' % (self.staffid,self.staffname,self.designation,self.department,self.querytype,self.querydate,self.querygiver,self.reasonforquery,self.userid,self.actiontaken)
    class Meta:
        ordering =['staffid','id']
        verbose_name_plural = "DELETED STAFF QUERY "


