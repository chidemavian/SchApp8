from django import forms
import os
import sys
from datetime import datetime, timedelta

class userform(forms.Form):
    username = forms.CharField(label = "Username",max_length = 20,required = True,widget = forms.TextInput(attrs={'size':'35'}))
    staffname = forms.CharField(label = "Staff Name",max_length = 210,required = True,widget = forms.TextInput(attrs={'size':'35'}))
    expiredate = forms.CharField(label = "Expire Date",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'15'}))#forms.DateField()#forms.DateField()
    #set up
    createacc = forms.BooleanField(label = "Create Account",required = False)
    inventory = forms.BooleanField(label = "Create Inventory",required = False)
    payables = forms.BooleanField(label = "Create Payables",required = False)
    receivables = forms.BooleanField(label = "Create Payables",required = False)
    #posting
    invoice = forms.BooleanField(label = "Invoice",required = False)
    receipt = forms.BooleanField(label = "Receipt",required = False)
    payment = forms.BooleanField(label = "Payment",required = False)
    genledger = forms.BooleanField(label = "General Ledger",required = False)
    standardledger = forms.BooleanField(label = "Standard Ledger",required = False)
     #Inventory
    stockin = forms.BooleanField(label = "Stock In",required = False)
    stockout = forms.BooleanField(label = "Stock Out",required = False)
    stockreport = forms.BooleanField(label = "Stock Report",required = False)
    #Work in progess
    jobsetup = forms.BooleanField(label = "Job Setup",required = False)
    addsetup = forms.BooleanField(label = "Additional Setup",required = False)
    jobcosting = forms.BooleanField(label = "Create Payables",required = False)
    returnmat = forms.BooleanField(label = "Return Item",required = False)
    wipinvoice = forms.BooleanField(label = "Invoice",required = False)
    wipreport = forms.BooleanField(label = "Report",required = False)
     #Reconciliation
    unpresented = forms.BooleanField(label = "Unpresented",required = False)
     #Report
    statutory = forms.BooleanField(label = "Statutory Report",required = False)
      #System Admin
    createuser = forms.BooleanField(label = "Create User",required = False)
    resetuser = forms.BooleanField(label = "Reset User",required = False)
    userreport = forms.BooleanField(label = "User Report",required = False)
    rollover = forms.BooleanField(label = "RollOver",required = False)
    def __init__(self, *args, **kwargs):
        super(userform, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['staffname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['expiredate'].widget.attrs['class'] = 'loginTxtbox'

class resetuserform(forms.Form):
    username = forms.CharField(label = "Username",max_length = 20,required = True)
    def __init__(self, *args, **kwargs):
        super(resetuserform, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'loginTxtbox'


class useraccform(forms.Form):
    username = forms.CharField(required = True)
    password = forms.CharField("Password",widget=forms.PasswordInput,required = True)
    def __init__(self, *args, **kwargs):
        super(useraccform, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['password'].widget.attrs['class'] = 'loginTxtbox'

class changepassform(forms.Form):
    oldpassword = forms.CharField("Password",widget=forms.PasswordInput,required = True)
    password = forms.CharField("Password",widget=forms.PasswordInput,required = True)
    password2 = forms.CharField("Password",widget=forms.PasswordInput,required = True)
    def __init__(self, *args, **kwargs):
        super(changepassform, self).__init__(*args, **kwargs)
        self.fields['oldpassword'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['password'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['password2'].widget.attrs['class'] = 'loginTxtbox'

class userloginform(forms.Form):
     email = forms.EmailField(label="Enter Your E-mail",required=True)
     def __init__(self, *args, **kwargs):
         super(userloginform, self).__init__(*args, **kwargs)
         self.fields['email'].widget.attrs['class'] = 'loginTxtbox'
        # self.fields['password'].widget.attrs['class'] = 'loginTxtbox'
        # self.fields['password2'].widget.attrs['class'] = 'loginTxtbox'
