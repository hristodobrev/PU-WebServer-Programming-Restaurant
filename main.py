from fastapi import FastAPI
from routers import table_router, product_router, order_router, order_item_router
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from db import get_session
from sqlalchemy.orm import Session
from models.entities import User
from models.dtos import CreateUserDTO, GetUserDTO
from auth import verify_password, create_access_token, get_password_hash, decode_access_token

app = FastAPI()

app.include_router(table_router.router)
app.include_router(product_router.router)
app.include_router(order_router.router)
app.include_router(order_item_router.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db: Annotated[Session, Depends(get_session)], username: str):
    pass


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_session)]):
    payload = decode_access_token(token)
    username: str = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return user

@app.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_session)]):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")   
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/regsister", status_code=201)
def register(user_dto: CreateUserDTO, db: Annotated[Session, Depends(get_session)]):
    user = User(username=user_dto.username, hashed_password= get_password_hash(user_dto.password), role=user_dto.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username}

@app.get("/me", response_model=GetUserDTO)
def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user