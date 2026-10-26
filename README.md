# 📋 Gestión de Tareas - Django CI/CD

Aplicación web de gestión de tareas desarrollada en **Django 4.2** con **PostgreSQL**, contenedorizada con **Docker** y con pipeline **CI/CD** en **GitHub Actions**.

## 🛠️ Stack Tecnológico

- **Backend:** Django 4.2 / Python 3.10
- **Base de datos:** PostgreSQL 15 / SQLite (desarrollo)
- **Servidor:** Gunicorn
- **Contenedores:** Docker + Docker Compose
- **CI/CD:** GitHub Actions

## ✨ Funcionalidades

- CRUD completo de tareas (crear, leer, editar, eliminar)
- Sistema de categorías con colores
- Prioridades (Baja, Media, Alta, Urgente)
- Estados (Pendiente, En Progreso, Completada, Cancelada)
- Filtros por estado, prioridad y categoría
- Búsqueda por texto
- Dashboard con estadísticas
- Marcar/desmarcar tareas como completadas
- Interfaz responsive con tema oscuro

## 🚀 Inicio Rápido

### Opción 1: Docker Compose (recomendado)
```bash
docker compose build
docker compose up -d
# Acceder a http://localhost:8000
```

### Opción 2: Desarrollo local
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 🧪 Ejecutar Tests
```bash
python manage.py test --verbosity=2
```

## 📁 Estructura del Proyecto
```
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .github/workflows/ci.yml
├── proyecto_config/          # Configuración Django
└── tareas/                   # App principal
```

## 📖 Documentación

- [`deploy-notes.md`](deploy-notes.md) - Pasos de despliegue
- [`docs/flujo-cicd-django.md`](docs/flujo-cicd-django.md) - Documento técnico del pipeline
