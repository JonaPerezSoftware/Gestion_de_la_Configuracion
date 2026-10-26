from django.db import models
from django.utils import timezone


class Categoria(models.Model):
    """Categoría para agrupar tareas."""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, default='')
    color = models.CharField(
        max_length=7,
        default='#3B82F6',
        help_text='Color en formato hexadecimal, ej: #3B82F6'
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Tarea(models.Model):
    """Modelo principal de tarea."""

    class Prioridad(models.TextChoices):
        BAJA = 'baja', 'Baja'
        MEDIA = 'media', 'Media'
        ALTA = 'alta', 'Alta'
        URGENTE = 'urgente', 'Urgente'

    class Estado(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        EN_PROGRESO = 'en_progreso', 'En Progreso'
        COMPLETADA = 'completada', 'Completada'
        CANCELADA = 'cancelada', 'Cancelada'

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, default='')
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tareas'
    )
    prioridad = models.CharField(
        max_length=10,
        choices=Prioridad.choices,
        default=Prioridad.MEDIA
    )
    estado = models.CharField(
        max_length=15,
        choices=Estado.choices,
        default=Estado.PENDIENTE
    )
    fecha_vencimiento = models.DateField(null=True, blank=True)
    completada = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering = ['-creado_en']

    def __str__(self):
        return self.titulo

    @property
    def esta_vencida(self):
        """Retorna True si la tarea está vencida."""
        if self.fecha_vencimiento and not self.completada:
            return self.fecha_vencimiento < timezone.now().date()
        return False

    def marcar_completada(self):
        """Marca la tarea como completada."""
        self.completada = True
        self.estado = self.Estado.COMPLETADA
        self.save()
