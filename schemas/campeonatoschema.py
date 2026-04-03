from datetime import date

from pydantic import BaseModel

class CampeonatoSchema(BaseModel):
    nome: str
    data_inicio: date
    ano: int
    class Config: 
        from_attributes = True