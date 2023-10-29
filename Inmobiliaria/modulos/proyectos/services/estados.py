from django.conf import settings
from helpers.messageBox import emit_message_error, emit_message_success

import requests

dominio = getattr(settings, 'API_URL', 'https://inversiones-368.onrender.com/api/v1')
url = f"{dominio}/in"

headers = {'Content-type': 'application/json; charset=UTF-8'}

def get_estados_all(request, search):
    """Obtiene todos los estados de un proyecto"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        if(search != ''):
            r = requests.get(f'{url}/get/estadosProyecto?name='+search, allow_redirects=False, headers=headers)
        else :
            r = requests.get(f'{url}/get/estadosProyecto', allow_redirects=False, headers=headers)  
        
        r.raise_for_status()

        return r.json()
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return []

def get_estados_cb(request):
    """Obtiene los estados para el combobox"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.get(f'{url}/get/estadosProyecto', allow_redirects=False, headers=headers)
            
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
    
def get_estado_one(request, estado_id):
    """Obtener un solo estado de proyecto"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    try:
        r = requests.get(f'{url}/get/estadoProyecto/{estado_id}', allow_redirects=False, headers=headers)

        r.raise_for_status()
            
        return r.json()['dato']
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)

def create_estado(request, data):
    """Crea un nuevo estado de proyecto"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.post(f'{url}/post/estadoProyecto', json=data, headers=headers)
        r.raise_for_status()

        emit_message_success(request, 'El estado se creó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'
    
def update_estado(request, estado_id):
    """Actualizar estado de proyecto"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.put(f'{url}/put/estadoProyecto/{estado_id}', headers=headers)
        r.raise_for_status()
        emit_message_success(request, 'El estado se actualizó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request,errors)
        return 'error'
