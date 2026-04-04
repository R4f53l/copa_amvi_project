from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from core.security import verificar_admin
from database import get_db
from sqlalchemy.orm import Session
from models.eventojogo import EventoJogo
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

@jogos_router.post("/iniciar_jogo/{id_jogo}")
async def iniciar_jogo(id_jogo: int, session: Session = Depends(get_db), usuario: Usuario = Depends(verificar_admin)):
    jogo = session.query(Jogo).filter(Jogo.id_jogo == id_jogo).first()
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    
    if jogo.status != "agendado":
        raise HTTPException(status_code=400, detail="Jogo já foi iniciado ou finalizado")
    
    jogo.status = "em_andamento"
    jogo.inicio_real = datetime.now(timezone.utc)
    session.commit()
    
    return {"message": "Jogo iniciado com sucesso!", "id_jogo": id_jogo}

@jogos_router.post("/finalizar_jogo/{id_jogo}")
async def finalizar_jogo(id_jogo: int, session: Session = Depends(get_db), usuario: Usuario = Depends(verificar_admin)):
    jogo = session.query(Jogo).filter(Jogo.id_jogo == id_jogo).first()
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    
    if jogo.status == "finalizado": #a comparação é melhor com finalizado do que com em_andamento, pq o jogo pode estar no intervalo.
        raise HTTPException(status_code=400, detail="O jogo já foi finalizado")
    
    jogo.status = "finalizado"
    jogo.fim_real = datetime.now(timezone.utc)
    session.commit()
    
    return {"message": "Jogo finalizado com sucesso!", "id_jogo": id_jogo}


@jogos_router.get("/listar_jogos_em_andamento")
async def listar_jogos_em_andamento(session: Session = Depends(get_db)):
    jogos_em_andamento = session.query(Jogo).filter(Jogo.status == "em_andamento").all()
    resultado = []
    for jogo in jogos_em_andamento:
        time_casa = session.query(Time).filter(Time.id_time == jogo.id_time_casa).first()
        time_visitante = session.query(Time).filter(Time.id_time == jogo.id_time_visitante).first()
        resultado.append({
            "id_jogo": jogo.id_jogo,
            "time_casa": time_casa.nome,
            "gols_time_casa": jogo.gols_time_casa,
            "time_visitante": time_visitante.nome,
            "gols_time_visitante": jogo.gols_time_visitante,
            "data_hora": jogo.data_hora,
            "fase": jogo.fase,
            "grupo": jogo.grupo
        })
    return resultado

@jogos_router.get("/listar_jogos_agendados")
async def listar_jogos_agendados(session: Session = Depends(get_db)):
    jogos_agendados = session.query(Jogo).filter(Jogo.status == "agendado").all()
    resultado = []
    for jogo in jogos_agendados:
        time_casa = session.query(Time).filter(Time.id_time == jogo.id_time_casa).first()
        time_visitante = session.query(Time).filter(Time.id_time == jogo.id_time_visitante).first()
        resultado.append({
            "id_jogo": jogo.id_jogo,
            "time_casa": time_casa.nome,
            "gols_time_casa": jogo.gols_time_casa,
            "time_visitante": time_visitante.nome,
            "gols_time_visitante": jogo.gols_time_visitante,
            "data_hora": jogo.data_hora,
            "fase": jogo.fase,
            "grupo": jogo.grupo
        })
    return resultado

@jogos_router.get("/listar_jogos_finalizados")
async def listar_jogos_finalizados(session: Session = Depends(get_db)):
    jogos_finalizados = session.query(Jogo).filter(Jogo.status == "finalizado").all()
    resultado = []
    for jogo in jogos_finalizados:
        time_casa = session.query(Time).filter(Time.id_time == jogo.id_time_casa).first()
        time_visitante = session.query(Time).filter(Time.id_time == jogo.id_time_visitante).first()
        resultado.append({
            "id_jogo": jogo.id_jogo,
            "time_casa": time_casa.nome,
            "gols_time_casa": jogo.gols_time_casa,
            "time_visitante": time_visitante.nome,
            "gols_time_visitante": jogo.gols_time_visitante,
            "data_hora": jogo.data_hora,
            "fase": jogo.fase,
            "grupo": jogo.grupo
        })
    return resultado

@jogos_router.get("/sumula_jogo/{id_jogo}")
async def sumula_jogo(id_jogo: int, session: Session = Depends(get_db)):
    jogo = session.query(Jogo).filter(Jogo.id_jogo == id_jogo).first()
    if not jogo: 
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    
    time_casa = session.query(Time).filter(Time.id_time == jogo.id_time_casa).first()
    time_visitante = session.query(Time).filter(Time.id_time == jogo.id_time_visitante).first() 
    eventos = session.query(EventoJogo).filter(EventoJogo.id_jogo == id_jogo).all()
    sumula = {
        "id_jogo": jogo.id_jogo,
        "time_casa": time_casa.nome,
        "gols_time_casa": jogo.gols_time_casa,
        "time_visitante": time_visitante.nome,
        "gols_time_visitante": jogo.gols_time_visitante,
        "data_hora": jogo.data_hora,
        "fase": jogo.fase,
        "grupo": jogo.grupo,
        "eventos": []
    }

    return sumula
