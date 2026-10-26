# 📝 Notas de Despliegue - Gestión de Tareas

## Información del Proyecto
- **Proyecto:** Gestión de Tareas (Django 4.2)
- **Base de datos:** PostgreSQL 15
- **Servidor WSGI:** Gunicorn
- **Contenedorización:** Docker + Docker Compose

---

## 🚀 Pasos para el Despliegue Simulado

### Prerrequisitos
- Docker Desktop instalado y corriendo
- Docker Compose disponible
- Git instalado

### Paso 1: Clonar el repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd gesion
```

### Paso 2: Verificar la estructura del proyecto
```bash
# Verificar archivos esenciales
ls manage.py
ls proyecto_config/settings.py
ls tareas/
ls requirements.txt
ls Dockerfile
ls docker-compose.yml
```

### Paso 3: Construir y levantar los contenedores
```bash
# Construir las imágenes
docker compose build

# Levantar los servicios en segundo plano
docker compose up -d
```

### Paso 4: Verificar que los contenedores están corriendo
```bash
# Ver estado de los contenedores
docker compose ps

# Salida esperada:
# NAME                    STATUS      PORTS
# gestion_tareas_db       running     0.0.0.0:5432->5432/tcp
# gestion_tareas_web      running     0.0.0.0:8000->8000/tcp
```

### Paso 5: Verificar los logs
```bash
# Ver logs de Django
docker compose logs web

# Ver logs de PostgreSQL
docker compose logs db
```

### Paso 6: Acceder a la aplicación
1. Abrir el navegador
2. Navegar a: **http://localhost:8000/**
3. Verificar que la página de tareas carga correctamente

### Paso 7: Crear un superusuario (opcional)
```bash
docker compose exec web python manage.py createsuperuser
```
Luego acceder al admin en: **http://localhost:8000/admin/**

### Paso 8: Detener los servicios
```bash
# Detener sin eliminar volúmenes
docker compose down

# Detener y eliminar volúmenes (borra la base de datos)
docker compose down -v
```

---

## 🔄 Flujo CI/CD Automatizado

El pipeline de GitHub Actions ejecuta automáticamente:

1. **Test (CI):** Ejecuta `python manage.py test` con SQLite
2. **Build:** Construye la imagen Docker y la guarda como artefacto
3. **Deploy Simulation:** Descarga la imagen, la carga, y verifica que corre

### Trigger del pipeline
- **Push** a las ramas `main` o `ci-setup`
- **Pull Request** hacia `main`

---

## ⚠️ Notas Importantes

- Las credenciales en `docker-compose.yml` son para **desarrollo local únicamente**
- En producción, usar variables de entorno seguras o un servicio de secretos
- El `SECRET_KEY` de Django debe ser único y secreto en producción
- `DEBUG` debe ser `False` en producción
- Configurar `ALLOWED_HOSTS` con el dominio real en producción

---

## 📋 Checklist de Validación

- [ ] `docker compose build` completa sin errores
- [ ] `docker compose up -d` levanta ambos contenedores
- [ ] PostgreSQL acepta conexiones (healthcheck pasa)
- [ ] Django ejecuta migraciones automáticamente
- [ ] La aplicación responde en http://localhost:8000/
- [ ] Se pueden crear, editar y eliminar tareas
- [ ] Los tests pasan con `python manage.py test`
- [ ] GitHub Actions ejecuta el pipeline correctamente
