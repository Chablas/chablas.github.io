import json
import requests

from django.conf import settings
from helpers.messageBox import emit_message_error, emit_message_success

dominio = getattr(settings, 'API_URL', 'https://inversiones-368.onrender.com/api/v1')
urlAuth = f"{dominio}/auth"
urlProfile = f"{dominio}/profile"

headers = {'Content-type': 'application/json; charset=UTF-8'}

def login(request, data):
    """Servicio de autenticacion de usuario"""
    headers['Content-type'] = 'application/x-www-form-urlencoded'
    r = None
    try:
        r = requests.post(f"{urlAuth}/login", data = data, headers=headers)
        
        r.raise_for_status()
        
        data = r.json() 
        
        request.session["token"] = data['access_token']

        emit_message_success(request, 'Inicio sesión correcto')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']
        
        request.session['token'] = None
        request.session['usuario'] = None
        emit_message_error(request, errors)
        return 'error'

def logout(request):
    """Servicio de cerrado de sesion"""
    headers['Authorization'] = f"Bearer {request.session.get('token')}"
    r = None
    try:
        r = requests.post(f"{urlAuth}/logout", headers=headers)
        
        r.raise_for_status()
        
        del request.session['token']
        del request.session['usuario']
        
        emit_message_success(request, 'Salió de la sesión correctamente')
    except requests.exceptions.RequestException:
        emit_message_error(request, 'Error de servidor')
    return 'error'

def obtener_perfil(request):
    """Servicio de obtner perfil"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.get(f"{urlProfile}/get", headers=headers)
        
        r.raise_for_status()
        
        data = r.json() 
        request.session["usuario"] = json.dumps(data['dato'])

    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']
            
        request.session['token'] = None
        request.session['usuario'] = None
        emit_message_error(request, errors)
        return 'error'