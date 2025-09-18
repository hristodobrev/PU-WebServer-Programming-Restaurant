from pydantic import BaseModel

# Tables
class CreateTableDTO(BaseModel):
    number: int

class GetTableDTO(BaseModel):
    id: int
    number: int

class UpdateTableDTO(BaseModel):
    number: int

# Products
class CreateProductDTO(BaseModel):
    name: str
    price: float

class GetProductDTO(BaseModel):
    id: int
    name: str
    price: float

class UpdateProductDTO(BaseModel):
    name: str
    price: float

# Orders
class CreateOrderDTO(BaseModel):
    table_id: int

class GetOrderDTO(BaseModel):
    id: int
    table: GetTableDTO

class UpdateOrderDTO(BaseModel):
    table_id: int