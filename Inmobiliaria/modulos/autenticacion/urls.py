# administracion/urls.py

from django.urls import path
from modulos.autenticacion import views

#*Se pone el nombre de la app, en este caso administración
app_name = "modulos.autenticacion"

#*Se crean los urlpatterns que son básicamente las url para acceder a cada caso de uso
urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('doble-paso', views.DoblePasoView.as_view(), name='doblePaso'),
    path('recuperar-contrasena', views.RecuperarContrasenaView.as_view(), name='recuperarContrasena'),
    path('logout', views.logout_view, name='logout')
]