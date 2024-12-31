# Generated by Django 4.2.7 on 2024-12-31 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alquiler', '0005_alter_alquiler_seña'),
    ]

    operations = [
        migrations.AddField(
            model_name='saco',
            name='reparacion',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='saco',
            name='tintoreria',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='alquiler',
            name='estado',
            field=models.CharField(choices=[('reservado', 'Reservado'), ('alquilado', 'Alquilado')], default='reservado', max_length=20),
        ),
        migrations.AlterField(
            model_name='alquiler',
            name='seña',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10),
        ),
    ]
