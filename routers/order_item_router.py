from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db import get_session
from services.order_item_service import OrderItemService
from services.order_service import OrderService
from services.product_service import ProductService
from models.dtos import GetOrderItemDTO, CreateOrderItemDTO, UpdateOrderItemDTO

router = APIRouter(prefix="/api/v1/order-items", tags=["OrderItems"])

def _get_order_item_service(db: Session = Depends(get_session)) -> OrderItemService:
    return OrderItemService(db)

def _get_order_service(db: Session = Depends(get_session)) -> OrderService:
    return OrderService(db)

def _get_product_service(db: Session = Depends(get_session)) -> ProductService:
    return ProductService(db)

OIService = Annotated[OrderItemService, Depends(_get_order_item_service)]
OService = Annotated[OrderService, Depends(_get_order_service)]
PService = Annotated[ProductService, Depends(_get_product_service)]

@router.get("/", status_code=status.HTTP_200_OK)
def get_order_items(service: OIService) -> list[GetOrderItemDTO]:
    return service.get_all_order_items()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_order_item(order_item_dto: CreateOrderItemDTO, order_item_service: OIService, product_service: PService, order_service: OService) ->  int:
    product_service._get_product_by_id(order_item_dto.product_id) # Ensure product exists
    order_service._get_order_by_id(order_item_dto.order_id) # Ensure order exists
    return order_item_service.create_order_item(order_item_dto)

@router.put("/{order_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_order_item(order_item_id: int, order_item_dto: UpdateOrderItemDTO, order_item_service: OIService, product_service: PService, order_service: OService) -> None:
    product_service._get_product_by_id(order_item_dto.product_id) # Ensure product exists
    order_service._get_order_by_id(order_item_dto.order_id) # Ensure order exists
    order_item_service.update_order_item(order_item_id, order_item_dto)

@router.delete("/{order_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_item(order_item_id: int, order_item_service: OIService) -> None:
    order_item_service.delete_order_item(order_item_id)