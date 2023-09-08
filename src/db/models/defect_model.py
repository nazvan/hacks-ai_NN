from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from db.config import Base
from uuid import UUID, uuid4


from datetime import datetime
import time
from typing import List, Optional
from sqlalchemy.orm import relationship


class Defect(Base):
    __tablename__ = "defect"

    id = Column(String, primary_key=True, default=uuid4)
    text = Column(String, nullable=True)  # Название сессии
    type = Column(String, nullable=True)  # Описание сессии
    timeStart = Column(Integer, nullable=True)  # Время от старта видео в секундах
    timeEnd = Column(Integer, nullable=True)  # Время от старта видео в секундах

    technique = relationship("Technique", back_populates="events")
    technique_id = Column(String, ForeignKey("technique.id"), nullable=False)
