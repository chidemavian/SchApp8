from django import forms
import os
import sys
from datetime import datetime, timedelta

MONTH_CHIOCES = (
    (1,'January'),
    (2,'February'),
    (3,'March'),
    (4,'April'),
    (5,'May'),
    (6,'June'),
    (7,'July'),
    (8,'August'),
    (9,'September'),
    (10,'October'),
    (11,'November'),
    (12,'December'),
    )

class userform(forms.Form):
    username = forms.CharField(label = "Username",max_length = 20,required = True)
    staffname = forms.CharField(label = "Staff Name",max_length = 210,required = True,widget = forms.Textarea(attrs={'cols':'25','rows':'0'}))
    expiredate = forms.CharField(label = "Expire Date",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))#forms.DateField()#forms.DateField()
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

class resetuserform(forms.Form):
    username = forms.CharField(label = "Username",max_length = 20,required = True)
    def __init__(self, *args):
        super(resetuserform, self).__init__(*args)
        self.fields['username'].widget.attrs['class'] = 'loginTxtbox'

class verifytransform(forms.Form):
    transid = forms.CharField(label = "Transaction Id",max_length = 35,widget= forms.TextInput(attrs ={'size':'40'}))
    def __init__(self, *args, **kwargs):
        super(verifytransform, self).__init__(*args, **kwargs)
        self.fields['transid'].widget.attrs['class'] = 'loginTxtbox'

class unlockform(forms.Form):
    pin = forms.CharField(label = " Enter PIN",max_length = 12,widget= forms.PasswordInput(attrs ={'size':'12'}))
    def __init__(self, *args):
        super(unlockform, self).__init__(*args)
        self.fields['pin'].widget.attrs['class'] = 'loginTxtbox'

class monthendform(forms.Form):
    month = forms.ChoiceField(choices =MONTH_CHIOCES,label='Start Date')

class paybillform(forms.Form):
    year = forms.IntegerField(label = " Enter Year",min_value=2000,max_value=9999,widget= forms.TextInput(attrs ={'size':'12'}))
    def __init__(self, *args):
        super(paybillform, self).__init__(*args)
        self.fields['year'].widget.attrs['class'] = 'loginTxtbox'

class dateform(forms.Form):
    startdate = forms.CharField(label = "Start Date",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'15'}))#forms.DateField()#forms.DateField()
    enddate = forms.CharField(label = "End Date",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'15'}))#forms.DateField()#forms.DateField()
    def __init__(self, *args, **kwargs):
        super(dateform, self).__init__(*args, **kwargs)
        self.fields['enddate'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['startdate'].widget.attrs['class'] = 'loginTxtbox'

