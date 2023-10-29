from datetime import datetime
from operator import itemgetter

from django.conf import settings
from helpers.messageBox import emit_message_error, emit_message_success

import requests

dominio = getattr(settings, 'API_URL', 'https://inversiones-368.onrender.com/api/v1')
url = f"{dominio}/superadmin"

headers = {'Content-type': 'application/json; charset=UTF-8'}

def get_logs_all(request, search):
    """Obtiene todos los logs de un usuario"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.get(f'{url}/get/logs/{search}', allow_redirects=False, headers=headers) 
 
        r.raise_for_status()

        data = r.json()

        for x in data : 
            x['fecha'] = datetime.strptime(x['fecha'], '%Y-%m-%d')
        
        return sorted(data, key=itemgetter('fecha', 'hora'), reverse=True)
    except requests.exceptions.RequestException:
        errors = 'Internal server error'
        print(r.status_code)
        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)

        return []

def get_logs_one(request, log_id):
    """Obtiene un log"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.get(f'{url}/get/log/{log_id}', allow_redirects=False, headers=headers) 
 
        r.raise_for_status()
   
        return r.json()
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)

        return []