from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db
from .routers import manga, users, reviews, recommendations, auth

app = FastAPI(title="manga Rec API")

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

app.include_router(users.router, prefix="/api")
app.include_router(manga.router, prefix="/api")
app.include_router(reviews.router, prefix="/api")
app.include_router(recommendations.router, prefix="/api")
app.include_router(auth.router, prefix="/api")


@app.get("/")
def root():
    return {"status": "ok", "message": "manga Rec backend running!"}
