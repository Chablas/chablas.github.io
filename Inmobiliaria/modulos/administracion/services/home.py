from django.conf import settings
import requests

dominio = getattr(settings, 'API_URL', 'https://inversiones-368.onrender.com/api/v1')
url = f"{dominio}/empresa/g_usuarios"

    
