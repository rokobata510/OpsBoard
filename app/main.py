from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import logging
import time 
from fastapi import Request
from app.logging import configure_logging


from app.api.routes.health import router as health_router
from app.api.routes.incidents import router as incidents_router
from app.api.routes.auth import router as auth_router

configure_logging()
logger = logging.getLogger("opsboard")

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter()-start)* 1000, 2)
    
    logger.info(
        "request_completed",
        extra={
            "extra": {
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            }
        },
    )
    return response

app.include_router(health_router)
app.include_router(incidents_router)
app.include_router(auth_router)

Instrumentator().instrument(app).expose(app)