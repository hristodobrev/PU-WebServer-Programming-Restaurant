from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db import get_session
from typing import Annotated
from models.dtos import GetTableDTO, CreateTableDTO, UpdateTableDTO
from services.tables_service import TableService

router = APIRouter(prefix="/api/v1/table", tags=["Tables"])

def _get_service(db: Session = Depends(get_session)) -> TableService:
    return TableService(db)

Service = Annotated[TableService, Depends(_get_service)]

@router.get("/", status_code=status.HTTP_200_OK)
def get_tables(service: Service) -> list[GetTableDTO]:
    return service.get_all_tables()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_table(table_dto: CreateTableDTO, service: Service) -> int:
    return service.create_table(table_dto)

@router.put("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_table(table_id: int, table_dto: UpdateTableDTO, service: Service) -> None:
    service.update_table(table_id, table_dto)

@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_table(table_id: int, service: Service) -> None:
    service.delete_table(table_id)