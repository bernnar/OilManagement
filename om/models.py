from django.db import models
from django.utils import timezone
from decimal import Decimal
from .models import *
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db.models import F
from datetime import date

#import django_tables2 as tables

class Deposito(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    nombre = models.CharField(max_length=60)
    capacidad = models.IntegerField(default=0)
    cantidad = models.DecimalField(max_digits=8, decimal_places=5,default=Decimal('0.000'))

    def __str__(self):
        return self.nombre

class Cuenta(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    nombre = models.CharField(max_length=60)
    saldo = models.DecimalField(max_digits=8, decimal_places=2,default=Decimal('0.00'))
    esAcreedor = models.BooleanField(default=False, verbose_name='Es Acreedor')

    def __str__(self):
        return self.nombre

class Vehiculo(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    nombre = models.CharField(max_length=60)
    exigirKm = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Conductor(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    nombre = models.CharField(max_length=60)

    def __str__(self):
        return self.nombre

class Operacion(models.Model):
    SALIDA = 'S'
    ENTRADA= 'E'
    TIPO_OPERACION_CHOICE = (
        (SALIDA, 'Salida'),
        (ENTRADA, 'Entrada')
    )
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    fecha = models.DateField(_("Fecha"), default=date.today)
    litros = models.DecimalField(max_digits=8, decimal_places=3,default=Decimal('0.000'))
    precio = models.DecimalField(max_digits=8, decimal_places=3,default=Decimal('0.000'))
    importe = models.DecimalField(max_digits=8, decimal_places=2,default=Decimal('0.00'))
    acreedor = models.ForeignKey('cuenta',  on_delete=models.CASCADE, related_name='Operacion_request_acreedor', default=0)
    deudor = models.ForeignKey('cuenta',  on_delete=models.CASCADE, related_name='Operacion_request_deudor', default=0)
    deposito = models.ForeignKey('deposito',on_delete=models.CASCADE)
    vehiculo= models.ForeignKey('vehiculo', on_delete=models.CASCADE, blank=True, null=True)
    conductor = models.ForeignKey('conductor', on_delete=models.CASCADE, blank=True, null=True)
    vehiculoKm  = models.IntegerField(blank=True, null=True, verbose_name="Km.Vehiculo")
    tipoOperacion = models.CharField(
        max_length=2,
        choices=TIPO_OPERACION_CHOICE,
        default=SALIDA,
    )

    def clean_litros(self):
        data = self.cleaned_data['litros']
        if data <= 0:
            raise ValidationError(_('Cantidad de litros no válida.'))
        return data

    def crean_precio(self):
        data = self.cleaned_data['precio']
        if data <= 0:
            raise ValidationError(_('Precio/litro no válido.'))

    def save(self, *args, **kwargs):
        #Operacion
        if self.tipoOperacion== 'S':
            print(self.fecha)
            lastOp = Operacion.objects.filter(fecha__lte = self.fecha).order_by('-fecha').first()
            self.precio = lastOp.precio
        self.importe = round((self.litros * self.precio),2)
        super(Operacion, self).save(*args, **kwargs)

        #Deposito cantidad
        currentDeposito = Deposito.objects.filter(pk=self.deposito_id).first()
        if self.tipoOperacion== 'S':
            currentDeposito.cantidad = currentDeposito.cantidad - self.litros
        if self.tipoOperacion == 'E':
            currentDeposito.cantidad = currentDeposito.cantidad + self.litros
        currentDeposito.save()

        #Apunte
        ctaAcreedor=Cuenta.objects.filter(pk=self.acreedor_id).first()
        ctaDeudor = Cuenta.objects.filter(pk=self.deudor_id).first()
        ap = Apunte(user=self.user, created_date=timezone.now(), acreedor = ctaAcreedor, deudor=ctaDeudor, fecha=self.fecha, motivo='DEUDA', importe=self.importe)
        ap.save()

class Apunte(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    acreedor = models.ForeignKey('cuenta',  on_delete=models.CASCADE, related_name='Apunte_request_acreedor', default=0)
    deudor = models.ForeignKey('cuenta',  on_delete=models.CASCADE, related_name='Apunte_request_deudor', default=0)
    fecha = models.DateField(_("Date"), default=date.today)
    motivo = models.CharField(max_length=60)
    importe = models.DecimalField(max_digits=8, decimal_places=2,default=Decimal('0.00'))



    #Update saldos de ctas.
    def save(self, *args, **kwargs):
        ctaAcreedor=Cuenta.objects.filter(pk=self.acreedor_id).first()
        ctaAcreedor.saldo = ctaAcreedor.saldo + self.importe
        ctaDeudor = Cuenta.objects.filter(pk=self.deudor_id).first()
        ctaDeudor.saldo = ctaDeudor.saldo - self.importe
        ctaAcreedor.save()
        ctaDeudor.save()
        super(Apunte, self).save(*args, **kwargs)









#class CombustibleTable(tables.Table):
#    class Meta:
#        model = Salida
#        template_name = 'django_tables2/bootstrap.html'
#        fields = ('fecha', 'precio', 'importe', 'litros', 'cuenta', 'vehiculo', 'conductor')
#        #attrs = {"class": "table-striped table-bordered"}
#        empty_text = "Sin resultados..."
