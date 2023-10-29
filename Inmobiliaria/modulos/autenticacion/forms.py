from django import forms

class LoginForm(forms.Form):
    correoElectronico = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())

class DoblePasoForm(forms.Form):
    codigo = forms.CharField(max_length=4, min_length=4)
