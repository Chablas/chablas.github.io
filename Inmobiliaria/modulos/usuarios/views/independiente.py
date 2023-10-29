import os

from datetime import date
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import FormView, ListView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from modulos.seguridad.services.rol import get_roles_cb
from modulos.sistema.services.tipoDocumento import get_tipos_documentos_cb
from modulos.proyectos.services.proyectos import get_proyectos_cb

from helpers.firebase import firebase_generate_url, firebase_upload_image

from decorators.messages import eliminar_mensajes
from decorators.user import esta_logueado, modulo_requerido

from ..services.empleados import get_empleado_one
from ..services.independientes import get_independientes_all, get_independiente_one, create_independiente, update_independiente, update_estado_independiente

from ..forms import UsuarioFotoForm, IndependienteForm

TEMPLEATE_ROOT = 'usuarios'

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class IndependienteView(ListView):
    """ Vista global de independientes """
    template_name = f"{TEMPLEATE_ROOT}/independiente/index.html"
    context_object_name='independientes'
    paginate_by=15

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        return get_independientes_all(self.request, search)

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class IndependienteCreateView(FormView):
    """ Vista de creacion de independiente """
    template_name=f"{TEMPLEATE_ROOT}/independiente/form.html"
    form_class = IndependienteForm
    success_url=reverse_lazy('usuarios:independientesIndex')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        context['title'] = 'Nuevo independiente'
        context['routes'] = [
            {
                "route":reverse_lazy('usuarios:independientesIndex'),
                "name":'Independientes'
            }
        ]
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields['tipo_documento_id'].choices = get_tipos_documentos_cb(self.request)
        form.fields['rol_id'].choices = get_roles_cb(self.request)
        form.fields['proyecto_id'].choices = get_proyectos_cb(self.request)

        return form
    
    def form_valid(self, form) :
        data = form.cleaned_data

        data['fecha_contratacion'] = date.strftime(data['fecha_contratacion'], '%Y-%m-%d')
        data['inicio_proyecto'] = "2021-01-01"
        data['url_foto'] = "Fotos/user-default.jpg"
        
        if create_independiente(self.request, data) == 'error':
            return super(IndependienteCreateView, self).form_invalid(form)

        return super(IndependienteCreateView, self).form_valid(form)

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class IndependienteUpdateView(FormView):
    """ Vista de actualizacion de independiente """
    template_name=f"{TEMPLEATE_ROOT}/independiente/form.html"
    success_url=reverse_lazy('usuarios:independientesIndex')
    form_class = IndependienteForm

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
            initial['proyecto_id'] = self.empleado['proyecto']['id']
            
            initial['password'] = None
            initial['password_confirm'] = None


        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = self.title
        context['routes'] = [
            {
                "route":reverse_lazy('usuarios:independientesIndex'),
                "name":'Independientes'
            }
        ]
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['tipo_documento_id'].choices = get_tipos_documentos_cb(self.request)
        form.fields['rol_id'].choices = get_roles_cb(self.request)
        form.fields['proyecto_id'].choices = get_proyectos_cb(self.request)

        form.fields['id'].widget.attrs['readonly'] = True
        form.fields['correo'].widget.attrs['readonly'] = True
        form.fields['celular'].widget.attrs['readonly'] = True
        form.fields['fecha_contratacion'].widget.attrs['disabled'] = True

        form.fields['tipo_documento_id'].widget.attrs['disabled'] = True
        form.fields['proyecto_id'].widget.attrs['disabled'] = True

        form.fields['fecha_contratacion'].required = False
        form.fields['tipo_documento_id'].required = False
        form.fields['proyecto_id'].required = False
        form.fields['password'].required = False
        form.fields['password_confirm'].required = False

        form.fields['password'].widget.attrs['placeholder'] = "No es obligatorio"
        form.fields['password_confirm'].widget.attrs['placeholder'] = "No es obligatorio"
        return form

    def form_valid(self, form) :
        data = form.cleaned_data

        data['url_foto'] = self.empleado["url_foto"]

        if(data['password'] == ''):
            data['password'] = None
            data['password_confirm'] = None

        if (update_independiente(self.request, data['id'], data) == 'error'):
            return super(IndependienteUpdateView, self).form_invalid(form)

        return super(IndependienteUpdateView, self).form_valid(form)
    
@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class IndependienteFotoView(FormView):
    """ Vista de actualizacion de usuario """
    template_name=f"{TEMPLEATE_ROOT}/independiente/foto.html"
    success_url=reverse_lazy('usuarios:independientesIndex')
    form_class = UsuarioFotoForm

    title = None
    independiente = None

    def get_initial(self):
        initial = super().get_initial()
        user_id = self.kwargs['id']

        self.independiente = get_independiente_one(self.request, user_id)
        
        if(isinstance(self.independiente, dict)):
            self.title = f"{self.independiente['apellidoPaterno']} {self.independiente['apellidoMaterno']}, {self.independiente['nombres']}"

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        url_foto = str(self.independiente['url_foto']).capitalize()

        context["foto_usuario"] = firebase_generate_url(url_foto)

        context['title'] = self.title
        context['routes'] = [
            {
                "route":reverse_lazy('usuarios:independientesIndex'),
                "name":'independientes'
            }
        ]
        return context
    
    def form_valid(self, form) :
        data = form.cleaned_data
        print(data)
        imagen = data["url_foto"]

        extension = os.path.splitext(imagen.name)[1]

        new_data = {
            'id': self.independiente['id'],
            'nombres': self.independiente['nombres'],
            'apellidoPaterno': self.independiente['apellidoPaterno'],
            'apellidoMaterno': self.independiente['apellidoMaterno'],
            'correo': self.independiente['correo'],
            'direccion': self.independiente['direccion'],
            'rol_id': self.independiente['rol']['id'],
            'nivel': self.independiente['nivel'],
            'url_foto':  f"Fotos/{self.independiente['id']}{extension}"
        }
        
        if (update_independiente(self.request, new_data['id'], new_data) == 'error'):
            return super(IndependienteFotoView, self).form_invalid(form)

        firebase_upload_image(imagen, self.independiente['id'])

        return super(IndependienteFotoView, self).form_valid(form)

@esta_logueado
@modulo_requerido
@eliminar_mensajes
@require_http_methods(["GET"])
def independiente_estado_update_view(request, **kwargs):
    """ Funcion de actualizacion de estado de un independiente"""
    update_estado_independiente(request, kwargs['id'])
    return redirect("usuarios:independientesIndex")