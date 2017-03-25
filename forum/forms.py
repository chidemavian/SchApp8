from django import forms


class userform(forms.Form):
    email = forms.EmailField(label = "Email Address",max_length = 120,required = True)
    password = forms.CharField("Password",widget=forms.PasswordInput,required = True)



class userregform(forms.Form):
    email = forms.EmailField(label = "Email Address",max_length = 120,required = True)
    password = forms.CharField("Password",widget=forms.PasswordInput,required = True)
    name = forms.CharField(label = "Name",max_length = 250,required = True,widget = forms.Textarea(attrs={'cols':'30','rows':'3'}))

class postform(forms.Form):
    post = forms.CharField(label="Post Your Comment",max_length=300,required=True,widget=forms.Textarea(attrs = {'col':'38','rows':'5'}))
    def __init__(self, *args):
        super(postform, self).__init__(*args)
        self.fields['post'].widget.attrs['class'] = 'loginTxtbox1'

class recoverpassform(forms.Form):
    email = forms.EmailField(label = "Email Address",max_length = 120,required = True)