# 🚀 Blog Platform — FastAPI, PostgreSQL & Docker

## 🟢 Demo en vivo
**App:** https://blog-platform-m5fx.onrender.com
**API Docs (Swagger):** https://blog-platform-m5fx.onrender.com/docs

> ⚠️ Nota: corre en plan gratuito de Render — si está inactiva, el primer request puede tardar ~50 segundos en responder mientras el servicio "despierta".


[ES] Plataforma web profesional para gestión de blogs y servicios, desarrollada con FastAPI, PostgreSQL, Alembic y Docker en Linux Mint.  
[EN] Robust web platform built with FastAPI, PostgreSQL, Alembic, and Docker on Linux Mint.

---

## 🛠️ Requisitos Previos / Prerequisites

- **OS:** Linux Mint / Ubuntu / Debian
- **Containers:** Docker & Docker Compose
- **Package Manager:** Poetry (opcional para desarrollo local / optional for local dev)

---

## 🏎️ Arranque Rápido con Docker / Quick Start with Docker

1. **Clonar el repositorio / Clone repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)fabian2024-arch/blog_platform.git
   cd blog_platform


Configurar variables de entorno / Establecer variables de entorno:

Intento
cp .env.example .env
Iniciar los servicios y aplicar migraciones / Iniciar servicios y aplicar migraciones:

Intento
docker compose up --build -d
Acceder a la aplicación / Acceder a la aplicación:

Página Principal / Home: http://localhost:8000

Salud del Sistema / Healthcheck: http://localhost:8000/health

Documentación Interactiva / Swagger Docs: http://localhost:8000/docs

🗄️ Migraciones de Base de Datos / Database Migrations
Las migraciones se ejecutan automáticamente al iniciar el contenedor web. Si necesitas ejecutarlas manualmente:

Intento
docker compose exec web alembic upgrade head
🩺 Diagnóstico y Mantenimiento / Diagnóstico y Mantenimiento
Si experimenta problemas con los contenedores o el puerto 5432:

Intento
# 1. Dar permisos y ejecutar script de diagnóstico
chmod +x scripts/docker-diag.sh
./scripts/docker-diag.sh

# 2. Reiniciar el entorno completamente limpiando volúmenes
docker compose down -v
docker compose up --build -d
📦 Licencia / License
silvertech (Aldo Fabian Perez Lezcano)
