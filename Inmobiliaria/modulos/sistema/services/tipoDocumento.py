from django.conf import settings
from helpers.messageBox import emit_message_error, emit_message_success

import requests

dominio = getattr(settings, 'API_URL', 'https://inversiones-368.onrender.com/api/v1')
url = f"{dominio}/in"

headers = {'Content-type': 'application/json; charset=UTF-8'}

def get_tipos_documentos_all(request, search):
    """Obtiene todos los estados de un proyecto"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        if(search != ''):
            r = requests.get(f'{url}/get/tiposDocumento?name='+search, allow_redirects=False, headers=headers)
        else :
            r = requests.get(f'{url}/get/tiposDocumento', allow_redirects=False, headers=headers)  
        
        r.raise_for_status()

        return r.json()
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return []

def get_tipos_documentos_cb(request):
    """Obtiene los tipos de documento"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.get(f'{url}/get/tiposDocumento', allow_redirects=False, headers=headers)
        r.raise_for_status()

        tupla = []

        for item in r.json() :
            if item['estado'] is True:
                tupla.append((item['id'], item['nombre']))

        return (tupla)
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return []

def update_tipo_documento(request, tipo_documento_id):
    """Actualizar estado de proyecto"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.put(f'{url}/update/tipoDocumento/{tipo_documento_id}/status', headers=headers)
        r.raise_for_status()
        emit_message_success(request, 'El tipo de documento se actualizó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'
