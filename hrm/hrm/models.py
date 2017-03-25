from django.db import models
from PIL import Image

class staffrec(models.Model):
    picture = models.ImageField(upload_to = 'staff', null=True, blank=True)
    staffid = models.CharField("Staff Id",max_length = 280,null = False) #LG File no
    name = models.CharField("Name",max_length = 480,null = False)
    address = models.CharField("Address",max_length = 480,null = False)
    phoneno = models.CharField("Phone No",max_length = 280,null = False)
    dateofbirth = models.DateField()
    sex = models.CharField("Sex",max_length = 10,null = False)
    maritalstatus = models.CharField("Marital Status",max_length = 80,null = False)
    nationality = models.CharField("Nationality",max_length = 150,null = False)
    stateoforigin = models.CharField("State of origin",max_length = 80,null = False)
    localgovt = models.CharField("Local Govt Of Origin",max_length = 180,null = False)
    email = models.CharField("E-mail",max_length = 180,null = False)
    nextofkin = models.CharField("Next Of Kin",max_length = 380,null = False)
    nextofkinaddress = models.CharField("Next Of Kin Address",max_length = 480,null = False)
    nextofkinphone = models.CharField("Next Of Kin Phone",max_length = 280,null = False)
    department = models.CharField("Department",max_length = 280,null = False)
    dateofresum = models.DateField()
    firstguarantor = models.CharField("First Guarantor Name",max_length = 380,null = False)
    firstguarantoraddress = models.CharField("First Guarantor Name",max_length = 480,null = False)
    secondguarantor = models.CharField("First Guarantor Name",max_length = 380,null = False)
    secondguarantoraddress = models.CharField("First Guarantor Name",max_length = 480,null = False)
    designation = models.CharField("Designation",max_length = 280,null = False)
    qualification = models.CharField("Qualification",max_length = 180,null = False)
    branch = models.CharField("Branch",max_length = 180,null = False)
    profession = models.CharField("Residing State",max_length = 180,null = False)
    workedday = models.IntegerField()
    status = models.CharField("Status",max_length = 150,null = False )
    level = models.IntegerField()
    step = models.IntegerField()
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s' % (self.staffid,self.name,self.address,self.sex,self.designation,self.department,self.phoneno,self.email,self.status)

    def save(self, size=(200, 200), **kwargs):
        """
	Save Photo after ensuring it is not blank. Resize as needed.
	"""

        if not self.id and not self.picture:
            return

        super(staffrec, self).save(**kwargs)

        filename = self.picture.path
        image = Image.open(filename)

        image.thumbnail(size, Image.ANTIALIAS)
        image.save(filename)


    class Meta:
        ordering =['name']
        verbose_name_plural = "Staff Data"

class tblstaffedu(models.Model):
    staffid = models.CharField("staffid",max_length = 150,null = False )
    staffname = models.CharField("staffname",max_length = 350,null = False )
    nameofsch = models.CharField("nameofsch",max_length = 350,null = False )
    courseofstu = models.CharField("courseofstu",max_length = 250,null = False )
    certificateob = models.CharField("certificateob",max_length = 250,null = False )
    gradeobtained = models.CharField("gradeobtained",max_length = 150,null = False )
    entryyear = models.CharField("entry year",max_length = 10,null = False )
    exityear = models.CharField("exit year",max_length = 10,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s %s %s' % (self.staffid,self.staffname,self.nameofsch,self.courseofstu,self.certificateob,self.gradeobtained,self.entryyear,self.exityear,self.userid)
    class Meta:
        ordering =['staffid']
        verbose_name_plural = "STAFF EDUCATION"

class tblstaffproff(models.Model):
    staffid = models.CharField("staffid",max_length = 150,null = False )
    staffname = models.CharField("staffname",max_length = 350,null = False )
    bodyname = models.CharField("nameofsch",max_length = 350,null = False )
    qualification = models.CharField("courseofstu",max_length = 250,null = False )
    exityear = models.CharField("exit year",max_length = 10,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s %s ' % (self.staffid,self.staffname,self.bodyname,self.qualification,self.exityear,self.userid)
    class Meta:
        ordering =['staffid']
        verbose_name_plural = "STAFF PROFESSIONAL "

class tblstaffnonpension(models.Model):
    category = models.CharField("category",max_length = 190,null = False )
    staffname = models.CharField("staffname",max_length = 350,null = False )
    address = models.CharField("address",max_length = 450,null = False )
    phoneno = models.CharField("phoneno",max_length = 250,null = False )
    nextofkin = models.CharField("nextofkin",max_length = 350,null = False )
    sex = models.CharField("sex",max_length = 10,null = False )
    session = models.CharField("Session",max_length = 210,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s %s %s' % (self.category,self.staffname,self.address,self.phoneno,self.nextofkin,self.sex,self.userid)
    class Meta:
        ordering =['category','id']
        verbose_name_plural = "NON-PENSIONABLE "

class tblstaffhmo(models.Model):
    staffid = models.CharField("staffid",max_length = 150,null = False )
    staffname = models.CharField("staffname",max_length = 350,null = False )
    hmoname = models.CharField("HMO Name",max_length = 350,null = False )
    hmoprovider = models.CharField("Provider",max_length= 300)
    provideraddress = models.CharField("Provider Address",max_length=500)
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s  ' % (self.staffid,self.staffname,self.hmoname,self.userid)
    class Meta:
        ordering =['staffid']
        verbose_name_plural = "STAFF HMO RECORD "

class tblstaffpfa(models.Model):
    staffid = models.CharField("staffid",max_length = 150,null = False )
    staffname = models.CharField("staffname",max_length = 350,null = False )
    hmoname = models.CharField("PFA Name",max_length = 350,null = False )
    accno = models.CharField("PFA Number",max_length = 350,null = False )
    userid = models.CharField("User Id",max_length = 150,null = False )

    def __unicode__(self):
        return  u'%s %s %s %s %s ' % (self.staffid,self.staffname,self.hmoname,self.userid,self.accno)
    class Meta:
        ordering =['staffid']
        verbose_name_plural = "STAFF PENSION FUND RECORD "



