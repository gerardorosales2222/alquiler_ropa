# Generated by Django 4.2.7 on 2024-11-25 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alquiler', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoria',
            options={'verbose_name': 'categiria', 'verbose_name_plural': 'categorias'},
        ),
        migrations.AlterModelOptions(
            name='localidad',
            options={'verbose_name': 'localidad', 'verbose_name_plural': 'localidades'},
        ),
        migrations.AlterModelTable(
            name='categoria',
            table='categoria',
        ),
        migrations.AlterModelTable(
            name='localidad',
            table='localidad',
        ),
    ]
