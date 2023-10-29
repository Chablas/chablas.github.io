from datetime import date

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.forms import formset_factory
from django.views.generic import FormView, ListView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from decorators.messages import eliminar_mensajes
from decorators.user import esta_logueado, modulo_requerido

from modulos.proveedores.services.categorias import get_categorias_cb

from  modulos.sistema.services.unidadmedida import get_unidades_medida_cb
from ..services.materiales import get_materiales_all, get_material_one, create_material_by_proveedor, update_estado_material, update_material

from ..forms import MaterialCreateForm, MaterialUpdateForm 

TEMPLEATE_ROOT = 'proveedores'

# Create your views here.

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class MaterialesView(ListView):
    """ Vista de todos los materiales """
    template_name = f"{TEMPLEATE_ROOT}/materiales/index.html"
    context_object_name='materiales'
    paginate_by=15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        context['proveedor_id'] =  self.kwargs['proveedor_id']
        context['proveedor'] =  self.kwargs['proveedor']

        context['title'] = f"Materiales de {self.kwargs['proveedor']}"

        context['routes'] = [
            {
                "route":reverse_lazy('proveedores:proveedoresIndex'),
                "name": "Proveedores"
            }
        ]

        return context
    
    def get_queryset(self):
        search = self.request.GET.get('search', '')
        return get_materiales_all(self.request, self.kwargs['proveedor_id'], search)
    
@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class MaterialCreateView(FormView):
    """ Vista de creacion de material """
    template_name = f"{TEMPLEATE_ROOT}/materiales/form.html"

    def get_form_class(self):
        """Return the form class to use."""
        cantidad = int(self.request.GET.get('cantidad', 1))
        return formset_factory(MaterialCreateForm, extra=cantidad, max_num=10)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['proveedor_id'] = self.kwargs['proveedor_id']
        context['title'] = f"Nuevos Materiales de {self.kwargs['proveedor']}"

        context['routes'] = [
            {
                "route":reverse_lazy('proveedores:proveedoresIndex'),
                "name": "Proveedores"
            },
            { 
                "route":reverse_lazy('proveedores:materialesIndex', kwargs={"proveedor_id": self.kwargs['proveedor_id'], "proveedor": self.kwargs['proveedor']}),
                "name": f"Materiales de {self.kwargs['proveedor']}"
            }
        ]

        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        categorias =  get_categorias_cb(self.request)
        unidades_medida = get_unidades_medida_cb(self.request)

        for f in form:
            f.fields['categoria_id'].choices = categorias
            f.fields['unidad_medida_id'].choices = unidades_medida
        
        return form

    def form_valid(self, form) :
        data = []

        for f in form:
            item = f.cleaned_data
            
            item['precio_actual'] = str(item['precio_actual'])
            item['cantidad_contenedora'] = str(item['cantidad_contenedora'])
            item['fecha_vencimiento'] = date.strftime(item['fecha_vencimiento'], '%Y-%m-%d')

            data.append(item)
        
        if create_material_by_proveedor(self.request, self.kwargs['proveedor_id'], data) == 'error':
            return super(MaterialCreateView, self).form_invalid(form)
        else:
            return super(MaterialCreateView, self).form_valid(form)
        
    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            self.success_url = reverse_lazy('proveedores:materialesIndex',  kwargs={"proveedor_id": self.kwargs['proveedor_id'], "proveedor": self.kwargs['proveedor']})
        return str(self.success_url)  # success_url may be lazy

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class MaterialUpdateView(FormView): 
    """ Vista de actualizacion de material"""
    template_name=f"{TEMPLEATE_ROOT}/materiales/form.html"
    form_class = formset_factory(MaterialUpdateForm, max_num=1)
    
    data = None
    title = None

    def get_initial(self):
        initial = super().get_initial()
        material_id = self.kwargs['id']

        self.data = get_material_one(self.request, material_id)

        if isinstance(self.data, dict):
            self.title = self.data['codigo_proveedor']
            initial = [
                {
                    'codigo_proveedor':  self.data['codigo_proveedor'],
                    'categoria_id':  self.data['categoria']['id'],
                    'unidad_medida_id':  self.data['unidad_medida']['id'],
                    'cantidad_contenedora':  self.data['cantidad_contenedora'],
                    'descripcion':  self.data['descripcion'],
                    'precio_actual':  self.data['precio_actual'],
                    'fecha_vencimiento':  self.data['fecha_vencimiento'],
                    'fecha_creacion':  self.data['fecha_creacion']
                } 
            ]

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = self.title
        context['routes'] = [
            {
                "route": reverse_lazy("proveedores:proveedoresIndex") ,
                "name": "Proveedores"
            },
            {
                "route":reverse_lazy('proveedores:materialesIndex', kwargs={"proveedor_id": self.kwargs['proveedor_id'], "proveedor": self.kwargs['proveedor']}),
                "name": f"Materiales de {self.kwargs['proveedor']}"
            }
        ]
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form[0].fields['codigo_proveedor'].widget.attrs['readonly'] = True
        form[0].fields['cantidad_contenedora'].widget.attrs['readonly'] = True
        form[0].fields['fecha_creacion'].widget.attrs['readonly'] = True

        form[0].fields['categoria_id'].choices =  [(self.data['categoria']['id'], self.data['categoria']['nombre'])]
        form[0].fields['unidad_medida_id'].choices = [(self.data['unidad_medida']['id'], self.data['unidad_medida']['nombre'])]

        form[0].fields['categoria_id'].widget.attrs['disabled'] = True
        form[0].fields['unidad_medida_id'].widget.attrs['disabled'] = True

        form[0].fields['categoria_id'].required = False
        form[0].fields['unidad_medida_id'].required = False
        return form
        
    def form_valid(self, form) :
        data = form[0].cleaned_data
        
        data['precio_actual'] = str(data['precio_actual'])
        data['cantidad_contenedora'] = str(data['cantidad_contenedora'])
        data['fecha_creacion'] = date.strftime(data['fecha_creacion'], '%Y-%m-%d')
        data['fecha_vencimiento'] = date.strftime(data['fecha_vencimiento'], '%Y-%m-%d')

        if update_material(self.request, self.kwargs['id'], data) == 'error':
            return super(MaterialUpdateView, self).form_invalid(form)
        
        return super(MaterialUpdateView, self).form_valid(form)
    
    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            self.success_url = reverse_lazy('proveedores:materialesIndex', kwargs={"proveedor_id": self.kwargs['proveedor_id'], "proveedor": self.kwargs['proveedor']})
        return str(self.success_url)  # success_url may be lazy
    
@esta_logueado
@modulo_requerido
@eliminar_mensajes
@require_http_methods(["GET"])
def material_estado_update_view(request, **kwargs):
    """ Funcion de actualizacion del estado de un material"""
    update_estado_material(request, kwargs['id'])
    return redirect("proveedores:materialesIndex", proveedor_id=kwargs['proveedor_id'], proveedor=kwargs['proveedor'])

