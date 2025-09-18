from sqlalchemy.orm import Session
from models.entities import Product
from models.dtos import GetProductDTO
from fastapi import HTTPException as HttpException
from models.mapper import map_entity_to_get_product_dto, map_update_product_dto_to_entity, map_create_product_dto_to_entity

class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_products(self) -> list[GetProductDTO]:
        return [map_entity_to_get_product_dto(product) for product in self.db.query(Product).all()]
    
    def create_product(self, product_dto) -> int:
        new_product = map_create_product_dto_to_entity(product_dto)
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)
        return new_product.id
    
    def update_product(self, product_id: int, product_dto) -> None:
        product = self._get_product_by_id(product_id)
        map_update_product_dto_to_entity(product, product_dto)
        self.db.commit()

    def delete_product(self, product_id: int) -> None:
        product = self._get_product_by_id(product_id)
        self.db.delete(product)
        self.db.commit()
    
    def _get_product_by_id(self, product_id: int) -> Product | None:
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if product is None:
            raise HttpException(status_code=404, detail="Product not found")
        return product