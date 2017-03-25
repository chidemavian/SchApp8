from django import forms
import os
import sys
from datetime import datetime, timedelta
from myproject.ruffwal.rsetup.models import *



GROUP_CHOICES1 = [(t.groupname, t.groupname) for t in tblgroup.objects.all().order_by('groupcode')]

GROUP_CHIOCES = (
('FIXED ASSETS','FIXED ASSETS'),
('ACCUMULATED DEPRECIATION','ACCUMULATED DEPRECIATION'),
('CURRENT ASSETS','CURRENT ASSETS'),
('CURRENT LIABILITIES','CURRENT LIABILITIES'),
('LONG TERM LIABILITIES','LONG TERM LIABILITIES'),
('CAPITAL AND RESERVES','CAPITAL AND RESERVES'),
('INCOME','INCOME'),
('EXPENSES','EXPENSES'),
('COST OF SALES','COST OF SALES'),
)
class groupform(forms.Form):
    frgroup = forms.ChoiceField(choices =GROUP_CHOICES1)
    subname = forms.CharField(label = "Sub Group Name",max_length = 280,widget=forms.Textarea(attrs={'cols':'35','rows':'0'}))
    def __init__(self, *args, **kwargs):
        super(groupform, self).__init__(*args, **kwargs)
        self.fields['frgroup'].choices = [(t.groupname, t.groupname) for t in tblgroup.objects.all().order_by('groupcode')]
        self.fields['frgroup'].initial = tblgroup.objects.all().order_by('groupcode')
        self.fields['subname'].widget.attrs['class'] = 'loginTxtbox'
class groupformdetails(forms.Form):
    frgroup = forms.ChoiceField(choices =GROUP_CHIOCES)
class accountform(forms.Form):
    TYPE_CHOICES =  [(t.groupname, t.groupname) for t in tblgroup.objects.all().order_by('groupcode')]
    COLOR_CHOICES = [(c.subgroupname, c.subgroupname) for c in tblsubgroup.objects.all().order_by('subgroupcode')]
    grpname = forms.ChoiceField(choices=TYPE_CHOICES)
    subgrname = forms.ChoiceField(label= 'Subject', choices = COLOR_CHOICES)
    accname = forms.CharField(label= "Account Name",max_length = 35,widget=forms.TextInput(attrs={'size':'35'}))
    def __init__(self, *args, **kwargs):
        super(accountform, self).__init__(*args, **kwargs)
        self.fields['subgrname'].choices = [(c.subgroupname, c.subgroupname) for c in tblsubgroup.objects.all().order_by('subgroupcode')]
        self.fields['subgrname'].initial = tblsubgroup.objects.all().order_by('subgroupcode')
        self.fields['accname'].widget.attrs['class'] = 'loginTxtbox'


class inventoryform(forms.Form):
    COLOR_CHOICES = [(c.accname, c.accname) for c in tblaccount.objects.filter(subgroupname = 'STOCKS',groupname ='CURRENT ASSETS').order_by('acccode')]
    subgrname = forms.ChoiceField(choices=COLOR_CHOICES)
    accname = forms.CharField(label= "Account Name",max_length = 35,widget=forms.TextInput(attrs={'size':'35'}))
    def __init__(self, *args, **kwargs):
        super(inventoryform, self).__init__(*args, **kwargs)
        self.fields['subgrname'].choices = [(c.accname, c.accname) for c in tblaccount.objects.filter(subgroupname = 'STOCKS',groupname ='CURRENT ASSETS').order_by('acccode')]
        self.fields['subgrname'].initial = tblaccount.objects.filter(subgroupname = 'STOCKS',groupname ='CURRENT ASSETS').order_by('acccode')
        self.fields['accname'].widget.attrs['class'] = 'loginTxtbox'

class debtorsform(forms.Form):
      accname = forms.CharField(label= "Account Name",max_length = 35,widget=forms.TextInput(attrs={'size':'35'}))
      address = forms.CharField(label= "Address",max_length = 300,widget=forms.Textarea(attrs={'cols':'35','rows':'2'}))
      phoneno = forms.CharField(label= "Phone No",max_length = 35)
      def __init__(self, *args, **kwargs):
          super(debtorsform, self).__init__(*args, **kwargs)
          self.fields['phoneno'].widget.attrs['class'] = 'loginTxtbox'
          self.fields['accname'].widget.attrs['class'] = 'loginTxtbox'

class creditorsform(forms.Form):
      accname = forms.CharField(label= "Account Name",max_length = 300,widget=forms.Textarea(attrs={'cols':'35','rows':'0'}))
      address = forms.CharField(label= "Address",max_length = 300,widget=forms.Textarea(attrs={'cols':'35','rows':'2'}))
      phoneno = forms.CharField(label= "Phone No",max_length = 100)
      def __init__(self, *args, **kwargs):
          super(creditorsform, self).__init__(*args, **kwargs)
          self.fields['phoneno'].widget.attrs['class'] = 'loginTxtbox'
          self.fields['accname'].widget.attrs['class'] = 'loginTxtbox'
class ministoreform(forms.Form):
    accname = forms.CharField(label= "Name",max_length = 300,widget=forms.TextInput(attrs={'size':'35'}))
    def __init__(self, *args, **kwargs):
        super(ministoreform, self).__init__(*args, **kwargs)
        self.fields['accname'].widget.attrs['class'] = 'loginTxtbox'

class studentaccform(forms.Form):
    accname = forms.CharField(label= "Account Name",max_length = 300,widget=forms.Textarea(attrs={'cols':'35','rows':'0'}))
    accno = forms.CharField(label= "Account No",max_length = 300)
