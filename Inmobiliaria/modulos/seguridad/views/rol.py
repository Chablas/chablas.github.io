from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from django.views.generic import FormView, ListView

from decorators.messages import eliminar_mensajes
from decorators.user import esta_logueado, modulo_requerido

from helpers.user import get_all_modulos

from ..forms import RolForm, RolModuloForm

from ..services.rol import get_roles_all, get_rol_one, create_rol, update_rol, deallocate_modulo_to_rol, allocate_modulo_to_rol

TEMPLEATE_ROOT = 'seguridad'

# Create your views here.
@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class RolListView(ListView):
    """Vista global de estados de roles"""
    template_name = f"{TEMPLEATE_ROOT}/rol/index.html"
    context_object_name='roles'
    paginate_by=15

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        return get_roles_all(self.request, search)

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class RolCreateView(FormView):
    """ Vista de creacion de rol """
    template_name = f"{TEMPLEATE_ROOT}/rol/form.html"
    form_class = RolForm
    success_url=reverse_lazy('seguridad:rolesIndex')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo rol'
        context['routes'] = [
            {
                "route":reverse_lazy('seguridad:rolesIndex'),
                "name":'Roles'
            }
        ]
        return context
    
    def form_valid(self, form) :
        data = form.cleaned_data
        data['nombre'] = str(data['nombre']).upper()
        if create_rol(self.request, data) == 'error':
            return super(RolCreateView, self).form_invalid(form)
        else:
            return super(RolCreateView, self).form_valid(form)

@esta_logueado
@modulo_requerido
@eliminar_mensajes
@require_http_methods(["GET"])
def rol_update_view(request, **kwargs):
    """ Funcion de actualizacion de etapa """
    update_rol(request, kwargs['id'])
    return redirect("seguridad:rolesIndex")

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class RolModuloview(FormView):
    """ Vista de modulos de rol """
    template_name = f"{TEMPLEATE_ROOT}/rol/modulo.html"
    form_class = RolModuloForm

    title = None
    modulos = []
    rol = None

    def get_initial(self):
        initial = super().get_initial()
        rol_id = self.kwargs['id']

        data = get_rol_one(self.request, rol_id)

        if isinstance(data, dict):
            self.rol = data
            self.modulos = data['modulos']

            self.title = f"Modulos de {self.rol['nombre']}"

            initial['id'] = self.rol['id']

        return initial


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['routes'] = [
            {
                "route":reverse_lazy('seguridad:rolesIndex'),
                "name":'Roles'
            }
        ]
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        modulos = get_all_modulos()

        categorias_allocate = []
        categorias_deallocate = []

        for x in modulos:
            if(x[0] in self.modulos):
                categorias_allocate.append(x)
            else:
                categorias_deallocate.append(x)

        form.fields['modulo_to_allocate'].choices = categorias_deallocate
        form.fields['modulo_to_deallocate'].choices = categorias_allocate
        return form
    
    def form_valid(self, form) :
        data = form.cleaned_data

        response = None

        if(data['modulo_to_allocate'] != ''):
            response = allocate_modulo_to_rol(self.request, data['id'], data['modulo_to_allocate'])
        else:
            response = deallocate_modulo_to_rol(self.request, data['id'], data['modulo_to_deallocate'])
        
        if response == 'error':
            return super(RolModuloview, self).form_invalid(form)
        else:
            return super(RolModuloview, self).form_valid(form)
        
    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            self.success_url = reverse_lazy('seguridad:rolesModulo', kwargs={"id": self.rol['id']})
        return str(self.success_url)  # success_url may be lazy