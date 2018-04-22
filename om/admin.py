from django.contrib import admin
from .models import Vehiculo, Cuenta, Deposito, Conductor, Operacion

admin.site.register(Vehiculo)
admin.site.register(Cuenta)
admin.site.register(Deposito)
admin.site.register(Conductor)
admin.site.register(Operacion)
