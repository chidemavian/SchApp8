from django import forms
import os
from myproject.hrm.rcsetup.models import *
from myproject.hrm.hrm.models import *

SEX_CHIOCES = (
('Nil','Nil'),
('MALE','MALE'),
('FEMALE','FEMALE'),
)

STAFFREP_CHIOCES = (
('ACTIVE','ACTIVE'),
('INACTIVE','INACTIVE'),
('DISMISSED','DISMISSED'),
('RESIGNED','RESIGNED'),
('RETIRED','RETIRED'),
)

DEPT_CHIOCES = (
('ADMIN','ADMIN'),
('ACCOUNT','ACCOUNT'),
('HUMAN RESOURCES','HUMAN RESOURCES'),
('INFORMATION TECHNOLOGY','INFORMATION TECHNOLOGY'),
('SECURITY','SECURITY'),
('FINANCE','FINANCE'),
('HEALTH','HEALTH'),
('MARKETING','MARKETING'),
('LEGAL','LEGAL'),
('EDUCATION','EDUCATION'),

)

MAR_CHIOCES = (
('SINGLE','SINGLE'),
('MARRIED','MARRIED'),
('DIVORCE','DIVORCE'),
('WIDOW','WIDOW'),
)


STATE_CHIOCES = (
('Nil','Nil'),
('Abia','Abia'),
('Abuja','Abuja'),
('Adamawa','Adamawa'),
('Akwa Ibom','Akwa Ibom'),
('Anambra','Anambra'),
('Bauchi','Bauchi'),
('Bayelsa','Bayelsa'),
('Benue','Benue'),
('Borno','Borno'),
('Cross River','Cross River'),
('Delta','Delta'),
('Ebonyi','Ebonyi'),
('Edo','Edo'),
('Ekiti','Ekiti'),
('Enugu','Enugu'),
('Gombe','Gombe'),
('Imo','Imo'),
('Jigawa','Jigawa'),
('Kaduna','Kaduna'),
('Kano','Kano'),
('Katsina','Katsina'),
('Kebbi','Kebbi'),
('Kogi','Kogi'),
('Kwara','Kwara'),
('Lagos','Lagos'),
('Nassarawa','Nassarawa'),
('Niger','Niger'),
('Ogun','Ogun'),
('Ondo','Ondo'),
('Osun','Osun'),
('Oyo','Oyo'),
('Plateau','Plateau'),
('Rivers','Rivers'),
('Sokoto','Sokoto'),
('Taraba','Taraba'),
('Yobe','Yobe'),
('Zamfara','Zamfara'),
('Others','Others'),
)


CERT_CHIOCES = (
('Nil','Nil'),
('SSCE','SSCE'),
('GRADE 2','GRADE 2'),
('NCE','NCE'),
('OND','OND'),
('ND','ND'),
('HND','HND'),
('BSC','BSC'),
('BA','BA'),
('BTECH','BTECH'),
('B.EDU','B.EDU'),
('B.ENG','B.ENG'),
('LLB','LLB'),
('MBBL','MBBL'),
('MBA','MBA'),
('MSC','MSC'),
('MBA','MBA'),
('PHD','PHD'),
('FSLC','FSLC'),
('JSS','JSS'),
('OTHERS','OTHERS'),
)

GRADE_CHIOCES = (
('JSS','JSS'),
('FSLC','FSLC'),
('PASS','PASS'),
('MERIT','MERIT'),
('LOWER CREDIT','LOWER CREDIT'),
('UPPER CREDIT','UPPER CREDIT'),
('DINSTICTION','DINSTICTION'),
('THIRD CLASS','THIRD CLASS'),
('SECOND CLASS LOWER','SECOND CLASS LOWER'),
('SECOND CLASS UPPER','SECOND CLASS UPPER'),
('FIRST CLASS','FIRST CLASS'),
('OTHERS','OTHERS'),
)

NATION_CHIOCES = (
('NIGERIAN','NIGERIAN'),
('NON-NIGERIAN','NON-NIGERIAN'),
)

RELATION_CHIOCES = (
('NIL','NIL'),
('FATHER','FATHER'),
('MOTHER','MOTHER'),
('HUSBAND','HUSBAND'),
('WIFE','WIFE'),
('BROTHER','BROTHER'),
('SISTER','SISTER'),
('SON','SON'),
('DAUGHTER','DAUGHTER'),
('UNCLE','UNCLE'),
('AUNT','AUNT'),
('COUSIN','COUSIN'),
('NEPHEW','NEPHEW'),
('NIECE','NIECE'),
('BROTHER-IN-LAW','BROTHER-IN-LAW'),
('SISTER-IN-LAW','SISTER-IN-LAW'),
('FATHER-IN-LAW','FATHER-IN-LAW'),
('MOTHER-IN-LAW','MOTHER-IN-LAW'),
('SON-IN-LAW','SON-IN-LAW'),
('DAUGHTER-IN-LAW','DAUGHTER-IN-LAW'),
)

LEVEL_CHIOCES = (
('1','1'),
('2','2'),
('3','3'),
('4','4'),
('5','5'),
('6','6'),
('7','7'),
('8','8'),
('9','9'),
('10','10'),
('11','11'),
('12','12'),
('13','13'),
('14','14'),
('15','15'),
('16','16'),
('17','17'),
('18','18'),
('19','19'),
('20','20'),

)
STEP_CHIOCES = (
('1','1'),
('2','2'),
('3','3'),
('4','4'),
('5','5'),
('6','6'),
('7','7'),
('8','8'),
('9','9'),
('10','10'),
('11','11'),
('12','12'),
('13','13'),
('14','14'),
('15','15'),
('16','16'),
('17','17'),
('18','18'),
('19','19'),
('20','20'),

)

IMPORT_FILE_TYPES = ['.jpeg','.jpg','.png','bmp','.JPG','.JPEG','.PNG' ]
class staffdataform(forms.Form):
    TYPE_CHOICES =  [(t.desc, t.desc) for t in tbldesig.objects.all().order_by('desc')]
    LG_CHOICES =  [(t.lgname, t.lgname) for t in tbllg.objects.all().order_by('lgname')]
    DEP_CHOICES =  [(t.name, t.name) for t in tbldepartment.objects.all().order_by('name')]
    staffid = forms.CharField(label = "staffid",max_length = 280,required = True,widget = forms.TextInput(attrs={'size':'12'})) #LG File no
    name = forms.CharField(label = "Name",max_length = 280,required = True,widget = forms.Textarea(attrs={'cols':'20','rows':'2'}))
    address = forms.CharField(label = "Address",max_length = 280,required = True,widget = forms.Textarea(attrs={'cols':'20','rows':'2'}))
    phoneno = forms.CharField(label = "Phone No",max_length = 280,required = True,widget = forms.TextInput(attrs={'size':'25'}))
    dateofbirth = forms.CharField(label = "Date Of Birth",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'12'}))
    sex = forms.ChoiceField(choices = SEX_CHIOCES)
    maritalstatus = forms.ChoiceField(choices = MAR_CHIOCES)
    nationality = forms.ChoiceField(choices = NATION_CHIOCES)
    stateoforigin = forms.ChoiceField(choices = STATE_CHIOCES)
    localgovt = forms.ChoiceField(choices = STATE_CHIOCES)#forms.CharField(label = "Local Govt",max_length = 280,required = True)
    email = forms.CharField(label = "Email",max_length = 280,required = True,widget = forms.TextInput(attrs={'size':'12'}))
    nextofkin = forms.CharField(label = "Next Of Kin",max_length = 380,required = True,widget = forms.TextInput(attrs={'size':'25'}))
    nextofkinaddress = forms.CharField(label = "Next Of Kin Address",max_length = 480,required = True,widget = forms.TextInput(attrs={'size':'25'}))
    nextofkinphone = forms.CharField(label = "Next Of Kin Phone",max_length = 480,required = True,widget = forms.TextInput(attrs={'size':'25'}))
    department = forms.ChoiceField(DEP_CHOICES)
    dateofresum = forms.CharField(label = "Date Of Resumption",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'12'}))
    firstguarantor = forms.CharField(label = "First Guarantor Name",max_length = 380,required = True,widget = forms.TextInput(attrs={'size':'25'}))
    firstguarantoraddress = forms.CharField(label = "First Guarantor Address",max_length = 480,required = True,widget = forms.TextInput(attrs={'size':'25'}))
    secondguarantor = forms.CharField(label = "Second Guarantor Name",max_length = 380,required = True,widget = forms.TextInput(attrs={'size':'25'}))
    secondguarantoraddress = forms.CharField(label = "Second Guarantor Address",max_length = 480,required = True,widget = forms.TextInput(attrs={'size':'25'}))
    designation = forms.ChoiceField(TYPE_CHOICES)
    qualification = forms.ChoiceField(choices = CERT_CHIOCES)
    branch = forms.ChoiceField(LG_CHOICES)
    profession = forms.ChoiceField(choices = STATE_CHIOCES)
    picture = forms.ImageField(required=False,widget=forms.FileInput(attrs={'size':'5'}))
    level = forms.ChoiceField(choices=[(t.level, t.level) for t in tbllevel.objects.all().order_by('level')])
    step = forms.ChoiceField(choices= [(t.step, t.step) for t in tblstep.objects.all().order_by('level')])

    def __init__(self, *args):
        super(staffdataform, self).__init__(*args)
        self.fields['designation'].choices = [(t.desc, t.desc) for t in tbldesig.objects.all().order_by('desc')]
        self.fields['designation'].initial = tbldesig.objects.all().order_by('desc')
        self.fields['branch'].choices = [(t.lgname, t.lgname) for t in tbllg.objects.all().order_by('lgname')]
        self.fields['branch'].initial = tbllg.objects.all().order_by('lgname')
        self.fields['department'].choices = [(t.name, t.name) for t in tbldepartment.objects.all().order_by('name')]
        self.fields['department'].initial = tbldepartment.objects.all().order_by('name')
        self.fields['stateoforigin'].choices = [(t.state, t.state) for t in tblstate.objects.all().order_by('state')]
        self.fields['stateoforigin'].initial = tblstate.objects.all().order_by('state')
        self.fields['profession'].choices = [(t.state, t.state) for t in tblstate.objects.all().order_by('state')]
        self.fields['profession'].initial = tblstate.objects.all().order_by('state')
        self.fields['localgovt'].choices = [(t.localgovt, t.localgovt) for t in tbllocalgovt.objects.all().order_by('localgovt')]
        self.fields['localgovt'].initial = tbllocalgovt.objects.all().order_by('localgovt')
        self.fields['level'].choices = [(t.level, t.level) for t in tbllevel.objects.all().order_by('level')]
        self.fields['level'].initial = tbllevel.objects.all().order_by('level')
        self.fields['step'].choices = [(t.step, t.step) for t in tblstep.objects.all().order_by('level')]
        self.fields['step'].initial = tblstep.objects.all().order_by('level')
        self.fields['staffid'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['address'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['phoneno'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['dateofbirth'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['email'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['nextofkin'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['nextofkinaddress'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['nextofkinphone'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['dateofresum'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['firstguarantor'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['firstguarantoraddress'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['secondguarantor'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['secondguarantoraddress'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['name'].widget.attrs['class'] = 'loginTxtbox'


    def clean_rfile(self):
          rfile = self.cleaned_data['picture']
          if rfile is None:
              pass
              #print "OK"
          else:
              #print rfile
              rrfile = self.cleaned_data['picture'].name
              extension = os.path.splitext(rrfile)[1]
              if not (extension in IMPORT_FILE_TYPES):
                raise forms.ValidationError( u'%s is not a valid Image file.' % extension )
              else:
                return rfile

class editstaform(forms.Form):
    staffname = forms.CharField(label = "Staff Name",max_length = 110,required = True,widget=forms.TextInput(attrs={'size':'35'}))
    def __init__(self, *args):
        super(editstaform, self).__init__(*args)
        self.fields['staffname'].widget.attrs['class'] = 'loginTxtbox'


class staffeduform(forms.Form):
    staffid = forms.CharField(label = "Staff Id",max_length = 50,required = True,widget = forms.TextInput(attrs={'size':'25','readonly':'readonly'}))
    staffname = forms.CharField(label = "Staff Name",max_length = 310,required = True,widget = forms.TextInput(attrs={'size':'35'}))
    nameofsch = forms.CharField(label = "Name Of Sch",max_length = 280,required = True,widget = forms.TextInput(attrs={'size':'25'}))
    courseofstu = forms.CharField(label = "Course Of Studied",max_length = 280,required = True,widget = forms.TextInput(attrs={'size':'25'}))#widget = forms.TextInput(attrs={})
    certificateob = forms.ChoiceField(choices = CERT_CHIOCES)
    gradeobtained = forms.ChoiceField(choices = GRADE_CHIOCES)
    entryyear = forms.IntegerField(max_value = 9999,min_value =1900)
    exityear = forms.IntegerField(max_value = 9999,min_value =1900)
    def __init__(self, *args):
        super(staffeduform, self).__init__(*args)
        self.fields['staffid'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['staffname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['nameofsch'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['courseofstu'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['entryyear'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['exityear'].widget.attrs['class'] = 'loginTxtbox'


class proffeduform(forms.Form):
    staffid = forms.CharField(label = "Staff Id",max_length = 50,required = True,widget = forms.TextInput(attrs={'size':'35','readonly':'readonly'}))
    staffname = forms.CharField(label = "Staff Name",max_length = 310,required = True,widget = forms.TextInput(attrs={'size':'35'}))
    bodyname = forms.CharField(label = "Name Of Sch",max_length = 280,required = True,widget = forms.Textarea(attrs={'cols':'20','rows':'2'}))
    qualification = forms.CharField(label = "Qualification",max_length = 280,required = True ,widget = forms.TextInput(attrs={'size':'35'}))
    exityear = forms.IntegerField(max_value = 9999,min_value =1900 ,widget = forms.TextInput(attrs={'size':'5'}))
    def __init__(self, *args):
        super(proffeduform, self).__init__(*args)
        self.fields['staffid'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['staffname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['bodyname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['qualification'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['exityear'].widget.attrs['class'] = 'loginTxtbox'

class nonpensionform(forms.Form):
    CATY_CHOICES =  [(t.name, t.name) for t in tblcategory.objects.all().order_by('name')]
    category = forms.ChoiceField(choices = CATY_CHOICES)
    staffname = forms.CharField(label = "Staff Name",max_length = 310,required = True)
    address = forms.CharField(label = "Address",max_length = 280,required = True,widget = forms.Textarea(attrs={'cols':'20','rows':'2'}))
    phoneno = forms.CharField(label = "Phone",max_length = 280,required = True)#widget = forms.TextInput(attrs={})
    nextofkin = forms.CharField(label = "Next Of Kin",max_length = 280,required = True)
    sex = forms.ChoiceField(choices = SEX_CHIOCES)
    session = forms.CharField(label = "session",max_length = 280,required = True)
    def __init__(self, *args):
        super(nonpensionform, self).__init__(*args)
        self.fields['address'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['staffname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['phoneno'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['nextofkin'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['category'].choices = [(t.name, t.name) for t in tblcategory.objects.all().order_by('name')]
        self.fields['category'].initial = tblcategory.objects.all().order_by('name')

class staffrepform(forms.Form):
    status = forms.ChoiceField(choices = STAFFREP_CHIOCES)
    qualification = forms.ChoiceField(choices = CERT_CHIOCES)
    sex = forms.ChoiceField(choices = SEX_CHIOCES)
    excelfile = forms.BooleanField(label='Download In Excel',required=False)


"""class staffindrepform(forms.Form):
    status = forms.CharField(label = "staff id",max_length = 310,required = True)
    def __init__(self, *args):
        super(staffindrepform, self).__init__(*args)
        self.fields['status'].widget.attrs['class'] = 'loginTxtbox'"""

class staffindrepform(forms.Form):
    staffid = forms.CharField(label = "staff id",max_length = 310,required = True)
    def __init__(self, *args):
        super(staffindrepform, self).__init__(*args)
        self.fields['staffid'].widget.attrs['class'] = 'loginTxtbox'

class lengthofserviceform(forms.Form):
    yearvalue = forms.IntegerField(label='Year',max_value=99)
    caldate = forms.CharField(label = "Date",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    age = forms.BooleanField(label='View By AGE',required=False)
    def __init__(self, *args):
        super(lengthofserviceform, self).__init__(*args)
        self.fields['yearvalue'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['caldate'].widget.attrs['class'] = 'loginTxtbox'


class staffhmoform(forms.Form):
    CATY_CHOICES =  [(t.name, t.name) for t in tblhmo.objects.all().order_by('name')]
    staffid = forms.CharField(label = "Staff Id",max_length = 50,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'35'}))
    staffname = forms.CharField(label = "Staff Name",max_length = 310,required = True,widget = forms.TextInput(attrs={'size':'35'}))
    hmoname = forms.ChoiceField(label='HMO Name',choices = CATY_CHOICES)
    hmoprovider = forms.ChoiceField(label='Provider Name', choices = [(t.name, t.name) for t in tblhmoprovide.objects.all().order_by('name')])


    def __init__(self, *args):
        super(staffhmoform, self).__init__(*args)
        self.fields['hmoname'].choices = [(t.name, t.name) for t in tblhmo.objects.all().order_by('name')]
        self.fields['hmoname'].initial = tblhmo.objects.all().order_by('name')
        self.fields['hmoprovider'].choices = [(t.name, t.name) for t in tblhmoprovide.objects.all().order_by('name')]
        self.fields['staffid'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['staffname'].widget.attrs['class'] = 'loginTxtbox'

class staffpfaform(forms.Form):
    CATY_CHOICES =  [(t.accname, t.accname) for t in tblpfa.objects.all().order_by('accname')]
    staffid = forms.CharField(label = "Staff Id",max_length = 50,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'35'}))
    staffname = forms.CharField(label = "Staff Name",max_length = 310,required = True,widget = forms.TextInput(attrs={'size':'35'}))
    accno = forms.CharField(label = "PFA Number",max_length = 150,required = True)
    hmoname = forms.ChoiceField(label='PFA Name',choices = CATY_CHOICES)

    def __init__(self, *args):
        super(staffpfaform, self).__init__(*args)
        self.fields['hmoname'].choices = [(t.accname, t.accname) for t in tblpfa.objects.all().order_by('accname')]
        self.fields['hmoname'].initial = tblpfa.objects.all().order_by('accname')
        self.fields['staffid'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['staffname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['accno'].widget.attrs['class'] = 'loginTxtbox'

class staffrepformbydep(forms.Form):
    status = forms.ChoiceField(choices = STAFFREP_CHIOCES)
    department = forms.ChoiceField(choices = [(t.name, t.name) for t in tbldepartment.objects.all().order_by('name')])
    #sex = forms.ChoiceField(choices = SEX_CHIOCES)
    excelfile = forms.BooleanField(label='Download In Excel',required=False)
    def __init__(self, *args):
        super(staffrepformbydep, self).__init__(*args)

        self.fields['department'].choices = [(t.name, t.name) for t in tbldepartment.objects.all().order_by('name')]
        self.fields['department'].initial = tbldepartment.objects.all().order_by('name')


class staffrepformbydesg(forms.Form):
    status = forms.ChoiceField(choices = STAFFREP_CHIOCES)
    designation = forms.ChoiceField(choices = [(t.desc, t.desc) for t in tbldesig.objects.all().order_by('desc')])
    #sex = forms.ChoiceField(choices = SEX_CHIOCES)
    excelfile = forms.BooleanField(label='Download In Excel',required=False)
    def __init__(self, *args):
        super(staffrepformbydesg, self).__init__(*args)
        self.fields['designation'].choices = [(t.desc, t.desc) for t in tbldesig.objects.all().order_by('desc')]
        self.fields['designation'].initial = tbldesig.objects.all().order_by('desc')

