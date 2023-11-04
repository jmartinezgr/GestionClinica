from django.db import models
from django.utils import timezone
from personaladministrativo.models import Paciente
from user.models import Usuario

class HistoriaClinica(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    medico = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Cédula del médico
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)  # Cédula del paciente
    motivo_consulta = models.TextField()
    sintomatologia = models.TextField()
    diagnostico = models.TextField()
    ordenes = models.ManyToManyField('Orden', related_name='historias_clinicas')

    def save(self, *args, **kwargs):
        if not self.fecha:
            self.fecha = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Historia Clínica de {self.paciente.nombre_completo} ({self.fecha})'

class Orden(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_solicitud = models.DateTimeField(default=timezone.now)
    TIPOS_ORDEN = (
        ('medicamento', 'Medicamento'),
        ('procedimiento', 'Procedimiento'),
        ('hospitalizacion', 'Hospitalización'),
        ('ayuda_diagnostica', 'Ayuda Diagnóstica'),
    )
    tipo_orden = models.CharField(max_length=20, choices=TIPOS_ORDEN)
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return f'Orden de {self.get_tipo_orden_display()} para {self.paciente.nombre_completo} ({self.fecha_solicitud})'
    
class OrdenMedicamento(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='medicamentos')
    numero_item = models.PositiveIntegerField()  # Número de ítem dentro de la orden
    nombre_medicamento = models.CharField(max_length=200)
    dosis = models.CharField(max_length=50)
    duracion_tratamiento = models.CharField(max_length=50)
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Orden de Medicamento: {self.nombre_medicamento} para {self.orden.paciente.nombre_completo}'

class OrdenProcedimiento(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='procedimientos')
    numero_item = models.PositiveIntegerField()  # Número de ítem dentro de la orden
    nombre_procedimiento = models.CharField(max_length=200)
    numero_veces = models.PositiveIntegerField()
    frecuencia = models.CharField(max_length=50)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    requiere_asistencia_especialista = models.BooleanField()

    def __str__(self):
        return f'Orden de Procedimiento: {self.nombre_procedimiento} para {self.orden.paciente.nombre_completo}'


class OrdenAyudaDiagnostica(models.Model):
    orden = models.ForeignKey(Orden, verbose_name=("Ayuda diagnostica"), on_delete=models.CASCADE)
    nombre_ayuda_diagnostica = models.CharField(max_length=200)
    cantidad = models.IntegerField(verbose_name="cantidad")
    requiere_asistencia_especialista = models.BooleanField()
    finalizado = models.BooleanField(default=False)
    resultados = models.CharField(max_length=2000,blank=True)


