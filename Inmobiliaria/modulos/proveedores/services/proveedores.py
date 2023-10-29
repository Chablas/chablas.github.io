from django.conf import settings
from helpers.messageBox import emit_message_error, emit_message_success

import requests

dominio = getattr(settings, 'API_URL', 'https://inversiones-368.onrender.com/api/v1')
url = f"{dominio}/in"

headers = {'Content-type': 'application/json; charset=UTF-8'}

def get_proveedores_all(request, search):
    """Obtiene todas las proveedores"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        if(search != ''):
            r = requests.get(f'{url}/get/proveedores?name='+search, allow_redirects=False, headers=headers)
        else :
            r = requests.get(f'{url}/get/proveedores', allow_redirects=False, headers=headers)  

        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return []

def get_proveedores_cb(request):
    """Obtiene todas las proveedores para un combobox"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.get(f'{url}/get/proveedores', allow_redirects=False, headers=headers)  
        
        r.raise_for_status()

        tupla = []

        for x in r.json() :
            if x['estado'] == 'ACTIVO':
                tupla.append((x['id'], x['nombre_empresa']))

        return tupla
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return []
    
def get_proveedor_one(request, proveedor_id):
    """Obtiene solo un proveedor"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.get(f'{url}/get/proveedor/{proveedor_id}', allow_redirects=False, headers=headers)  

        r.raise_for_status()

        return r.json()['dato']
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return []

def get_proveedor_categorias(request, proveedor_id):
    """Obtiene las categorias de un proveedor"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.get(f'{url}/get/proveedor/{proveedor_id}', allow_redirects=False, headers=headers)  

        r.raise_for_status()

        categorias = r.json()['dato']['categorias']

        tupla = []

        for x in categorias : tupla.append((x['id'], x['nombre']))
               
        return (tupla)
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return []
    
def create_proveedor(request, data):
    """Crea nueva proveedor"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.post(f'{url}/post/proveedor', json=data, headers=headers)

        r.raise_for_status()

        emit_message_success(request, 'El proveedor se creó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'
    
def update_proveedor(request, proveedor_id, data):
    """Actualiza nueva proveedor"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.put(f'{url}/put/proveedor/{proveedor_id}', json=data, headers=headers)

        r.raise_for_status()

        emit_message_success(request, 'El proveedor se actualizó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'

def allocate_proveedor_categoria(request, proveedor_id, categoria_id):
    """Asigna una categoria al proveedor"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.put(f'{url}/put/proveedor/{proveedor_id}/add_categoria/{categoria_id}', headers=headers)

        r.raise_for_status()

        emit_message_success(request, 'Se asignó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'

def deallocate_proveedor_categoria(request, proveedor_id, categoria_id):
    """Desasigna una categoria al proveedor"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.put(f'{url}/put/proveedor/{proveedor_id}/delete_categoria/{categoria_id}', headers=headers)

        r.raise_for_status()

        emit_message_success(request, 'Se desasignó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'
    
def allocate_proveedor_zona(request, proveedor_id, zona_id):
    """Asigna una zona al proveedor"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.put(f'{url}/put/proveedor/{proveedor_id}/add_zona/{zona_id}', headers=headers)

        r.raise_for_status()

        emit_message_success(request, 'Se asignó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'

def deallocate_proveedor_zona(request, proveedor_id, zona_id):
    """Desasigna una zona al proveedor"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.put(f'{url}/put/proveedor/{proveedor_id}/delete_zona/{zona_id}', headers=headers)

        r.raise_for_status()

        emit_message_success(request, 'Se desasignó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'