import re

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.views.generic import FormView, ListView

from decorators.messages import eliminar_mensajes
from decorators.user import esta_logueado, modulo_requerido

from ..forms import LogForm

from ..services.log import get_logs_all, get_logs_one

from helpers.messageBox import emit_message_error

TEMPLEATE_ROOT = 'seguridad'

# Create your views here.

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class LogListView(ListView):
    """Vista global de logs"""
    template_name = f"{TEMPLEATE_ROOT}/log/index.html"
    context_object_name='logs'
    paginate_by=15

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        
        regex = re.compile(r"\d*$")
        length = len(search)

        if(search == '' or regex.match(search) is None or length < 8 or length > 15): 
            emit_message_error(self.request, 'Nro.Documento inválido')
            return []

        return get_logs_all(self.request, search)
    
class LogFormView(FormView):
    """ Vista de un log """
    template_name = f"{TEMPLEATE_ROOT}/log/form.html"
    form_class = LogForm
    title = ''

    def get_initial(self):
        initial = super().get_initial()

        data = get_logs_one(self.request, self.kwargs['id'])

        if(isinstance(data, dict)):
            initial = data['data']
            usuario_id = data['data']['usuario']['id']
            usuario = data['data']['usuario']['apellidoPaterno']+' '+data['data']['usuario']['apellidoMaterno']+', '+data['data']['usuario']['nombres']
            initial['cliente_ip'] = data['client_ip']
            initial['usuario_id'] = usuario_id
            initial['usuario'] = usuario
            self.title = f"{usuario}"

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['routes'] = [
            {
                "route":reverse_lazy('seguridad:logsIndex'),
                "name":'Logs'
            }
        ]
        return context
