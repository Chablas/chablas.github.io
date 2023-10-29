from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from django.views.generic import FormView, ListView

from decorators.user import esta_logueado, modulo_requerido
from decorators.messages import eliminar_mensajes

from ..services.estados import get_estados_all, create_estado, update_estado

from ..forms import EstadoForm

# Create your views here.

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class EstadoListView(ListView):
    """Vista global de estados de proyectos"""
    template_name = "proyectos/estado/index.html"
    context_object_name='estados'
    paginate_by=15

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        return get_estados_all(self.request, search)

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class EstadoCreateView(FormView):
    """ Vista de creacion de estado """
    template_name = "proyectos/estado/form.html"
    form_class = EstadoForm
    success_url=reverse_lazy('proyectos:estadosIndex')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Estado'
        context['routes'] = [
            {
                "route":reverse_lazy('proyectos:estadosIndex'),
                "name":'Estados'
            }
        ]
        return context
    
    def form_valid(self, form) :
        data = form.cleaned_data
        data['nombre'] = str(data['nombre']).upper()
        if create_estado(self.request, data) == 'error':
            return super(EstadoCreateView, self).form_invalid(form)
        else:
            return super(EstadoCreateView, self).form_valid(form)

@esta_logueado
@modulo_requerido
@eliminar_mensajes
@require_http_methods(["GET"])
def estado_update_view(request, **kwargs):
    """ Funcion de actualizacion de estado """
    update_estado(request, kwargs['id'])
    return redirect("proyectos:estadosIndex")