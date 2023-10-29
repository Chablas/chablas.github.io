from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import FormView, ListView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from decorators.messages import eliminar_mensajes
from decorators.user import esta_logueado, modulo_requerido

from ..services.categorias import get_categorias_all, create_categoria, update_categoria

from ..forms import CategoriaForm

TEMPLEATE_ROOT = 'proveedores'

# Create your views here.
@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class CategoriasView(ListView):
    """Vista general de las categorias"""
    template_name = f"{TEMPLEATE_ROOT}/categoria/index.html"
    context_object_name='categorias'
    paginate_by=15

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        return get_categorias_all(self.request, search)
    
@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class CategoriaCreateView(FormView):
    """ Vista de creacion de categoria """
    template_name =f"{TEMPLEATE_ROOT}/categoria/form.html"
    form_class = CategoriaForm
    success_url=reverse_lazy('proveedores:categoriasIndex')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Categoria'
        context['routes'] = [
            {
                "route":reverse_lazy('proveedores:categoriasIndex'),
                "name":'Categorias'
            }
        ]
        return context
    
    def form_valid(self, form) :
        data = form.cleaned_data
  
        data['nombre'] = str(data['nombre']).upper() 
        
        if create_categoria(self.request, data) == 'error':
            return super(CategoriaCreateView, self).form_invalid(form)
        else:
            return super(CategoriaCreateView, self).form_valid(form)

@esta_logueado
@modulo_requerido
@eliminar_mensajes
@require_http_methods(["GET"])
def categoria_update_view(request, **kwargs):
    """ Funcion de actualizacion una categoria """
    update_categoria(request, kwargs['id'])
    return redirect("proveedores:categoriasIndex")