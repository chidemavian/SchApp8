from django import forms
import os
import sys
from datetime import datetime, timedelta


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

