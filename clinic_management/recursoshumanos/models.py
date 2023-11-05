from django.db import models
from user.models import Usuario

class RegistroAsistencia(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateField()
    asistencia = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.fecha} ({self.asistencia})'
    
