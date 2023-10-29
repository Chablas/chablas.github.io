import os

from datetime import date
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import FormView, ListView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from modulos.seguridad.services.rol import get_roles_cb
from modulos.sistema.services.tipoDocumento import get_tipos_documentos_cb

from helpers.firebase import firebase_generate_url, firebase_upload_image

from decorators.messages import eliminar_mensajes
from decorators.user import esta_logueado, modulo_requerido

from ..services.empleados import get_empleados_all, get_empleado_one, create_empleado, update_empleado, update_estado_empleado

from ..forms import EmpleadoCreateForm, EmpleadoUpdateForm, UsuarioFotoForm

TEMPLEATE_ROOT = 'usuarios'

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class EmpleadosView(ListView):
    """ Vista global de usuarios """
    template_name = f"{TEMPLEATE_ROOT}/empleados/index.html"
    context_object_name='empleados'
    paginate_by=15

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        return get_empleados_all(self.request, search)

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class CreateEmpleadoView(FormView):
    """ Vista de creacion de usuario """
    template_name=f"{TEMPLEATE_ROOT}/empleados/form.html"
    form_class = EmpleadoCreateForm
    success_url=reverse_lazy('usuarios:empleadosIndex')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        context['title'] = 'Nuevo empleado'
        context['routes'] = [
            {
                "route":reverse_lazy('usuarios:empleadosIndex'),
                "name":'Empleados'
            }
        ]
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # form.fields['tipo_documento_id'].choices = get_tipos_documentos_cb(self.request)
        # form.fields['rol_id'].choices = get_roles_cb(self.request)
        
        return form
    
    def form_valid(self, form) :
        data = form.cleaned_data

        data['fecha_contratacion'] = date.strftime(data['fecha_contratacion'], '%Y-%m-%d')
        data['url_foto'] = "Fotos/user-default.jpg"
        
        if create_empleado(self.request, data) == 'error':
            return super(CreateEmpleadoView, self).form_invalid(form)

        return super(CreateEmpleadoView, self).form_valid(form)

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class UpdateEmpleadoView(FormView):
    """ Vista de actualizacion de usuario """
    template_name=f"{TEMPLEATE_ROOT}/empleados/form.html"
    success_url=reverse_lazy('usuarios:empleadosIndex')
    form_class = EmpleadoUpdateForm

    title = None
    empleado = None

    def get_initial(self):
        initial = super().get_initial()
        user_id = self.kwargs['id']

        self.empleado = get_empleado_one(self.request, user_id)
        
        if(isinstance(self.empleado, dict)):
            self.title = f"{self.empleado['apellidoPaterno']} {self.empleado['apellidoMaterno']}, {self.empleado['nombres']}"
            initial = self.empleado
            initial['tipo_documento_id'] = self.empleado['tipoDocumento']['id']
            initial['rol_id'] = self.empleado['rol']['id']

            initial['password'] = None
            initial['password_confirm'] = None


        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = self.title
        context['routes'] = [
            {
                "route":reverse_lazy('usuarios:empleadosIndex'),
                "name":'Empleados'
            }
        ]
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields['tipo_documento_id'].choices = get_tipos_documentos_cb(self.request)
        form.fields['rol_id'].choices = get_roles_cb(self.request)

        form.fields['id'].widget.attrs['readonly'] = True
        form.fields['correo'].widget.attrs['readonly'] = True
        form.fields['celular'].widget.attrs['readonly'] = True
        form.fields['anexo_oficina'].widget.attrs['readonly'] = True
        form.fields['telefono_oficina'].widget.attrs['readonly'] = True
        form.fields['fecha_contratacion'].widget.attrs['readonly'] = True

        form.fields['tipo_documento_id'].widget.attrs['disabled'] = True

        form.fields['tipo_documento_id'].required = False
        form.fields['password'].required = False
        form.fields['password_confirm'].required = False

        form.fields['password'].widget.attrs['placeholder'] = "No es obligatorio"
        form.fields['password_confirm'].widget.attrs['placeholder'] = "No es obligatorio"

        return form

    def form_valid(self, form) :
        data = form.cleaned_data

        data['url_foto'] = self.empleado["url_foto"]
        data['fecha_contratacion'] = date.strftime(data['fecha_contratacion'], '%Y-%m-%d')

        if(data['password'] == ''):
            data['password'] = None
            data['password_confirm'] = None

        print(data)

        if (update_empleado(self.request, data['id'], data) == 'error'):
            return super(UpdateEmpleadoView, self).form_invalid(form)

        return super(UpdateEmpleadoView, self).form_valid(form)

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class UpdateEmpleadoFotoView(FormView):
    """ Vista de actualizacion de usuario """
    template_name=f"{TEMPLEATE_ROOT}/empleados/foto.html"
    success_url=reverse_lazy('usuarios:empleadosIndex')
    form_class = UsuarioFotoForm

    title = None
    empleado = None

    def get_initial(self):
        initial = super().get_initial()
        user_id = self.kwargs['id']

        self.empleado = get_empleado_one(self.request, user_id)
        
        if(isinstance(self.empleado, dict)):
            self.title = f"{self.empleado['apellidoPaterno']} {self.empleado['apellidoMaterno']}, {self.empleado['nombres']}"

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        url_foto = str(self.empleado['url_foto']).capitalize()

        context["foto_usuario"] = firebase_generate_url(url_foto)

        context['title'] = self.title
        context['routes'] = [
            {
                "route":reverse_lazy('usuarios:empleadosIndex'),
                "name":'Empleados'
            }
        ]
        return context
    
    def form_valid(self, form) :
        data = form.cleaned_data
        print(data)
        imagen = data["url_foto"]

        extension = os.path.splitext(imagen.name)[1]

        new_data = {
            'id': self.empleado['id'],
            'nombres': self.empleado['nombres'],
            'apellidoPaterno': self.empleado['apellidoPaterno'],
            'apellidoMaterno': self.empleado['apellidoMaterno'],
            'correo': self.empleado['correo'],
            'direccion': self.empleado['direccion'],
            'rol_id': self.empleado['rol']['id'],
            'nivel': self.empleado['nivel'],
            'url_foto':  f"Fotos/{self.empleado['id']}{extension}"
        }
        
        if (update_empleado(self.request, new_data['id'], new_data) == 'error'):
            return super(UpdateEmpleadoFotoView, self).form_invalid(form)

        firebase_upload_image(imagen, self.empleado['id'])

        return super(UpdateEmpleadoFotoView, self).form_valid(form)

@esta_logueado
@modulo_requerido
@eliminar_mensajes
@require_http_methods(["GET"])
def empleado_estado_update_view(request, **kwargs):
    """ Funcion de actualizacion de estado de un empleado"""
    update_estado_empleado(request, kwargs['id'])
    return redirect("usuarios:empleadosIndex")