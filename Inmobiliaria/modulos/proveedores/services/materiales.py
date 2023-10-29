from datetime import datetime
from django.conf import settings
from helpers.messageBox import emit_message_error, emit_message_success

import requests

dominio = getattr(settings, 'API_URL', 'https://inversiones-368.onrender.com/api/v1')
url = f"{dominio}/in"

headers = {'Content-type': 'application/json; charset=UTF-8'}

def get_materiales_all(request, proveedor_id, search):
    """Obtener Todos los Materiales de los Proveedores"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        if(search != ''):
            r = requests.get(f'{url}/get/materiales_proveedor/{proveedor_id}/?name='+search, allow_redirects=False, headers=headers)
        else :
            r = requests.get(f'{url}/get/materiales_proveedor/{proveedor_id}', allow_redirects=False, headers=headers)  
        
        r.raise_for_status()
        
        data = r.json()

        for item in data : 
            item['fecha_vencimiento'] = datetime.strptime(item['fecha_vencimiento'], '%Y-%m-%d')

        return data
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']
        
        emit_message_error(request, errors)
        
        return []


"""Obtener Materiales por su Id"""
def get_material_one(request, material_id):
    headers['Authorization'] = f"Bearer {request.session['token']}"
    try:
        r = requests.get(f'{url}/get/material/{material_id}', allow_redirects=False, headers=headers)

        r.raise_for_status()
            
        return r.json()['dato']
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']

        emit_message_error(request, errors)

        return 'error'

def create_material_by_proveedor(request, id_proveedor, data):
    """Registrar Materiales con el Id del Proveedor"""
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.post(f'{url}/post/materiales_proveedor/{id_proveedor}', json=data, allow_redirects=False, headers=headers)
        r.raise_for_status()

        emit_message_success(request, 'Los materiales han sido registrados con el proveedor seleccionado')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']

        emit_message_error(request, errors)
        return 'error'

"""Actualizar los datos de un Material"""
def update_material(request,material_id,data):
     headers['Authorization'] = f"Bearer {request.session['token']}"
     r = None
     try:
        r = requests.put(f'{url}/put/material/{material_id}',json = data, headers=headers)
        r.raise_for_status()
        emit_message_success(request, 'Se han actualizado los datos del material correctamente')
     except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500):
            errors = r.json()['detail']

        emit_message_error(request, errors)
        return 'error'
     
"""Actualizar el estado de un material"""

def update_estado_material(request,material_id):
    headers['Authorization'] = f"Bearer {request.session['token']}"
    r = None
    try:
        r = requests.put(f'{url}/put/material/{material_id}/update_estado', headers=headers)
        r.raise_for_status()

        emit_message_success(request, 'Se ha actualizado el estado del material')
    except requests.exceptions.RequestException:
        errors = 'Internal server error'

        if(r.status_code < 500) :
            errors = r.json()['detail']
            
        emit_message_error(request, errors)
        return 'error'
     


