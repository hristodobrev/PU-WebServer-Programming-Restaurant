from sqlalchemy.orm import Session
from models.entities import Table
from models.dtos import CreateTableDTO, GetTableDTO, UpdateTableDTO
from models.mapper import map_create_table_dto_to_entity, map_entity_to_get_table_dto, map_update_table_dto_to_entity
from fastapi import HTTPException

class TableService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_tables(self) -> list[GetTableDTO]:
        return [map_entity_to_get_table_dto(t) for t in self.db.query(Table).all()]

    def create_table(self, table_dto: CreateTableDTO) -> int:
        new_table = map_create_table_dto_to_entity(table_dto)
        self.db.add(new_table)
        self.db.commit()
        self.db.refresh(new_table)
        return new_table.id
    
    def update_table(self, table_id: int, table_dto: UpdateTableDTO) -> None:
        table = self._get_table_by_id(table_id)
        map_update_table_dto_to_entity(table, table_dto)
        self.db.commit()
            
    def delete_table(self, table_id: int) -> None:
        table = self._get_table_by_id(table_id)
        self.db.delete(table)
        self.db.commit()

    def _get_table_by_id(self, table_id: int) -> Table | None:
        table = self.db.query(Table).filter(Table.id == table_id).first()
        if table is None:
            raise HTTPException(status_code=404, detail="Table not found")
        return table