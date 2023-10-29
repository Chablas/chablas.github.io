from django.shortcuts import redirect
from helpers.messageBox import emit_message_error, emit_message_success

import json

def esta_logueado(func):
    """ Verifica si el usuario ha iniciado sesion """
    def wrapper(request, *args, **kwargs):

        # if request.session.get("token") is None:
        #     emit_message_error(request, 'Por favor autentiquese')
        #     return redirect("autenticacion:login")      
    
        return func(request, *args, **kwargs)

    return wrapper

def modulo_requerido(func):
    """ Verifica si el usuario tiene asignado el modulo """
    def wrapper(request, *args, **kwargs):
        # usuario = json.loads(request.session.get("usuario"))

        # modulos = usuario['rol']['modulos']

        # rol_requerido = kwargs['modulo'] if 'modulo' in kwargs else 0

        # if(rol_requerido not in modulos):
        #     emit_message_error(request, 'Sin autorizacion')
        #     return redirect("administracion:index")
        
        return func(request, *args, **kwargs)
    
    return wrapper