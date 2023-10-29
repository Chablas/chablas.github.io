import json

from datetime import date

from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from ..forms import ActividadForm

TEMPLEATE_ROOT = 'proyectos/actividad'

# Create your views here.
class ActividadesListView(TemplateView):
    template_name = f"{TEMPLEATE_ROOT}/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['routes'] = [
            {
                "route":reverse_lazy('proyectos:proyectosIndex'),
                "name" : "Proyectos"
            }
        ]  
        
        context['title'] = f"Actividades {self.kwargs['proyecto']}"
        context['proyecto'] = self.kwargs['proyecto']
        
        context['events'] = json.loads(self.request.session.get('eventos', '[]'))

        return context
    
class ActividadCreateView(FormView):
    """ Vista de creación de actividades"""
    template_name = f"{TEMPLEATE_ROOT}/form.html"
    form_class = ActividadForm
    
    def get_initial(self):
        initial = super().get_initial()
        
        initial['nombre_proyecto'] = self.kwargs['proyecto']

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        context['title'] = "Nueva Actividad"
        context['routes'] = [
             {
                "route":reverse_lazy('proyectos:actividadesIndex', kwargs={'proyecto_id':self.kwargs['proyecto_id'], 'proyecto':self.kwargs['proyecto']}),
                "name":'Actividades'
            }
        ]
        return context
        
    def form_valid(self, form) :
        data = form.cleaned_data
        
        eventos = json.loads(self.request.session.get('eventos', '[]'))
           
        eventos.append(
            {
                'id': f'event-{len(eventos)+1}',
                'calendarId': 'cal1',
                'title': data['nombre'],
                'start': date.strftime(data['fecha_inicio'], '%Y-%m-%d'),
                'end': date.strftime(data['fecha_fin'], '%Y-%m-%d'),
                'isAllday': True,
                'category': 'allday'
            }
        )

        self.request.session["eventos"] = json.dumps(eventos)

        return super(ActividadCreateView, self).form_valid(form)

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            self.success_url = reverse_lazy('proyectos:actividadesIndex', kwargs={'proyecto_id':self.kwargs['proyecto_id'], 'proyecto':self.kwargs['proyecto']})
        return str(self.success_url)  # success_url may be lazy

class ActividadUpdateView(FormView):
    """ Vista de creación de guias de remision"""
    template_name = f"{TEMPLEATE_ROOT}/form.html"
    success_url = None
    form_class = ActividadForm
    
    def get_initial(self):
        initial = super().get_initial()
        
        evento = None
        eventos = json.loads(self.request.session.get('eventos', '[]'))

        for e in eventos:
            if(e['id'] == f"event-{self.kwargs['actividad_id']}"):
                evento = e
                print(e)

        initial['nombre'] = evento['title']
        initial['fecha_inicio'] = evento['start']
        initial['fecha_fin'] = evento['end']
        initial['tipo_actividad'] = 1
        initial['nombre_proyecto'] = self.kwargs['proyecto']

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = "Actividades"
        context['routes'] = [
             {
                "route":reverse_lazy('proyectos:actividadesIndex', kwargs={'proyecto_id':self.kwargs['proyecto_id'], 'proyecto':self.kwargs['proyecto']}),
                "name":'Actividades'
            }
        ]
        return context
    
    def form_valid(self, form) :
        data = form.cleaned_data
        
        eventos = json.loads(self.request.session.get('eventos', '[]'))
       
        for e in eventos:
            if(e['id'] == f"event-{self.kwargs['actividad_id']}"):
                e['title'] = data['nombre']
                e['start'] = date.strftime(data['fecha_inicio'], '%Y-%m-%d')
                e['end'] = date.strftime(data['fecha_fin'], '%Y-%m-%d')

        self.request.session["eventos"] = json.dumps(eventos)

        return super(ActividadUpdateView, self).form_valid(form)
    
    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            self.success_url = reverse_lazy('proyectos:actividadesIndex', kwargs={'proyecto_id':self.kwargs['proyecto_id'], 'proyecto':self.kwargs['proyecto']})
        return str(self.success_url)  # success_url may be lazy

