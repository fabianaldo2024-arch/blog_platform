from sqlalchemy.orm import Session

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


def get_posts(db: Session, skip: int = 0, limit: int = 100) -> list[Post]:
    """Retrieve a list of posts with pagination."""
    return db.query(Post).offset(skip).limit(limit).all()


def get_post_by_id(db: Session, post_id: int) -> Post | None:
    """Retrieve a single post by its ID."""
    return db.query(Post).filter(Post.id == post_id).first()


def create_user_post(db: Session, post: PostCreate, user_id: int) -> Post:
    """Create a new post assigned to a specific user."""
    db_post = Post(**post.model_dump(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, db_post: Post, post_in: PostUpdate) -> Post:
    """Update an existing post."""
    update_data = post_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_post, field, value)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int) -> bool:
    """Delete a post by ID."""
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
        return True
    return False