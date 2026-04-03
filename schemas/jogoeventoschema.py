from pydantic import BaseModel
from datetime import datetime
from typing import List
from schemas.participante_schema import ParticipanteSchema

class JogoEventoSchema(BaseModel):    
    id_jogo: int
    tipo_evento: int
    minuto: int    
    participantes: List[ParticipanteSchema]

    class Config: 
        from_attributes = True