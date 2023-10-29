from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.views.generic import FormView, ListView

from decorators.messages import eliminar_mensajes
from decorators.user import esta_logueado, modulo_requerido

from modulos.sistema.services.unidadmedida import get_unidades_medida_cb
from modulos.proveedores.services.categorias import get_categorias_cb

from ..forms import MaterialForm, MaterialUpdateForm

from ..services.materiales import get_materiales_all, get_material_one

TEMPLEATE_ROOT = 'almacen'

# Create your views here.
@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class MaterialListView(ListView):
    """Vista global de materiales de la empresa"""
    template_name = f"{TEMPLEATE_ROOT}/material/index.html"
    context_object_name='materiales'
    paginate_by=15

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        return []

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class MaterialCreateView(FormView):
    """ Vista de creacion de materiales """
    template_name = f"{TEMPLEATE_ROOT}/material/form.html"
    form_class = MaterialForm
    success_url=reverse_lazy('almacen:materialIndex')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Material'
        context['routes'] = [
            {
                "route":reverse_lazy('almacen:materialIndex'),
                "name":'Materiales'
            }
        ]
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['unidad_medida_id'].choices = get_unidades_medida_cb(self.request)
        form.fields['categoria_id'].choices = get_categorias_cb(self.request)
        return form

    def form_valid(self, form) :
        data = form.cleaned_data
        
        data['nombre'] = str(data['nombre']).upper()
        
        # if create_estado(self.request, data) == 'error':
        #     return super(EstadoCreateView, self).form_invalid(form)
        # else:

        return super(MaterialCreateView, self).form_valid(form)
    
@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class MaterialUpdateView(FormView):
    """ Vista de creacion de materiales """
    template_name = f"{TEMPLEATE_ROOT}/material/form.html"
    form_class = MaterialUpdateForm
    success_url=reverse_lazy('almacen:materialIndex')

    data = {}

    def get_initial(self):
        initial = super().get_initial()

        material_id = self.kwargs['id']

        self.data = {}
        
        if isinstance(self.data, dict):
            initial = self.data
            
            # self.title = self.data['nombre']

            # initial['unidad_medida_id'] = self.data['unidad_medida']['id']
            # initial['categoria_id'] = self.data['categoria']['id']

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Material {self.data.get('nombre')}"
        context['routes'] = [
            {
                "route":reverse_lazy('almacen:materialIndex'),
                "name":'Materiales'
            }
        ]
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['unidad_medida_id'].choices = get_unidades_medida_cb(self.request)
        form.fields['categoria_id'].choices = get_categorias_cb(self.request)
        return form

    def form_valid(self, form) :
        data = form.cleaned_data
        
        data['nombre'] = str(data['nombre']).upper()
        
        # if create_estado(self.request, data) == 'error':
        #     return super(EstadoCreateView, self).form_invalid(form)
        # else:

        return super(MaterialUpdateView, self).form_valid(form)