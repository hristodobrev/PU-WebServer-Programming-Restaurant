from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db import get_session
from typing import Annotated
from services.product_service import ProductService
from models.dtos import GetProductDTO, CreateProductDTO, UpdateProductDTO

router = APIRouter(prefix="/api/v1/product", tags=["Products"])

def _get_service(db: Session = Depends(get_session)) -> ProductService:
    return ProductService(db)

Service = Annotated[ProductService, Depends(_get_service)]

@router.get("/", status_code=status.HTTP_200_OK)
def get_products(service: Service) -> list[GetProductDTO]:
    return service.get_all_products()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(product_dto: CreateProductDTO, service: Service) -> int:
    return service.create_product(product_dto)

@router.put("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_product(product_id: int, product_dto: UpdateProductDTO, service: Service) -> None:
    service.update_product(product_id, product_dto)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, service: Service) -> None:
    service.delete_product(product_id)  