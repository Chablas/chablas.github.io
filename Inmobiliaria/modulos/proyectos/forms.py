from datetime import datetime

from django import forms

class EstadoForm(forms.Form):
    nombre = forms.CharField(max_length=150, min_length=3)

class EtapaForm(forms.Form):
    nombre = forms.CharField(max_length=150, min_length=3)

class ZonaForm(forms.Form):
    id = forms.CharField(required=False)
    nombre = forms.CharField(max_length=150, min_length=3)
    descripcion = forms.CharField(max_length=255, min_length=3, widget=forms.Textarea())

class ZonaCreateForm(ZonaForm):
    """Formulario de creacion de zona"""

class ZonaUpdateForm(ZonaForm):
    """Formulario de actulizacion de zona"""
    estado = forms.BooleanField(required=False, initial=True)

class ActividadForm(forms.Form):
    nombre = forms.CharField(max_length=150, min_length=3)
    fecha_inicio = forms.DateField()
    fecha_fin = forms.DateField()
    tipo_actividad = forms.ChoiceField(choices=[(1,'Opción 1')])
    nombre_proyecto= forms.CharField(widget=forms.TextInput({'readonly':True}))
    participantes = forms.CharField(required=False, max_length=150, min_length=3)

    def clean_fecha_fin(self):
        fecha_fin = self.cleaned_data.get('fecha_fin', '')
        fecha_inicio = self.cleaned_data.get('fecha_inicio', '')
        
        if fecha_fin <= fecha_inicio:
            raise forms.ValidationError("La fecha de fin no puede ser anterior o igual a la fecha de inicio")
        
        return fecha_fin
    
class ProyectoForm(forms.Form):
    id = forms.CharField(required=False)
    zona_id = forms.ChoiceField()
    nombre = forms.CharField(max_length=150, min_length=3)
    direccion = forms.CharField(max_length=255, min_length=3)
    descripcion = forms.CharField(max_length=255, min_length=3, widget=forms.Textarea())
    fecha_inicio = forms.DateField()
    fecha_fin = forms.DateField()
    etapa_id = forms.ChoiceField()
    estado_id =forms.ChoiceField()
    proveedores_id = forms.MultipleChoiceField()

    def clean(self):
        cleaned_data = super().clean()
        now = datetime.now()

        f_inicio = cleaned_data.get('fecha_inicio', '')
        f_fin = cleaned_data.get('fecha_fin', '')
        f_actual = datetime.date(datetime(now.year-1, now.month, now.day))       
     
        if f_inicio < f_actual:
            self.add_error('fecha_inicio', "La fecha de inicio no puede ser menor a un año antes")

        if f_fin <= f_inicio:
            self.add_error('fecha_fin', "La fecha de fin no puede ser anterior o igual a la fecha de inicio")

        return cleaned_data

class ArchivoForm(forms.Form):
    """Formulario de archivo"""
    nombre = forms.CharField(max_length=150, min_length=3)
    url_archivo = forms.FileField(allow_empty_file=False, required=True)
    tipo_archivo_id = forms.ChoiceField()
    descripcion = forms.CharField(max_length=255, min_length=3, widget=forms.Textarea())