from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from backend import models, schemas, utils
from backend.database import engine, get_db
from backend.utils import get_current_user
from backend.auth import auth_router
from backend.auctions import router as auctions_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(auctions_router)

# --------------------------- FRONTEND ROUTES ---------------------------

@app.get("/", response_class=HTMLResponse)
def serve_home():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/host", response_class=HTMLResponse)
def serve_host():
    with open("templates/host.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/join", response_class=HTMLResponse)
def serve_join():
    with open("templates/join.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/auctions", response_class=HTMLResponse)
def serve_auctions():
    with open("templates/ongoing.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/ongoing", response_class=HTMLResponse)
def serve_ongoing():
    with open("templates/ongoing.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())
