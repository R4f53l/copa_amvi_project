from pydantic import BaseModel
class EstadioSchema(BaseModel):
    nome: str
    cidade: str
    capacidade: int 
    class Config: 
        from_attributes = True