from django.conf import settings
from helpers.messageBox import emit_message_error, emit_message_success

import requests

dominio = getattr(settings, 'API_URL', 'https://inversiones-368.onrender.com/api/v1')
url = f"{dominio}/in"

headers = {'Content-type': 'application/json; charset=UTF-8'}

def get_categorias_all(request, search):
    """Obtiene todas las categorias"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        if(search != ''):
            r = requests.get(f'{url}/get/categorias_proveedor_material?name='+search, allow_redirects=False, headers=headers)
        else :
            r = requests.get(f'{url}/get/categorias_proveedor_material', allow_redirects=False, headers=headers)  

        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']
            
        emit_message_error(request, errors)
        return []
    
def get_categorias_cb(request):
    """Obtiene las categorias para el combobox"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.get(f'{url}/get/categorias_proveedor_material', allow_redirects=False, headers=headers)
            
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
    
def get_categorias_one(request, categoria_id):
    """Obtiene todas las categorias"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.get(f'{url}/get/categoria_proveedor_material/{categoria_id}', allow_redirects=False, headers=headers)  

        r.raise_for_status()

        return r.json()['dato']
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']

        emit_message_error(request, errors)
        return []
    
def create_categoria(request, data):
    """Crea nueva categoria"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.post(f'{url}/post/categoria_proveedor_material', json=data, headers=headers)

        r.raise_for_status()

        emit_message_success(request, 'La categoria se creó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']

        emit_message_error(request, errors)
        return 'error'
    
def update_categoria(request, categoria_id):
    """Actualiza nueva categoria"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.put(f'{url}/put/categoria_proveedor_material/{categoria_id}', headers=headers)

        r.raise_for_status()

        emit_message_success(request, 'La categoria se actualizó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
            
        emit_message_error(request, errors)
        return 'error'