from fastapi import APIRouter, HTTPException

from core.security import verificar_admin
from database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from models.eventojogo import EventoJogo
from models.tipoevento import TipoEvento
from models.jogo import Jogo
from models.usuario import Usuario
from schemas.jogoeventoschema import JogoEventoSchema
from models.papelevento import PapelEvento
from models.eventoparticipante import EventoParticipante
from services.evento_consequencia import MAPA_EVENTOS
jogo_eventos_router = APIRouter(prefix = "/jogo_eventos", tags=["jogo_eventos"])


@jogo_eventos_router.post("/registrar_evento/{id_jogo}")
async def registrar_evento(id_jogo: int, evento_schema: JogoEventoSchema, session: Session = Depends(get_db), usuario: Usuario = Depends(verificar_admin)):

    jogo = session.query(Jogo).filter(Jogo.id_jogo == id_jogo).first()
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")

    tipo_evento = session.query(TipoEvento).filter(TipoEvento.id_tipo_evento == evento_schema.tipo_evento).first()
    if not tipo_evento:
        raise HTTPException(status_code=404, detail="Tipo de evento não encontrado")
    
    novo_evento = EventoJogo(
        id_jogo=id_jogo, 
        id_tipo_evento=evento_schema.tipo_evento, 
        minuto_ocorrido=evento_schema.minuto, 
        criado_por=usuario.id
    )
    session.add(novo_evento)
    session.flush() # O flush gera o ID do evento sem fechar a transação
    
    for p in evento_schema.participantes:
        participante = EventoParticipante(
            id_evento_jogo=novo_evento.id_evento_jogo, 
            id_time=p.id_time, 
            id_jogador_time=p.id_jogador, 
            papel_id=p.papel
        )
        session.add(participante)

    
    funcao_acao = MAPA_EVENTOS.get(tipo_evento.acao_slug) 
    if funcao_acao:        
        funcao_acao(session, jogo, evento_schema, tipo_evento)

    
    session.commit()
    session.refresh(jogo) 

    return {
        "message": "Evento registrado com sucesso!", 
        "placar_atual": {
            jogo.time_casa.nome: jogo.gols_time_casa, 
            jogo.time_visitante.nome: jogo.gols_time_visitante
        }
    }

    


@jogo_eventos_router.post("/deletar_evento/{evento_id}")
async def deletar_evento(evento_id: int, session: Session = Depends(get_db), usuario: Usuario = Depends(verificar_admin)):
    evento = session.query(EventoJogo).filter(EventoJogo.id_evento_jogo == evento_id).first()
    if not evento:
        raise HTTPException(status_code = 404, detail = "Evento não encontrado!")
    session.delete(evento)
    session.commit()
    return {"message": f"Evento {evento_id} deletado com sucesso!"}