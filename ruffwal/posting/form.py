from django import forms
from myproject.bill.models import *
from myproject.sysadmin.models import *
from myproject.student.models import *
currse = currentsession.objects.get(id = 1)

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

class invoiceformsc(forms.Form):
    session = forms.CharField(label='Session',max_length= 190,required=True,widget= forms.TextInput(attrs ={'size':10}),initial=currse)
    klass = forms.ChoiceField(label='Class',choices = [(c.klass, c.klass) for c in Class.objects.all()])
    term = forms.ChoiceField(label='Term',choices=(('First', 'First'), ('Second', 'Second'), ('Third', 'Third')))
    def __init__(self, *args):
        super(invoiceformsc, self).__init__(*args)
        self.fields['klass'].choices = [(c.klass, c.klass) for c in Class.objects.all()]
        self.fields['klass'].initial = Class.objects.all()
        self.fields['session'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['term'].choices = [(a.term, a.term) for a in tblterm.objects.filter(status = 'ACTIVE')]
       # self.fields['name'].choices = [(c.fullname, c.fullname) for c in Student.objects.all()]
        # self.fields['name'].initial = Class.objects.all()

class invoiceform(forms.Form):
    cuscode = forms.CharField(label = "Customer Id",max_length = 25,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    cusname = forms.CharField(label = "Name",max_length = 280,required = True,widget = forms.TextInput(attrs={'size':'35'}))
    cusbal = forms.CharField(label = "Balance",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    transdate = forms.CharField(label = "TransDate",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    acccode = forms.CharField(label = "Acc Code",max_length = 20,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    accname = forms.CharField(label = "Name",max_length = 280,required = True,widget = forms.TextInput(attrs={'size':'35'}))
    transamount = forms.DecimalField(max_digits=25,decimal_places=2,required = True)
    particulars = forms.CharField(label = "Particulars",max_length = 380,required = True, widget = forms.TextInput(attrs={'size':'45'}))
    invoiceno = forms.CharField(label = "Job No",max_length = 25,required = True)
    def __init__(self, *args, **kwargs):
        super(invoiceform, self).__init__(*args, **kwargs)
        self.fields['cuscode'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['cusname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['cusbal'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['transdate'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['acccode'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['accname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['transamount'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['particulars'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['invoiceno'].widget.attrs['class'] = 'loginTxtbox'


class ledgerform(forms.Form):
    dracccode = forms.CharField(label = "Customer Id",max_length = 35,widget = forms.TextInput(attrs={'readonly':'readonly','size':'35'}))
    draccname = forms.CharField(label = "Name",max_length = 280,widget = forms.TextInput(attrs={'size':'35'}))
    dramount = forms.DecimalField(max_digits=20,decimal_places=2,widget = forms.TextInput(attrs={'size':'35'}))
    drparticulars = forms.CharField(label = "Particulars",max_length = 380,widget = forms.TextInput(attrs={'size':'35'}))
    drrefno = forms.CharField(label = "Job No",max_length = 41)
    drtransdate = forms.CharField(label = "TransDate",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))#forms.DateField()
    def __init__(self, *args, **kwargs):
        super(ledgerform, self).__init__(*args, **kwargs)
        self.fields['dracccode'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['draccname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['dramount'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['drparticulars'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['drrefno'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['drtransdate'].widget.attrs['class'] = 'loginTxtbox'

class ledgerform2(forms.Form):
    cracccode = forms.CharField(label = "Acc Code",max_length = 35,widget = forms.TextInput(attrs={'readonly':'readonly','size':'35'}))
    craccname = forms.CharField(label = "Name",max_length = 280,widget = forms.TextInput(attrs={'size':'35'}))
    cramount = forms.DecimalField(max_digits=20,decimal_places=2,widget = forms.TextInput(attrs={'size':'35'}))
    crparticulars = forms.CharField(label = "Particulars",max_length = 380,widget = forms.TextInput(attrs={'size':'35'}))
    crrefno = forms.CharField(label = "Job No",max_length = 41)
    crtransdate = forms.CharField(label = "TransDate",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))#forms.DateField()
    def __init__(self, *args, **kwargs):
        super(ledgerform2, self).__init__(*args, **kwargs)
        self.fields['cracccode'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['craccname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['cramount'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['crparticulars'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['crrefno'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['crtransdate'].widget.attrs['class'] = 'loginTxtbox'

class standardform(forms.Form):
    dracccode = forms.CharField(label = "Customer Id",max_length = 35,widget = forms.TextInput(attrs={'readonly':'readonly','size':'35'}))
    draccname = forms.CharField(label = "Name",max_length = 280,widget = forms.TextInput(attrs={'size':'35'}))
    dramount = forms.DecimalField(max_digits=20,decimal_places=2)
    drparticulars = forms.CharField(label = "Particulars",max_length = 380,widget = forms.TextInput(attrs={'size':'35'}))
    drrefno = forms.CharField(label = "Job No",max_length = 41)
    cracccode = forms.CharField(label = "Acc Code",max_length = 35,widget = forms.TextInput(attrs={'readonly':'readonly','size':'35'}))
    craccname = forms.CharField(label = "Name",max_length = 280,widget = forms.TextInput(attrs={'size':'35'}))
    duration = forms.IntegerField(label='Duration',widget = forms.TextInput(attrs={'size':'6'}))

    def __init__(self, *args, **kwargs):
        super(standardform, self).__init__(*args, **kwargs)
        self.fields['dracccode'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['draccname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['dramount'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['drparticulars'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['drrefno'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['cracccode'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['craccname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['duration'].widget.attrs['class'] = 'loginTxtbox'


class prostandardform(forms.Form):
    monthly = forms.CharField(label = "TransDate",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))#forms.DateField()#forms.DateField()

class verifytransform(forms.Form):
    transid = forms.CharField(label = "verify",max_length = 30)
    def __init__(self, *args, **kwargs):
        super(verifytransform, self).__init__(*args, **kwargs)
        self.fields['transid'].widget.attrs['class'] = 'loginTxtbox'

class pocketform(forms.Form):
    cuscode = forms.CharField(label = "Customer Id",max_length = 25,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    cusname = forms.CharField(label = "Name",max_length = 280,required = True,widget = forms.TextInput(attrs={'size':'35'}))
    cusbal = forms.CharField(label = "Balance",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    transdate = forms.CharField(label = "TransDate",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    acccode = forms.CharField(label = "Acc Code",max_length = 20,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    accname = forms.CharField(label = "Name",max_length = 280,required = True,widget = forms.TextInput(attrs={'size':'35','readonly':'readonly'}))
    transamount = forms.DecimalField(max_digits=25,decimal_places=2,required = True)
    particulars = forms.ChoiceField(label='Particulars',choices=(('Deposit', 'Deposit'), ('Cloth Repair', 'Cloth Repair'), ('Bag Repair', 'Bag Repair'),('Photocopy', 'Photocopy'),('Hair Cut', 'Hair Cut'),('Hair Dressing', 'Hair Dressing'),('Tuck Shop', 'Tuck Shop'),('Shoe Repair', 'Shoe Repair'),('Repairs', 'Repairs'),('Refund', 'Refund'),('Name Tagging', 'Name Tagging'),('Offering', 'Offering'),('Others', 'Others')))
    invoiceno = forms.CharField(label = "Job No",max_length = 25,required = True)
    def __init__(self, *args, **kwargs):
        super(pocketform, self).__init__(*args, **kwargs)
        self.fields['cuscode'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['cusname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['cusbal'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['transdate'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['acccode'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['accname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['transamount'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['particulars'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['invoiceno'].widget.attrs['class'] = 'loginTxtbox'





