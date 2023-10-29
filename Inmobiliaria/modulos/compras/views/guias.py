import re

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.views.generic import ListView, FormView

from decorators.messages import eliminar_mensajes
from decorators.user import esta_logueado, modulo_requerido

from helpers.messageBox import emit_message_error

from ..forms import GuiaRemisionForm

TEMPLEATE_ROOT = 'compras'

# Create your views here.
@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class GuiaDeRemisionListView(ListView):
    """Vista global de guias de remision """
    template_name = f"{TEMPLEATE_ROOT}/guiaRemision/index.html"
    context_object_name='guias'
    paginate_by=15
    #Aqui esta el arreglo
    def get_queryset(self):
        search = self.request.GET.get('search', '')

        regex = re.compile(r"\d*$")

        if(search == '' or regex.match(search) is None):
            emit_message_error(self.request, 'Nro.Orden inválido')
            return []

        return [
            {
                'id': 5,
                'descripcion': 'Cemento',
                'cotizacion': 100
            }  
        ]

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class GuiaRemisionCreateView(FormView):
    """ Vista de creación de guias de remision"""
    template_name = f"{TEMPLEATE_ROOT}/guiaRemision/form.html"
    success_url = reverse_lazy('compras:guiasRemisionIndex')
    form_class = GuiaRemisionForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        context['title'] = "Nueva Guia de Remision"
        context['routes'] = [
             {
                "route":reverse_lazy('compras:guiasRemisionIndex'),
                "name":'Guias de Remision'
            }
        ]
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        return form
    
    def form_valid(self, form) :
        data = form.cleaned_data

        # if 'error':
        #     return super(GuiaRemisionCreateView, self).form_invalid(form)

        return super(GuiaRemisionCreateView, self).form_valid(form)

    
@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class GuiaRemisionUpdateView(FormView):
    """ Vista de actualización de guias de remision"""
    template_name = f"{TEMPLEATE_ROOT}/guiaRemision/form.html"
    success_url = reverse_lazy('compras:guiasRemisionIndex')
    form_class = GuiaRemisionForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        context['title'] = f"Guia de Remision {self.kwargs['id']}"
        context['routes'] = [
            {
                "route":reverse_lazy('compras:guiasRemisionIndex'),
                "name":'Guias de Remision'
            }
        ]
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['almacen_proyecto_id'].choices = [('1', '2')]
        form.fields['estado_remision'].choices = [('1', '2')]
        form.fields['detalle_compra_id'].choices = [('1', '2')]
        
        
        form.fields['detalle_compra_id'].disabled = True
        form.fields['almacen_proyecto_id'].disabled = True
        form.fields['estado_remision'].disabled = True

        form.fields['cantidad'].widget.attrs['readonly'] = True
        form.fields['fecha_entrega'].widget.attrs['readonly'] = True
        return form
    
    def form_valid(self, form) :
        data = form.cleaned_data

        # if 'error':
        #     return super(GuiaRemisionCreateView, self).form_invalid(form)

        return super(GuiaRemisionCreateView, self).form_valid(form)

