from sqlalchemy.orm import Session
from models.entities import Order
from models.dtos import CreateOrderDTO, GetOrderDTO, UpdateOrderDTO
from fastapi import HTTPException as HttpException
from models.mapper import map_entity_to_get_order_dto, map_update_order_dto_to_entity, map_create_order_dto_to_entity

class OrderService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_orders(self) -> list[GetOrderDTO]:
        return [map_entity_to_get_order_dto(order) for order in self.db.query(Order).all()]

    def create_order(self, order_dto: CreateOrderDTO) -> int:
        order_entity = map_create_order_dto_to_entity(order_dto)
        self.db.add(order_entity)
        self.db.commit()
        self.db.refresh(order_entity)
        return order_entity.id
    
    def update_order(self, order_id: int, order_dto: UpdateOrderDTO) -> None:
        order = self._get_order_by_id(order_id)
        map_update_order_dto_to_entity(order, order_dto)
        self.db.commit()

    def delete_order(self, order_id: int) -> None:
        order = self._get_order_by_id(order_id)
        self.db.delete(order)
        self.db.commit()
    
    def _get_order_by_id(self, order_id: int) -> Order | None:
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if order is None:
            raise HttpException(status_code=404, detail="Order not found")
        return order