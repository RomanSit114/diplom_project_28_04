from fastapi import FastAPI
from routers import core_routes
from middleware.cors import add_cors_middleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()
add_cors_middleware(app)
app.include_router(core_routes)

app.mount("/app/public", StaticFiles(directory="/app/public"), name="public")
