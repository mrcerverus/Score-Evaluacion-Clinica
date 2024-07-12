from django.contrib import admin
from app.models import *
from django.contrib.auth.admin import UserAdmin

admin.site.site_header = 'Administracion Score'
admin.site.index_title = 'Panel De Control'
admin.site.site_title = 'Score Clinico'

class UserAdmin(UserAdmin):
    resource_class = Usuario
    list_display = ['username','email','rut','first_name','last_name', 'tipo_usuario']
    fieldsets = UserAdmin.fieldsets + (
        ('Datos', {'fields': ('rut', 'tipo_usuario')}),
    )


# Register your models here.

admin.site.register(Usuario, UserAdmin)
admin.site.register(Cama)
admin.site.register(Paciente)
admin.site.register(Form_Score)
