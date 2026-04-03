from pydantic import BaseModel
from datetime import date 

class Jogo_Schema(BaseModel):
    id_time_casa: int
    id_time_visitante: int
    id_campeonato: int
    data_hora: date
    fase: str
    grupo: str
    gols_time_casa: int
    gols_time_visitante: int
    id_estadio: int

    class config:
        from_attributes = True
    


