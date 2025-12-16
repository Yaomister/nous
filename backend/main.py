from fastapi import FastAPI
from routers.user_management import router

app = FastAPI()

app.include_router(router, prefix="/user")