from models.entities import Table
from models.dtos import CreateTableDTO, GetTableDTO

def map_create_table_dto_to_entity(dto: CreateTableDTO) -> Table:
    from models.entities import Table
    return Table(number=dto.number)

def map_entity_to_get_table_dto(entity: Table) -> GetTableDTO:
    from models.dtos import GetTableDTO
    return GetTableDTO(id=entity.id, number=entity.number)