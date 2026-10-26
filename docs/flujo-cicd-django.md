# Flujo CI/CD para Django
## Gestión de Tareas - Documento Técnico del Pipeline

---

## 1. Descripción General

Este documento describe el pipeline de Integración Continua y Despliegue Continuo (CI/CD) implementado para el proyecto **Gestión de Tareas**, una aplicación web desarrollada en Django 4.2 con base de datos PostgreSQL.

### Stack Tecnológico
| Componente | Tecnología | Versión |
|---|---|---|
| Framework | Django | 4.2.16 |
| Lenguaje | Python | 3.10 |
| Base de datos | PostgreSQL | 15 |
| Servidor WSGI | Gunicorn | 22.0.0 |
| Contenedorización | Docker | Latest |
| Orquestación | Docker Compose | v2 |
| CI/CD | GitHub Actions | v4 |

---

## 2. Estructura del Proyecto

```
gesion/
├── manage.py                      # Punto de entrada Django
├── requirements.txt               # Dependencias Python
├── Dockerfile                     # Imagen Docker
├── docker-compose.yml             # Orquestación de servicios
├── deploy-notes.md                # Notas de despliegue
├── .gitignore                     # Archivos ignorados por Git
├── .dockerignore                  # Archivos ignorados por Docker
├── .github/
│   └── workflows/
│       └── ci.yml                 # Pipeline CI/CD
├── proyecto_config/               # Configuración del proyecto
│   ├── __init__.py
│   ├── settings.py                # Configuración Django
│   ├── urls.py                    # URLs raíz
│   ├── wsgi.py                    # WSGI config
│   └── asgi.py                    # ASGI config
└── tareas/                        # App principal
    ├── __init__.py
    ├── apps.py                    # Configuración de la app
    ├── models.py                  # Modelos (Tarea, Categoría)
    ├── views.py                   # Vistas (CRUD)
    ├── urls.py                    # URLs de la app
    ├── forms.py                   # Formularios
    ├── admin.py                   # Admin de Django
    ├── tests.py                   # Suite de tests (30+ tests)
    └── templates/tareas/          # Templates HTML
        ├── base.html
        ├── lista_tareas.html
        ├── form_tarea.html
        ├── detalle_tarea.html
        ├── confirmar_eliminar.html
        └── lista_categorias.html
```

---

## 3. Diagrama del Flujo CI/CD

```
┌─────────────────────────────────────────────────────────────────┐
│                    PIPELINE CI/CD                                │
│                                                                  │
│  ┌──────────┐     ┌──────────────┐     ┌───────────────────┐    │
│  │          │     │              │     │                   │    │
│  │  PUSH /  │────▶│  JOB 1: TEST │────▶│  JOB 2: BUILD     │    │
│  │   PR     │     │              │     │  DOCKER           │    │
│  │          │     │  • Checkout  │     │                   │    │
│  └──────────┘     │  • Python    │     │  • Checkout       │    │
│                   │    3.10      │     │  • Docker Buildx  │    │
│  Triggers:        │  • pip       │     │  • Build image    │    │
│  • push main      │    install   │     │  • Save artifact  │    │
│  • push ci-setup  │  • manage.py │     │  • Upload to GH   │    │
│  • PR to main     │    test      │     │                   │    │
│                   │  • Verificar │     └────────┬──────────┘    │
│                   │    estructura│              │               │
│                   └──────────────┘              │               │
│                                                 ▼               │
│                                    ┌───────────────────────┐    │
│                                    │                       │    │
│                                    │  JOB 3: DEPLOY        │    │
│                                    │  SIMULATION            │    │
│                                    │                       │    │
│                                    │  • Download artifact  │    │
│                                    │  • Load Docker image  │    │
│                                    │  • docker compose up  │    │
│                                    │  • Health check       │    │
│                                    │  • Generate report    │    │
│                                    │  • docker compose     │    │
│                                    │    down               │    │
│                                    │                       │    │
│                                    └───────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Explicación del Archivo ci.yml

### 4.1 Configuración General

```yaml
name: CI/CD Pipeline - Gestión de Tareas
on:
  push:
    branches: [ main, ci-setup ]
  pull_request:
    branches: [ main ]
```

- **name**: Nombre descriptivo del workflow
- **on**: Define los eventos que disparan el pipeline
  - `push` a ramas `main` y `ci-setup`
  - `pull_request` hacia `main`

### 4.2 Job 1: Test (Integración Continua)

**Propósito:** Verificar que el código funciona correctamente ejecutando la suite de tests.

| Paso | Acción | Descripción |
|------|--------|-------------|
| 1 | `actions/checkout@v4` | Descarga el código del repositorio |
| 2 | `actions/setup-python@v5` | Configura Python 3.10 con caché de pip |
| 3 | `pip install` | Instala las dependencias del requirements.txt |
| 4 | `manage.py test` | Ejecuta los 30+ tests unitarios |
| 5 | Verificación | Comprueba la estructura del proyecto |

**Notas:**
- Usa SQLite en CI para evitar configurar PostgreSQL en el runner
- Las variables de entorno (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`) se configuran inline

### 4.3 Job 2: Build Docker

**Propósito:** Construir la imagen Docker y guardarla como artefacto.

| Paso | Acción | Descripción |
|------|--------|-------------|
| 1 | `actions/checkout@v4` | Descarga el código |
| 2 | `docker/setup-buildx-action@v3` | Configura Docker Buildx |
| 3 | `docker/build-push-action@v5` | Construye la imagen con caché |
| 4 | `docker save` | Exporta la imagen a archivo .tar.gz |
| 5 | `actions/upload-artifact@v4` | Sube el artefacto a GitHub |

**Dependencia:** Solo se ejecuta si el Job 1 (test) pasa exitosamente.

### 4.4 Job 3: Simulación de Despliegue

**Propósito:** Simular un despliegue real descargando y ejecutando la imagen Docker.

| Paso | Acción | Descripción |
|------|--------|-------------|
| 1 | Checkout | Descarga el código (para docker-compose.yml) |
| 2 | Download artifact | Descarga la imagen Docker guardada |
| 3 | `docker load` | Carga la imagen en el daemon de Docker |
| 4 | `docker compose up -d` | Levanta los servicios |
| 5 | Health check | Verifica que la app responde |
| 6 | `docker compose down` | Limpia los contenedores |

---

## 5. Análisis del Dockerfile

```dockerfile
FROM python:3.10-slim          # Imagen base ligera
WORKDIR /app                   # Directorio de trabajo
RUN apt-get install gcc libpq-dev  # Deps para psycopg2
COPY requirements.txt .        # Copiar dependencias
RUN pip install -r requirements.txt  # Instalar dependencias
COPY . .                       # Copiar código
RUN collectstatic              # Archivos estáticos
EXPOSE 8000                    # Puerto
ENTRYPOINT gunicorn ...        # Servidor de producción
```

**Optimizaciones:**
- Usa `python:3.10-slim` para reducir tamaño de imagen
- Copia `requirements.txt` antes del código para aprovechar caché de Docker
- Limpia las listas de apt después de instalar
- Incluye healthcheck para monitoreo

---

## 6. Análisis del Docker Compose

Orquesta dos servicios:

### Servicio `db` (PostgreSQL)
- Imagen: `postgres:15-alpine`
- Healthcheck con `pg_isready`
- Volumen persistente para datos
- Puerto: 5432

### Servicio `web` (Django)
- Build desde Dockerfile local
- Depende de `db` (con condition: service_healthy)
- Variables de entorno para conexión a PostgreSQL
- Puerto: 8000

---

## 7. Suite de Tests

La suite contiene **30+ tests** organizados en las siguientes clases:

| Clase | Tests | Cobertura |
|-------|-------|-----------|
| `CategoriaModelTest` | 3 | Creación, unicidad, __str__ |
| `TareaModelTest` | 6 | CRUD, marcar completada, vencimiento |
| `TareaFormTest` | 3 | Validación de formularios |
| `CategoriaFormTest` | 2 | Validación de formularios |
| `VistaListaTareasTest` | 7 | Lista, filtros, búsqueda, estadísticas |
| `VistaCrearTareaTest` | 3 | GET form, POST válido, POST inválido |
| `VistaDetalleTareaTest` | 2 | Detalle existente, 404 |
| `VistaEliminarTareaTest` | 2 | POST elimina, GET muestra confirmación |
| `VistaToggleCompletadaTest` | 2 | Completar, descompletar |

---

## 8. Recomendaciones Finales

### Seguridad
1. **Nunca** commitear credenciales reales al repositorio
2. Usar **GitHub Secrets** para variables sensibles (SECRET_KEY, DB passwords)
3. Deshabilitar `DEBUG=False` en producción
4. Configurar `ALLOWED_HOSTS` con dominios específicos

### Rendimiento
1. Usar **multi-stage builds** en Docker para reducir tamaño de imagen
2. Activar **caché de GitHub Actions** (ya implementado con `cache: 'pip'`)
3. Considerar **nginx** como reverse proxy frente a Gunicorn

### Mejoras Futuras
1. **Cobertura de código:** Agregar `coverage` al pipeline y definir umbral mínimo
2. **Linting:** Agregar `flake8` o `ruff` como paso de verificación de calidad
3. **Staging:** Configurar un entorno de staging antes de producción
4. **DockerHub:** Publicar la imagen en DockerHub o GitHub Container Registry
5. **Notificaciones:** Configurar alertas por Slack/email cuando falla el pipeline
6. **Backups:** Automatizar backups de la base de datos PostgreSQL
7. **SSL/TLS:** Configurar HTTPS con Let's Encrypt en producción

### Comandos Útiles
```bash
# Ejecutar tests localmente
python manage.py test --verbosity=2

# Construir imagen Docker
docker compose build

# Levantar servicios
docker compose up -d

# Ver logs
docker compose logs -f web

# Acceder al shell de Django
docker compose exec web python manage.py shell

# Crear superusuario
docker compose exec web python manage.py createsuperuser
```

---

## 9. Referencias

- [Django Documentation](https://docs.djangoproject.com/4.2/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

---

> **Proyecto:** Gestión de Tareas  
> **Framework:** Django 4.2.16  
> **Pipeline:** GitHub Actions CI/CD  
> **Contenedorización:** Docker + Docker Compose
