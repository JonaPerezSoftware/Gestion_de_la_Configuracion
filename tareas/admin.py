from django.contrib import admin
from .models import Categoria, Tarea


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'color', 'creado_en')
    search_fields = ('nombre',)


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'prioridad', 'estado', 'completada', 'fecha_vencimiento')
    list_filter = ('estado', 'prioridad', 'completada', 'categoria')
    search_fields = ('titulo', 'descripcion')
    list_editable = ('estado', 'completada')
    date_hierarchy = 'creado_en'
