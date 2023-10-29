import re
from datetime import datetime 

from django import forms

class PerfilForm(forms.Form):
    nombres = forms.CharField(max_length=150, disabled=True)
    apellidoPaterno = forms.CharField(max_length=100, disabled=True)
    apellidoMaterno = forms.CharField(max_length=100, disabled=True)
    direccion = forms.CharField(max_length=255, disabled=True)
    url_foto = forms.CharField(required=False, max_length=150, disabled=True)
    celular = forms.CharField(min_length=9, max_length=9, disabled=True)

class PerfilPassword(forms.Form):
    password = forms.CharField(max_length=150, widget=forms.PasswordInput())
    password_new =  forms.CharField(max_length=150, widget=forms.PasswordInput())
    password_new_confirm = forms.CharField(max_length=150, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()

        password_new = cleaned_data.get('password_new', '')
        password_new_confirm = cleaned_data.get('password_new_confirm', '')

        if password_new != password_new_confirm:
            self.add_error('password_new', "La nueva contraseña y confirmar contraseña no coinciden")
            self.add_error('password_new_confirm', "La nueva contraseña y confirmar contraseña no coinciden")
        
        return cleaned_data

class UsuarioForm(forms.Form):
    """Formulario global de un usuario"""
    id = forms.CharField(min_length=8, max_length=15)
    nombres = forms.CharField(max_length=150)
    apellidoPaterno = forms.CharField(max_length=100)
    apellidoMaterno = forms.CharField(max_length=100)
    direccion = forms.CharField(max_length=255)
    tipo_documento_id = forms.ChoiceField()
    password = forms.CharField(max_length=150, widget=forms.PasswordInput())
    password_confirm = forms.CharField(max_length=150, widget=forms.PasswordInput())
    rol_id = forms.ChoiceField()
    correo = forms.EmailField(max_length=100)
    celular = forms.CharField(min_length=9, max_length=9)
    nivel = forms.CharField(min_length=1, max_length=1, widget=forms.NumberInput(attrs={'min':'1'}))
    fecha_contratacion = forms.DateField()

    def clean_password_confirm(self):
        """Validacion de confirmacion de contraseña"""
        password = self.cleaned_data.get('password', '')
        password_confirm = self.cleaned_data.get('password_confirm', '')
        
        if password_confirm is None:
            return password_confirm
        
        if password != password_confirm:
            raise forms.ValidationError("El campo contraseña y confirmar contaseña deben ser iguales")
        
        return password_confirm

class EmpleadoForm(UsuarioForm):
    """Formulario global de un empleado"""
    telefono_oficina = forms.CharField(max_length=20)
    anexo_oficina = forms.CharField(max_length=10)

    def clean(self):
        cleaned_data = super().clean()
        id = cleaned_data.get('id', '')
        celular = cleaned_data.get('celular', '')
        telefono_oficina = cleaned_data.get('telefono_oficina', '')
        anexo_oficina = cleaned_data.get('anexo_oficina', '')

        regex = re.compile(r"\d*$")

        if regex.match(id) is None:
            self.add_error('celular', "Numero de documento inválido")
        if regex.match(celular) is None:
            self.add_error('celular', "Numero de celular inválido")
        if regex.match(telefono_oficina) is None:
            self.add_error('telefono_oficina', "Telefono de oficina inválido")
        if regex.match(anexo_oficina) is None:
            self.add_error('anexo_oficina', "Anexo de oficina inválido")
       
        return cleaned_data

class EmpleadoCreateForm(EmpleadoForm):
    """Formulario para creacion de empleado"""
    def clean_fecha_contratacion(self):
        """Validacion de fecha de contratacion"""
        fecha_contratacion = self.cleaned_data.get('fecha_contratacion', '')
     
        fecha_actual = datetime.date(datetime.now())
        current_year = fecha_actual.year - 1
        old_date = datetime.date(datetime.strptime(f"01-01-{current_year}", "%d-%m-%Y"))

        if fecha_contratacion > fecha_actual:
            raise forms.ValidationError("La fecha de contratación no puede se mayor a la fecha actual")
        if fecha_contratacion < old_date:
            raise forms.ValidationError(f"La fecha de contratación no puede ser menor a 01/01/{current_year}")

        return fecha_contratacion

class EmpleadoUpdateForm(EmpleadoForm):
    """Formulario para actualizacion de un usuario"""

class IndependienteForm(UsuarioForm):
    """Formulario para creacion de independiente"""
    proyecto_id = forms.ChoiceField()
    password = forms.CharField(max_length=150, widget=forms.PasswordInput())
    password_confirm = forms.CharField(max_length=150, widget=forms.PasswordInput())

    def clean_fecha_contratacion(self):
        """Validacion de fecha de contratacion"""
        fecha_contratacion = self.cleaned_data.get('fecha_contratacion', '')

        if fecha_contratacion is None:
            return fecha_contratacion
        
        fecha_actual = datetime.date(datetime.now())
        current_year = fecha_actual.year - 1
        old_date = datetime.date(datetime.strptime(f"01-01-{current_year}", "%d-%m-%Y"))

        if fecha_contratacion > fecha_actual:
            raise forms.ValidationError("La fecha de contratación no puede se mayor a la fecha actual")
        if fecha_contratacion < old_date:
            raise forms.ValidationError(f"La fecha de contratación no puede ser menor a 01/01/{current_year}")

        return fecha_contratacion

    def clean(self):
        cleaned_data = super().clean()
        celular = cleaned_data.get('celular', '')

        regex = re.compile(r"\d*$")

        if regex.match(celular) is None:
            self.add_error('celular', "Numero de celular inválido")
       
        return cleaned_data

class UsuarioFotoForm(forms.Form):
    """Formulario de foto de un usuario"""
    id = forms.CharField(required=False)
    url_foto = forms.FileField(allow_empty_file=False, required=True)
