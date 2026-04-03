from fastapi import APIRouter

from core.security import verificar_admin
from database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from models.time import Time
from schemas.timeschema import TimeSchema
from fastapi import HTTPException
from schemas.jogadortimeschema import JogadorTimeSchema
from models.jogadortime import JogadorTime
from models.jogador import Jogador

timesjogadores_router = APIRouter(prefix = "/timesjogadores", tags = ["timesjogadores"])

@timesjogadores_router.post("/adicionar_jogador_time")
async def adicionar_jogador_time(jogadortime_schema: JogadorTimeSchema, session: Session = Depends(get_db), usuario = Depends(verificar_admin)):
    jogador = session.query(Jogador).filter(Jogador.id_jogador == jogadortime_schema.id_jogador).first()
    if not jogador: 
        raise HTTPException(status_code = 404, detail = "Jogador não encontrado!")
    time = session.query(Time).filter(Time.id_time == jogadortime_schema.id_time).first()
    if not time: 
        raise HTTPException(status_code = 404, detail = "Time não encontrado!")
    if jogadortime_schema.data_fim and jogadortime_schema.data_fim < jogadortime_schema.data_inicio:
        raise HTTPException(status_code = 400, detail = "data_fim não pode ser menor que data_inicio")
    jogador_time = session.query(JogadorTime).filter(JogadorTime.id_jogador == jogadortime_schema.id_jogador, JogadorTime.id_time == jogadortime_schema.id_time, JogadorTime.id_campeonato == jogadortime_schema.id_campeonato, JogadorTime.data_fim == None).first()
    if jogador_time: 
        raise HTTPException(status_code = 400, detail = "Jogador já está nesse time para esse campeonato!")
    novo_jogador_time = JogadorTime(id_jogador = jogadortime_schema.id_jogador, id_time = jogadortime_schema.id_time, id_campeonato = jogadortime_schema.id_campeonato, numero_camisa = jogadortime_schema.numero_camisa, data_inicio = jogadortime_schema.data_inicio, data_fim = jogadortime_schema.data_fim)
    session.add(novo_jogador_time)
    session.commit()
    return {"message": f"Jogador {jogador.nome} adicionado ao time {time.nome} para o campeonato {jogadortime_schema.id_campeonato} com sucesso!"}