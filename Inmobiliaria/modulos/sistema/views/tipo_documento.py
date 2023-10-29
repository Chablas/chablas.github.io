from django.shortcuts import redirect
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from decorators.messages import eliminar_mensajes
from decorators.user import esta_logueado, modulo_requerido

from ..services.tipoDocumento import get_tipos_documentos_all, update_tipo_documento

TEMPLEATE_ROOT = 'sistema'

# Create your views here.

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class TipoDocumentoListView(ListView):
    """Vista global de estados de tipos de documento"""
    template_name = f"{TEMPLEATE_ROOT}/tipo-documento/index.html"
    context_object_name='tipos_documento'
    paginate_by=15

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        return get_tipos_documentos_all(self.request, search)

@esta_logueado
@modulo_requerido
@eliminar_mensajes
@require_http_methods(["GET"])
def tipo_documento_update_view(request, **kwargs):
    """ Funcion de actualizacion de etapa """
    update_tipo_documento(request, kwargs['id'])
    return redirect("sistema:tiposDocumentoIndex")