from fastapi import APIRouter, Depends
from schemas.estadio_schema import EstadioSchema
from sqlalchemy.orm import Session
from models.estadio import Estadio
from database import SessionLocal, get_db

estadio_router = APIRouter(prefix = "/estadio", tags=["estadio"])

@estadio_router.post("/")
async def create_estadio(estadio_schema: EstadioSchema, session: Session = Depends(get_db)):    
    estadio = session.query(Estadio).filter(Estadio.nome == estadio_schema.nome , Estadio.cidade == estadio_schema.cidade).first()
    if estadio:
        return {"message": "Estádio já existe!"}    
    novo_estadio = Estadio(nome=estadio_schema.nome, cidade=estadio_schema.cidade, capacidade=estadio_schema.capacidade)
    session.add(novo_estadio)
    session.commit()    
    return {"message": "Estádio criado com sucesso!", "estadio": novo_estadio}

