# Generated by Django 4.1.12 on 2023-11-06 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enfermeras', '0002_visitas_informacion_adicional'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitas',
            name='fecha_realizacion',
            field=models.DateTimeField(null=True),
        ),
    ]
