# proyecto/urls.py

from django.urls import path
from modulos.proyectos.views import estado, etapa, zona, proyecto, archivo, actividad

#*Se pone el nombre de la app, en este caso proyecto
app_name = "modulos.proyecto"

#*Se crean los urlpatterns que son básicamente las url para acceder a cada caso de uso
urlpatterns = [
    path('zonas/', zona.ZonaListView.as_view(), { 'modulo': 5 }, name='zonasIndex'),
    path('zonas/create', zona.ZonaCreateView.as_view(), { 'modulo': 5 }, name='zonasCreate'),
    path('zonas/<id>', zona.ZonaUpdateView.as_view(), { 'modulo': 5 }, name='zonasUpdate'),

    path('etapas/', etapa.EtapaListView.as_view(), { 'modulo': 3 },name='etapasIndex'),
    path('etapas/create', etapa.EtapaCreateView.as_view(), { 'modulo': 3 },name='etapasCreate'),
    path('etapas/update/<int:id>', etapa.etapa_update_view,{ 'modulo': 3 }, name='etapasUpdate'),

    path('estados/', estado.EstadoListView.as_view(), { 'modulo':4 },name='estadosIndex'),
    path('estados/create', estado.EstadoCreateView.as_view(), { 'modulo':4 },name='estadosCreate'),
    path('estados/update/<int:id>', estado.estado_update_view, { 'modulo':4 }, name='estadosUpdate'),

    path('proyectos/', proyecto.ProyectoListView.as_view(), {'modulo': 2 },name='proyectosIndex'),
    path('proyectos/create', proyecto.ProyectoCreateView.as_view(), {'modulo': 2 },name='proyectosCreate'),
    path('proyectos/update/<int:id>', proyecto.ProyectoUpdateView.as_view(), {'modulo': 2 }, name='proyectosUpdate'),

    path('archivos/<str:proyecto>/<proyecto_id>', archivo.ArchivoView.as_view(), { 'modulo': 11 }, name='archivosIndex'),
    path('archivos/<str:proyecto>/<proyecto_id>/create', archivo.ArchivoCreateView.as_view(), { 'modulo': 11 }, name='archivosCreate'),
    path('archivos/<str:proyecto>/<proyecto_id>/update/<id>', archivo.ArchivoUpdateView.as_view(), { 'modulo': 11 }, name='archivosUpdate'),

    path('descargar', archivo.create_temporal_archivo_view, { 'modulo': 11 }, name='archivosDownload'),
    path('eliminar', archivo.delete_temporal_archivo_view, { 'modulo': 11 }, name='archivosDelete'),

    path('actividades/<proyecto>/<proyecto_id>', actividad.ActividadesListView.as_view(), { 'modulo': 0 }, name='actividadesIndex'),
    path('actividades/<proyecto>/<proyecto_id>/create', actividad.ActividadCreateView.as_view(), { 'modulo': 0 }, name='actividadesCreate'),
    path('actividades/<proyecto>/<proyecto_id>/<actividad_id>', actividad.ActividadUpdateView.as_view(), { 'modulo': 0 }, name='actividadesUpdate'),
]