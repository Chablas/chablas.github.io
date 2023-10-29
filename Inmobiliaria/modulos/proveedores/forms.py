from datetime import datetime

from django import forms

class CategoriaForm(forms.Form):
    """Formulario de Categoria"""
    id = forms.CharField(required=False)
    nombre = forms.CharField(max_length=150, min_length=3)

class ProveedorForm(forms.Form):
    """Formulario global de proveedor"""
    id = forms.CharField(max_length=15, min_length=8)
    nombre_empresa = forms.CharField(max_length=150, min_length=3)
    direccion_empresa = forms.CharField(max_length=255, min_length=3)
    correo_empresa = forms.EmailField(max_length=100, min_length=3)
    telefono_empresa = forms.CharField(max_length=20, min_length=3)
    nombre_representante = forms.CharField(max_length=150, min_length=3)
    correo_representante = forms.CharField(max_length=100, min_length=3)
    telefono_representante = forms.CharField(max_length=20, min_length=3)
  
class ProveedorCreateForm(ProveedorForm):
    """Formulario de creacion de proveedor"""
    id_categoria_empresas = forms.ChoiceField()
    id_zonas = forms.ChoiceField()

class ProveedorUpdateForm(ProveedorForm):
    """Formulario de creacion de proveedor"""
    estado = forms.BooleanField(required=False, initial=True)

class ProveedorCategoriaForm(forms.Form):
    """Formulario de Categoria de un proveedor"""
    id = forms.CharField(required=False, disabled=True, widget=forms.TextInput({'hidden' : True}))
    id_categoria_to_deallocate = forms.ChoiceField(required=False)
    id_categoria_to_allocate = forms.ChoiceField(required=False)

class ProveedorZonaForm(forms.Form):
    """Formulario de Zona de un proveedor"""
    id = forms.CharField(required=False, disabled=True, widget=forms.TextInput({'hidden' : True}))
    id_zona_to_deallocate = forms.ChoiceField(required=False)
    id_zona_to_allocate = forms.ChoiceField(required=False)

class MaterialForm(forms.Form):
    codigo_proveedor = forms.CharField(max_length=150, min_length=1)
    categoria_id = forms.ChoiceField()
    unidad_medida_id = forms.ChoiceField()
    cantidad_contenedora = forms.IntegerField(min_value=1)
    descripcion = forms.CharField(max_length=150, min_length=3)
    precio_actual = forms.DecimalField(max_digits = 6, decimal_places = 2, min_value=0.01)
    fecha_vencimiento = forms.DateField()

class MaterialCreateForm(MaterialForm):
    def clean_fecha_vencimiento(self):
        f_vencimiento = self.cleaned_data.get('fecha_vencimiento', '')
        f_actual = datetime.date(datetime.now())

        if f_vencimiento <= f_actual:
            raise forms.ValidationError("La fecha de vencimiento no puede ser anterior o igual a la fecha actual")
             
        return f_vencimiento
    
class MaterialUpdateForm(MaterialForm):
    fecha_creacion = forms.DateField()

    def clean(self):
        cleaned_data = super().clean()

        f_vencimiento = cleaned_data.get('fecha_vencimiento', '')
        f_creacion = cleaned_data.get('fecha_creacion', '')

        if f_vencimiento < f_creacion:
            self.add_error('fecha_vencimiento', "La fecha de vencimiento no puede ser anterior a la fecha de creación")
             
        return cleaned_data