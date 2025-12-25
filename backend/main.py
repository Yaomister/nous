from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.user_management import router as user_management_routes
from routers.books import router as book_routes
from routers.explore import router as explore_routes
from contextlib import asynccontextmanager
from utils.recommender import load_recommender



@asynccontextmanager
async def lifespan(app: FastAPI):
    load_recommender()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_management_routes, prefix="/user")
app.include_router(book_routes, prefix="/book")
app.include_router(explore_routes, prefix="/explore")





app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)