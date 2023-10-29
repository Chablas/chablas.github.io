import requests

from django.conf import settings
from helpers.messageBox import emit_message_error, emit_message_success

dominio = getattr(settings, 'API_URL', 'https://inversiones-368.onrender.com/api/v1')
url = f"{dominio}/in"

headers = {'Content-type': 'application/json; charset=UTF-8'}

def get_tipos_archivo_all(request, search):
    """Obtener los tipos de archivo"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        if(search != ''):
            r = requests.get(f'{url}/get/tipos_archivo?name='+search, allow_redirects=False, headers=headers)
        else :
            r = requests.get(f'{url}/get/tipos_archivo', allow_redirects=False, headers=headers)  
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']

        emit_message_error(request, errors)
        return []

def get_tipos_archivo_cb(request):
    """Obtener los tipos de archivo para el combobox"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.get(f'{url}/get/tipos_archivo', allow_redirects=False, headers=headers)  
        
        r.raise_for_status()

        tuplas = []

        for item in r.json():
            if(item['estado'] is True):
                tuplas.append((item['id'], item['nombre']))

        return tuplas
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']

        emit_message_error(request, errors)
        return []

def get_tipos_archivo_one(request, user_id):
    """Obtener un solo tipo de archivo"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    try:
        r = requests.get(f'{url}/get/tipo_archivo/{user_id}', allow_redirects=False, headers=headers)
        r.raise_for_status()
        return r.json()['dato']
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']

        emit_message_error(request, errors)
        return 'error'

def create_tipo_archivo(request, data):
    """Crear tipo archivo"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.post(f'{url}/post/tipo_archivo', json=data, headers=headers)
        r.raise_for_status()
        emit_message_success(request, 'El tipo de archivo se creó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']

        emit_message_error(request, errors)
        return 'error'

def update_tipo_archivo(request, user_id):
    """Actualizar tipo archivo"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.put(f'{url}/put/tipo_archivo/{user_id}', headers=headers)
        r.raise_for_status()
        emit_message_success(request, 'El tipo de archivo se actualizó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']

        emit_message_error(request, errors)
        return 'error'


    