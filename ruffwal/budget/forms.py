from django import forms

class budgetform(forms.Form):
    accname = forms.CharField(label= "Account Name :",max_length = 240,required=False,widget=forms.TextInput(attrs={'size':'40'}))
    acccode = forms.CharField(label = "Account Code :",max_length = 20,required=False,widget = forms.TextInput(attrs={'readonly':'readonly','size':'35'}))
    acctype = forms.CharField(label = "Account Type :",max_length = 20,required=False,widget = forms.TextInput(attrs={'readonly':'readonly','size':'35'}))
    amount = forms.DecimalField(max_digits=20,decimal_places=2,required = True,label='Budget Value :')
    def __init__(self, *args, **kwargs):
        super(budgetform, self).__init__(*args, **kwargs)
        self.fields['acccode'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['accname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['acctype'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['amount'].widget.attrs['class'] = 'loginTxtbox'

class reportform(forms.Form):
    varyear = forms.CharField(label = "Select Year",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly'}))#forms.#forms.ChoiceField(choices=YEAR_CHIOCES)
    excelfile = forms.BooleanField(label='Download In Excel',required=False)
    def __init__(self, *args, **kwargs):
        super(reportform, self).__init__(*args, **kwargs)
        self.fields['varyear'].widget.attrs['class'] = 'loginTxtbox'

class dateform(forms.Form):
    startdate = forms.CharField(label = "Start Date",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'15'}))#forms.DateField()#forms.DateField()
    enddate = forms.CharField(label = "End Date",max_length = 280,required = True,widget = forms.TextInput(attrs={'readonly':'readonly','size':'15'}))#forms.DateField()#forms.DateField()
    excelfile = forms.BooleanField(label='Download In Excel',required=False)
    def __init__(self, *args, **kwargs):
        super(dateform, self).__init__(*args, **kwargs)
        self.fields['enddate'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['startdate'].widget.attrs['class'] = 'loginTxtbox'

class budgetformmonth(forms.Form):
    accname = forms.CharField(label = "Account Name :",max_length = 240,required=False,widget=forms.TextInput(attrs={'size':'40'}))
    acccode = forms.CharField(label = "Account Code :",max_length = 20,required=False,widget = forms.TextInput(attrs={'readonly':'readonly','size':'35'}))
    acctype = forms.CharField(label = "Account Type :",max_length = 20,required=False,widget = forms.TextInput(attrs={'readonly':'readonly','size':'35'}))
    first = forms.DecimalField(max_digits=20,decimal_places=2,required = True,label='First Month :')
    second = forms.DecimalField(max_digits=20,decimal_places=2,required = True,label='Second Month :')
    third = forms.DecimalField(max_digits=20,decimal_places=2,required = True,label='Third Month :')
    four = forms.DecimalField(max_digits=20,decimal_places=2,required = True,label='Fourth Month :')
    five = forms.DecimalField(max_digits=20,decimal_places=2,required = True,label='Fifth Month :')
    six = forms.DecimalField(max_digits=20,decimal_places=2,required = True,label='Sixth Month :')
    seven = forms.DecimalField(max_digits=20,decimal_places=2,required = True,label='Seventh Month :')
    eight = forms.DecimalField(max_digits=20,decimal_places=2,required = True,label='Eighth Month :')
    nine = forms.DecimalField(max_digits=20,decimal_places=2,required = True,label='Ninth Month :')
    ten = forms.DecimalField(max_digits=20,decimal_places=2,required = True,label='Tenth Month :')
    eleven = forms.DecimalField(max_digits=20,decimal_places=2,required = True,label='Eleventh Month :')
    twelve = forms.DecimalField(max_digits=20,decimal_places=2,required = True,label='Twelfth Month :')
    def __init__(self, *args, **kwargs):
        super(budgetformmonth, self).__init__(*args, **kwargs)
        self.fields['acccode'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['accname'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['acctype'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['first'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['second'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['third'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['four'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['five'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['six'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['seven'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['eight'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['nine'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['ten'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['eleven'].widget.attrs['class'] = 'loginTxtbox'
        self.fields['twelve'].widget.attrs['class'] = 'loginTxtbox'
