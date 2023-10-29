from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from django.views.generic import FormView, ListView

from decorators.messages import eliminar_mensajes
from decorators.user import esta_logueado, modulo_requerido

from ..services.etapas import get_etapas_all, create_etapa, update_etapa

from ..forms import EtapaForm

# Create your views here.

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class EtapaListView(ListView):
    """ Vista de global de estapas """   
    template_name = "proyectos/etapa/index.html"
    context_object_name='etapas'
    paginate_by=15

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        return get_etapas_all(self.request, search)
    
@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class EtapaCreateView(FormView):
    """ Vista de creacion de etapa """
    template_name = "proyectos/etapa/form.html"
    form_class = EtapaForm
    success_url=reverse_lazy('proyectos:etapasIndex')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Etapa'
        context['routes'] = [
            {
                "route":reverse_lazy('proyectos:etapasIndex'),
                "name":'Etapas'
            }
        ]
        return context
    
    def form_valid(self, form) :
        data = form.cleaned_data
        data['nombre'] = str(data['nombre']).upper()
        if create_etapa(self.request, data) == 'error':
            return super(EtapaCreateView, self).form_invalid(form)
        else:
            return super(EtapaCreateView, self).form_valid(form)

@esta_logueado
@modulo_requerido
@eliminar_mensajes
@require_http_methods(["GET"])
def etapa_update_view(request, **kwargs):
    """ Funcion de actualizacion de etapa """
    update_etapa(request, kwargs['id'])
    return redirect("proyectos:etapasIndex")