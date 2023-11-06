# custom_decorators.py
from functools import wraps
from django.http import HttpResponseForbidden

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def check_role(request, *args, **kwargs):
            if request.user.is_authenticated:
                user_role = request.user.rol  # Asume que tienes un atributo 'rol' en tu modelo de usuario
                if user_role.name in allowed_roles:  # Suponiendo que 'name' es el campo que almacena el nombre del rol en el modelo 'Role'
                    return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        return check_role
    return decorator
