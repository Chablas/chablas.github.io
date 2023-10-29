from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import FormView, ListView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from decorators.messages import eliminar_mensajes
from decorators.user import esta_logueado, modulo_requerido

from ..services.unidadmedida import get_unidades_medida_all, create_unidad_medida, update_unidad_medida

from ..forms import UnidadMedidaForm

TEMPLEATE_ROOT = 'sistema'

# Create your views here.

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class UnidadMedidaView(ListView):
    """Vista general de las unidades de medida"""
    template_name = f"{TEMPLEATE_ROOT}/unidad-medida/index.html"
    context_object_name='unidades_medida'
    paginate_by=15

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        return get_unidades_medida_all(self.request, search)

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class UnidadMedidaCreateView(FormView):
    """ Vista de creacion de unidades de medida """
    template_name =f"{TEMPLEATE_ROOT}/unidad-medida/form.html"
    form_class = UnidadMedidaForm
    success_url=reverse_lazy('sistema:unidadesMedidaIndex')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva unidad de medida'
        context['routes'] = [
            {
                "route":reverse_lazy('sistema:unidadesMedidaIndex'),
                "name":'Unidades de medida'
            }
        ]
        return context
    
    def form_valid(self, form) :
        data = form.cleaned_data
        
        data['nombre'] = str(data['nombre']).upper()
        
        if create_unidad_medida(self.request, data) == 'error':
            return super(UnidadMedidaCreateView, self).form_invalid(form)
        else:
            return super(UnidadMedidaCreateView, self).form_valid(form)

@esta_logueado
@modulo_requerido
@eliminar_mensajes
@require_http_methods(["GET"])
def unidad_medida_update_view(request, **kwargs):
    """ Funcion de actualizacion de unidad de medida """
    update_unidad_medida(request, kwargs['id'])
    return redirect("sistema:unidadesMedidaIndex")