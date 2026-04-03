from datetime import datetime

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from core.security import verificar_admin, verificar_token
from database import get_db
from fastapi import Depends 
from models.usuario import Usuario
from schemas.campeonatoschema import CampeonatoSchema
from models.campeonatos import Campeonato

campeonatos_router = APIRouter(prefix = "/campeonatos", tags=["campeonatos"])


@campeonatos_router.post("/criar_campeonato")
async def criar_campeonato(campeonato_schema: CampeonatoSchema, session: Session = Depends(get_db), usuario = Depends(verificar_admin)):
    campeonato = session.query(Campeonato).filter(Campeonato.nome == campeonato_schema.nome, Campeonato.ano == campeonato_schema.ano).first()
    if campeonato:
        raise HTTPException(status_code = 400, detail = "Campeonato já existe!")
    novo_campeonato = Campeonato(nome=campeonato_schema.nome, data_inicio = campeonato_schema.data_inicio, ano=campeonato_schema.ano)
    session.add(novo_campeonato)
    session.commit()
    return {"message": "Campeonato criado com sucesso!", "campeonato": novo_campeonato}

@campeonatos_router.post("/cancelar_campeonato/{campeonato_id}") 
async def cancelar_campeonato(campeonato_id: int, session: Session = Depends(get_db), usuario: Usuario = Depends(verificar_admin)):
    campeonato = session.query(Campeonato).filter(Campeonato.id_campeonato == campeonato_id).first()
    if not campeonato:
        raise HTTPException(status_code = 404, detail = "Campeonato não encontrado!")
    if campeonato.status != "ativo":
        raise HTTPException(status_code = 400, detail = "Campeonato não pode ser cancelado!")
    campeonato.status = "cancelado"
    campeonato.data_fim = datetime.now().date() #marca a data de fim como a data atual para indicar que o campeonato foi cancelado
    session.commit()
    return {"message": f"Campeonato {campeonato.id_campeonato} cancelado com sucesso!", "campeonato": campeonato.nome}

@campeonatos_router.get("/campeonato/listar_campeonatos")
async def listar_campeonatos(session: Session = Depends(get_db)):
    campeonatos = session.query(Campeonato).all()
    return campeonatos

@campeonatos_router.get("/")
def get_campeonatos():
    return {"message": "Lista de campeonatos"}
