# administracion/urls.py

from django.urls import path
from modulos.compras.views import pedidos, guias, compras

#*Se pone el nombre de la app, en este caso compras
app_name = "modulos.compras"

#*Se crean los urlpatterns que son básicamente las url para acceder a cada caso de uso
urlpatterns = [
    # Pedidos
    path('pedidos/', pedidos.PedidoListView.as_view(), { 'modulo': 0 }, name='pedidosIndex'),
    path('pedidos/create', pedidos.PedidoCreateView.as_view(), { 'modulo': 0 }, name='pedidosCreate'),
    path('pedidos/delete/detalle', pedidos.pedido_detalle_delete_view, { 'modulo': 0 }, name='pedidosDeleteDetalle'),
    path('pedidos/create/detalles', pedidos.pedido_detalle_create_view, { 'modulo': 0 }, name='pedidosCreateDetalle'),
    path('pedidos/delete/detalles', pedidos.pedido_detalle_clear_view, { 'modulo': 0 }, name='pedidosDeleteDetalles'),

    # Ordenes de Compra
    path('ordenes-compra/<int:id>', compras.OrdenCompraUpdateView.as_view(), { 'modulo': 0 }, name='comprasUpdate'),
    path('ordenes-compra/', compras.OrdenCompraListView.as_view(), { 'modulo': 0 }, name='comprasList'),

    # Guias de Remision  
    path('guias-remision/', guias.GuiaDeRemisionListView.as_view(), { 'modulo': 0 }, name='guiasRemisionIndex'),
    path('guias-remision/create', guias.GuiaRemisionCreateView.as_view(), { 'modulo': 0 }, name='guiasRemisionCreate'),
    path('guias-remision/<int:id>/update', guias.GuiaRemisionUpdateView.as_view(), { 'modulo': 0 }, name='guiasRemisionUpdate'),
]