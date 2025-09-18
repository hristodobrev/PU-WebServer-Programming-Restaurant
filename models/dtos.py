from pydantic import BaseModel

class CreateTableDTO(BaseModel):
    number: int

class UpdateTableDTO(BaseModel):
    number: int

class GetTableDTO(BaseModel):
    id: int
    number: int