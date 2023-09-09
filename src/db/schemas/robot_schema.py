from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4


class Robot(BaseModel):
    name: Optional[str]
    type: Optional[str]
    desc: Optional[str]
    isActive: bool

    class Config:
        orm_mode = True

class GetRobots(Robot):
    id: uuid4


class Route(BaseModel):
    robotId: str
    name: Optional[str]
    desc: Optional[str]
    length: Optional[float]
    timeDuration: Optional[String]