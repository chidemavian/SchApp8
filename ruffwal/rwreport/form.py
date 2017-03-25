from django import forms
from myproject.setup.models import *
from myproject.ruffwal.rsetup.models import *

YEAR_CHIOCES = (
('2011','2011'),
('2012','2012'),
('2013','2013'),
('2014','2014'),
('2015','2015'),
('2016','2016'),
('2017','2017'),
('2018','2018'),
('2019','2019'),
('2020','2020'),
('2021','2021'),
('2022','2022'),
)


class dateform(forms.Form):
    #startdate = forms.DateField()
    enddate = forms.CharField(label = "TransDate",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))#forms.
    excelfile = forms.BooleanField(label='Download In Excel',required=False)
    def __init__(self, *args, **kwargs):
        super(dateform, self).__init__(*args, **kwargs)
        self.fields['enddate'].widget.attrs['class'] = 'loginTxtbox'


class dateformpl(forms.Form):
    startdate = forms.CharField(label = "TransDate",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'15'}))#forms.DateField()#forms.DateField()
    enddate = forms.CharField(label = "TransDate",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'15'}))#forms.DateField()#forms.DateField()
    excelfile = forms.BooleanField(label='Download In Excel',required=False)
    def __init__(self, *args, **kwargs):
        super(dateformpl, self).__init__(*args, **kwargs)
        self.fields['enddate'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['startdate'].widget.attrs['class'] = 'loginTxtbox'

class staterep(forms.Form):
    TYPE_CHOICES =  [(t.groupname, t.groupname) for t in tblgroup.objects.all().order_by('groupcode')]
    COLOR_CHOICES = [(c.subgroupname, c.subgroupname) for c in tblsubgroup.objects.all().order_by('subgroupcode')]
    grpname = forms.ChoiceField(choices=TYPE_CHOICES)
    subgrname = forms.ChoiceField(label= 'Subject', choices = COLOR_CHOICES)
    startdate = forms.CharField(label = "TransDate",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'10'}))
    enddate = forms.CharField(label = "TransDate",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'10'}))
    excelfile = forms.BooleanField(label='Download In Excel',required=False)
    def __init__(self, *args, **kwargs):
        super(staterep, self).__init__(*args, **kwargs)
        self.fields['subgrname'].choices = [(c.subgroupname, c.subgroupname) for c in tblsubgroup.objects.all().order_by('subgroupcode')]
        self.fields['subgrname'].initial = tblsubgroup.objects.all().order_by('subgroupcode')
        self.fields['enddate'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['startdate'].widget.attrs['class'] = 'loginTxtbox'

class valueform(forms.Form):
    varyear = forms.CharField(label = "Select Year",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))#forms.#forms.ChoiceField(choices=YEAR_CHIOCES)
    excelfile = forms.BooleanField(label='Download In Excel',required=False)
    def __init__(self, *args, **kwargs):
        super(valueform, self).__init__(*args, **kwargs)
        self.fields['varyear'].widget.attrs['class'] = 'loginTxtbox'

class staterepall(forms.Form):
    acccode = forms.CharField(label = "Account Code",max_length = 20,required=False,widget = forms.TextInput(attrs={'readonly':'readonly','size':'10'}))
    accname = forms.CharField(label= "Account Name",max_length = 240,required=False,widget=forms.TextInput(attrs={'size':'20'}))
    startdate = forms.CharField(label = "TransDate",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'10'}))#forms.DateField()#forms.DateField()
    enddate = forms.CharField(label = "TransDate",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'10'}))#forms.DateField()#forms.DateField()
    excelfile = forms.BooleanField(label='Download In Excel',required=False)
    def __init__(self, *args, **kwargs):
        super(staterepall, self).__init__(*args, **kwargs)
        self.fields['enddate'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['startdate'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['acccode'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['accname'].widget.attrs['class'] = 'loginTxtbox'


class chartform(forms.Form):
     excelfile = forms.BooleanField(label='Download In Excel',required=False)

class studentForm(forms.Form):
    admitted_class = forms.ChoiceField(label= 'Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    admitted_arm = forms.ChoiceField(label= 'Arm', choices = [(a.arm, a.arm) for a in Arm.objects.all()])
    excelfile = forms.BooleanField(label='View All',required=False)
    excelfile1 = forms.BooleanField(label='Download In Excel',required=False)
    def __init__(self, *args):
        super(studentForm, self).__init__(*args)
        self.fields['admitted_arm'].choices = [(a.arm, a.arm) for a in Arm.objects.all()]
        self.fields['admitted_arm'].initial = Arm.objects.all()
        self.fields['admitted_class'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['admitted_class'].initial = Class.objects.all()



