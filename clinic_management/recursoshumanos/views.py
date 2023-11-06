from django.shortcuts import render,redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required 
from user.forms import RegistroForm
from .models import RegistroAsistencia
from .forms import UsuarioEditForm,RegistroAsistenciaForm
from django.contrib import messages
from user.models import Usuario
from django.contrib.auth import logout
from decorators.custom_decorators import role_required

# Create your views here.

@role_required(['Recursos Humanos','Soporte de Información'])
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, "La cuenta ha sido creada con exito")
            return redirect('registro_usuarios')
        else:
            if 'username' in form.errors:
                messages.error(request, "Nombre de usuario ya existe.")
            elif 'password2' in form.errors:
                messages.error(request, "Contraseña no es suficientemente segura. Prueba agregar todo tipo de caracteres.")
            elif 'email' in form.errors:
                messages.error(request, "Este correo ya existe en la base de datos o no es válido")
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

@role_required(['Recursos Humanos','Soporte de Información'])
def buscar_usuario(request):
    if request.method == 'POST':
        cedula = request.POST.get('numero_identificacion')

        try :
            usuario = Usuario.objects.get(cedula=cedula)

            return redirect('editar_usuario',usuario.id)
        except:
            messages.error(request, "No existe un usuario con esta cedula")
            return redirect('buscar_usuario')

    return render(request, 'busqueda_usuario.html')


@role_required(['Recursos Humanos','Soporte de Información'])
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, instance=usuario)
        if form.is_valid():
            if form.cleaned_data.get('nueva_password'):
                # La contraseña ha sido modificada, cerrar la sesión
                logout(request)
                form.save()
                messages.success(request, 'Usuario actualizado correctamente. Pero debes volver a iniciar sesion')
                return redirect('login_view')
            form.save()
            messages.success(request, 'Usuario actualizado correctamente')
            return redirect('buscar_usuario') 
    else:
        form = UsuarioEditForm(instance=usuario)

    return render(request, 'editar_usuario.html', {'form': form, 'usuario': usuario})

@role_required(['Recursos Humanos','Soporte de Información'])
def registrar_asistencia(request):
    if request.method == 'POST':
        form = RegistroAsistenciaForm(request.POST)
        if form.is_valid():
            
            usuario_cedula = form.cleaned_data['usuario']
            fecha = form.cleaned_data['fecha']

            try:
                usuario = Usuario.objects.get(cedula=usuario_cedula)
            except:
                messages.error(request,'No existe un usuario con esa cedula')
                return redirect('registro_asistencia')
            
            registro = RegistroAsistencia(
                usuario = usuario,
                fecha = fecha
            )

            registro.save()

            messages.success(request,'Asistencia registrada con exito')
            return redirect('registro_asistencia')
            
    else:
        form = RegistroAsistenciaForm()
    return render(request, 'registrar_asistencia.html', {'form': form})