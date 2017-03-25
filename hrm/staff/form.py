from django import forms

class redeploymentform(forms.Form):
    staffname = forms.CharField(label = "Staff Name",max_length = 310,required = True,widget = forms.TextInput(attrs={'size':'35'}))
    def __init__(self, *args):
        super(redeploymentform, self).__init__(*args)
        self.fields['staffname'].widget.attrs['class'] = 'loginTxtbox'

