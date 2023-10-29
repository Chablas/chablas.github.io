from django.conf import settings
from helpers.messageBox import emit_message_error, emit_message_success

import requests

dominio = getattr(settings, 'API_URL', 'https://inversiones-368.onrender.com/api/v1')
url = f"{dominio}/in"

headers = {'Content-type': 'application/json; charset=UTF-8'}

def get_empleados_all(request, search):
    """Obtener los empleados"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
       
        if(search != ''):
           r = requests.get(f'{url}/get/usuarios?name='+search, allow_redirects=False, headers=headers)
        else :
            r = requests.get(f'{url}/get/usuarios', allow_redirects=False, headers=headers)

        r.raise_for_status()

        empleados = []

        for item in r.json():
            if item['tipo_usuario'] == 'EMPLEADO':
                empleados.append(item)

        return empleados
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return []

def get_empleado_one(request, user_id):
    """Obtener un solo usuario"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    try:
        r = requests.get(f'{url}/get/usuario/{user_id}', allow_redirects=False, headers=headers)
        
        r.raise_for_status()
        
        return r.json()['dato']
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)

def create_empleado(request, data):
    """Crear usuario"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.post(f'{url}/post/empleado', json=data, headers=headers)
        
        r.raise_for_status()

        emit_message_success(request, 'El empleado se creó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'

def update_empleado(request, user_id, data):
    """Actualizar empleado"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.put(f'{url}/put/usuario/{user_id}', json=data, headers=headers)

        r.raise_for_status()
        
        emit_message_success(request, 'El empleado se actualizó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'
    
def update_estado_empleado(request, user_id):
    """Actualizar estado de un empleado"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.put(f'{url}/put/usuario/{user_id}/status', headers=headers)

        r.raise_for_status()
        
        emit_message_success(request, 'El estado de empleado se actualizó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'



    