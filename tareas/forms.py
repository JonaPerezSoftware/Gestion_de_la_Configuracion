from django import forms
from .models import Tarea, Categoria


class TareaForm(forms.ModelForm):
    """Formulario para crear y editar tareas."""

    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'categoria', 'prioridad', 'estado', 'fecha_vencimiento']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la tarea'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción detallada...'
            }),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'prioridad': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'fecha_vencimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }


class CategoriaForm(forms.ModelForm):
    """Formulario para crear categorías."""

    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'color']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la categoría'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de la categoría...'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color'
            }),
        }
