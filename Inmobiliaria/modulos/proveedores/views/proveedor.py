from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from django.utils.decorators import method_decorator

from decorators.messages import eliminar_mensajes
from decorators.user import esta_logueado, modulo_requerido

from modulos.proyectos.services.zonas import get_zonas_cb

from ..services.categorias import get_categorias_cb
from ..services.proveedores import get_proveedores_all, create_proveedor, get_proveedor_one, update_proveedor
from ..services.proveedores import allocate_proveedor_categoria, deallocate_proveedor_categoria, allocate_proveedor_zona, deallocate_proveedor_zona

from ..forms import ProveedorCreateForm, ProveedorUpdateForm, ProveedorCategoriaForm, ProveedorZonaForm

TEMPLEATE_ROOT = 'proveedores'

# Create your views here.    

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class ProveedoresView(ListView):
    """Vista general de los proveedores"""
    template_name = f"{TEMPLEATE_ROOT}/proveedor/index.html"
    context_object_name='proveedores'
    paginate_by=15

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        return get_proveedores_all(self.request, search)
    
@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class ProveedoresCreateView(FormView):
    """ Vista de creacion de categoria """
    template_name =f"{TEMPLEATE_ROOT}/proveedor/form.html"
    form_class = ProveedorCreateForm
    success_url=reverse_lazy('proveedores:proveedoresIndex')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Proveedor'
        context['routes'] = [
            {
                "route":reverse_lazy('proveedores:proveedoresIndex'),
                "name":'Proveedores'
            }
        ]
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # form.fields['id_categoria_empresas'].choices = get_categorias_cb(self.request)
        # form.fields['id_zonas'].choices = get_zonas_cb(self.request)
        return form
    
    def form_valid(self, form) :
        data = form.cleaned_data

        if create_proveedor(self.request, data) == 'error':
            return super(ProveedoresCreateView, self).form_invalid(form)
        else:
            return super(ProveedoresCreateView, self).form_valid(form)
        
@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class ProveedorUpdateView(FormView):
    """ Vista de actualizacion de proyecto """
    template_name=f"{TEMPLEATE_ROOT}/proveedor/form.html"
    success_url=reverse_lazy('proveedores:proveedoresIndex')
    form_class = ProveedorUpdateForm
    data = None
    title = None

    def get_initial(self):
        initial = super().get_initial()
        proyecto_id = self.kwargs['id']

        self.data = get_proveedor_one(self.request, proyecto_id)
        
        if isinstance(self.data, dict):
            self.title = self.data['nombre_empresa']
            initial = self.data
            initial['id'] = self.data['id']
            initial['estado'] = self.data['estado'] == 'ACTIVO'

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['id'] =  self.kwargs['id']
        context['routes'] = [
            {
                "route":reverse_lazy('proveedores:proveedoresIndex'),
                "name":'Proveedores'
            }
        ]
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['id'].widget.attrs['readonly'] = True
        return form

    def form_valid(self, form) :
        data = form.cleaned_data

        if update_proveedor(self.request, data['id'], data) == 'error':
            return super(ProveedorUpdateView, self).form_invalid(form)
        else:
            return super(ProveedorUpdateView, self).form_valid(form)

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class ProveedorCategoriaView(FormView):
    """Vsita para asignar y desaginar categorias"""
    template_name = f"{TEMPLEATE_ROOT}/proveedor/categoria.html"
    form_class = ProveedorCategoriaForm

    title = None
    data = None

    def get_initial(self):
        initial = super().get_initial()
        proyecto_id = self.kwargs['id']

        self.data = get_proveedor_one(self.request, proyecto_id)
        
        if isinstance(self.data, dict):
            self.title = self.data['nombre_empresa']
            initial = self.data
            initial['id'] = self.data['id']

        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['routes'] = [
            {
                "route":reverse_lazy('proveedores:proveedoresIndex'),
                "name":'Proveedores'
            }
        ]
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        categorias_allocate = []
        categorias_deallocate = []

        if(self.data is not None):
            for x in self.data['categorias'] :
                categorias_allocate.append((x['id'], x['nombre']))

            for x in get_categorias_cb(self.request) :
                if(x not in categorias_allocate):
                    categorias_deallocate.append(x)
        
        form.fields['id_categoria_to_allocate'].choices = categorias_deallocate
        form.fields['id_categoria_to_deallocate'].choices = categorias_allocate

        return form
    
    def form_valid(self, form) :
        data = form.cleaned_data

        response = None

        if(data['id_categoria_to_allocate'] != ''):
            response = allocate_proveedor_categoria(self.request, data['id'], data['id_categoria_to_allocate'])
        else:
            response = deallocate_proveedor_categoria(self.request, data['id'], data['id_categoria_to_deallocate'])
        
        if response == 'error':
            return super(ProveedorCategoriaView, self).form_invalid(form)
        else:
            return super(ProveedorCategoriaView, self).form_valid(form)
            
    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            self.success_url = reverse_lazy('proveedores:proveedoresCategoria',  kwargs={"id": self.data['id']})
        return str(self.success_url)  # success_url may be lazy

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class ProveedorZonaView(FormView):
    """Vsita para asignar y desaginar zonas"""
    template_name = f"{TEMPLEATE_ROOT}/proveedor/zona.html"
    form_class = ProveedorZonaForm

    title = None
    data = None

    def get_initial(self):
        initial = super().get_initial()
        proyecto_id = self.kwargs['id']

        self.data = get_proveedor_one(self.request, proyecto_id)
        
        if isinstance(self.data, dict):
            self.title = self.data['nombre_empresa']
            initial = self.data
            initial['id'] = self.data['id']

        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['routes'] = [
            {
                "route":reverse_lazy('proveedores:proveedoresIndex'),
                "name":'Proveedores'
            }
        ]
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        zonas_allocate = []
        zonas_deallocate = []
        
        if(self.data is not None):
            for x in self.data['zonas'] :
                zonas_allocate.append((x['id'], x['nombre']))

            for x in get_zonas_cb(self.request) :
                if(x not in zonas_allocate):
                    zonas_deallocate.append(x)
    
        form.fields['id_zona_to_allocate'].choices = zonas_deallocate
        form.fields['id_zona_to_deallocate'].choices = zonas_allocate
        return form
    
    def form_valid(self, form) :
        data = form.cleaned_data

        response = None

        if(data['id_zona_to_allocate'] != ''):
            response = allocate_proveedor_zona(self.request, data['id'], data['id_zona_to_allocate'])
        else:
            response = deallocate_proveedor_zona(self.request, data['id'], data['id_zona_to_deallocate'])
        
        if response == 'error':
            return super(ProveedorZonaView, self).form_invalid(form)
        else:
            return super(ProveedorZonaView, self).form_valid(form)
            
    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            self.success_url = reverse_lazy('proveedores:proveedoresZona',  kwargs={"id": self.data['id']})
        return str(self.success_url)  # success_url may be lazy
