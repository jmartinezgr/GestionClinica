from django.contrib import admin
from .models import CustomUser,Role  # Asegúrate de importar tu modelo

admin.site.register(CustomUser)  # Registra el modelo en la interfaz de administración
admin.site.register(Role)