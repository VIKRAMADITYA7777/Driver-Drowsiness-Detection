from fastapi import APIRouter
from app.routes.health import router as health_router
from app.routes.monitoring import router as monitoring_router
from app.routes.dashboard import router as dashboard_router

api_router = APIRouter()
api_router.include_router(health_router, prefix="/health", tags=["Health"])
api_router.include_router(monitoring_router, prefix="/monitoring", tags=["Monitoring"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
