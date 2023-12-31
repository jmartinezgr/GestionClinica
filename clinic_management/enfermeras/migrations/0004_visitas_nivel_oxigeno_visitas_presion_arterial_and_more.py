# Generated by Django 4.1.12 on 2023-11-13 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enfermeras', '0003_visitas_fecha_realizacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitas',
            name='nivel_oxigeno',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='visitas',
            name='presion_arterial',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='visitas',
            name='pulso',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='visitas',
            name='temperatura',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
