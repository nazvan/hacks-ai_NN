from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4


class RoutePoint(BaseModel):
    robotId: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    timestamp: Optional[int]

    class Config:
        orm_mode = True

class Defect(BaseModel):
    robotId: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    timestamp: Optional[int]
    imageId: Optional[str]
    type: Optional[str]
    

    class Config:
        orm_mode = True