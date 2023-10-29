import re
from django import forms

class TipoArchivoForm(forms.Form):
    """Formulario de Tipo de archivo"""
    nombre = forms.CharField(max_length=150, min_length=3)

class ActividadForm(forms.Form):
    """Formulario de Actividad"""
    nombre = forms.CharField(max_length=150, min_length=3)

class UnidadMedidaForm(forms.Form):
    nombre = forms.CharField(max_length=150, min_length=3)

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '')
        
        regex = re.compile(r"^([a-zA-Z\s]+)$")

        if regex.match(nombre) is None:
            raise forms.ValidationError("El nombre solo puede tener letras y espacios entre las palabras")
             
        return nombre

class EmpresaForm(forms.Form):
    ruc = forms.CharField(max_length=15, min_length=11)
    razon_social = forms.CharField(max_length=150, min_length=3)
    descripcion = forms.CharField(max_length=150, min_length=3)
    direccion_empresa = forms.CharField(max_length=150, min_length=3)
    direccion_almacen = forms.CharField(max_length=150, min_length=3)
    telefono = forms.CharField(max_length=15, min_length=6)
    email = forms.EmailField(max_length=150, min_length=3)

    def clean(self):
        cleaned_data = super().clean()
        ruc = cleaned_data.get('ruc', '')
        telefono = cleaned_data.get('telefono', '')

        regex = re.compile(r"^(\d*)$")

        if regex.match(ruc) is None:
            self.add_error('ruc', "El RUC debe ser un número válido")
        if regex.match(telefono) is None:
            self.add_error('telefono', "El télefono debe ser un número válido")
       
        return cleaned_data