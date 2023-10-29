from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from django.views.generic import FormView, ListView

from decorators.user import esta_logueado, modulo_requerido
from decorators.messages import eliminar_mensajes

from ..forms import EmpresaForm

TEMPLEATE_ROOT = 'sistema'

# Create your views here.
@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class EmpresaFormView(FormView):
    """Vista de empresa"""
    template_name = f"{TEMPLEATE_ROOT}/empresa/form.html"
    form_class = EmpresaForm
    success_url=reverse_lazy('seguridad:empresaForm')
    
    def get_initial(self):
        initial = super().get_initial()
        
        data = None
        
        if(isinstance(data, dict)):
            initial = data

        return initial
    
    def form_valid(self, form) :
        data = form.cleaned_data
        data['razon_social'] = str(data['razon_social']).upper()
        # if create_rol(self.request, data) == 'error':
        #     return super(EmpresaFormView, self).form_invalid(form)
        # else:
        return super(EmpresaFormView, self).form_valid(form)