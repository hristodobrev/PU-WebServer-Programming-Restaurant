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
    products: list[GetProductDTO]

class UpdateOrderDTO(BaseModel):
    table_id: int

# OrderItems
class CreateOrderItemDTO(BaseModel):
    order_id: int
    product_id: int
    quantity: int

class GetOrderItemDTO(BaseModel):
    id: int
    order: GetOrderDTO
    product: GetProductDTO
    quantity: int

class UpdateOrderItemDTO(BaseModel):
    order_id: int
    product_id: int
    quantity: int

# Users
class CreateUserDTO(BaseModel):
    username: str
    password: str
    role: str = 'user'

class GetUserDTO(BaseModel):
    id: int
    username: str
    role: str
    hashed_password: str