from sqlalchemy import Column, Integer, String, ForeignKey, Float
from db.config import Base
from dependencies import uuid


class Defect(Base):
    __tablename__ = "defect"

    id = Column(String, primary_key=True, default=uuid)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(Integer, nullable=False)
    imageId = Column(Integer, nullable=True)
    type = Column(String, default='u',nullable=False)

    routeId = Column(String, ForeignKey("route.id"), nullable=False)
    robotId = Column(String, ForeignKey("robot.id"), nullable=False)
