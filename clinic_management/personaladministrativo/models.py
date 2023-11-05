from django.db import models
from datetime import date

class Paciente(models.Model):
    numero_identificacion = models.CharField(max_length=10, unique=True)
    nombre_completo = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=10)
    direccion = models.CharField(max_length=200)
    numero_telefono = models.CharField(max_length=10)
    correo_electronico = models.EmailField(blank=True, null=True)

    # Información de contacto de emergencia
    nombre_contacto_emergencia = models.CharField(max_length=200)
    relacion_contacto_emergencia = models.CharField(max_length=50)
    numero_telefono_emergencia = models.CharField(max_length=10)

    # Información de seguro médico
    nombre_compania_seguro = models.CharField(max_length=100)
    numero_poliza_seguro = models.CharField(max_length=50)
    estado_poliza_seguro = models.BooleanField()

    # Agregar un campo para realizar un seguimiento de los copagos totales
    copagos_acumulados = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.nombre_completo

    # Método para calcular el copago y manejar la facturación
    def calcular_copago(self, costo_servicio):
        if self.estado_poliza_seguro:
            if self.copagos_acumulados > 1000000:
                # No se cobra más copago
                copago = 0
            else:
                copago = 50000
                self.copagos_acumulados += copago
        else:
            # Sin seguro o póliza inactiva
            copago = costo_servicio

        self.save()
        return copago
    
    def pago(self):
        self.save()
