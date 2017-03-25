from django import forms
import os
import sys
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

MONTH_CHIOCES = (
('01','January'),
('02','February'),
('03','March'),
('04','April'),
('05','May'),
('06','June'),
('07','July'),
('08','August'),
('09','September'),
('10','October'),
('11','November'),
('12','December'),
)


class reconstatementform(forms.Form):
    TYPE_CHOICES =  [(t.accname, t.accname) for t in tblaccount.objects.filter(groupname = "CURRENT ASSETS",subgroupname = "CASH-AND-BANK-BALANCES")]
   # month = forms.ChoiceField(choices=MONTH_CHIOCES)
    #year = forms.ChoiceField(choices=YEAR_CHIOCES)
    transdate = forms.CharField(label = "Date",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    bankname = forms.ChoiceField(choices= TYPE_CHOICES)
    excelfile = forms.BooleanField(label='Download In Excel',required=False)

    def __init__(self, *args):
        super(reconstatementform, self).__init__(*args)
        self.fields['bankname'].choices =  [(t.accname, t.accname) for t in tblaccount.objects.filter(groupname = "CURRENT ASSETS",subgroupname = "CASH-AND-BANK-BALANCES")]
        self.fields['bankname'].initial = tblaccount.objects.filter(groupname = "CURRENT ASSETS",subgroupname = "CASH-AND-BANK-BALANCES")
        self.fields['transdate'].widget.attrs['class'] = 'loginTxtbox'

class unpresentedform(forms.Form):
    acccode = forms.CharField(label = "Acc Code",max_length = 10,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    accname = forms.CharField(label = "Name",max_length = 280,widget = forms.TextInput(attrs={'size':'35'}))
    accbal = forms.CharField(label = "Balance",max_length = 280,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    transdate = forms.CharField(label = "TransDate",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))#forms.DateField()
    transamount = forms.DecimalField(max_digits=20,decimal_places=2)
    particulars = forms.CharField(label = "Particulars",max_length = 380,widget = forms.TextInput(attrs={'size':'35'}))
    refno = forms.CharField(label = "Ref No",max_length = 11)
    def __init__(self, *args, **kwargs):
        super(unpresentedform, self).__init__(*args, **kwargs)
        self.fields['acccode'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['accname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['accbal'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['transdate'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['transamount'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['particulars'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['refno'].widget.attrs['class'] = 'loginTxtbox'


class daterangeform(forms.Form):
    acccode = forms.CharField(label = "Acc Code",max_length = 10,required=False,widget = forms.TextInput(attrs={'readonly':'readonly','size':'10'}))
    accname = forms.CharField(label = "Name",max_length = 280,required=False,widget = forms.TextInput(attrs={'size':'30'}))
    startdate = forms.CharField(label = "Start Date",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'10'}))#forms.DateField()
    enddate = forms.CharField(label = "End Date",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'10'}))#forms.DateField()
    excelfile = forms.BooleanField(label='Download In Excel',required=False)
    def __init__(self, *args, **kwargs):
        super(daterangeform, self).__init__(*args, **kwargs)
        self.fields['acccode'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['accname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['startdate'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['enddate'].widget.attrs['class'] = 'loginTxtbox'




