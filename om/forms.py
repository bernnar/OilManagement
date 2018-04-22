from django.core.exceptions import ValidationError
from django import forms
from .models import Deposito, Cuenta, Vehiculo, Conductor, Operacion, Apunte
from django.contrib.admin import widgets



class DepositoForm(forms.ModelForm):

    class Meta:
        model = Deposito
        fields = ('nombre', 'capacidad', 'cantidad',)
        #labels = { 'capacidad': ('capacidad'), }
        #help_texts = { 'cantidad': ('Cantidad actual. (Expresada en litros).'), 'capacidad': ('Capacidad total del depósito.'),}
        widgets = {
            'nombre': forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Introduzca un nombre...', 'required': True, } ),
            'capacidad': forms.NumberInput( attrs={ 'class': 'form-control', 'placeholder': 'Introduzca la capacidad del depósoto. (En litros)', 'required': True, } ),
            'cantidad': forms.NumberInput( attrs={ 'class': 'form-control', 'placeholder': 'Introduzca la cantidad actual del depósoto. (En litros)', 'required': True, } ),
        }

class CuentaForm(forms.ModelForm):

    class Meta:
        model = Cuenta
        fields = ('nombre', 'saldo', 'esAcreedor')
        widgets = {
            'nombre': forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Introduzca un nombre...', 'required': True, } ),
            'saldo' : forms.NumberInput( attrs={ 'class': 'form-control', 'placeholder': 'Saldo inicial...(En euros)', 'required': True, } ),
        }

class VehiculoForm(forms.ModelForm):

    class Meta:
        model = Vehiculo
        fields = ('nombre', 'exigirKm',)
        widgets = {
            'nombre': forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Introduzca un nombre...', 'required': True, } ),
        }

class ConductorForm(forms.ModelForm):

    class Meta:
        model = Conductor
        fields = ('nombre', )
        widgets = {
            'nombre': forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Introduzca un nombre...', 'required': True, } ),
        }


class OperacionForm(forms.ModelForm):

    class Meta:
        model = Operacion
        fields = ('fecha', 'litros', 'precio', 'importe' ,'acreedor' ,'deudor' ,'deposito', 'vehiculo' , 'conductor' , 'vehiculoKm' ,'tipoOperacion' , )
        #labels = { 'capacidad': ('capacidad'), }
        #help_texts = { 'cantidad': ('Cantidad actual. (Expresada en litros).'), 'capacidad': ('Capacidad total del depósito.'),}
        widgets = {
            'fecha': forms.TextInput( attrs={ 'class': 'form-control', 'type':'date' } ),
            'litros': forms.NumberInput( attrs={ 'class': 'form-control', 'required': True, 'step':'1'} ),
            'precio' : forms.NumberInput( attrs={ 'class': 'form-control', 'placeholder': 'Precio del litro. (En euros)', 'required': False, } ),
            'importe' : forms.NumberInput( attrs={ 'class': 'form-control', 'placeholder': 'Importe resultado de precio x litros. (En euros)', 'required': False, } ),
            'acreedor' : forms.Select( attrs={ 'class': 'form-control','required':True, } ),
            'deudor' : forms.Select( attrs={ 'class': 'selectpicker','required':True, } ),
            #'tipoOperacion' : forms.Select(choices= TIPO_OPERACION_CHOICE), 'required':True,
        }

    def __init__(self, user, *args, **kwargs):
        super(OperacionForm, self).__init__(*args, **kwargs)
        self.fields['acreedor'].queryset = Cuenta.objects.filter(esAcreedor=True)

class ApunteForm(forms.ModelForm):

    class Meta:
        model= Apunte
        fields = ( 'fecha', 'acreedor', 'deudor' , 'importe' ,)
        widgets = {
            'fecha': forms.TextInput( attrs={ 'class': 'form-control', 'type':'date' } ),
        }
    def __init__(self, user, *args, **kwargs):
        super(ApunteForm, self).__init__(*args, **kwargs)
        self.fields['acreedor'].queryset = Cuenta.objects.filter(esAcreedor=True)


    def clean(self):
        cleaned_data = super(ApunteForm, self).clean()
        importe = cleaned_data.get('importe')
        acreedor = cleaned_data.get('acreedor')
        deudor = cleaned_data.get('deudor')
        fecha = cleaned_data.get('fecha')
        if importe <= 0:
            raise ValidationError('Importe no válido')
        if acreedor==deudor:
            raise ValidationError('Acreedor no puede ser tambien Deudor')
        if not fecha:
            raise ValidationError('Fecha no válida')
