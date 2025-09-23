from models.entities import Table, Product, Order, OrderItem
from models.dtos import (
    CreateTableDTO, UpdateTableDTO, GetTableDTO,
    CreateProductDTO, GetProductDTO, UpdateProductDTO,
    CreateOrderDTO, GetOrderDTO, UpdateOrderDTO,
    CreateOrderItemDTO, GetOrderItemDTO, UpdateOrderItemDTO
)

# Tables
def map_create_table_dto_to_entity(dto: CreateTableDTO) -> Table:
    return Table(number=dto.number)

def map_entity_to_get_table_dto(entity: Table) -> GetTableDTO:
    return GetTableDTO(id=entity.id, number=entity.number)

def map_update_table_dto_to_entity(entity: Table, dto: UpdateTableDTO) -> Table:
    entity.number = dto.number
    return entity

# Products
def map_create_product_dto_to_entity(dto: CreateProductDTO) -> Product:
    return Product(name=dto.name, price=dto.price)

def map_entity_to_get_product_dto(entity: Product) -> GetProductDTO:
    return GetProductDTO(id=entity.id, name=entity.name, price=entity.price)

def map_update_product_dto_to_entity(entity: Table, dto: UpdateProductDTO) -> Product:
    entity.name = dto.name
    entity.price = dto.price
    return entity

# Orders
def map_create_order_dto_to_entity(dto: CreateOrderDTO) -> Order:
    order = Order(table_id=dto.table_id)
    return order

def map_entity_to_get_order_dto(entity: Order) -> GetOrderDTO:
    return GetOrderDTO(
        id=entity.id,
        table=map_entity_to_get_table_dto(entity.table),
        products=[map_entity_to_get_product_dto(oi.product) for oi in entity.order_items]
    )

def map_update_order_dto_to_entity(entity: Order, dto: UpdateOrderDTO) -> Order:
    entity.table_id = dto.table_id
    return entity

# OrderItems
def map_create_order_item_dto_to_entity(dto: CreateOrderItemDTO) -> OrderItem:
    return OrderItem(order_id=dto.order_id, product_id=dto.product_id, quantity=dto.quantity)

def map_entity_to_get_order_item_dto(entity: OrderItem) -> GetOrderItemDTO:
    return GetOrderItemDTO(
        id=entity.id,
        order=map_entity_to_get_order_dto(entity.order),
        product=map_entity_to_get_product_dto(entity.product),
        quantity=entity.quantity
    )

def map_update_order_item_dto_to_entity(entity: OrderItem, dto: UpdateOrderItemDTO) -> OrderItem:
    entity.order_id = dto.order_id
    entity.product_id = dto.product_id
    entity.quantity = dto.quantity
    return entity