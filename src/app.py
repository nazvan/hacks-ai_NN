import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from routers.robot_router import robot_router, routes_router
from routers.api_router import api_router
# from routers.video_router import VIDEO_PATH

app = FastAPI(version="0.3.0")

from db.config import engine, Base


app = FastAPI(
    docs_url=f"/docs",
    openapi_url="/api/openapi.json",
)

routers = [robot_router, routes_router, api_router]

for router in routers:
    app.include_router(router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    uvicorn.run("app:app", host="25.38.72.80")
