"""
URL configuration for Inversiones368 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.views.static import serve
from django.urls import path,include,re_path
from django.views.generic import RedirectView

#*Asignación de Urls
#*Includes para los módulos
urlpatterns = [
    path("", include("modulos.autenticacion.urls", namespace = "autenticacion")),

    path('', RedirectView.as_view(url='administracion/'), name='home'),

    path("administracion/", include("modulos.administracion.urls", namespace = "administracion")),

    path("usuarios/", include("modulos.usuarios.urls", namespace = "usuarios")),
    
    path("gestion-almacenes/", include("modulos.almacen.urls", namespace = "almacen")),
    path("gestion-proyectos/", include("modulos.proyectos.urls", namespace = "proyectos")),
    path("gestion-ordenes-compras/", include("modulos.compras.urls", namespace = "compras")),
    path("gestion-proveedores/", include("modulos.proveedores.urls", namespace = "proveedores")),
    
    path("sistema/", include("modulos.sistema.urls", namespace = "sistema")),
    path("seguridad/", include("modulos.seguridad.urls", namespace = "seguridad")),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT
    })
]