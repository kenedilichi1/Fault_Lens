from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.dependency import get_db
from app.api.router import router as api_router


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="1.0.1",
    description="FaultLens is an AI-powered observability platform for developers and SREs."
)

app.include_router(
    api_router,
    prefix="/api",
)
@app.get('/')
async def root():
    return {"status": "ok","application": settings.app_name}

@app.get('/health/db')
async def database_health(db:AsyncSession = Depends(get_db)):
    await db.execute(text("SELECT 1"))

    return {"status":"ok","database":"connected"}

