from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, computed_field


class PostBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255, examples=["Mi primer post"])
    content: str = Field(..., min_length=5, examples=["Contenido detallado de la publicación."])


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    content: Optional[str] = Field(None, min_length=5)


class PostResponse(PostBase):
    id: int
    author_id: int
    created_at: datetime

    # Exposición de 'owner_id' solicitada por la suite de pruebas de integración
    @computed_field
    @property
    def owner_id(self) -> int:
        return self.author_id

    model_config = ConfigDict(from_attributes=True)