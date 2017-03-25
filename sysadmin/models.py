from django.db import models
from django.contrib.admin.models import User
from PIL import Image

# Create your models here.
class userprofile(models.Model):
    username = models.CharField('username',max_length=150)
    password = models.CharField('password',max_length=150)
    staffname = models.CharField('Staff FullName',max_length=450)
    created = models.DateTimeField('Created', auto_created=True)
    expires = models.DateField('Expires')
    photo = models.ImageField('User Photo', upload_to='staffs',blank=True,default='user.png')
    status = models.CharField('status',max_length= 150)
    userid = models.CharField("User Id",max_length = 150,null = False )
    #SET UP
    setup = models.BooleanField('Class And Arm', default=False)
    #assessment = models.BooleanField('Assessment', default=False)
    #duties = models.BooleanField('Duties And Department', default=False)
    #schhouse = models.BooleanField('School House', default=False)
    #STUDENT INFORMATION
    studentregistration = models.BooleanField('Student Registration', default=False)
    editregistration = models.BooleanField('Edit Student Registration', default=False)
    studentreport = models.BooleanField('Student Registration Report', default=False)
    withdraw = models.BooleanField('Student Withdraw', default=False)
    returngonestudent = models.BooleanField('Return Gone Student', default=False)
    withdrawnreport = models.BooleanField('Student Withdrawn Report', default=False)
    #BILL MANAGEMENT
    expensedecription = models.BooleanField('Expense Description', default=False)
    billsetup = models.BooleanField('Set Up Bill', default=False)
    additionalexpenses = models.BooleanField('Additional Expenses', default=False)
    printbill = models.BooleanField('Print Bill', default=False)
    billschedule = models.BooleanField('Bill Schedule', default=False)
    #ASSESSMENT AND REPORT
    #principalcomment = models.BooleanField('Principal Comment', default=False)
    reportsheet = models.BooleanField('Report Sheet', default=False)
    broadsheet = models.BooleanField('Broad Sheet', default=False)
    #ADMIN
    createuser = models.BooleanField('Create User', default=False)
    email = models.CharField('Email', max_length=150,default='nill')

    def __unicode__(self):
        return "%s , ---: %s ,---%s,--%s" %(self.username,self.password,self.staffname,self.createuser)

    def save(self, size=(100, 100), **kwargs):
        """
	Save Photo after ensuring it is not blank. Resize as needed.
	"""

        if not self.id and not self.photo:
            return

        super(userprofile, self).save(**kwargs)

        filename = self.photo.path
        image = Image.open(filename)

        image.thumbnail(size, Image.ANTIALIAS)
        image.save(filename)

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'User Account Profile'

class subjectteacher(models.Model):
    teachername = models.CharField('Username', max_length=125)
    subject = models.CharField('Subject', max_length=125)
    klass = models.CharField('Class', max_length=25)
    arm = models.CharField('Arm', max_length=35)
    session = models.CharField('Session', max_length=25)
    term = models.CharField('Term', max_length=25)
    creator = models.CharField('User Id',max_length=100)
    status = models.CharField('Teacher Status',max_length= 15)
    def __unicode__(self):
        return " Teacher's Name :-%s , Subject -: %s ,Class :-%s,Arm :-%s, Session :- %s" %(self.teachername,self.subject,self.klass,self.arm,self.session)

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Subject Teacher Profile'

class ClassTeacher(models.Model):
    teachername = models.CharField('Username', max_length=125)
    klass = models.CharField('Class', max_length=25)
    arm = models.CharField('Arm', max_length=25)
    userid = models.CharField('User Id', max_length=125)
    session = models.CharField('Session', max_length=25)
    def __unicode__(self):
        return " Teacher's Name :-%s  ,Class :-%s,Arm :-%s ,Session : - %s" %(self.teachername,self.klass,self.arm,self.session)
    class Meta:
        ordering = ['klass','id']
        verbose_name_plural = 'Class Teacher Profile'

class currentsession(models.Model):
    session = models.CharField('Current Session',max_length= 25)

    def __unicode__(self):
        return "%s" %self.session
    class Meta:
        ordering = ['id']
        verbose_name_plural = 'School Calender Year'

class Principal(models.Model):
    teachername = models.CharField('Username', max_length=125)
    session = models.CharField('Session', max_length=25)
    userid = models.CharField('User Id', max_length=125)


    def __unicode__(self):
        return " Teacher's Name :-%s  ,Session :-%s,Userid :- %s" %(self.teachername,self.session,self.userid)
    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Principal Profile'

class tblpin(models.Model):
    ydate = models.DateField('Date')
    pin = models.CharField("PIN",max_length = 290,null = False )
    used = models.CharField("Used",max_length = 290,null = False )
    def __unicode__(self):
        return  u'%s - %s - %s' % (self.ydate,self.pin,self.used)
    class Meta:
        ordering =['ydate',]
        verbose_name_plural = "Yearly PIN"

class tblterm(models.Model):
    term = models.CharField('Term', max_length=25)
    creator = models.CharField('User Id',max_length=100)
    status = models.CharField('Teacher Status',max_length= 15)
    def __unicode__(self):
        return " Term :-%s , Status -: %s " %(self.term,self.status)
    class Meta:
        ordering = ['term']
        verbose_name_plural = 'Term Table'



