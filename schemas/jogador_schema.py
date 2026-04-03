from pydantic import BaseModel
from datetime import date

class JogadorSchema(BaseModel):    
    nome: str
    posicao: str
    data_nascimento: date

    class Config:
        from_attributes = True