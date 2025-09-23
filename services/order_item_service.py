from sqlalchemy.orm import Session
from models.entities import OrderItem
from models.dtos import GetOrderItemDTO, CreateOrderItemDTO, UpdateOrderItemDTO
from fastapi import HTTPException as HttpException
from models.mapper import map_entity_to_get_order_item_dto, map_update_order_item_dto_to_entity, map_create_order_item_dto_to_entity

class OrderItemService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_order_items(self) -> list[GetOrderItemDTO]:
        return [map_entity_to_get_order_item_dto(order_item) for order_item in self.db.query(OrderItem).all()]
    
    def create_order_item(self, order_item_dto: CreateOrderItemDTO) -> int:
        new_order_item = map_create_order_item_dto_to_entity(order_item_dto)
        self.db.add(new_order_item)
        self.db.commit()
        self.db.refresh(new_order_item)
        return new_order_item.id
    
    def update_order_item(self, order_item_id: int, order_item_dto: UpdateOrderItemDTO) -> None:
        order_item = self._get_order_item_by_id(order_item_id)
        map_update_order_item_dto_to_entity(order_item, order_item_dto)
        self.db.commit()

    def delete_order_item(self, order_item_id: int) -> None:
        order_item = self._get_order_item_by_id(order_item_id)
        self.db.delete(order_item)
        self.db.commit()

    def _get_order_item_by_id(self, order_item_id: int) -> OrderItem | None:
        order_item = self.db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
        if order_item is None:
            raise HttpException(status_code=404, detail="Order item not found")
        return order_item