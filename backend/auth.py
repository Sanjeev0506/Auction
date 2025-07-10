from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import models, schemas, utils

auth_router = APIRouter()

@auth_router.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = utils.get_password_hash(user.password)
    new_user = models.User(email=user.email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@auth_router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not utils.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = utils.create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user_id": user.id}

@auth_router.get("/me")
def get_me(current_user: dict = Depends(utils.get_current_user)):
    return current_user
