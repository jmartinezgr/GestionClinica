from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password

class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, nombre, cedula, nacimiento, direccion, telefono, rol, password=None):
        if not email:
            raise ValueError("El campo de correo electrónico es obligatorio.")

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            nombre=nombre,
            cedula=cedula,
            nacimiento=nacimiento,
            direccion=direccion,
            telefono=telefono,
            rol=rol,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, nombre, cedula, telefono='', password=None):
        user = self.create_user(
            username=username,
            email=email,
            nombre=nombre,
            cedula=cedula,
            telefono=telefono,  # Añadir el telefono aquí (con un valor predeterminado opcional)
            nacimiento="2000-01-01",  # Proporciona un valor por defecto
            direccion="",  # Proporciona un valor por defecto para otros campos requeridos
            rol=None,  # Proporciona un valor por defecto para otros campos requeridos
            password=password,
        )
        user.usuario_administrador = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Nombre de usuario', unique=True, max_length=100)
    email = models.EmailField('Correo Electronico', max_length=254, unique=True)
    cedula = models.CharField('Cedula de Ciudadania',unique=True,max_length=10,default="111111111")
    nombre = models.CharField('Nombres', max_length=200, blank=True)
    nacimiento = models.DateField(default="2000-01-01",null=True)
    direccion = models.CharField('Direccion', max_length=30, blank=True)
    telefono = models.CharField('Numero de Telefono',max_length=10, blank=True)
    rol = models.ForeignKey("user.Role", verbose_name=("Rol Laboral"), on_delete=models.CASCADE,default=1,null=True)
    usuario_activo = models.BooleanField(default=True)
    usuario_administrador = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nombre','cedula']

    def __str__(self):
        return f'Usuario: {self.nombre}'

    def has_perm(self, perm, obj=None):
        return self.usuario_administrador

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_administrador
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
