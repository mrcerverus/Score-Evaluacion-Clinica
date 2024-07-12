from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


#Formulario Creacion de Usuario
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = [
            'email',
            'password1',
            'password2',
            'rut',
            'first_name',
            'last_name',
            ]
        
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Enviar'))
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if not user.username:
            user.username = user.email
        if commit:
            user.save()
        return user

#Formulario edicion de usuario
class UsuarioEditForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'direccion', 'telefono']

    def __init__(self, *args, **kwargs):
        super(UsuarioEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar cambios'))
        if 'password' in self.fields:
            del self.fields['password']

#Formulario cambio de password
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Cambiar Contraseña'))

#Formulario Cita
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['mensaje']
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Reservar'))

#Formulario Nueva Agenda
class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = ['fecha_disponible', 'hora_disponible', 'especialista_id', 'centro_medico_id']
        widgets = {
            'fecha_disponible': forms.DateInput(attrs={'type': 'date'}),
            'hora_disponible': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Crear Agenda'))

#Editar Agenda
class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = ['fecha_disponible', 'hora_disponible', 'especialista_id', 'centro_medico_id']
        widgets = {
            'fecha_disponible': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_disponible': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'especialista_id': forms.Select(attrs={'class': 'form-control'}),
            'centro_medico_id': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Editar Agenda'))

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['mensaje']
        widgets = {
            'mensaje': forms.Textarea(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Editar Agenda'))