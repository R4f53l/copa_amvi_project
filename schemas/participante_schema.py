from pydantic import BaseModel
from typing  import Optional
class ParticipanteSchema(BaseModel):
    id_jogador: Optional[int]
    id_time: int
    papel: int  

    class Config:
        from_attributes = True