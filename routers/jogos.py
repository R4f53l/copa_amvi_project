from fastapi import APIRouter, Depends, HTTPException
from core.security import verificar_admin
from database import get_db
from sqlalchemy.orm import Session
from models.time import Time
from models.usuario import Usuario
from schemas.jogo_schema import Jogo_Schema
from models.jogo import Jogo

jogos_router = APIRouter(prefix = "/jogos", tags = ["jogos"])

@jogos_router.post("/criar")
async def criar_jogo(jogo_schema: Jogo_Schema,session: Session = Depends(get_db), usuario: Usuario = Depends(verificar_admin)):
    jogo_atual = session.query(Jogo).filter(Jogo.id_time_casa == jogo_schema.id_time_casa, Jogo.id_time_visitante == jogo_schema.id_time_visitante, Jogo.data_hora == jogo_schema.data_hora).first()
    if jogo_atual:
        raise HTTPException(status_code = 400, detail = "Jogo já existe!")
    novo_jogo = Jogo(id_time_casa = jogo_schema.id_time_casa, id_time_visitante = jogo_schema.id_time_visitante, id_campeonato = jogo_schema.id_campeonato, data_hora = jogo_schema.data_hora, fase = jogo_schema.fase, grupo = jogo_schema.grupo, gols_time_casa = jogo_schema.gols_time_casa, gols_time_visitante = jogo_schema.gols_time_visitante, id_estadio = jogo_schema.id_estadio, criado_por = usuario.id)
    session.add(novo_jogo)
    session.commit()
    return {"message": "Jogo criado com sucesso!", "jogo": novo_jogo, "criado_por" : usuario.nome}

@jogos_router.get("/listar")
async def listar_jogos(session: Session = Depends(get_db)):
    jogos = session.query(Jogo).first()
    time1 = session.query(Time).filter(Time.id_time == jogos.id_time_casa).first()
    time2 = session.query(Time).filter(Time.id_time == jogos.id_time_visitante).first()
    return {
        time1.nome: jogos.gols_time_casa,
        time2.nome: jogos.gols_time_visitante,
    }