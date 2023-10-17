from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
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
                return redirect('home')
            else:
                messages.error(request, "Error: Credenciales inválidas. Inténtalo de nuevo.")
                return redirect('login_view')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Tu cuenta ha sido creada. Ahora puedes iniciar sesión.")
            return redirect('login_view')  # Puedes redirigir a la página de inicio de sesión o donde lo necesites
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})