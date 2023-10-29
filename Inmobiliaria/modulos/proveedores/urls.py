# usuarios/urls.py

from django.urls import path
from modulos.proveedores.views import categoria, proveedor, material

#*Se pone el nombre de la app, en este caso usuarios
app_name = "modulos.proveedores"

#*Se crean los urlpatterns que son básicamente las url para acceder a cada caso de uso
urlpatterns = [
    path('categorias', categoria.CategoriasView.as_view(), kwargs={ 'modulo': 6 }, name='categoriasIndex'),
    path('categorias/create', categoria.CategoriaCreateView.as_view(), kwargs={'modulo': 6}, name='categoriasCreate'),
    path('categorias/<id>', categoria.categoria_update_view, kwargs={ 'modulo': 6 }, name='categoriasUpdate'),
    
    path('proveedores', proveedor.ProveedoresView.as_view(), kwargs={ 'modulo': 7 }, name='proveedoresIndex'),
    path('proveedores/create', proveedor.ProveedoresCreateView.as_view(), kwargs={ 'modulo': 7 }, name='proveedoresCreate'),
    path('proveedores/<id>', proveedor.ProveedorUpdateView.as_view(), kwargs={ 'modulo': 7 }, name='proveedoresUpdate'),
    path('proveedores/<id>/categorias', proveedor.ProveedorCategoriaView.as_view(), kwargs={ 'modulo': 7 }, name='proveedoresCategoria'),
    path('proveedores/<id>/zonas', proveedor.ProveedorZonaView.as_view(), kwargs={ 'modulo': 7 }, name='proveedoresZona'),

     path('materiales/<proveedor>/<proveedor_id>', material.MaterialesView.as_view(), { 'modulo': 14 }, name='materialesIndex'),
    path('materiales/<proveedor>/<proveedor_id>/create', material.MaterialCreateView.as_view(), { 'modulo': 14 }, name='materialesCreate'),
    path('materiales/<proveedor>/<proveedor_id>/update/<id>', material.MaterialUpdateView.as_view(), { 'modulo': 14 }, name='materialesUpdate'),
    path('materiales//<proveedor>/<proveedor_id>/<id>/status/update', material.material_estado_update_view, { 'modulo': 14 }, name='materialesEstadoUpdate'),
]