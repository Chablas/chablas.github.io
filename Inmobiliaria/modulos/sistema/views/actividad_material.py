from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import FormView, ListView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from decorators.messages import eliminar_mensajes
from decorators.user import esta_logueado, modulo_requerido

from ..services.actividades import get_actividades_all, create_actividad, update_actividad

from ..forms import ActividadForm

TEMPLEATE_ROOT = 'sistema'

# Create your views here.

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class ActividadesView(ListView):
    """Vista general de las actividades de material"""
    template_name = f"{TEMPLEATE_ROOT}/actividades/index.html"
    context_object_name='actividades'
    paginate_by=15

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        return get_actividades_all(self.request, search)
    
@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class ActividadesCreateView(FormView):
    """ Vista de creacion de actividades """
    template_name =f"{TEMPLEATE_ROOT}/actividades/form.html"
    form_class = ActividadForm
    success_url=reverse_lazy('sistema:actividadesIndex')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Actividad de Material'
        context['routes'] = [
            {
                "route":reverse_lazy('sistema:actividadesIndex'),
                "name":'Actividades de Materiales'
            }
        ]
        return context
    
    def form_valid(self, form) :
        data = form.cleaned_data
        
        data['nombre'] = str(data['nombre']).upper()
        
        if create_actividad(self.request, data) == 'error':
            return super(ActividadesCreateView, self).form_invalid(form)
        else:
            return super(ActividadesCreateView, self).form_valid(form)
        
@esta_logueado
@modulo_requerido
@eliminar_mensajes
@require_http_methods(["GET"])
def actividad_update_view(request, **kwargs):
    """ Funcion de actualizacion de actividad de material """
    update_actividad(request, kwargs['id'])
    return redirect("sistema:actividadesIndex")