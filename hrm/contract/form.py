from django import forms
import os
from myproject.hrm.rcsetup.models import *

SEX_CHIOCES = (
    ('Nil','Nil'),
    ('MALE','MALE'),
    ('FEMALE','FEMALE'),
    )

class contractform(forms.Form):
    staffname = forms.CharField(label = "Staff Name",max_length = 310,required = True,widget = forms.TextInput(attrs={'size':'35'}))
    address = forms.CharField(label = "Address",max_length = 280,required = True,widget = forms.TextInput(attrs={'size':'35'}))
    phoneno = forms.CharField(label = "Phone",max_length = 280,required = True,widget = forms.TextInput(attrs={'size':'25'}))#widget = forms.TextInput(attrs={})
    nextofkin = forms.CharField(label = "Next Of Kin",max_length = 280,required = True,widget = forms.TextInput(attrs={'size':'35'}))
    nextofkinphone = forms.CharField(label = "Next Of Kin Phone",max_length = 280,required = True,widget = forms.TextInput(attrs={'size':'25'}))
    accname = forms.ChoiceField(choices =  [(t.name, t.name) for t in tblbank.objects.all().order_by('name')],label='Account Name')
    accno = forms.CharField(label = "Account Number",max_length = 280,required = True,widget = forms.TextInput(attrs={'size':'25'}))
    allowance = forms.DecimalField(max_digits=20,decimal_places=2,required = True,label='Allowance',widget = forms.TextInput(attrs={'size':'25'}))
    #deduction = forms.DecimalField(max_digits=20,decimal_places=2,required = True,label='Deduction',widget = forms.TextInput(attrs={'size':'25'}))
    #overtime = forms.DecimalField(max_digits=20,decimal_places=2,required = True,label='Overtime',widget = forms.TextInput(attrs={'size':'25'}))

    def __init__(self, *args):
        super(contractform, self).__init__(*args)
        self.fields['accname'].choices = [(t.name, t.name) for t in tblbank.objects.all().order_by('name')]
        self.fields['accname'].initial = tblbank.objects.all().order_by('name')
        self.fields['address'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['staffname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['phoneno'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['nextofkin'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['nextofkinphone'].widget.attrs['class'] = 'loginTxtbox'
        #self.fields['accname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['accno'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['allowance'].widget.attrs['class'] = 'loginTxtbox'
       # self.fields['deduction'].widget.attrs['class'] = 'loginTxtbox'
       # self.fields['overtime'].widget.attrs['class'] = 'loginTxtbox'

