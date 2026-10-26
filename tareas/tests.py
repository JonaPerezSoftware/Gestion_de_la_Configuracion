from datetime import date, timedelta
from django.test import TestCase, Client
from django.urls import reverse
from .models import Tarea, Categoria
from .forms import TareaForm, CategoriaForm


class CategoriaModelTest(TestCase):
    """Tests para el modelo Categoria."""

    def test_crear_categoria(self):
        """Debe crear una categoría correctamente."""
        cat = Categoria.objects.create(nombre='Trabajo', color='#EF4444')
        self.assertEqual(cat.nombre, 'Trabajo')
        self.assertEqual(cat.color, '#EF4444')
        self.assertEqual(str(cat), 'Trabajo')

    def test_categoria_nombre_unico(self):
        """No debe permitir nombres duplicados."""
        Categoria.objects.create(nombre='Personal')
        with self.assertRaises(Exception):
            Categoria.objects.create(nombre='Personal')

    def test_categoria_str(self):
        """__str__ debe retornar el nombre."""
        cat = Categoria.objects.create(nombre='Estudio')
        self.assertEqual(str(cat), 'Estudio')


class TareaModelTest(TestCase):
    """Tests para el modelo Tarea."""

    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='General')
        self.tarea = Tarea.objects.create(
            titulo='Tarea de prueba',
            descripcion='Descripción de prueba',
            categoria=self.categoria,
            prioridad=Tarea.Prioridad.MEDIA,
            estado=Tarea.Estado.PENDIENTE,
        )

    def test_crear_tarea(self):
        """Debe crear una tarea correctamente."""
        self.assertEqual(self.tarea.titulo, 'Tarea de prueba')
        self.assertEqual(self.tarea.prioridad, 'media')
        self.assertEqual(self.tarea.estado, 'pendiente')
        self.assertFalse(self.tarea.completada)

    def test_tarea_str(self):
        """__str__ debe retornar el título."""
        self.assertEqual(str(self.tarea), 'Tarea de prueba')

    def test_marcar_completada(self):
        """Debe marcar la tarea como completada y cambiar el estado."""
        self.tarea.marcar_completada()
        self.tarea.refresh_from_db()
        self.assertTrue(self.tarea.completada)
        self.assertEqual(self.tarea.estado, Tarea.Estado.COMPLETADA)

    def test_esta_vencida_true(self):
        """Debe retornar True si la tarea está vencida."""
        self.tarea.fecha_vencimiento = date.today() - timedelta(days=1)
        self.tarea.save()
        self.assertTrue(self.tarea.esta_vencida)

    def test_esta_vencida_false(self):
        """Debe retornar False si la tarea no está vencida."""
        self.tarea.fecha_vencimiento = date.today() + timedelta(days=7)
        self.tarea.save()
        self.assertFalse(self.tarea.esta_vencida)

    def test_esta_vencida_completada(self):
        """No debe estar vencida si ya fue completada."""
        self.tarea.fecha_vencimiento = date.today() - timedelta(days=1)
        self.tarea.completada = True
        self.tarea.save()
        self.assertFalse(self.tarea.esta_vencida)

    def test_prioridades_validas(self):
        """Debe aceptar todas las prioridades definidas."""
        for prioridad_value, _ in Tarea.Prioridad.choices:
            tarea = Tarea.objects.create(
                titulo=f'Tarea {prioridad_value}',
                prioridad=prioridad_value,
            )
            self.assertEqual(tarea.prioridad, prioridad_value)

    def test_estados_validos(self):
        """Debe aceptar todos los estados definidos."""
        for estado_value, _ in Tarea.Estado.choices:
            tarea = Tarea.objects.create(
                titulo=f'Tarea estado {estado_value}',
                estado=estado_value,
            )
            self.assertEqual(tarea.estado, estado_value)


class TareaFormTest(TestCase):
    """Tests para el formulario TareaForm."""

    def test_form_valido(self):
        """Debe aceptar datos válidos."""
        data = {
            'titulo': 'Nueva tarea',
            'descripcion': 'Descripción',
            'prioridad': 'media',
            'estado': 'pendiente',
        }
        form = TareaForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_titulo_requerido(self):
        """El título es obligatorio."""
        form = TareaForm(data={'descripcion': 'Sin título'})
        self.assertFalse(form.is_valid())
        self.assertIn('titulo', form.errors)

    def test_form_con_categoria(self):
        """Debe aceptar una categoría válida."""
        cat = Categoria.objects.create(nombre='Dev')
        data = {
            'titulo': 'Con categoría',
            'categoria': cat.pk,
            'prioridad': 'alta',
            'estado': 'pendiente',
        }
        form = TareaForm(data=data)
        self.assertTrue(form.is_valid())


class CategoriaFormTest(TestCase):
    """Tests para el formulario CategoriaForm."""

    def test_form_valido(self):
        """Debe aceptar datos válidos."""
        form = CategoriaForm(data={'nombre': 'Test', 'color': '#FF0000'})
        self.assertTrue(form.is_valid())

    def test_form_nombre_requerido(self):
        """El nombre es obligatorio."""
        form = CategoriaForm(data={'color': '#FF0000'})
        self.assertFalse(form.is_valid())


class VistaListaTareasTest(TestCase):
    """Tests para la vista de lista de tareas."""

    def setUp(self):
        self.client = Client()
        self.cat = Categoria.objects.create(nombre='Test')
        self.tarea1 = Tarea.objects.create(
            titulo='Tarea 1', prioridad='alta', estado='pendiente', categoria=self.cat
        )
        self.tarea2 = Tarea.objects.create(
            titulo='Tarea 2', prioridad='baja', estado='completada', completada=True
        )

    def test_lista_tareas_status_200(self):
        """La página principal debe responder con 200."""
        response = self.client.get(reverse('lista_tareas'))
        self.assertEqual(response.status_code, 200)

    def test_lista_tareas_template(self):
        """Debe usar el template correcto."""
        response = self.client.get(reverse('lista_tareas'))
        self.assertTemplateUsed(response, 'tareas/lista_tareas.html')

    def test_lista_tareas_contiene_datos(self):
        """Debe mostrar las tareas creadas."""
        response = self.client.get(reverse('lista_tareas'))
        self.assertContains(response, 'Tarea 1')
        self.assertContains(response, 'Tarea 2')

    def test_filtro_por_estado(self):
        """Debe filtrar por estado correctamente."""
        response = self.client.get(reverse('lista_tareas') + '?estado=pendiente')
        self.assertContains(response, 'Tarea 1')
        self.assertNotContains(response, 'Tarea 2')

    def test_filtro_por_prioridad(self):
        """Debe filtrar por prioridad correctamente."""
        response = self.client.get(reverse('lista_tareas') + '?prioridad=alta')
        self.assertContains(response, 'Tarea 1')
        self.assertNotContains(response, 'Tarea 2')

    def test_busqueda(self):
        """Debe buscar por título."""
        response = self.client.get(reverse('lista_tareas') + '?q=Tarea+1')
        self.assertContains(response, 'Tarea 1')
        self.assertNotContains(response, 'Tarea 2')

    def test_estadisticas_contexto(self):
        """Debe incluir estadísticas en el contexto."""
        response = self.client.get(reverse('lista_tareas'))
        self.assertEqual(response.context['total'], 2)
        self.assertEqual(response.context['pendientes'], 1)
        self.assertEqual(response.context['completadas'], 1)


class VistaCrearTareaTest(TestCase):
    """Tests para la vista de crear tarea."""

    def setUp(self):
        self.client = Client()

    def test_crear_tarea_get(self):
        """Debe mostrar el formulario de creación."""
        response = self.client.get(reverse('crear_tarea'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], TareaForm)

    def test_crear_tarea_post_valido(self):
        """Debe crear la tarea y redirigir."""
        data = {
            'titulo': 'Tarea creada por test',
            'prioridad': 'media',
            'estado': 'pendiente',
        }
        response = self.client.post(reverse('crear_tarea'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Tarea.objects.filter(titulo='Tarea creada por test').exists())

    def test_crear_tarea_post_invalido(self):
        """Debe mostrar errores si el formulario es inválido."""
        response = self.client.post(reverse('crear_tarea'), {})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())


class VistaDetalleTareaTest(TestCase):
    """Tests para la vista de detalle."""

    def setUp(self):
        self.client = Client()
        self.tarea = Tarea.objects.create(titulo='Detalle test')

    def test_detalle_tarea(self):
        """Debe mostrar el detalle de la tarea."""
        response = self.client.get(reverse('detalle_tarea', args=[self.tarea.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Detalle test')

    def test_detalle_tarea_404(self):
        """Debe retornar 404 si la tarea no existe."""
        response = self.client.get(reverse('detalle_tarea', args=[9999]))
        self.assertEqual(response.status_code, 404)


class VistaEliminarTareaTest(TestCase):
    """Tests para la vista de eliminar."""

    def setUp(self):
        self.client = Client()
        self.tarea = Tarea.objects.create(titulo='Para eliminar')

    def test_eliminar_tarea_post(self):
        """Debe eliminar la tarea y redirigir."""
        response = self.client.post(reverse('eliminar_tarea', args=[self.tarea.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Tarea.objects.filter(pk=self.tarea.pk).exists())

    def test_eliminar_tarea_get(self):
        """GET debe mostrar confirmación, no eliminar."""
        response = self.client.get(reverse('eliminar_tarea', args=[self.tarea.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Tarea.objects.filter(pk=self.tarea.pk).exists())


class VistaToggleCompletadaTest(TestCase):
    """Tests para toggle de completada."""

    def setUp(self):
        self.client = Client()
        self.tarea = Tarea.objects.create(titulo='Toggle test')

    def test_toggle_completar(self):
        """Debe marcar como completada."""
        self.client.get(reverse('toggle_completada', args=[self.tarea.pk]))
        self.tarea.refresh_from_db()
        self.assertTrue(self.tarea.completada)

    def test_toggle_descompletar(self):
        """Debe desmarcar si ya está completada."""
        self.tarea.completada = True
        self.tarea.estado = Tarea.Estado.COMPLETADA
        self.tarea.save()
        self.client.get(reverse('toggle_completada', args=[self.tarea.pk]))
        self.tarea.refresh_from_db()
        self.assertFalse(self.tarea.completada)
