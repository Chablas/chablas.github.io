from django import forms

class PedidoForm(forms.Form):
    fecha_atencion = forms.DateField()
    descripcion = forms.CharField(max_length=250, min_length=3)
    observacion = forms.CharField(max_length=250, min_length=3)
    origin_id = forms.CharField()

class DetallePedidoForm(forms.Form):
    pedido_id = forms.CharField()
    material_proveedor_id = forms.CharField(max_length=250, min_length=3)
    cantidad = forms.DecimalField(max_digits = 6, decimal_places = 2, min_value=0.01)
    precio_unitario = forms.DecimalField()

class OrdenCompraForm(forms.Form):
    proveedor_id = forms.CharField(max_length=150, min_length=3, widget=forms.TextInput(attrs={'readonly': True}))
    total = forms.DecimalField(widget=forms.TextInput(attrs={'readonly': True}))
    estado_id = forms.CharField(max_length=150, min_length=3, widget=forms.TextInput(attrs={'readonly': True}))

class GuiaRemisionForm(forms.Form):
    detalle_compra_id = forms.ChoiceField(required=False)
    almacen_proyecto_id = forms.ChoiceField(required=False)
    cantidad = forms.DecimalField(max_digits = 6, decimal_places = 2, min_value=0.01)
    fecha_entrega = forms.DateField()
    estado_remision = forms.ChoiceField()