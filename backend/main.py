from fastapi import FastAPI
from app.api import api_router
from app.config import settings
from app.logger import configure_logging
from fastapi.middleware.cors import CORSMiddleware

configure_logging()

app = FastAPI(
    title="Driver Drowsiness Detection API",
    description="Backend API for the Intelligent Driver Drowsiness Detection system.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "service": "driver-drowsiness-backend"}
