# Generated by Django 5.1.6 on 2025-02-17 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alquiler', '0008_alter_alquiler_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='traje',
            name='prendas',
            field=models.ManyToManyField(blank=True, related_name='trajes', to='alquiler.prenda'),
        ),
    ]
