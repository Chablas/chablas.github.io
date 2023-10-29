from django import forms

class RolForm(forms.Form):
    nombre = forms.CharField(max_length=150, min_length=3)
    
class RolModuloForm(forms.Form):
    id = forms.CharField(required=False, disabled=True, widget=forms.TextInput({'hidden' : True}))
    modulo_to_allocate = forms.ChoiceField(required=False)
    modulo_to_deallocate = forms.ChoiceField(required=False)

class LogForm(forms.Form):
    usuario_id = forms.CharField(widget=forms.TextInput({'readonly' : True}))
    usuario = forms.CharField(widget=forms.TextInput({'readonly' : True}))
    cliente_ip = forms.CharField(widget=forms.TextInput({'readonly' : True}))
    datos_entrada = forms.CharField(widget=forms.Textarea({'readonly' : True}))
    datos_salida = forms.CharField(widget=forms.Textarea({'readonly' : True}))
    endpoint = forms.CharField(widget=forms.TextInput({'readonly' : True}))
    accion = forms.CharField(widget=forms.TextInput({'readonly' : True}))
    fecha = forms.CharField(widget=forms.TextInput({'readonly' : True}))
    hora = forms.CharField(widget=forms.TextInput({'readonly' : True}))
    navegador = forms.CharField(widget=forms.TextInput({'readonly' : True}))