from fastapi import FastAPI, Depends

from app.api import organizations, activities, buildings
from app.core.dependencies import verify_api_key
from app.core.middlewares import CatchExceptionsMiddleware

app = FastAPI(
    title="Handbook API",
    dependencies=[Depends(verify_api_key)]
)
app.include_router(organizations.router)
app.include_router(activities.router)
app.include_router(buildings.router)
app.add_middleware(CatchExceptionsMiddleware)
