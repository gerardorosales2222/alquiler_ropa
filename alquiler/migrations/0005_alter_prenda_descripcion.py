# Generated by Django 5.0 on 2024-11-29 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alquiler', '0004_alter_prenda_nro_articulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prenda',
            name='descripcion',
            field=models.TextField(blank=True, max_length=20, null=True),
        ),
    ]
