from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from .forms import CustomAuthenticationForm  # Importa el formulario personalizado
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
                return redirect('adentro')
            else:
                messages.error(request, "Error: Credenciales inválidas. Inténtalo de nuevo.")
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

