from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.incidents import router as incidents_router
from app.api.routes.auth import router as auth_router


app = FastAPI()

app.include_router(health_router)
app.include_router(incidents_router)
app.include_router(auth_router)