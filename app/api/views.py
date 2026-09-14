from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.crud.post import get_posts
from app.db.session import get_db

router = APIRouter(tags=["Frontend Views"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def home_page(
    request: Request,
    db: Annotated[Session, Depends(get_db)]
):
    """Render the public homepage with latest blog posts."""
    posts = get_posts(db, skip=0, limit=20)
    return templates.TemplateResponse(
        request=request,
        name="pages/index.html",
        context={"posts": posts}
    )


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    """Render the user login page."""
    return templates.TemplateResponse(
        request=request,
        name="pages/login.html"
    )


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    """Render the user registration page."""
    return templates.TemplateResponse(
        request=request,
        name="pages/register.html"
    )


@router.get("/posts/create", response_class=HTMLResponse)
def create_post_page(request: Request):
    """Render the post creation form."""
    return templates.TemplateResponse(
        request=request,
        name="pages/create_post.html"
    )