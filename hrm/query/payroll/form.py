from django import forms
from myproject.hrm.rcsetup.models import  *
from myproject.hrm.payroll.models import *

DEP_CHOICES =  [(t.name, t.name) for t in tblbank.objects.all().order_by('name')]

deduc_choices = [(t.deddes,t.deddes) for t in tblpayroll.objects.filter(dedamount__gt= 0).order_by('deddes')]

class payrollform1(forms.Form):
    payrolldate = forms.CharField(label = "Payroll Date",max_length = 110,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'15'}))
    def __init__(self, *args):
        super(payrollform1, self).__init__(*args)
        self.fields['payrolldate'].widget.attrs['class'] = 'loginTxtbox'

class bankform(forms.Form):

    staffid = forms.CharField(label = "Staff Id",max_length = 50,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'35'}))
    staffname = forms.CharField(label = "Staff Name",max_length = 310,required = True,widget = forms.TextInput(attrs={'size':'35'}))
    bankname = forms.ChoiceField(choices =  DEP_CHOICES)
    accountno = forms.CharField(label = "Account No",max_length = 280,required = True,widget = forms.TextInput(attrs={'size':'35'}))

    def __init__(self, *args):
        super(bankform, self).__init__(*args)
        self.fields['bankname'].choices = [(t.name, t.name) for t in tblbank.objects.all().order_by('name')]
        self.fields['bankname'].initial = tblbank.objects.all().order_by('name')
        self.fields['accountno'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['staffname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['staffid'].widget.attrs['class'] = 'loginTxtbox'

class payrollform(forms.Form):
    caldate = forms.CharField(label = "TransDate",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'20'}))
    def __init__(self, *args):
        super(payrollform, self).__init__(*args)
        self.fields['caldate'].widget.attrs['class'] = 'loginTxtbox'

class payrollform2(forms.Form):
    bankname = forms.ChoiceField(choices =  DEP_CHOICES)
    caldate = forms.CharField(label = "TransDate",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'20'}))
    excelfile = forms.BooleanField(label='Download In Excel',required=False)
    def __init__(self, *args):
        super(payrollform2, self).__init__(*args)
        self.fields['bankname'].choices = [(t.name, t.name) for t in tblbank.objects.all().order_by('name')]
        self.fields['bankname'].initial = tblbank.objects.all().order_by('name')
        self.fields['caldate'].widget.attrs['class'] = 'loginTxtbox'

class payrollscheduleform(forms.Form):
    caldate = forms.CharField(label = "Date",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'20'}))
    excelfile = forms.BooleanField(label='Download In Excel',required=False)
    def __init__(self, *args):
        super(payrollscheduleform, self).__init__(*args)
        self.fields['caldate'].widget.attrs['class'] = 'loginTxtbox'


class payslipform(forms.Form):
    caldate = forms.CharField(label = "Date",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'20'}))
    staffid = forms.CharField(label = "Staff Id",max_length = 50,required = True,widget = forms.TextInput(attrs={'size':'20'}))
    def __init__(self, *args):
        super(payslipform, self).__init__(*args)
        self.fields['caldate'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['staffid'].widget.attrs['class'] = 'loginTxtbox'


class dedreportform(forms.Form):
    caldate = forms.CharField(label = "Date",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    deductiontype = forms.ChoiceField(choices =  deduc_choices,label='Select Deduction Type')
    excelfile = forms.BooleanField(label='Download In Excel',required=False)
    def __init__(self, *args):
        super(dedreportform, self).__init__(*args)
        self.fields['deductiontype'].choices = deduc_choices
        self.fields['caldate'].widget.attrs['class'] = 'loginTxtbox'

class pensionscheduleform(forms.Form):
    caldate = forms.CharField(label = "Date",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    bankname = forms.ChoiceField(choices =  [(t.accname, t.accname) for t in tblpfa.objects.all().order_by('accname')])
    excelfile = forms.BooleanField(label='Download In Excel',required=False)
    def __init__(self, *args):
        super(pensionscheduleform, self).__init__(*args)
        self.fields['bankname'].choices = [(t.accname, t.accname) for t in tblpfa.objects.all().order_by('accname')]
        self.fields['caldate'].widget.attrs['class'] = 'loginTxtbox'

class loanform(forms.Form):
    bankname = forms.ChoiceField(choices =  [(t.name, t.name) for t in tblloancode.objects.all().order_by('name')])
    caldate = forms.CharField(label = "TransDate",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'20'}))
    def __init__(self, *args):
        super(loanform, self).__init__(*args)
        self.fields['caldate'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['bankname'].choices = [(t.name, t.name) for t in tblloancode.objects.all().order_by('name')]
        self.fields['bankname'].initial = tblloancode.objects.all().order_by('name')

class monthlyjournalform(forms.Form):
    caldate = forms.CharField(label = "Date",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    department = forms.ChoiceField(label="Department" ,choices =   [(t.name, t.name) for t in tbldepartment.objects.all().order_by('name')])
    excelfile = forms.BooleanField(label='View By Department',required=False)
    def __init__(self, *args):
        super(monthlyjournalform, self).__init__(*args)
        self.fields['department'].initial = tbldepartment.objects.all().order_by('name')
        self.fields['department'].choices = [(t.name, t.name) for t in tbldepartment.objects.all().order_by('name')]
        self.fields['caldate'].widget.attrs['class'] = 'loginTxtbox'


