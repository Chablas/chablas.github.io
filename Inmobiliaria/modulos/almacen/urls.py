# usuarios/urls.py

from django.urls import path
from modulos.almacen.views import material

#*Se pone el nombre de la app, en este caso almacen
app_name = "modulos.almacen"

#*Se crean los urlpatterns que son básicamente las url para acceder a cada caso de uso
urlpatterns = [
    path('materiales/', material.MaterialListView.as_view(), { 'modulo': 0 }, name='materialIndex'),
    path('materiales/create', material.MaterialCreateView.as_view(), { 'modulo': 0 }, name='materialCreate'),
    path('materiales/<id>/update', material.MaterialUpdateView.as_view(), { 'modulo': 0 }, name='materialUpdate'),
]