import json

from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from django.views.generic import ListView, FormView

from decorators.messages import eliminar_mensajes
from decorators.user import esta_logueado, modulo_requerido

from modulos.proyectos.services.proyectos import get_proyectos_cb

from ..forms import PedidoForm

TEMPLEATE_ROOT = 'compras/pedido'

# Create your views here.
@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class PedidoListView(ListView):
    """Vista global de pedidos """
    template_name = f"{TEMPLEATE_ROOT}/index.html"
    context_object_name='pedidos'
    paginate_by=15
    
    def get_queryset(self):
        search = self.request.GET.get('search', '')
        return []
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        proyectos = {}

        for p in get_proyectos_cb(self.request):
            proyectos.setdefault(p[0],p[1])

        context['proyectos'] = json.dumps(proyectos)
  
        return context
    
@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class PedidoCreateView(FormView):
    """ Vista de creacion de etapa """
    template_name = f"{TEMPLEATE_ROOT}/form.html"
    form_class = PedidoForm
    success_url=reverse_lazy('compras:pedidosIndex')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Nuevo Pedido'
        context['proyecto'] = self.request.GET.get('proyecto', '')
        context['routes'] = [
            {
                "route":reverse_lazy('compras:pedidosIndex'),
                "name":'Pedidos'
            }
        ]
        context['detalles'] = json.loads(self.request.session.get('materiales', '[]'))

        return context
    
    def form_valid(self, form) :
        data = form.cleaned_data
        data['nombre'] = str(data['nombre']).upper()
        # if create_zona(self.request, data) == 'error':
        #     return super(ZonaCreateView, self).form_invalid(form)
        # else:
        return super(PedidoCreateView, self).form_valid(form)

@esta_logueado
@modulo_requerido
@eliminar_mensajes
@require_http_methods(["GET"])
def pedido_detalle_clear_view(request, **kwargs):
    """ Funcion de limpiar materiales de la session storage"""
    request.session['materiales'] = '[]'

    return redirect('compras:pedidosIndex')

@esta_logueado
@modulo_requerido
@eliminar_mensajes
@require_http_methods(["GET"])
def pedido_detalle_create_view(request, **kwargs):
    """ Funcion de actualizacion de detalles de pedido"""
    materiales = json.loads(request.session.get('materiales', '[]'))
    
    materiales.append({
        'id': len(materiales) + 1,
        'material': 'Madera',
        'cantidad': '2',
        'precio_unitario': '1.2'
    })
    
    request.session['materiales'] = json.dumps(materiales)

    return redirect(reverse('compras:pedidosCreate')+f"?proyecto={request.GET.get('proyecto', '')}")

@esta_logueado
@modulo_requerido
@eliminar_mensajes
@require_http_methods(["GET"])
def pedido_detalle_delete_view(request, **kwargs):
    """ Funcion de actualizacion de detalles de pedido"""
    materiales = json.loads(request.session.get('materiales', '[]'))

    for m in materiales:
        index = materiales.index(m)
        if(str(materiales[index]['id']) == str(request.GET.get('material', ''))):
            del materiales[index]
    
    print(materiales)

    request.session['materiales'] = json.dumps(materiales)

    return redirect(reverse('compras:pedidosCreate')+f"?proyecto={request.GET.get('proyecto', '')}")