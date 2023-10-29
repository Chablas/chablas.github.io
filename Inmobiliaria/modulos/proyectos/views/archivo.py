import os
# import time
# import aspose.cad as cad
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from decorators.messages import eliminar_mensajes
from decorators.user import esta_logueado, modulo_requerido

from helpers.firebase import firebase_upload_file, firebase_download

from modulos.sistema.services.tiposArchivo import get_tipos_archivo_cb
from ..services.archivo import get_archivo_all, create_archivo, get_archivo_one, update_archivo

from ..forms import ArchivoForm

# Create your views here.

TEMPLEATE_ROOT = 'proyectos'

@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class ArchivoView(ListView):
    """ Vista global de archivo """
    template_name = f"{TEMPLEATE_ROOT}/archivo/index.html"
    context_object_name='archivos'
    paginate_by=15
    proyecto = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        context['proyecto_id'] = self.kwargs['proyecto_id']
        context['proyecto'] = self.kwargs['proyecto']

        context['title'] = f"Archivos de {self.kwargs['proyecto']}"
        context['routes'] = [
            {
                "route":reverse_lazy('proyectos:proyectosIndex'),
                "name": "Proyectos"
            }
        ]

        return context
    
    def get_queryset(self):
        search = self.request.GET.get('search', '')
        proyecto_id = self.kwargs['proyecto_id']

        return get_archivo_all(self.request, proyecto_id, search)
    
@method_decorator(esta_logueado, name='dispatch')
@method_decorator(modulo_requerido, name='dispatch')
@method_decorator(eliminar_mensajes, name='setup')
class ArchivoCreateView(FormView):
    """ Vista de creacion de archivo """
    template_name=f"{TEMPLEATE_ROOT}/archivo/form.html"
    form_class = ArchivoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['routes'] = [
            {
                "route":reverse_lazy('proyectos:proyectosIndex'),
                "name" : "Proyectos"
            },
            {
                "route":reverse_lazy('proyectos:archivosIndex', kwargs={'proyecto_id':self.kwargs['proyecto_id'], 'proyecto':self.kwargs['proyecto']}),
                "name": f"Archivos de {self.kwargs['proyecto']}"
            }
        ]  
        context['title'] = f"Nuevo archivo de {self.kwargs['proyecto']}"

        return context
   
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
      
        form.fields['tipo_archivo_id'].choices = get_tipos_archivo_cb(self.request)

        return form

    def form_valid(self, form) :
        data = form.cleaned_data

        data['nombre'] = str(data['nombre']).upper()

        imagen = data['url_archivo']

        data['url_archivo'] = firebase_upload_file(self.request, imagen, self.kwargs['proyecto_id'])
    
        if data['url_archivo'] == 'error' or create_archivo(self.request, self.kwargs['proyecto_id'], data) == 'error':
            return super(ArchivoCreateView, self).form_invalid(form)

        return super(ArchivoCreateView, self).form_valid(form)
    
    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            self.success_url = reverse_lazy('proyectos:archivosIndex', kwargs={'proyecto_id':self.kwargs['proyecto_id'], 'proyecto':self.kwargs['proyecto']})
        return str(self.success_url)  # success_url may be lazy

class ArchivoUpdateView(FormView):
    """ Vista de actualizacion de archivo """
    template_name=f"{TEMPLEATE_ROOT}/archivo/form.html"
    form_class = ArchivoForm

    archivo = None

    def get_initial(self):
        initial = super().get_initial()

        self.archivo = get_archivo_one(self.request, self.kwargs['id'])

        if isinstance(self.archivo, dict):
            initial['nombre'] = self.archivo['nombre']
            initial['tipo_archivo_id'] = self.archivo['tipo']['id']
            initial['descripcion'] = self.archivo['versiones'][len(self.archivo['versiones'])-1]['descripcion']
            initial['url_archivo'] = None

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.archivo['nombre']
        context['routes'] = [
            {
                "route":reverse_lazy('proyectos:proyectosIndex'),
                "name" : "Proyectos"
            },
            {
                "route":reverse_lazy('proyectos:archivosIndex', kwargs={'proyecto_id':self.kwargs['proyecto_id'], 'proyecto':self.kwargs['proyecto']}),
                "name": f"Archivos de {self.kwargs['proyecto']}"
            }
        ]

        return context
   
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
   
        form.fields['tipo_archivo_id'].choices = [(self.archivo['tipo']['id'], self.archivo['tipo']['nombre'])]

        form.fields['tipo_archivo_id'].widget.attrs['disabled']  = True
        form.fields['tipo_archivo_id'].required = False

        form.fields['url_archivo'].required = False
    
        return form

    def form_valid(self, form) :
        data = form.cleaned_data

        data['nombre'] = str(data['nombre']).upper()

        if (data['url_archivo'] is not None):
            imagen = data['url_archivo']
            data['url_archivo'] = firebase_upload_file(self.request, imagen, self.kwargs['proyecto_id'])
    
        if data['url_archivo'] == 'error' or update_archivo(self.request, self.archivo['id'], data) == 'error':
            return super(ArchivoUpdateView, self).form_invalid(form)

        return super(ArchivoUpdateView, self).form_valid(form)
    
    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            self.success_url = reverse_lazy('proyectos:archivosIndex', kwargs={'proyecto_id':self.kwargs['proyecto_id'], 'proyecto':self.kwargs['proyecto']})
        return str(self.success_url)  # success_url may be lazy

@esta_logueado
@modulo_requerido
@eliminar_mensajes
@require_http_methods(["GET"])
def create_temporal_archivo_view(request, **kwargs):
    """ Funcion de descarga de archivo """
    blob_path = request.GET.get('blob_path', '')
    
    extension = os.path.splitext(blob_path)[1]
    
    filename = firebase_download(blob_path, extension)

    # if(extension == '.dwg'):
    #     new_name = os.path.splitext(filename)[0]

    #     new_filename = f"{new_name}.pdf"

    #     image = cad.Image.load(f'media/{filename}')
    #     pdf_options = cad.imageoptions.PdfOptions()

    #     image.save(f'media/{new_filename}', pdf_options)
        
    #     filename = new_filename
    
    #     time.sleep(30)

    return HttpResponse(f'{filename}|{extension}', content_type='text/plain')

@esta_logueado
@modulo_requerido
@eliminar_mensajes
@require_http_methods(["GET"])
def delete_temporal_archivo_view(request, **kwargs):
    """ Funcion de eliminar archivo """
    
    pdf = request.GET.get('pdf', '')
    extend = request.GET.get('extend', '')
    
    print(pdf)

    print(os.path.split(pdf))

    arr = str(pdf).split('/')

    count = len(arr)
    
    file = arr[count-1]
    
    root = f"{arr[count-2]}"

    if(extend == '.dwg'):
        arr = str(file).split('.')
        name = arr[0]
        dwg = f'{root}/{name}{extend}'
        os.remove(dwg)

    os.remove(f'{root}/{file}')

    return HttpResponse('', content_type='text/plain')
