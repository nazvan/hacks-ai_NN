from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import select, delete, update
from dependencies import uuid

from dependencies import get_session
from db.config import async_session

from db.schemas.api_schema import RoutePoint as PointSchema

from db.models.robot_model import RoutePoint as PointModel
from db.models.robot_model import Robot as RobotsModel


active_robots = {}

api_router = APIRouter(
    prefix="/api",
    tags=["API"],
)

@api_router.post("/add_point")
async def add_points_to_routes(point: PointSchema, session: async_session = Depends(get_session)):
    if point.robotId not in active_robots:
        active_robots[point.robotId]=uuid()
        update(RobotsModel).where(RobotsModel.id==point.robotId).values({'isActive':1})
        new_route = RoutesModel()
        session.add(new_route)
    new_point = PointModel(**point.dict())
    session.add(new_point)
    await session.commit()
    return {"status": "200"}


# @router.delete("/")
# async def delete_technic_class(video: TechnicSchema, session: async_session = Depends(get_session)):
#         q = delete(TechnicModel).where(TechnicModel.id==video.id)
#         await session.execute(q)
#         await session.commit()
#         return {'status':'200'}
