from django import forms
import os
import sys
from datetime import datetime, timedelta
from myproject.ruffwal.rsetup.models import *

DURATION_CHIOCES = (
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
)

MONTH_CHIOCES = (
('January','January'),
('February','February'),
('March','March'),
('April','April'),
('May','May'),
('June','June'),
('July','July'),
('August','August'),
('September','September'),
('October','October'),
('November','November'),
('December','December'),
)


class invoiceform(forms.Form):
    cuscode = forms.CharField(label = "Customer Id",max_length = 10,required = True)
    cusname = forms.CharField(label = "Name",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    cusbal = forms.CharField(label = "Balance",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    transdate = forms.CharField(label = "TransDate",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))#forms.DateField()
    acccode = forms.CharField(label = "Acc Code",max_length = 10,required = True)
    accname = forms.CharField(label = "Name",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    transamount = forms.DecimalField(max_digits=20,decimal_places=2,required = True)
    particulars = forms.CharField(label = "Particulars",max_length = 380,required = True)
    invoiceno = forms.CharField(label = "Job No",max_length = 11,required = True)


class ledgerform(forms.Form):
    dracccode = forms.CharField(label = "Customer Id",max_length = 10)
    draccname = forms.CharField(label = "Name",max_length = 280,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    dramount = forms.DecimalField(max_digits=20,decimal_places=2)
    drparticulars = forms.CharField(label = "Particulars",max_length = 380)
    drrefno = forms.CharField(label = "Job No",max_length = 11)
    drtransdate = forms.CharField(label = "TransDate",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))

class ledgerform2(forms.Form):
    cracccode = forms.CharField(label = "Acc Code",max_length = 10)
    craccname = forms.CharField(label = "Name",max_length = 280,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    cramount = forms.DecimalField(max_digits=20,decimal_places=2)
    crparticulars = forms.CharField(label = "Particulars",max_length = 380)
    crrefno = forms.CharField(label = "Job No",max_length = 11)
    crtransdate = forms.CharField(label = "TransDate",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))

class standardform(forms.Form):
    dracccode = forms.CharField(label = "Customer Id",max_length = 10)
    draccname = forms.CharField(label = "Name",max_length = 280,widget = forms.Textarea(attrs={'readonly':'readonly','cols':'25','rows':'0'}))
    dramount = forms.DecimalField(max_digits=20,decimal_places=2)
    drparticulars = forms.CharField(label = "Particulars",max_length = 380)
    drrefno = forms.CharField(label = "Job No",max_length = 11)
    cracccode = forms.CharField(label = "Acc Code",max_length = 10)
    craccname = forms.CharField(label = "Name",max_length = 280,widget = forms.Textarea(attrs={'readonly':'readonly','cols':'25','rows':'0'}))
    duration = forms.ChoiceField(choices =DURATION_CHIOCES)

class prostandardform(forms.Form):
    monthly = forms.CharField(label = "TransDate",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))

class verifytransform(forms.Form):
    transid = forms.CharField(label = "verify",max_length = 30)




