from django.contrib import messages
from django.contrib.sessions.models import Session

def eliminar_mensajes(func):
    """ Elimina los mensajes del cache """
    def wrapper(request, *args, **kwargs):
        
        for s in Session.objects.all():  
            decoded_data_dict = s.get_decoded()

        # for key in request.session.keys():  
        #     del request.session[key]

        storage = messages.get_messages(request)
        storage.used = True

        return func(request, *args, **kwargs)

    return wrapper