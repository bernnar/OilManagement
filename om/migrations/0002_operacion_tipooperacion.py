# Generated by Django 2.0.3 on 2018-03-18 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('om', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='operacion',
            name='tipoOperacion',
            field=models.CharField(choices=[('S', 'Salida'), ('E', 'Entrada')], default='S', max_length=2),
        ),
    ]
