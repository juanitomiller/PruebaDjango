# Generated by Django 5.0.7 on 2024-07-17 05:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0004_carrito_userprofile_delete_itemcarrito'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='fecha_creacion',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='producto',
            name='sexo',
            field=models.CharField(choices=[('Femenino', 'Femenino'), ('Masculino', 'Masculino'), ('Unisex', 'Unisex')], default='Unisex', max_length=10),
        ),
    ]