from django.conf import settings
from helpers.messageBox import emit_message_error, emit_message_success

import requests

dominio = getattr(settings, 'API_URL', 'https://inversiones-368.onrender.com/api/v1')
url = f"{dominio}/in"

headers = {'Content-type': 'application/json; charset=UTF-8'}

def get_unidades_medida_all(request, search):
    """Obtiene todos los unidades medida de un proyecto"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        if(search != ''):
            r = requests.get(f'{url}/get/unidades_medida?name='+search, allow_redirects=False, headers=headers)
        else :
            r = requests.get(f'{url}/get/unidades_medida', allow_redirects=False, headers=headers)  
        
        r.raise_for_status()

        return r.json()
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']

        emit_message_error(request, errors)
        return []

def get_unidades_medida_cb(request):
    """Obtiene las unidades_medidas para el combobox"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.get(f'{url}/get/unidades_medida', allow_redirects=False, headers=headers)
            
        r.raise_for_status()

        tupla = []

        for x in r.json() :
            if x['estado'] is True:
                tupla.append((x['id'], x['nombre']))

        return (tupla)
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']

        emit_message_error(request, errors)
        return []
    

def get_unidad_medida_one(request, unidad_medida_id):
    """Obtener un solo unidad de medida"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    try:
        r = requests.get(f'{url}/get/unidad_medida/{unidad_medida_id}', allow_redirects=False, headers=headers)

        r.raise_for_status()
            
        return r.json()['dato']
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']

        emit_message_error(request, errors)
        return 'error'

def create_unidad_medida(request, data):
    """Crea un nuevo unidad de medida"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.post(f'{url}/post/unidad_medida', json=data, headers=headers)
        r.raise_for_status()

        emit_message_success(request, 'La unidad medida se creó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'
    
def update_unidad_medida(request, unidad_medida_id):
    """Actualizar estado de unidad de medida"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.put(f'{url}/put/unidad_medida/{unidad_medida_id}', headers=headers)
        r.raise_for_status()
        emit_message_success(request, 'La unidad medida se actualizó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']
            
        emit_message_error(request, errors)
        return 'error'
