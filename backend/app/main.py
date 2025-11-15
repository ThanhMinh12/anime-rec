from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db
from .routers import users, anime, reviews, recommendations, auth

app = FastAPI(title="Anime Rec API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()
    print("Database tables initialized")

app.include_router(users.router)
app.include_router(anime.router)
app.include_router(reviews.router)
app.include_router(recommendations.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"status": "ok", "message": "Anime Rec backend running!"}
