from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from decorators.user import esta_logueado
from decorators.messages import eliminar_mensajes

from .services.autenticacion import login, obtener_perfil, logout

from .forms import LoginForm

# Create your views here.
@method_decorator(eliminar_mensajes, name='setup')
class LoginView(FormView):
    """ Vista de inicio de sesion """
    form_class = LoginForm
    template_name = "autenticacion/login.html"
    success_url=reverse_lazy('administracion:index')
    
    def form_valid(self, form):
        data = {
            'username': form.cleaned_data['correoElectronico'],
            'password': form.cleaned_data['password']
        }
        
        # if (login(self.request,data) == 'error'):
        #     return super().form_invalid(form)
        
        # if(obtener_perfil(self.request) == 'error'):
        #     return super().form_invalid(form)

        return super().form_valid(form)
        
@method_decorator(eliminar_mensajes, name='setup')
class DoblePasoView(FormView):
    """ Vista de inicio de sesion """
    form_class = LoginForm
    template_name = "autenticacion/doble-paso.html"
    success_url=reverse_lazy('administracion:index')
    
    def form_valid(self, form):
        data = {
            'username': form.cleaned_data['correoElectronico'],
            'password': form.cleaned_data['password']
        }
        
        if (login(self.request,data) == 'error'):
            return super().form_invalid(form)
        
        if(obtener_perfil(self.request) == 'error'):
            return super().form_invalid(form)

        return super().form_valid(form)

@method_decorator(eliminar_mensajes, name='setup')
class RecuperarContrasenaView(FormView):
    """Vista de inicio de sesion """
    form_class = LoginForm
    template_name = "autenticacion/recuperar-contrasena.html"
    success_url=reverse_lazy('autenticacion:login')

    def form_valid(self, form):
        data = {
            'username': form.cleaned_data['correoElectronico'],
            'password': form.cleaned_data['password']
        }
        
        return super().form_valid(form)
            
@esta_logueado
@eliminar_mensajes
@require_http_methods(["GET"])
def logout_view(request):
    """Sale de la sesión estableciendo al usuario en None"""
    logout(request)
    
    return redirect("autenticacion:login")
