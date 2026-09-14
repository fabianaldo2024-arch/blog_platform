from pathlib import Path
from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Comment, Post

router = APIRouter(tags=["Vistas SSR / Salubridad"])

# Resolución de ruta absoluta hacia el directorio templates/ raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "ok"}


@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return templates.TemplateResponse(
        request=request, name="index.html", context={"posts": posts}
    )


@router.post("/posts/{post_id}/comments/htmx", response_class=HTMLResponse)
def add_comment_htmx(
    request: Request,
    post_id: int,
    author_name: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Publicación no encontrada"
        )

    new_comment = Comment(author_name=author_name, content=content, post_id=post_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return templates.TemplateResponse(
        request=request,
        name="partials/comment_card.html",
        context={"comment": new_comment},
    )