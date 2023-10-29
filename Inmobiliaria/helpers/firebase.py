import os
import random
import string

from datetime import datetime, timedelta

from firebase_admin import storage
from google.cloud.exceptions import GoogleCloudError
from helpers.messageBox import emit_message_error


def get_bucket():
    """Obtiene el bucket de firebase"""
    return storage.bucket(name="inversiones368-abce4.appspot.com")

def firebase_generate_url(blob_path):
    """Genera el url de la imagen"""
    bucket = get_bucket()

    blob = bucket.blob(blob_path)

    if not blob.exists():
        return None
    
    return blob.generate_signed_url(expiration=datetime.utcnow() + timedelta(hours=9))

def firebase_download(blob_path, extension):
    """Genera el url de la imagen"""
    bucket = get_bucket()

    blob = bucket.blob(blob_path)

    if not blob.exists():
        return None
    
    length_of_string = 10

    name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))

    # f'media/{name}{extension}'
    path = os.path.join('media', f'{name}{extension}') 
    print(path)
    blob.download_to_filename(path)
    
    return f'{name}{extension}'

def firebase_upload_image(imagen, name):
    """Sube la imagen al firebase storage"""
    bucket = get_bucket()
    
    extension = os.path.splitext(imagen.name)[1]

    unique_filename = f'Fotos/{name}{extension}'

    blob = bucket.blob(unique_filename)

    blob.upload_from_file(imagen)

def firebase_upload_file(request, imagen, proyecto):
    """Sube la imagen al firebase storage"""
    try:
        bucket = get_bucket()
    
        unique_filename = f'Documentos/{proyecto}/{imagen.name}'

        blob = bucket.blob(unique_filename)

        blob.upload_from_file(imagen)

        return unique_filename
    except GoogleCloudError:
        emit_message_error(request, "ERROR FIREBASE")
        return "error"
    