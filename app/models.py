from itertools import cycle
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
import re


#Validacion Rut:
def validate_rut(value):
    # Expresión regular para el formato del RUT
    rut_regex = re.compile(r'^\d{1,2}\d{3}\d{3}-[\dkK]$')
    if not rut_regex.match(value):
        raise ValidationError('El RUT debe tener el formato XXXXXXXXX-X')
    
    # Separar el número del dígito verificador
    rut_body, dv = value.split('-')
    rut_body = int(rut_body)
    
    # Calcular el dígito verificador
    reversed_digits = map(int, reversed(str(rut_body)))
    factors = cycle(range(2, 8))
    checksum = sum(d * f for d, f in zip(reversed_digits, factors))
    calculated_dv = (-checksum) % 11
    if calculated_dv == 10:
        calculated_dv = 'K'
    else:
        calculated_dv = str(calculated_dv)
    
    if dv.upper() != calculated_dv:
        raise ValidationError('El RUT no es válido')

#manager personalizado que maneje la creación de usuarios y superusuarios
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# Create your models here.

#Usuario personalizado
class Usuario(AbstractUser):
    TIPO_USER_CHOICES = [
        ('CLINICO', 'CLINICO'),
        ('ADMINISTRADOR', 'ADMINISTRADOR'),
    ]
    email = models.EmailField(max_length=254, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'rut']
    rut = models.CharField(max_length=12, validators=[validate_rut])
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USER_CHOICES, null=False, blank=False, default='CLINICO')

    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.rut}"

# Modelo Cama
class Cama():
    cama = models.CharField(max_length=7, verbose_name="Cama")
    unidad = models.TextField(verbose_name="Unidad")

    def __str__(self):
        return f"{self.cama, self.unidad}"

# Modelo Paciente
class Paciente():
    nombre = models.TextField(verbose_name="Nombre Paciente", )
    apellido = models.TextField(verbose_name="Apellido Paciente",)
    rut = models.CharField(max_length=12, validators=[validate_rut])
    id_cama = models.ForeignKey(Cama, on_delete=models.CASCADE, verbose_name='ID_Cama')

    def __str__(self):
        return f"{self.nombre, self.apellido}"

# Modelo Formulario
class Form_Score():
    TIPO_o2suple = [
        ('SI', 'SI'),
        ('NO', 'NO'),
    ]

    TIPO_nivConc = [
        ('ALERTA', 'Alerta'),
        ('COMPROMISO_CONCIENCIA_O_AGITACION', 'Compromiso Conciencia o Agitación'),
    ]
    

    fr = models.IntegerField(verbose_name="Frec. Respiratorio", null=False, blank=False)
    o2suple =models.CharField(max_length=2, choices=TIPO_o2suple, null=False, blank=False, default='NO',verbose_name="Oxigeno Suplementario")
    temp = models.FloatField(verbose_name="Temperatura", null=False, blank=False)
    prArtSis = models.IntegerField(verbose_name="Presion Art. Sistolica", null=False, blank=False)
    frCard = models.IntegerField(verbose_name="Frec. Cardiaca", null=False, blank=False)
    nivConc = models.CharField(max_length=30, choices=TIPO_o2suple, null=False, blank=False, default='Alerta',verbose_name="Nivel Conciencia")
    score = models.TextField(verbose_name="Score Obtenido", null=False, blank=False)
    fecha = models.DateField(verbose_name="Fecha Registro", auto_now=True, auto_now_add=True)
    hora = models.TimeField(verbose_name="Hora Registro", auto_now=True, auto_now_add=True)
    id_Paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, verbose_name='ID_Paciente')
    id_user = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='ID_Usuario')

    def __str__(self):
        return self.score