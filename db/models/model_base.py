from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class ModelBase(SQLModel):
    id: Optional[int] = Field(primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
