from typing import List
from datetime import datetime, timezone
from models.escalacao import Escalacao
from fastapi import APIRouter, Depends, HTTPException
from core.security import verificar_admin
from database import get_db
from sqlalchemy.orm import Session, joinedload
from models.eventojogo import EventoJogo
from models.eventoparticipante import EventoParticipante
from models.time import Time
from models.tipoevento import TipoEvento
from models.usuario import Usuario
from schemas.escalacaoschema import EscalacaoSchema
from schemas.jogo_schema import Jogo_Schema
from models.jogo import Jogo
from models.jogadortime import JogadorTime


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


from sqlalchemy.orm import joinedload

@jogos_router.get("/listar_jogos_em_andamento")
async def listar_jogos_em_andamento(session: Session = Depends(get_db)):
    # O joinedload diz ao SQLAlchemy: "Já traz os objetos Time junto com o Jogo"
    jogos = session.query(Jogo).options(
        joinedload(Jogo.time_casa),
        joinedload(Jogo.time_visitante)
    ).filter(Jogo.status == "em_andamento").all()

    # Agora o loop apenas lê o que já está na memória (Zero novas consultas ao banco!)
    return [
        {
            "id_jogo": jogo.id_jogo,
            "time_casa": jogo.time_casa.nome,
            "gols_time_casa": jogo.gols_time_casa,
            "time_visitante": jogo.time_visitante.nome,
            "gols_time_visitante": jogo.gols_time_visitante,
            "data_hora": jogo.data_hora,
            "fase": jogo.fase,
            "grupo": jogo.grupo
        } for jogo in jogos
    ]

@jogos_router.get("/listar_jogos_agendados")
async def listar_jogos_agendados(session: Session = Depends(get_db)):
    # O joinedload diz ao SQLAlchemy: "Já traz os objetos Time junto com o Jogo"
    jogos = session.query(Jogo).options(
        joinedload(Jogo.time_casa),
        joinedload(Jogo.time_visitante)
    ).filter(Jogo.status == "agendado").all()

    # Agora o loop apenas lê o que já está na memória (Zero novas consultas ao banco!)
    return [
        {
            "id_jogo": jogo.id_jogo,
            "time_casa": jogo.time_casa.nome,
            "gols_time_casa": jogo.gols_time_casa,
            "time_visitante": jogo.time_visitante.nome,
            "gols_time_visitante": jogo.gols_time_visitante,
            "data_hora": jogo.data_hora,
            "fase": jogo.fase,
            "grupo": jogo.grupo
        } for jogo in jogos
    ]

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
    # Buscamos o jogo e JÁ TRAZEMOS os times, eventos e participantes numa tacada só
    jogo = session.query(Jogo).options(
        joinedload(Jogo.time_casa),
        joinedload(Jogo.time_visitante),
        joinedload(Jogo.eventos).joinedload(EventoJogo.tipo_evento),
        joinedload(Jogo.eventos).joinedload(EventoJogo.participantes).joinedload(EventoParticipante.jogador),
        joinedload(Jogo.eventos).joinedload(EventoJogo.participantes).joinedload(EventoParticipante.papel)
    ).filter(Jogo.id_jogo == id_jogo).first()

    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")

    
    return {
        "id_jogo": jogo.id_jogo,
        "placar": f"{jogo.time_casa.nome} {jogo.gols_time_casa} x {jogo.gols_time_visitante} {jogo.time_visitante.nome}",
        "status": jogo.status,
        "eventos": [
            {
                "minuto": ev.minuto_ocorrido,
                "tipo": ev.tipo_evento.nome,
                "descricao": ev.descricao,
                "participantes": [
                    {
                        "nome": p.jogador.jogador.nome if p.jogador else "N/A",
                        "papel": p.papel.nome
                    } for p in ev.participantes
                ]
            } for ev in sorted(jogo.eventos, key=lambda x: x.minuto_ocorrido)
        ]
    }


@jogos_router.post("/escalacao/{id_jogo}")
async def definir_escalacao (id_jogo: int, escalacao: List[EscalacaoSchema], session: Session = Depends(get_db), usuario: Usuario = Depends(verificar_admin)):
    jogo = session.query(Jogo).filter(Jogo.id_jogo == id_jogo).first()
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")    

    for item in escalacao: 
        nova_escalacao = Escalacao(id_jogo=item.id_jogo, id_jogador=item.id_jogador, titular=item.titular)
        session.add(nova_escalacao)    
    session.commit()
    return {"message": "Escalação definida com sucesso!"}

@jogos_router.get("/escalacao/{id_jogo}")
async def obter_escalacao(id_jogo: int, session: Session = Depends(get_db)): 
    # Usamos o joinedload em cadeia para trazer tudo de uma vez
    escalacao = session.query(Escalacao).options(
        joinedload(Escalacao.jogador_time).joinedload(JogadorTime.jogador)
    ).filter(Escalacao.id_jogo == id_jogo).all()

    if not escalacao:
        raise HTTPException(status_code=404, detail="Escalação não encontrada")
    
    # Agora acessamos os dados como atributos do objeto
    return [
        {
            "nome": item.jogador_time.jogador.nome,
            "titular": item.titular,
            "Nome do Time": item.jogador_time.time.nome # Se você tiver essa coluna na escalação
        } for item in escalacao
    ]