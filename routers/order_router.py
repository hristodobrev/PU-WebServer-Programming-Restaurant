from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db import get_session
from services.order_service import OrderService
from services.table_service import TableService
from models.dtos import CreateOrderDTO, UpdateOrderDTO, GetOrderDTO

router = APIRouter(prefix="/api/v1/order", tags=["Orders"])

def _get_order_service(db: Session = Depends(get_session)) -> OrderService:
    return OrderService(db)

def _get_table_service(db: Session = Depends(get_session)) -> TableService:
    return TableService(db)

OService = Annotated[OrderService, Depends(_get_order_service)]
TService = Annotated[TableService, Depends(_get_table_service)]

@router.get("/", status_code=status.HTTP_200_OK)
def get_orders(service: OService) -> list[GetOrderDTO]:
    return service.get_all_orders()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_order(order_dto: CreateOrderDTO, order_service: OService, table_service: TService) -> int:
    table_service._get_table_by_id(order_dto.table_id) # Ensure table exists
    return order_service.create_order(order_dto)

@router.put("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_order(order_id: int, order_dto: UpdateOrderDTO, order_service: OService, table_service: TService) -> None:
    table_service._get_table_by_id(order_dto.table_id) # Ensure table exists
    order_service.update_order(order_id, order_dto)

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, service: OService) -> None:
    service.delete_order(order_id)