# Generated by Django 4.2.7 on 2024-12-31 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alquiler', '0006_saco_reparacion_saco_tintoreria_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pantalon',
            name='reparacion',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pantalon',
            name='tintoreria',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='prenda',
            name='reparacion',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='prenda',
            name='tintoreria',
            field=models.BooleanField(default=False),
        ),
    ]
