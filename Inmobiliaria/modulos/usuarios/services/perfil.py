import json
import requests

from django.conf import settings
from helpers.messageBox import emit_message_error, emit_message_success


dominio = getattr(settings, 'API_URL', 'https://inversiones-368.onrender.com/api/v1')
url = f"{dominio}/profile"
headers = {'Content-type': 'application/json; charset=UTF-8'}

def get_perfil(request):
    """Obtener perfil"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    try:
        r = requests.get(f'{url}/get', headers=headers)
       
        r.raise_for_status()
        
        data = r.json()

        request.session["usuario"] = json.dumps(data['dato'])
        
        return data['dato']
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'

def update_password(request, data):
    """Cambiar Contraseña"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.put(f'{url}/put/password', json=data, headers=headers)
        r.raise_for_status()
        emit_message_success(request, 'Su contraseña se actualizó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'
