from pydantic import BaseModel


class EscalacaoSchema(BaseModel):
    id_jogo: int
    id_jogador: int
    titular: bool

    class config: 
        from_attributes = True
