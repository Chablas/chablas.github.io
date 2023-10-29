from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from decorators.user import esta_logueado
from decorators.messages import eliminar_mensajes

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class IndexView(TemplateView):
    template_name = "home/home.html"


