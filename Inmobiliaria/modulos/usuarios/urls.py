# usuarios/urls.py

from django.urls import path
from modulos.usuarios.views import empleado, independiente, perfil

#*Se pone el nombre de la app, en este caso usuarios
app_name = "modulos.usuarios"

#*Se crean los urlpatterns que son básicamente las url para acceder a cada caso de uso
urlpatterns = [
    path('mi-perfil', perfil.PerfilView.as_view(), name='ver-perfil'),
    path('cambiar_contraseña', perfil.UpdateContraseniaView.as_view(), name='cambiar_contraseña'),

    path('empleados', empleado.EmpleadosView.as_view(), { 'modulo': 1 }, name='empleadosIndex'),
    path('empleados/create', empleado.CreateEmpleadoView.as_view(), { 'modulo': 1 }, name='empleadosCreate'),
    path('empleados/<int:id>', empleado.UpdateEmpleadoView.as_view(), { 'modulo': 1 }, name='empleadosUpdate'),
    path('empleados/<int:id>/estado', empleado.empleado_estado_update_view, { 'modulo': 1 }, name='empleadosEstadoUpdate'),
    path('empleados/<int:id>/foto', empleado.UpdateEmpleadoFotoView.as_view(), { 'modulo': 1 }, name='empleadosFoto'),
    
    path('inpendientes', independiente.IndependienteView.as_view(), { 'modulo': 15 }, name='independientesIndex'),
    path('inpendientes/create', independiente.IndependienteCreateView.as_view(), { 'modulo': 15 }, name='independientesCreate'),
    path('inpendientes/<int:id>', independiente.IndependienteUpdateView.as_view(), { 'modulo': 15 }, name='independientesUpdate'),
    path('inpendientes/<int:id>/estado', independiente.independiente_estado_update_view, { 'modulo': 15 }, name='independientesEstadoUpdate'),
    path('inpendientes/<int:id>/foto', independiente.IndependienteFotoView.as_view(), { 'modulo': 15 }, name='independientesFoto'),
]