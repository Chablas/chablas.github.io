from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.views.generic import ListView, FormView

from decorators.user import esta_logueado, modulo_requerido
from decorators.messages import eliminar_mensajes

from ..forms import OrdenCompraForm

TEMPLEATE_ROOT = 'compras'

# Create your views here.
@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class OrdenCompraListView(ListView):
    """Vista global de ordenes de compra """
    template_name = f"{TEMPLEATE_ROOT}/ordenCompra/index.html"
    context_object_name='compras'
    paginate_by=15
    #Aqui esta el arreglo
    def get_queryset(self):
        search = self.request.GET.get('search', '')
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
class OrdenCompraUpdateView(FormView):
    """ Vista de actualizacion de ordenes de compra"""
    template_name = f"{TEMPLEATE_ROOT}/ordenCompra/form.html"
    success_url = reverse_lazy('compras:comprasList')
    form_class = OrdenCompraForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        context['title'] = f"Orden de Compra  N° {self.kwargs['id']}"
        context['detalles'] = [
            {
                'id': 1,
                'material': 'Cemento',
                'cantidad_solicitada': 100,
                'cantidad_entregada': 0,
                'ultima_fecha_entrega': '20/09/2023'
            }
        ]
        context['routes'] = [
            {
                "route":reverse_lazy('compras:comprasUpdate', kwargs={'id': 1}),
                "name":'Ordenes de Compra'
            }
        ]
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        return form
    
    def form_valid(self, form) :
        data = form.cleaned_data

        # if 'error':
        #     return super(CreateEmpleadoView, self).form_invalid(form)

        return super(OrdenCompraUpdateView, self).form_valid(form)