# Generated by Django 2.0.3 on 2018-03-19 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('om', '0002_operacion_tipooperacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apunte',
            name='cuenta',
        ),
        migrations.RemoveField(
            model_name='operacion',
            name='cuenta',
        ),
        migrations.AddField(
            model_name='apunte',
            name='acreedor',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='Apunte_request_acreedor', to='om.Cuenta'),
        ),
        migrations.AddField(
            model_name='apunte',
            name='deudor',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='Apunte_request_deudor', to='om.Cuenta'),
        ),
        migrations.AddField(
            model_name='operacion',
            name='acreedor',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='Operacion_request_acreedor', to='om.Cuenta'),
        ),
        migrations.AddField(
            model_name='operacion',
            name='deudor',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='Operacion_request_deudor', to='om.Cuenta'),
        ),
        migrations.AlterField(
            model_name='operacion',
            name='conductor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='om.Conductor'),
        ),
        migrations.AlterField(
            model_name='operacion',
            name='vehiculo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='om.Vehiculo'),
        ),
    ]
