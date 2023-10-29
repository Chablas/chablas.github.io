from django.conf import settings
from helpers.messageBox import emit_message_error, emit_message_success

import requests

dominio = getattr(settings, 'API_URL', 'https://inversiones-368.onrender.com/api/v1')
url = f"{dominio}/in"

headers = {'Content-type': 'application/json; charset=UTF-8'}

def get_materiales_all(request, search):
    """Obtiene todos los materiales"""
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
    
def get_material_one(request, estado_id):
    """Obtener un solo material"""
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