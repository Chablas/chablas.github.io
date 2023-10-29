# administracion/urls.py

from django.urls import path
from modulos.administracion import views

#*Se pone el nombre de la app, en este caso administración
app_name = "modulos.administracion"

#*Se crean los urlpatterns que son básicamente las url para acceder a cada caso de uso
urlpatterns = [
    path('', views.IndexView.as_view(), name='index')
]