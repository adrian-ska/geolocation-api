from fastapi import FastAPI
import uvicorn
from app.api.controllers.geolocation import router
from app.core.config import settings
from app.core.logger import logger


app = FastAPI(title="Geolocation API")


app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """Triggered when the application starts."""
    logger.info(f"Starting Geolocation API on {settings.HOST}:{settings.PORT}")

@app.on_event("shutdown")
async def shutdown_event():
    """Triggered when the application shuts down."""
    logger.info("Shutting down Geolocation API")

if __name__ == "__main__":
    # Run the FastAPI application with Uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )