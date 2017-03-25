from django import forms
from myproject.hrm.query.models import *

class setupform(forms.Form):
    name = forms.CharField(label = "Name",max_length = 150,required = True,widget= forms.TextInput(attrs={'size':'35'}))
    def __init__(self, *args):
        super(setupform, self).__init__(*args)
        self.fields['name'].widget.attrs['class'] = 'loginTxtbox'

class querytostaff(forms.Form):
    staffid = forms.CharField(label= 'Staff Id',max_length=150,required= True,widget= forms.TextInput(attrs={'readonly':'readonly','size':'35'}))
    staffname = forms.CharField(label='Staff Name',max_length= 400,widget= forms.TextInput(attrs={'size':'35'}))
    querytype = forms.ChoiceField(label= 'Query Type',choices= [(t.name,t.name) for t in tblquerysetup.objects.all().order_by('name')])
    querydate = forms.CharField(label='Query Date',required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    linemanager = forms.CharField(label='Query Giver',required=True,widget=forms.TextInput(attrs = {'size':'35'}))
    reason = forms.CharField(label='Reason For Query',max_length=1000,required=True,widget=forms.Textarea(attrs={'cols':'25','rows':'4'}))
    action = forms.CharField(label='Action Taken',max_length=1000,required=True,widget=forms.Textarea(attrs={'cols':'25','rows':'4'}))

    def __init__(self, *args):
        super(querytostaff, self).__init__(*args)
        self.fields['querytype'].choices = [(t.name,t.name) for t in tblquerysetup.objects.all().order_by('name')]
        self.fields['querytype'].initial = tblquerysetup.objects.all().order_by('name')
        self.fields['staffid'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['staffname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['querydate'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['linemanager'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['reason'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['action'].widget.attrs['class'] = 'loginTxtbox'

class queryreportform(forms.Form):
    querytype = forms.ChoiceField(label= 'Query Type',choices= [(t.name,t.name) for t in tblquerysetup.objects.all().order_by('name')])
    queryyear = forms.IntegerField(label='Query Year',max_value=9999)
    def __init__(self, *args):
        super(queryreportform, self).__init__(*args)
        self.fields['querytype'].choices = [(t.name,t.name) for t in tblquerysetup.objects.all().order_by('name')]
        self.fields['querytype'].initial = tblquerysetup.objects.all().order_by('name')
        self.fields['queryyear'].widget.attrs['class'] = 'loginTxtbox'

