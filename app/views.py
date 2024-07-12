from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import *
from .forms import *

# Create your views here.

#Index
def index(request):
    return render(request,'index.html', {})

#Formulario de Contacto
def formulario_contacto(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Su mensaje fue enviado con exito')
            return redirect('indice')
    else:
        form = ContactForm()
    return render(request, 'registration/contacto.html', {'form': form})

#Formulario de registro
def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            email = user_creation_form.cleaned_data.get('email')
            password = user_creation_form.cleaned_data.get('password1')
            usuario = authenticate(request, email=email, password=password)
            if usuario is not None:
                login(request, usuario)
                return redirect('indice')
        else:
            data['form'] = user_creation_form

    return render(request, 'registration/register.html', data)

#Actualizar Usuario
@login_required
def editar_usuario(request):
    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('agendas')
    else:
        form = UsuarioEditForm(instance=request.user)

    return render(request, 'registration/editar_usuario.html', {'form': form})

#Actualizar Contrasena
@login_required
def cambiar_contrasena(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantener al usuario autenticado después de cambiar la contraseña
            messages.success(request, '¡Tu contraseña ha sido cambiada exitosamente!')
            return redirect('agendas')  # Redirige a una página de perfil u otra página relevante
        else:
            messages.error(request, 'Por favor corrige los errores a continuación.')
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'registration/cambiar_contrasena.html', {'form': form})

#Formulario Nueva Agenda
@login_required
def create_agenda(request):
    if request.method == 'POST':
        form = AgendaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_agenda')
    else:
        form = AgendaForm()
    return render(request, 'agenda_nueva.html', {'form': form})


@login_required
def reservar_agenda(request, agenda_id):
    agenda = get_object_or_404(Agenda, pk=agenda_id)
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.agenda_id = agenda
            reserva.usuario_id = request.user
            reserva.save()
            agenda.reservada = True
            agenda.save()
            return redirect('listar_agendas')
    else:
        form = ReservaForm()
    return render(request, 'agenda_reserva.html', {'form': form, 'agenda': agenda})

#Listados de agenda
@login_required
def listar_agendas(request):
    tabla_agenda = Agenda.objects.all()
    especialista = Especialista.objects.all()
    centro_medico = CentroMedico.objects.all()

    # Obtener parámetros de filtro
    nombre_medico = request.GET.get('nombre_medico', '')
    especialidad = request.GET.get('especialidad', '')
    centro_medico = request.GET.get('centro_medico', '')
    fecha = request.GET.get('fecha', '')
    hora = request.GET.get('hora', '')

    # Construir el filtro
    filters = Q()
    if nombre_medico:
        filters &= Q(especialista_id__nombre__icontains=nombre_medico)
    if especialidad:
        filters &= Q(especialista_id__especialidad__icontains=especialidad)
    if centro_medico:
        filters &= Q(centro_medico_id__nombre__icontains=centro_medico)
    if fecha:
        filters &= Q(fecha_disponible=fecha)
    if hora:
        filters &= Q(hora_disponible=hora)

    # Obtener y filtrar las agendas
    agendas = Agenda.objects.filter(filters)

    # Paginación
    paginator = Paginator(agendas, 10)  # Mostrar 10 citas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pasar datos al template
    return render(request, 'agenda_lista.html', {
        'agendas': tabla_agenda, 'especialistas': especialista, 'centros_medicos': centro_medico,
        'page_obj': page_obj,
        'nombre_medico': nombre_medico,
        'especialidad': especialidad,
        'fecha': fecha,
        'hora': hora,
        'centro_medico': centro_medico,
    })

#Editar Agenda
@login_required
def editar_agenda(request, agenda_id):
    agenda = get_object_or_404(Agenda, id=agenda_id)
    if request.method == 'POST':
        form = AgendaForm(request.POST, instance=agenda)
        if form.is_valid():
            form.save()
            return redirect('listar_agendas')
    else:
        form = AgendaForm(instance=agenda)
    
    return render(request, 'registration/agenda_editar.html', {'form': form, 'agenda': agenda})

#Eliminar Agenda
@login_required
def eliminar_agenda(request, agenda_id):
    agenda = get_object_or_404(Agenda, id=agenda_id)
    if request.method == 'POST':
        agenda.delete()
        return redirect('listar_agendas')
    
    return render(request, 'registration/agenda_eliminar.html', {'agenda': agenda})

#Citas revervadas por pacientes
@login_required
def citas_reservadas(request):
    # Obtener las citas del usuario autenticado
    usuario = request.user
    if usuario.tipo_usuario == 'PACIENTE':
        citas = Cita.objects.filter(usuario_id=usuario)
    else:
        citas = Cita.objects.none()  # No devolver citas si el usuario no es un paciente

    return render(request, 'citas_reservadas.html', {'citas': citas})

#Editar cita
@login_required
def editar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, usuario_id=request.user)
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            return redirect('citas_reservadas')
    else:
        form = CitaForm(instance=cita)
    
    return render(request, 'registration/editar_cita.html', {'form': form, 'cita': cita})

#Eliminar Cita desde paciente
@login_required
def eliminar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, usuario_id=request.user)
    if request.method == 'POST':
        cita.delete()
        return redirect('citas_reservadas')
    
    return render(request, 'registration/eliminar_cita.html', {'cita': cita})