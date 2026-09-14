from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class CommentBase(BaseModel):
    author_name: str = Field(..., min_length=2, max_length=100, examples=["Juan Pérez"])
    content: str = Field(..., min_length=1, max_length=1000, examples=["Excelente artículo, muy claro."])


class CommentCreate(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: int
    post_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)