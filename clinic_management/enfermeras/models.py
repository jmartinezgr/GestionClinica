from django.db import models
from medicos.models import Orden, Paciente
from django.utils import timezone

class Hospitalizacion(models.Model):
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE, related_name='hospitalizacion')
    tiempo = models.PositiveIntegerField(help_text='Tiempo en días')
    cantidad_visitas_dia = models.PositiveIntegerField(default=1)
    visitas = models.IntegerField(default=0)
    estado = models.BooleanField(default=False)

    def agregar_visita(self):
        self.visitas+=1

        if self.visitas == self.tiempo*self.cantidad_visitas_dia:
            self.estado= True

            self.save()

            return False
        return True

    def __str__(self):
        return f'Hospitalización para Orden #{self.orden.id}'

class Visitas(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='paciente_hospitalizado')
    fecha = models.DateTimeField(default=timezone.now)
    orden_hospitalizacion = models.ForeignKey(Hospitalizacion,on_delete=models.CASCADE, related_name='orden_de_hospitalizacion')
    estado = models.BooleanField(default=False)
    fecha_realizacion = models.DateTimeField(null=True)
    informacion_adicional = models.TextField(max_length=2000,blank=True)
    temperatura = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    pulso = models.PositiveIntegerField(null=True, blank=True)
    nivel_oxigeno = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    presion_arterial = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'Visita de {self.paciente} el {self.fecha}'
