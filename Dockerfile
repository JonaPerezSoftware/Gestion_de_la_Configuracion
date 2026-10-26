# ====================================
# Dockerfile - Gestión de Tareas Django
# Sesión 2 - Contenedorización
# ====================================

# Imagen base Python 3.10
FROM python:3.10-slim

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (necesarias para psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . .

# Recolectar archivos estáticos
RUN python manage.py collectstatic --noinput 2>/dev/null || true

# Exponer el puerto
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

# Entrypoint: migrar y ejecutar el servidor
ENTRYPOINT ["sh", "-c", "python manage.py migrate --noinput && gunicorn proyecto_config.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
