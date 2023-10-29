from django.conf import settings
from django.contrib.messages.storage import default_storage
from helpers.messageBox import emit_message_error, emit_message_success

import requests

dominio = getattr(settings, 'API_URL', 'https://inversiones-368.onrender.com/api/v1')
url = f"{dominio}/in"

headers = {'Content-type': 'application/json; charset=UTF-8'}

def get_etapas_all(request, search):
    """Obtiene todos los etapas de un proyecto"""
    request._messages = default_storage(request)
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        if(search != ''):
            r = requests.get(f'{url}/get/etapasProyecto?name='+search, allow_redirects=False, headers=headers)
        else :
            r = requests.get(f'{url}/get/etapasProyecto', allow_redirects=False, headers=headers)  
        
        r.raise_for_status()

        return r.json()
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return []

def get_etapas_cb(request):
    """Obtiene las etapas de proyecto para el combobox"""
    request._messages = default_storage(request)
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.get(f'{url}/get/etapasProyecto', allow_redirects=False, headers=headers)
            
        r.raise_for_status()

        tupla = []

        for x in r.json() :
            if x['estado'] is True:
                tupla.append((x['id'], x['nombre']))

        return (tupla)
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return []
    

def get_etapa_one(request, etapa_id):
    """Obtener un solo estapa de proyecto"""
    request._messages = default_storage(request)
    headers['Authorization'] = f"Bearer {request.session['token']}"
    try:
        r = requests.get(f'{url}/get/etapaProyecto/{etapa_id}', allow_redirects=False, headers=headers)

        r.raise_for_status()
            
        return r.json()['dato']
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)

def create_etapa(request, data):
    """Crea un nuevo estado de proyecto"""
    request._messages = default_storage(request)
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.post(f'{url}/post/etapaProyecto', json=data, headers=headers)
        r.raise_for_status()

        emit_message_success(request, 'La etapa se creó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'
    
def update_etapa(request, etapa_id):
    """Actualizar estado de proyecto"""
    request._messages = default_storage(request)
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.put(f'{url}/put/etapaProyecto/{etapa_id}', headers=headers)
        r.raise_for_status()
        emit_message_success(request, 'La etapa se actualizó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'
