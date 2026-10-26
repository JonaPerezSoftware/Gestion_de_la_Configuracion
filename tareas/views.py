from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Count, Q
from .models import Tarea, Categoria
from .forms import TareaForm, CategoriaForm


def lista_tareas(request):
    """Vista principal: listado de tareas con filtros."""
    tareas = Tarea.objects.select_related('categoria').all()

    # Filtros por query params
    estado = request.GET.get('estado')
    prioridad = request.GET.get('prioridad')
    categoria_id = request.GET.get('categoria')
    busqueda = request.GET.get('q')

    if estado:
        tareas = tareas.filter(estado=estado)
    if prioridad:
        tareas = tareas.filter(prioridad=prioridad)
    if categoria_id:
        tareas = tareas.filter(categoria_id=categoria_id)
    if busqueda:
        tareas = tareas.filter(
            Q(titulo__icontains=busqueda) | Q(descripcion__icontains=busqueda)
        )

    # Estadísticas para el dashboard
    total = Tarea.objects.count()
    pendientes = Tarea.objects.filter(estado='pendiente').count()
    en_progreso = Tarea.objects.filter(estado='en_progreso').count()
    completadas = Tarea.objects.filter(estado='completada').count()

    categorias = Categoria.objects.all()

    context = {
        'tareas': tareas,
        'categorias': categorias,
        'total': total,
        'pendientes': pendientes,
        'en_progreso': en_progreso,
        'completadas': completadas,
        'filtro_estado': estado,
        'filtro_prioridad': prioridad,
        'filtro_categoria': categoria_id,
        'busqueda': busqueda or '',
    }
    return render(request, 'tareas/lista_tareas.html', context)


def crear_tarea(request):
    """Crear una nueva tarea."""
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save()
            messages.success(request, f'Tarea "{tarea.titulo}" creada exitosamente.')
            return redirect('lista_tareas')
    else:
        form = TareaForm()
    return render(request, 'tareas/form_tarea.html', {'form': form, 'accion': 'Crear'})


def editar_tarea(request, pk):
    """Editar una tarea existente."""
    tarea = get_object_or_404(Tarea, pk=pk)
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            messages.success(request, f'Tarea "{tarea.titulo}" actualizada.')
            return redirect('lista_tareas')
    else:
        form = TareaForm(instance=tarea)
    return render(request, 'tareas/form_tarea.html', {'form': form, 'accion': 'Editar', 'tarea': tarea})


def eliminar_tarea(request, pk):
    """Eliminar una tarea."""
    tarea = get_object_or_404(Tarea, pk=pk)
    if request.method == 'POST':
        titulo = tarea.titulo
        tarea.delete()
        messages.success(request, f'Tarea "{titulo}" eliminada.')
        return redirect('lista_tareas')
    return render(request, 'tareas/confirmar_eliminar.html', {'tarea': tarea})


def detalle_tarea(request, pk):
    """Ver detalle de una tarea."""
    tarea = get_object_or_404(Tarea, pk=pk)
    return render(request, 'tareas/detalle_tarea.html', {'tarea': tarea})


def toggle_completada(request, pk):
    """Marcar/desmarcar tarea como completada."""
    tarea = get_object_or_404(Tarea, pk=pk)
    if tarea.completada:
        tarea.completada = False
        tarea.estado = Tarea.Estado.PENDIENTE
    else:
        tarea.marcar_completada()
    tarea.save()
    return redirect('lista_tareas')


def lista_categorias(request):
    """Listar y crear categorías."""
    categorias = Categoria.objects.annotate(num_tareas=Count('tareas'))

    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            cat = form.save()
            messages.success(request, f'Categoría "{cat.nombre}" creada.')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()

    return render(request, 'tareas/lista_categorias.html', {
        'categorias': categorias,
        'form': form,
    })
