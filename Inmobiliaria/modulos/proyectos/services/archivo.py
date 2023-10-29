import requests
import jwt
import os
import mimetypes

from django.conf import settings
from helpers.firebase import firebase_generate_url
from helpers.messageBox import emit_message_error, emit_message_success

dominio = getattr(settings, 'API_URL', 'https://inversiones-368.onrender.com/api/v1')
url = f"{dominio}/in"

headers = {'Content-type': 'application/json; charset=UTF-8'}

def get_archivo_all(request, archivo_id, search):
    """Obtener los archivos"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        if(search != ''):
            r = requests.get(f'{url}/get/archivos/{archivo_id}?name='+search, allow_redirects=False, headers=headers)
        else :
            r = requests.get(f'{url}/get/archivos/{archivo_id}', allow_redirects=False, headers=headers)  
        r.raise_for_status()
        
        data = []

        for item in r.json():
            
            archivo = item['versiones'][len(item['versiones'])-1]['url_archivo']

            item['url'] = firebase_generate_url(archivo)
            
            item['blob_path'] = archivo

            # extension = os.path.splitext(archivo)
            #  or extension[1] == '.dwg'
            
            item['es_pdf'] = mimetypes.guess_type(archivo)[0] == 'application/pdf'
                
            data.append(item)

        return data
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']

        emit_message_error(request, errors)
        return []

def get_archivo_one(request, archivo_id):
    """Obtener los archivos"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.get(f'{url}/get/archivo/{archivo_id}', allow_redirects=False, headers=headers)

        r.raise_for_status()
        
        return r.json()['dato']
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']

        emit_message_error(request, errors)
        return 'error'

def create_archivo(request, proyecto_id, data):
    """Crear archivo"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.post(f'{url}/post/archivo/{proyecto_id}', json=data, headers=headers)
        
        r.raise_for_status()

        emit_message_success(request, 'El archivo se creó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']

        emit_message_error(request, errors)
        return 'error'
    

def update_archivo(request, archivo_id, data):
    """Crear archivo"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.put(f'{url}/put/archivo/{archivo_id}', json=data, headers=headers)
        
        r.raise_for_status()

        emit_message_success(request, 'El archivo se creó correctamente')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']

        emit_message_error(request, errors)
        return 'error'
    