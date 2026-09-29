from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers.auth import router as auth_router
from app.routers.comments import router as comments_router
from app.routers.posts import router as posts_router
from app.routers.views import router as views_router

app = FastAPI(
    title="Plataforma de Blog API",
    version="1.0.0",
)

# Archivos estáticos (CSS, JS, imágenes)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# API v1 endpoints (coincidentes con conftest.py)
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Autenticación"])
app.include_router(posts_router, prefix="/api/v1/posts", tags=["Publicaciones"])
app.include_router(comments_router, prefix="/api/v1")

# Vistas SSR e interfaz HTMX
app.include_router(views_router)
