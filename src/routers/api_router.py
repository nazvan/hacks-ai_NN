from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import select, delete, update
from dependencies import uuid
from time import time
import asyncio

from dependencies import get_session
from db.config import async_session

from db.schemas.api_schema import RoutePoint as PointSchema

from db.models.robot_model import RoutePoint as PointModel
from db.models.robot_model import Robot as RobotsModel
from db.models.robot_model import Route as RoutesModel

from db.config import async_session


active_robots = {}
timeDelay = 5 #Время задержки

async def check_active_robots():
    while True:
        current_time = int(time())
        for robot_id in list(active_robots):
            if current_time - active_robots[robot_id]['last_time'] > timeDelay:
                stmt = (update(RobotsModel).where(RobotsModel.id==robot_id).values({'isActive':0}))
                active_robots.pop(robot_id)
                async with async_session() as session:
                        async with session.begin():
                            await session.execute(stmt)
        await asyncio.sleep(1)

asyncio.ensure_future(check_active_robots())

async def create_route(point, session):
        active_robots[point.robotId] = {
            'routeId': uuid(),
            'last_time': point.timestamp
        }
        stmt = (update(RobotsModel).where(RobotsModel.id==point.robotId).values({'isActive':1}))
        result = await session.execute(stmt)
        route_data = {
            'id':active_robots[point.robotId]['routeId'],
            'robotId':point.robotId,
            'name':'name',
            'desc':'desc',
            'length':1.0,
            'timeDuration':'15 min'
        }
        print(route_data)
        new_route = RoutesModel(**route_data)
        session.add(new_route)

async def create_point(point, session):
        point_data = point.dict()
        point_data['routeId'] = active_robots[point.robotId]['routeId']
        new_point = PointModel(**point_data)
        session.add(new_point)
        active_robots[point.robotId]['last_time'] = point.timestamp




api_router = APIRouter(
    prefix="/api",
    tags=["API"],
)

@api_router.post("/add_point")
async def add_points_to_routes(point: PointSchema, session: async_session = Depends(get_session)):
    if point.robotId not in active_robots:
       await create_route(point,session)
       await create_point(point,session)
    else:
        await create_point(point,session)
    await session.commit()
    return {"status": "200"}





# @router.delete("/")
# async def delete_technic_class(video: TechnicSchema, session: async_session = Depends(get_session)):
#         q = delete(TechnicModel).where(TechnicModel.id==video.id)
#         await session.execute(q)
#         await session.commit()
#         return {'status':'200'}
