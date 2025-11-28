from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db import get_session
from typing import Annotated
from models.dtos import GetTableDTO, CreateTableDTO, UpdateTableDTO
from services.table_service import TableService
from fastapi.security import OAuth2PasswordBearer
from models.entities import User
from auth import decode_access_token
from fastapi import HTTPException

router = APIRouter(prefix="/api/v1/table", tags=["Tables"])

def _get_service(db: Session = Depends(get_session)) -> TableService:
    return TableService(db)

Service = Annotated[TableService, Depends(_get_service)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_admin_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_session)]):
    payload = decode_access_token(token)
    username: str = payload.get("sub")
    admin_user = db.query(User).filter(User.username == username, User.role == "admin").first()
    if admin_user is None:
        raise HTTPException(status_code=401, detail="This action requires admin privileges")
    return admin_user


@router.get("/", status_code=status.HTTP_200_OK)
def get_tables(current_user: Annotated[User, Depends(get_current_admin_user)], service: Service) -> list[GetTableDTO]:
    return service.get_all_tables()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_table(current_user: Annotated[User, Depends(get_current_admin_user)], table_dto: CreateTableDTO, service: Service) -> int:
    return service.create_table(table_dto)

@router.put("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_table(table_id: int, table_dto: UpdateTableDTO, service: Service) -> None:
    service.update_table(table_id, table_dto)

@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_table(table_id: int, service: Service) -> None:
    service.delete_table(table_id)