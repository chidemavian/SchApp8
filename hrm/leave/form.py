from django import forms
from myproject.hrm.leave.models import *

class setupform(forms.Form):
    name = forms.CharField(label = "Name",max_length = 150,required = True,widget = forms.TextInput(attrs={'size':'35'}))
    def __init__(self, *args):
        super(setupform, self).__init__(*args)
        self.fields['name'].widget.attrs['class'] = 'loginTxtbox'


class yettotrainform(forms.Form):
    DEP_CHOICES =  [(t.name, t.name) for t in tblleavesetup.objects.all().order_by('name')]
    typeoftrain = forms.ChoiceField(choices = DEP_CHOICES)
    trainyear = forms.IntegerField(max_value = 9999,min_value =1900,widget = forms.TextInput(attrs={'size':'5'}))

    def __init__(self, *args):
        super(yettotrainform, self).__init__(*args)
        self.fields['typeoftrain'].choices = [(t.name, t.name) for t in tblleavesetup.objects.all().order_by('name')]
        self.fields['typeoftrain'].initial = tblleavesetup.objects.all().order_by('name')
        self.fields['trainyear'].widget.attrs['class'] = 'loginTxtbox'