from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.views.generic import FormView, ListView

from decorators.messages import eliminar_mensajes
from decorators.user import esta_logueado, modulo_requerido

from ..services.zonas import get_zonas_all, get_zona_one, create_zona, update_zona

from ..forms import ZonaCreateForm,ZonaUpdateForm

# Create your views here.

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class ZonaListView(ListView):
    """ Vista de global de estapas """ 
    template_name = "proyectos/zona/index.html"
    context_object_name='zonas'
    paginate_by=15

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        return get_zonas_all(self.request, search)
    
@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class ZonaCreateView(FormView):
    """ Vista de creacion de etapa """
    template_name = "proyectos/zona/form.html"
    form_class = ZonaCreateForm
    success_url=reverse_lazy('proyectos:zonasIndex')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Zona'
        context['routes'] = [
            {
                "route":reverse_lazy('proyectos:zonasIndex'),
                "name":'Zonas'
            }
        ]
        return context
    
    def form_valid(self, form) :
        data = form.cleaned_data
        data['nombre'] = str(data['nombre']).upper()
        if create_zona(self.request, data) == 'error':
            return super(ZonaCreateView, self).form_invalid(form)
        else:
            return super(ZonaCreateView, self).form_valid(form)

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class ZonaUpdateView(FormView):
    """ Vista de actualizacion de usuario """
    template_name="proyectos/zona/form.html"
    success_url=reverse_lazy('proyectos:zonasIndex')
    form_class = ZonaUpdateForm

    title = None
    data = None

    def get_initial(self):
        initial = super().get_initial()
        zona_id = self.kwargs['id']

        self.data = get_zona_one(self.request, zona_id)
        
        if(isinstance(self.data, dict)):
            self.title = self.data['nombre']
            initial = self.data

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['routes'] = [
            {
                "route":reverse_lazy('proyectos:zonasIndex'),
                "name":'Zonas'
            }
        ]
        return context
    
    def form_valid(self, form) :
        data = form.cleaned_data
        
        data['id'] = self.data['id']

        if update_zona(self.request, data['id'], data) == 'error':
            return super(ZonaUpdateView, self).form_invalid(form)
        else:
            return super(ZonaUpdateView, self).form_valid(form)