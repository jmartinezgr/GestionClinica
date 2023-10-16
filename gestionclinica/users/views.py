from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Role

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role:
                role_name = user.role.name
                print(role_name)
                if role_name == 'Recursos Humanos':
                    return redirect('recursos_humanos_home')
                elif role_name == 'Personal Administrativo':
                    return redirect('admin_home')
                elif role_name == 'Soporte de Información':
                    return redirect('soporte_info_home')
                elif role_name == 'Enfermera':
                    return redirect('enfermera_home')
                elif role_name == 'Médico':
                    return redirect('medico_home')
                else:
                    return redirect('home')  # Redirección por defecto para otros roles
            else:
                return redirect('home')  # Redirección por defecto si no se ha establecido el rol
        else:
            pass
    return render(request, 'login.html')

@login_required
def admin_home(request):
    user = request.user
    context = {'user': user}
    return render(request, 'admin_home.html', context)
