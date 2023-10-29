# sistema/urls.py

from django.urls import path

from modulos.sistema.views import tipo_archivo, tipo_documento, empresa
from modulos.sistema.views import unidad_medida, actividad_material

#*Se pone el nombre de la app, en este caso usuarios
app_name = "modulos.sistema"

#*Se crean los urlpatterns que son básicamente las url para acceder a cada caso de uso
urlpatterns = [
    path('empresa', empresa.EmpresaFormView.as_view(), {'modulo': 0 },name='empresaForm'),

    path('tipos-archivo', tipo_archivo.TipoArchivoView.as_view(), { 'modulo': 10 }, name='tiposArchivoIndex'),
    path('tipos-archivo/create', tipo_archivo.TipoArchivoCreateView.as_view(), { 'modulo': 10 }, name='tiposArchivoCreate'),
    path('tipos-archivo/<id>/update', tipo_archivo.tipo_archivo_update_view, { 'modulo': 10 }, name='tiposArchivoUpdate'),

    path('tipos-documento', tipo_documento.TipoDocumentoListView.as_view(), {'modulo':12 },name='tiposDocumentoIndex'),
    path('tipos-documento/<id>/update', tipo_documento.tipo_documento_update_view, {'modulo':12 }, name='tiposDocumentoUpdate'),

    path('unidades-medida', unidad_medida.UnidadMedidaView.as_view(), { 'modulo': 8 }, name='unidadesMedidaIndex'),
    path('unidades-medida/create', unidad_medida.UnidadMedidaCreateView.as_view(), { 'modulo': 8 }, name='unidadesMedidaCreate'),
    path('unidades-medida/<id>/update', unidad_medida.unidad_medida_update_view, { 'modulo': 8 }, name='unidadesMedidaUpdate'),

    path('actividades', actividad_material.ActividadesView.as_view(), { 'modulo': 13 }, name='actividadesIndex'),
    path('actividades/create', actividad_material.ActividadesCreateView.as_view(), { 'modulo': 13 }, name='actividadesCreate'),
    path('actividades/<id>', actividad_material.actividad_update_view, { 'modulo': 13 }, name='actividadesUpdate'),
]