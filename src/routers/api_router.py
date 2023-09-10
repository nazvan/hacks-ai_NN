from typing import List, Optional

from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy import select, delete, update
from dependencies import uuid
from time import time, sleep
import asyncio

from dependencies import get_session
from db.config import async_session

from db.schemas.api_schema import RoutePoint as PointSchema
from db.schemas.api_schema import Defect as DefectSchema

from db.models.robot_model import RoutePoint as PointModel
from db.models.robot_model import Robot as RobotsModel
from db.models.robot_model import Route as RoutesModel
from db.models.defect_model import Defect as DefectModel

from db.config import async_session
from app import app

 


active_robots = {}
new_points = []
timeDelay = 5 #Время задержки

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        if len(new_points)>0: 
            await websocket.send_json(new_points)
            new_points.clear()
            print(new_points)
        await asyncio.sleep(1)

async def check_active_robots():
    while True:
        current_time = int(time())
        for robot_id in list(active_robots):
            if current_time - active_robots[robot_id]['last_time'] > timeDelay:
                async with async_session() as session:
                        async with session.begin():
                            stmt = (update(RobotsModel).where(RobotsModel.id==robot_id).values({'isActive':0}))
                            await session.execute(stmt)
                            stmt = (update(RoutesModel).where(RoutesModel.id==active_robots[robot_id]['routeId']).values({'isActive':0}))
                            await session.execute(stmt)
                            await session.commit()
                            active_robots.pop(robot_id)
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
            'name':'Нижний Новгород',
            'desc':'desc',
            'length':1.0,
            'timeDuration':'15 min',
            'isActive':1
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
        new_points.append(point_data)




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

@api_router.post("/add_defect")
async def add_defect_to_map(defect: DefectSchema, session: async_session = Depends(get_session)):
    defect_data = defect.dict()
    print(defect_data)
    defect_data['routeId'] = active_robots[defect.robotId]['routeId']
    new_defect = DefectModel(**defect_data)
    session.add(new_defect)
    await session.commit()