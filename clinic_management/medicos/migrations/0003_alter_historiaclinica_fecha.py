# Generated by Django 4.1.12 on 2023-11-05 06:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('medicos', '0002_historiaclinica_cerrada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historiaclinica',
            name='fecha',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
