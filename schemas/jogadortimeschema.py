from pydantic import BaseModel
from datetime import date 

class JogadorTimeSchema(BaseModel):
    id_time: int
    id_jogador: int
    id_campeonato: int
    numero_camisa: int
    data_inicio: date 
    data_fim: date | None = None #aceita date ou none mas o padrão é none incialmente

    class config:
        from_attributes = True
