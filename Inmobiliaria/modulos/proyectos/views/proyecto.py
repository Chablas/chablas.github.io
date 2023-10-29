from datetime import date

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.views.generic import FormView, ListView

from decorators.messages import eliminar_mensajes
from decorators.user import esta_logueado, modulo_requerido

from modulos.proveedores.services.proveedores import get_proveedores_cb

from ..services.zonas import get_zonas_cb
from ..services.etapas import get_etapas_cb
from ..services.estados import get_estados_cb

from ..services.proyectos import get_proyectos_all, get_proyecto_one, create_proyecto, update_proyecto

from ..forms import ProyectoForm

# Create your views here.

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class ProyectoListView(ListView):
    """ Vista global de proyectos """
    template_name = "proyectos/proyecto/index.html"
    context_object_name='proyectos'
    paginate_by=15

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        return get_proyectos_all(self.request, search)

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class ProyectoCreateView(FormView):
    """ Vista de creacion de etapa """
    template_name = "proyectos/proyecto/form.html"
    form_class = ProyectoForm
    success_url=reverse_lazy('proyectos:proyectosIndex')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Proyecto'
        context['routes'] = [
            {
                "route":reverse_lazy('proyectos:proyectosIndex'),
                "name":'Proyectos'
            }
        ]
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['zona_id'].choices = get_zonas_cb(self.request)
        form.fields['estado_id'].choices = get_estados_cb(self.request)
        form.fields['etapa_id'].choices = get_etapas_cb(self.request)
        form.fields['proveedores_id'].choices = get_proveedores_cb(self.request)
        return form

    def form_valid(self, form) :
        data = form.cleaned_data
  
        data['fecha_creacion'] = date.strftime(date.today(), '%Y-%m-%d')
        data['fecha_inicio'] = date.strftime(data['fecha_inicio'], '%Y-%m-%d')
        data['fecha_fin'] = date.strftime(data['fecha_fin'], '%Y-%m-%d')
        
        if create_proyecto(self.request, data) == 'error':
            return super(ProyectoCreateView, self).form_invalid(form)
        else:
            return super(ProyectoCreateView, self).form_valid(form)

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class ProyectoUpdateView(FormView):
    """ Vista de actualizacion de proyecto """
    template_name="proyectos/proyecto/form.html"
    success_url=reverse_lazy('proyectos:proyectosIndex')
    form_class = ProyectoForm
    data = None
    title = None

    def get_initial(self):
        initial = super().get_initial()
        proyecto_id = self.kwargs['id']

        self.data = get_proyecto_one(self.request, proyecto_id)
        
        if isinstance(self.data, dict):
            initial = self.data
            self.title = self.data['nombre']
            initial['id'] = self.data['id']
            initial['zona_id'] = self.data['zona']['id']
            initial['etapa_id'] = self.data['etapa']['id']
            initial['estado_id'] = self.data['estado']['id']

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['routes'] = [
            {
                "route":reverse_lazy('proyectos:proyectosIndex'),
                "name":'Proyectos'
            }
        ]
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        form.fields['zona_id'].choices = [(self.data['zona']['id'], self.data['zona']['nombre'])]

        proveedores = []

        for p in self.data['proveedores']:
            proveedores.append((p['id'], p['nombre_empresa']))

        form.fields['proveedores_id'].choices = proveedores
        
        form.fields['etapa_id'].choices = get_etapas_cb(self.request)
        form.fields['estado_id'].choices = get_estados_cb(self.request)
        
        form.fields['zona_id'].widget.attrs['disabled'] = True
        form.fields['proveedores_id'].widget.attrs['disabled'] = True

        form.fields['zona_id'].required = False
        form.fields['proveedores_id'].required = False

        return form

    def form_valid(self, form) :
        data = form.cleaned_data

        data['id'] = self.data['id']

        data['fecha_inicio'] = date.strftime(data['fecha_inicio'], '%Y-%m-%d')
        data['fecha_fin'] = date.strftime(data['fecha_fin'], '%Y-%m-%d')

        if update_proyecto(self.request, data['id'], data) == 'error':
            return super(ProyectoUpdateView, self).form_invalid(form)
        else:
            return super(ProyectoUpdateView, self).form_valid(form)
