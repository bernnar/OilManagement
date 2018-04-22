import django_tables2 as tables
from .models import Cuenta, Operacion

class CuentaTable(tables.Table):
    class Meta:
        model = Cuenta
        template_name = 'django_tables2/bootstrap.html'
        fields = ('nombre', 'saldo')

class OperacionTable(tables.Table):
    class Meta:
        model = Operacion
        template_name = 'django_tables2/bootstrap.html'
        fields = ('fecha' ,'litros' , 'precio' ,'importe' ,'acreedor' ,'deudor', 'deposito' , 'vehiculo' ,'conductor', 'vehiculoKm')
