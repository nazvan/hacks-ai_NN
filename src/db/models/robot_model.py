from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Boolean, Float
from db.config import Base
from uuid import UUID, uuid4
from dependencies import uuid


from datetime import datetime
import time
from typing import List, Optional
from sqlalchemy.orm import relationship


class Robot(Base): #Робот
    __tablename__ = "robot"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)  # Название робота
    type = Column(String, nullable=True)  # Тип робота
    desc = Column(String, nullable=True)  # Описание робота
    isActive = Column(Boolean, nullable=True)  # Активен ли в данный момент

    # routes = relationship("Route", back_populates="robot")

class Route(Base): ## Маршруты
    __tablename__ = "route"

    id = Column(String, primary_key=True, default=uuid)
    name = Column(String, nullable=True)  # Название маршрута
    desc = Column(String, nullable=True)  # Описание маршрута
    length = Column(String, nullable=True)  # длина маршрута, км
    timeDuration = Column(String, nullable=True)  # Длителность маршрута
    isActive = Column(Boolean, nullable=True)  # Активен ли в данный момент

    robotId = Column(String, ForeignKey("robot.id"), nullable=False)

class RoutePoint(Base): ## Маршруты
    __tablename__ = "route_point"

    id = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(Integer, nullable=False)

    routeId = Column(String, ForeignKey("route.id"), nullable=False)
    robotId = Column(String, ForeignKey("robot.id"), nullable=False)