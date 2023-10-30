import os
import django

# Establece la configuración de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clinic_management.settings")
django.setup()

from user.models import Role

def create_roles():
    roles_data = [
        {"name": "Recursos Humanos"},
        {"name": "Personal Administrativo"},
        {"name": "Soporte de Información"},
        {"name": "Enfermeras"},
        {"name": "Médicos"},
    ]

    for role_info in roles_data:
        role, created = Role.objects.get_or_create(**role_info)
        if created:
            print(f"Role '{role.name}' creado con éxito.")
        else:
            print(f"Role '{role.name}' ya existe en la base de datos.")

if __name__ == "__main__":
    create_roles()
