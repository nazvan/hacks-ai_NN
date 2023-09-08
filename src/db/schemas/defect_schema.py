from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4


class CreateDefectSchema(BaseModel):
    name: Optional[str]
    description: Optional[str]
    city: Optional[str]
    street: Optional[str]

    class Config:
        orm_mode = True
