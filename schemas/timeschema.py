from pydantic import BaseModel

class TimeSchema(BaseModel):
    nome: str
    cidade: str    

    class Config:
        from_attributes = True