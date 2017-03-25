from django import forms
from myproject.ruffwal.rsetup.models import *
from myproject.ruffwal.asset.models import *

class inventoryform(forms.Form):
    COLOR_CHOICES = [(c.subgroupname, c.subgroupname) for c in tblsubgroup.objects.filter(groupcode ='10000').order_by('subgroupcode')]
    subgrname = forms.ChoiceField(choices=COLOR_CHOICES,label= "Asset Class")
    accname = forms.CharField(label= "Asset Identification/ Name",max_length = 135,widget=forms.TextInput(attrs={'size':'45'}))
    recdate = forms.CharField(label= "Date Of Acquisition/Purchase",max_length = 35,widget=forms.TextInput(attrs={'size':'15','readonly':'readonly'}))
    deprate = forms.DecimalField(label= "Depreciation Rate(i.e 5 for 5%)",max_digits=20,min_value=0,decimal_places=5,initial=0,widget=forms.TextInput(attrs={'size':'35'}))
    department = forms.ChoiceField(choices=[(c.name, c.name) for c in tblassetdepartment.objects.all()],label= "Department")
    span = forms.DecimalField(label= "Life Span (In Years)",min_value=0,max_digits=20,decimal_places=2,initial=0,widget=forms.TextInput(attrs={'size':'35'}))
    opdepn = forms.DecimalField(label= "Opening DEPN.",min_value=0,max_digits=20,decimal_places=2,initial=0,widget=forms.TextInput(attrs={'size':'35'}))
    def __init__(self, *args, **kwargs):
        super(inventoryform, self).__init__(*args, **kwargs)
        self.fields['subgrname'].choices = [(c.subgroupname, c.subgroupname) for c in tblsubgroup.objects.filter(groupcode ='10000').order_by('subgroupcode')]
        self.fields['subgrname'].initial = tblsubgroup.objects.filter(groupcode ='10000').order_by('subgroupcode')
        self.fields['accname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['recdate'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['deprate'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['department'].choices = [(c.name, c.name) for c in tblassetdepartment.objects.all()]
        self.fields['department'].initial = tblassetdepartment.objects.all()
        self.fields['span'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['opdepn'].widget.attrs['class'] = 'loginTxtbox'

class assetdeptform(forms.Form):
    name = forms.CharField(label= "Department Name",max_length = 135,widget=forms.TextInput(attrs={'size':'35'}))
    def __init__(self, *args, **kwargs):
        super(assetdeptform, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'loginTxtbox'

class assetlistform(forms.Form):
    COLOR_CHOICES = [(c.subgroupname, c.subgroupname) for c in tblsubgroup.objects.filter(groupcode ='10000').order_by('subgroupcode')]
    subgrname = forms.ChoiceField(choices=COLOR_CHOICES,label= "Asset Class")
    allasset = forms.BooleanField(label='All Assets',required=False)
    def __init__(self, *args, **kwargs):
        super(assetlistform, self).__init__(*args, **kwargs)
        self.fields['subgrname'].choices = [(c.subgroupname, c.subgroupname) for c in tblsubgroup.objects.filter(groupcode ='10000').order_by('subgroupcode')]
        self.fields['subgrname'].initial = tblsubgroup.objects.filter(groupcode ='10000').order_by('subgroupcode')

class dateform(forms.Form):
    COLOR_CHOICES = [(c.subgroupname, c.subgroupname) for c in tblsubgroup.objects.filter(groupcode ='10000').order_by('subgroupcode')]
    subgrname = forms.ChoiceField(choices=COLOR_CHOICES,label= "Asset Class")
    enddate = forms.CharField(label = "TransDate",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))#forms.
    excelfile = forms.BooleanField(label='Download In Excel',required=False)
    def __init__(self, *args, **kwargs):
        super(dateform, self).__init__(*args, **kwargs)
        self.fields['enddate'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['subgrname'].choices = [(c.subgroupname, c.subgroupname) for c in tblsubgroup.objects.filter(groupcode ='10000').order_by('subgroupcode')]
        self.fields['subgrname'].initial = tblsubgroup.objects.filter(groupcode ='10000').order_by('subgroupcode')

class costform(forms.Form):
    transdate = forms.CharField(label = "Cost Date",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))#forms.
    value = forms.DecimalField(label= "Value",min_value=0,max_digits=20,decimal_places=2,initial=0,widget=forms.TextInput(attrs={'size':'35'}))
    def __init__(self, *args, **kwargs):
        super(costform, self).__init__(*args, **kwargs)
        self.fields['transdate'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['value'].widget.attrs['class'] = 'loginTxtbox'



