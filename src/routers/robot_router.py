from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import select, delete

from dependencies import get_session
from db.config import async_session

from db.schemas.robot_schema import GetRobots as GetRobotsSchema
from db.schemas.robot_schema import Robot as RobotSchema
from db.schemas.robot_schema import Route as RouteSchema

from db.models.robot_model import Robot as RobotsModel
from db.models.robot_model import Route as RoutesModel
from db.models.robot_model import RoutePoint as PointsModel


robot_router = APIRouter(
    prefix="/robots",
    tags=["Robots"],
)

routes_router = APIRouter(
    prefix="/routes",
    tags=["Routes"],
)


@robot_router.get("", status_code=200)
async def get_robots(session: async_session = Depends(get_session)):
    q = select(RobotsModel)
    result = await session.execute(q)
    data = result.scalars().all()
    return data


@robot_router.post("")
async def add_robots(robot: RobotSchema, session: async_session = Depends(get_session)):
    new_robot = RobotsModel(**robot.dict())
    session.add(new_robot)
    await session.commit()
    return {"status": "200"}


@robot_router.delete("")
async def delete_robot(robot_id: str, session: async_session = Depends(get_session)):
    q = delete(RobotsModel).where(RobotsModel.id == robot_id)
    await session.execute(q)
    await session.commit()
    return {"status": "200"}


@routes_router.get("/all")
async def get_all_routes(session: async_session = Depends(get_session)):
    q = select(RoutesModel)
    result = await session.execute(q)
    data = result.scalars().all()
    return data


@routes_router.get("/{robot_id}")
async def get_routes_by_robot_id(robot_id: str, session: async_session = Depends(get_session)):
    q = select(RoutesModel).where(RoutesModel.robotId == robot_id)
    result = await session.execute(q)
    data = result.scalars().all()
    return data


@routes_router.post("")
async def add_route(route: RouteSchema, session: async_session = Depends(get_session)):
    new_route = RoutesModel(**route.dict())
    session.add(new_route)
    await session.commit()
    return {"status": "200"}


@routes_router.delete("")
async def delete_route_by_route_id(route_id: str, session: async_session = Depends(get_session)):
    q = delete(RoutesModel).where(RoutesModel.id == route_id)
    await session.execute(q)
    await session.commit()
    return {"status": "200"}


@routes_router.post("/data")
async def get_route_data(route_id: str, session: async_session = Depends(get_session)):
    q = select(PointsModel).where(PointsModel.routeId == route_id)
    result = await session.execute(q)
    data = result.scalars().all()
    print(data)
    return data

# @router.delete("/")
# async def delete_technic_class(video: TechnicSchema, session: async_session = Depends(get_session)):
#         q = delete(TechnicModel).where(TechnicModel.id==video.id)
#         await session.execute(q)
#         await session.commit()
#         return {'status':'200'}
