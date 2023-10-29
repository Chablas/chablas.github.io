from django.conf import settings
from django.contrib.messages.storage import default_storage
from datetime import datetime

from helpers.messageBox import emit_message_error, emit_message_success

import requests

dominio = getattr(settings, 'API_URL', 'https://inversiones-368.onrender.com/api/v1')
url = f"{dominio}/in"

headers = {'Content-type': 'application/json; charset=UTF-8'}

def get_proyectos_all(request, search):
    """Obtiene todos los proyectos"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        if(search != ''):
           r = requests.get(f'{url}/get/proyectos?name='+search, allow_redirects=False, headers=headers)
        else :
           r = requests.get(f'{url}/get/proyectos', allow_redirects=False, headers=headers)  
        
        r.raise_for_status()

        data = r.json()

        for x in data : 
            x['fecha_creacion'] = datetime.strptime(x['fecha_creacion'], '%Y-%m-%d')
            x['fecha_inicio'] = datetime.strptime(x['fecha_inicio'], '%Y-%m-%d')
            x['fecha_fin'] = datetime.strptime(x['fecha_fin'], '%Y-%m-%d')
           
        return data
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return []

def get_proyectos_cb(request):
    """Obtiene todos los proyectos para un combobox"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.get(f'{url}/get/proyectos', allow_redirects=False, headers=headers)  
          
        r.raise_for_status()

        tupla = []

        for item in r.json() :
            tupla.append((item['id'], item['nombre']))
          
        return tupla
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return []
     
def get_proyecto_one(request, proyecto_id):
    """Obtener un solo proyecto"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    try:
        r = requests.get(f'{url}/get/proyecto/{proyecto_id}', allow_redirects=False, headers=headers)

        r.raise_for_status()
            
        return r.json()['dato']
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)

def create_proyecto(request, data):
    """Crea un nuevo proyecto"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.post(f'{url}/post/proyecto', json=data, headers=headers)
        r.raise_for_status()

        emit_message_success(request, 'El proyecto se creó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'
    
def update_proyecto(request, proyecto_id, data):
    """Actualizar proyecto"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.put(f'{url}/put/proyecto/{proyecto_id}', json = data, headers=headers)
        r.raise_for_status()
        emit_message_success(request, 'El proyecto se actualizó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
        emit_message_error(request, errors)
        return 'error'
