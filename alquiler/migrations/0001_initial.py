# Generated by Django 4.2.7 on 2024-11-25 21:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Localidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('provincia', models.CharField(max_length=20, verbose_name='Provincia')),
            ],
        ),
        migrations.CreateModel(
            name='Prenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('busto', models.IntegerField(blank=True, null=True)),
                ('cintura', models.IntegerField(blank=True, null=True)),
                ('cadera', models.IntegerField(blank=True, null=True)),
                ('talle', models.CharField(blank=True, max_length=20, null=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alquiler.categoria')),
            ],
            options={
                'verbose_name': 'prenda',
                'verbose_name_plural': 'prendas',
                'db_table': 'prenda',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.CharField(blank=True, max_length=8, null=True, unique=True, verbose_name='DNI')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=50, verbose_name='Apellido')),
                ('telefono', models.CharField(blank=True, max_length=12, verbose_name='Teléfono')),
                ('direccion', models.CharField(blank=True, max_length=50, verbose_name='Dirección')),
                ('genero', models.CharField(choices=[('F', 'Femenino'), ('M', 'Masculino'), ('O', 'Otro')], default='F', max_length=1)),
                ('observacion', models.CharField(blank=True, max_length=400, verbose_name='Observación')),
                ('localidad', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Localidad', to='alquiler.localidad')),
            ],
            options={
                'verbose_name': 'cliente',
                'verbose_name_plural': 'Clientes',
                'db_table': 'cliente',
            },
        ),
        migrations.CreateModel(
            name='Alquiler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_alquiler', models.DateField(auto_now_add=True)),
                ('fecha_devolucion', models.DateField()),
                ('precio_alquiler', models.DecimalField(decimal_places=2, max_digits=10)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('alquilado', 'Alquilado'), ('devuelto', 'Devuelto')], default='pendiente', max_length=20)),
                ('seña', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alquileres', to='alquiler.cliente')),
                ('prenda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alquileres', to='alquiler.prenda')),
            ],
            options={
                'verbose_name': 'alquiler',
                'verbose_name_plural': 'alquileres',
                'db_table': 'alquiler',
            },
        ),
    ]
