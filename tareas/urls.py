from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_tareas, name='lista_tareas'),
    path('tarea/nueva/', views.crear_tarea, name='crear_tarea'),
    path('tarea/<int:pk>/', views.detalle_tarea, name='detalle_tarea'),
    path('tarea/<int:pk>/editar/', views.editar_tarea, name='editar_tarea'),
    path('tarea/<int:pk>/eliminar/', views.eliminar_tarea, name='eliminar_tarea'),
    path('tarea/<int:pk>/toggle/', views.toggle_completada, name='toggle_completada'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
]
