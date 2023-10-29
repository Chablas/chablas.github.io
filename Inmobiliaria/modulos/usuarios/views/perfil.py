import json

from django.urls import reverse_lazy
from django.views.generic import FormView
from django.utils.decorators import method_decorator

from decorators.user import esta_logueado
from decorators.messages import eliminar_mensajes

from ..services.perfil import update_password

from ..forms import PerfilForm, PerfilPassword

TEMPLEATE_ROOT = 'usuarios'

# Create your views here.

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class PerfilView(FormView):
    """ Vista de actualizacion de Perfil """
    template_name=f"{TEMPLEATE_ROOT}/perfil/form.html"
    success_url=reverse_lazy('usuarios:actualizar-perfil')
    form_class = PerfilForm

    title = None
    perfil = None

    def get_initial(self):
        initial = super().get_initial()
        self.perfil = json.loads(self.request.session.get("usuario"))

        if isinstance(self.perfil,dict):
            self.title = f"{self.perfil['apellidoPaterno']} {self.perfil['apellidoMaterno']}, {self.perfil['nombres']}"
            initial = self.perfil
            initial['rol_id'] = self.perfil['rol']['id']

        return initial


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['routes'] = []
        context['title'] = self.title
        return context

@method_decorator(esta_logueado, name='dispatch')
class UpdateContraseniaView(FormView):
    """ Vista de actualizacion de contraseña """
    template_name=f"{TEMPLEATE_ROOT}/perfil/cambiar_contraseña.html"
    success_url=reverse_lazy('administracion:index')
    form_class = PerfilPassword

    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['routes'] = [
            {
                "route":reverse_lazy('administracion:index'),
                "name":'Administración'
            }
        ]

        context['title'] = "Cambiar Contraseña"

        return context


    def form_valid(self, form):
        data = form.cleaned_data

        if update_password(self.request, data) == 'error':
            return super(UpdateContraseniaView, self).form_invalid(form)

        return super(UpdateContraseniaView, self).form_valid(form)
        