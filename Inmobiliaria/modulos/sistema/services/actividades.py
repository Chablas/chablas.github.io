from django.conf import settings
from helpers.messageBox import emit_message_error, emit_message_success

import requests

dominio = getattr(settings, 'API_URL', 'https://inversiones-368.onrender.com/api/v1')
url = f"{dominio}/in"

headers = {'Content-type': 'application/json; charset=UTF-8'}

def get_actividades_all(request, search):
    """Obtiene todas las actividades"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        if(search != ''):
            r = requests.get(f'{url}/get/actividades_material?name='+search, allow_redirects=False, headers=headers)
        else :
            r = requests.get(f'{url}/get/actividades_material', allow_redirects=False, headers=headers)  

        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return []
    
def get_actividades_one(request, actividad_material_id):
    """Obtiene una actividad de un material"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.get(f'{url}/get/actividad_material/{actividad_material_id}', allow_redirects=False, headers=headers)  

        r.raise_for_status()

        return r.json()['dato']
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return []

def create_actividad(request, data):
    """Crea nueva actividad"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.post(f'{url}/post/actividad_material', json=data, headers=headers)

        r.raise_for_status()

        emit_message_success(request, 'La actividad se creó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'
    
def update_actividad(request, actividad_material_id):
    """Actualiza un proveedor"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.put(f'{url}/put/actividad_material/{actividad_material_id}', headers=headers)
        r.raise_for_status()
        emit_message_success(request, 'La actividad se actualizó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'