from pathlib import Path

from fastapi import APIRouter, Depends, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Comment, Post

router = APIRouter(tags=["Vistas SSR / HTMX"])

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "ok"}


@router.get("/", response_class=HTMLResponse)
def home_page(request: Request, db: Session = Depends(get_db)):
    """Página principal: lista de publicaciones."""
    posts = db.query(Post).order_by(Post.created_at.desc()).limit(20).all()
    return templates.TemplateResponse(
        request=request, name="pages/index.html", context={"posts": posts}
    )


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="pages/login.html")


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request=request, name="pages/register.html")


@router.get("/posts/create", response_class=HTMLResponse)
def create_post_page(request: Request):
    return templates.TemplateResponse(request=request, name="pages/create_post.html")


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
