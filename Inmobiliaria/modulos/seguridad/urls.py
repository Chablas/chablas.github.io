# usuarios/urls.py

from django.urls import path

from modulos.seguridad.views import rol, log

#*Se pone el nombre de la app, en este caso usuarios
app_name = "modulos.seguridad"

#*Se crean los urlpatterns que son básicamente las url para acceder a cada caso de uso
urlpatterns = [
    path('roles', rol.RolListView.as_view(), {'modulo':9 },name='rolesIndex'),
    path('roles/create', rol.RolCreateView.as_view(), {'modulo':9 }, name='rolesCreate'),
    path('roles/<id>/update', rol.rol_update_view, {'modulo':9 }, name='rolesUpdate'),
    path('roles/<id>/modulos', rol.RolModuloview.as_view(), {'modulo':9 },name='rolesModulo'),

    path('logs', log.LogListView.as_view(), {'modulo': 0 },name='logsIndex'),
    path('logs/<id>', log.LogFormView.as_view(), {'modulo': 0 },name='logsForm'),
]