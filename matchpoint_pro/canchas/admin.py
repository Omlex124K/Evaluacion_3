from django.contrib import admin
from .models import Disciplina, Cancha

admin.site.site_header = 'MatchPoint Pro - Panel de Control'
admin.site.site_title = 'MatchPoint Pro Admin'
admin.site.index_title = 'Gestión Operativa de Recursos y Servicios'

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Cancha)
class CanchaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'disciplina', 'superficie', 'tarifa_bloque', 'estado', 'activo')
    list_editable = ('estado', 'activo')
    list_filter = ('disciplina', 'estado', 'activo')
    search_fields = ('codigo', 'nombre', 'superficie')
    
    # Estructura modular del formulario en secciones lógicas temáticas
    fieldsets = (
        ('Identificación Básica', {
            'fields': ('codigo', 'nombre', 'disciplina')
        }),
        ('Características y Costos', {
            'fields': ('superficie', 'tarifa_bloque', 'imagen')
        }),
        ('Control de Estado y Vigencia', {
            'fields': ('estado', 'activo')
        }),
    )
