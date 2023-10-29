from django import forms

class MaterialForm(forms.Form):
    nombre = forms.CharField(max_length=150, min_length=3)
    descripcion = forms.CharField(max_length=150, min_length=3)
    unidad_medida_id = forms.ChoiceField()
    categoria_id = forms.ChoiceField()

class MaterialUpdateForm(MaterialForm):
    estado = forms.BooleanField()