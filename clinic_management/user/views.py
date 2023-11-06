from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required   
from .forms import CustomAuthenticationForm,RegistroForm  # Importa el formulario personalizado
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                if user.rol is None:
                    return redirect('home_recursos_humanos')
                elif user.rol.name == 'Enfermeras':
                    return redirect('home_enfermeras')
                elif user.rol.name == 'Recursos Humanos':
                    return redirect('home_recursos_humanos')
                elif user.rol.name == 'Personal Administrativo':
                    return redirect('home_personal_administrativo')
                elif user.rol.name == 'Médicos':
                    return redirect('home_medicos')
                elif user.rol.name == 'Soporte de Información':
                    return redirect('home_recursos_humanos')
                print(user.rol.name)                
            else:
                messages.error(request, "Error: Credenciales inválidas. Inténtalo de nuevo.")
                return redirect('login_view')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request=request)
    return redirect('login_view')