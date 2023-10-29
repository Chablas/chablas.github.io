from django.conf import settings
from helpers.messageBox import emit_message_error, emit_message_success

import requests

dominio = getattr(settings, 'API_URL', 'https://inversiones-368.onrender.com/api/v1')
url = f"{dominio}/in"

headers = {'Content-type': 'application/json; charset=UTF-8'}

def get_roles_all(request, search):
    """Obtiene todos los estados de un proyecto"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        if(search != ''):
            r = requests.get(f'{url}/get/roles?name='+search, allow_redirects=False, headers=headers)
        else :
            r = requests.get(f'{url}/get/roles', allow_redirects=False, headers=headers)  
        
        r.raise_for_status()

        return r.json()
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return []

def get_roles_cb(request):
    """Obtiene los estados para el combobox"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.get(f'{url}/get/roles', allow_redirects=False, headers=headers)
            
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
    
def get_rol_one(request, rol_id):
    """Obtener un solo estado de proyecto"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    try:
        r = requests.get(f'{url}/get/rol/{rol_id}', allow_redirects=False, headers=headers)

        r.raise_for_status()
            
        return r.json()['dato']
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)

def create_rol(request, data):
    """Crea un nuevo estado de proyecto"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.post(f'{url}/post/rol', json=data, headers=headers)
        r.raise_for_status()

        emit_message_success(request, 'El rol se creó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'
    
def update_rol(request, rol_id):
    """Actualizar estado de proyecto"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.put(f'{url}/put/rol/{rol_id}/status', headers=headers)
        r.raise_for_status()
        emit_message_success(request, 'El rol se actualizó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'

def allocate_modulo_to_rol(request, rol_id, modulo_id):
    """Asignar modulo a rol"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.put(f'{url}/put/rol/{rol_id}/add_modulo/{modulo_id}', headers=headers)

        r.raise_for_status()

        emit_message_success(request, 'Se asignó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'

def deallocate_modulo_to_rol(request, rol_id, modulo_id):
    """Desasignar modulo a rol"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.put(f'{url}/put/rol/{rol_id}/remove_modulo/{modulo_id}', headers=headers)

        r.raise_for_status()

        emit_message_success(request, 'Se desasignó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'
