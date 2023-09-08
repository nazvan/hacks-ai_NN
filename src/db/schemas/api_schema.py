from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4


class RoutePoint(BaseModel):
    routeId: Optional[str]
    robotId: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    timestamp: Optional[int]

    class Config:
        orm_mode = True