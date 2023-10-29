from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, FormView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from decorators.messages import eliminar_mensajes
from decorators.user import esta_logueado, modulo_requerido

from ..services.tiposArchivo import get_tipos_archivo_all, create_tipo_archivo, update_tipo_archivo

from ..forms import TipoArchivoForm

TEMPLEATE_ROOT = 'sistema'

# Create your views here.

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class TipoArchivoView(ListView):
    """ Vista global de tipos de archivo """
    template_name = f"{TEMPLEATE_ROOT}/tipo-archivo/index.html"
    context_object_name='tipos_archivo'
    paginate_by=15

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        return get_tipos_archivo_all(self.request, search)

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class TipoArchivoCreateView(FormView):
    """ Vista de creacion de tipo de archivo """
    template_name=f"{TEMPLEATE_ROOT}/tipo-archivo/form.html"
    form_class = TipoArchivoForm
    success_url=reverse_lazy('sistema:tiposArchivoIndex')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        context['title'] = 'Nuevo tipo de archivo'
        context['routes'] = [
            {
                "route": reverse_lazy('sistema:tiposArchivoIndex'),
                "name" :'Tipos de archivo'
            }
        ]
        return context
    
    def form_valid(self, form) :
        data = form.cleaned_data
        data['nombre'] = str(data['nombre']).upper()
        
        if create_tipo_archivo(self.request, data) == 'error':
            return super(TipoArchivoCreateView, self).form_invalid(form)

        return super(TipoArchivoCreateView, self).form_valid(form)

@esta_logueado
@modulo_requerido
@eliminar_mensajes
@require_http_methods(["GET"])
def tipo_archivo_update_view(request, **kwargs):
    """ Funcion de actualizacion de tipo de archivo """
    update_tipo_archivo(request, kwargs['id'])
    return redirect("sistema:tiposArchivoIndex")
