from fastapi import APIRouter, HTTPException

from core.security import verificar_admin
from database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from models.jogador import Jogador

from schemas.jogador_schema import JogadorSchema
jogadores_router = APIRouter(prefix = "/jogadores", tags=["jogadores"])



@jogadores_router.post("/criar_jogador")
async def criar_jogador(jogador_schema: JogadorSchema, session: Session = Depends(get_db), usuario = Depends(verificar_admin)):  
    jogador = session.query(Jogador).filter(Jogador.nome == jogador_schema.nome, Jogador.data_nascimento == jogador_schema.data_nascimento).first()
    if jogador:
        raise HTTPException(status_code = 400, detail = "Jogador já existe!")
    novo_jogador = Jogador(nome=jogador_schema.nome, posicao=jogador_schema.posicao, data_nascimento=jogador_schema.data_nascimento)
    session.add(novo_jogador)
    session.commit()
    session.refresh(novo_jogador)
    return {"message": "Jogador criado com sucesso!", "jogador": novo_jogador.nome}




