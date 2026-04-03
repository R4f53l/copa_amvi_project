from fastapi import APIRouter

from core.security import verificar_admin
from database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from models.time import Time
from schemas.timeschema import TimeSchema
from fastapi import HTTPException

times_router = APIRouter(prefix = "/times", tags = ["times"])

@times_router.post("/criar_time")
async def criar_time(time_schema: TimeSchema, session: Session = Depends(get_db), usuario = Depends(verificar_admin)):
    time = session.query(Time).filter(Time.nome == time_schema.nome, Time.cidade == time_schema.cidade).first()
    if time: 
        raise HTTPException(status_code = 400, detail = "Time já existe!")
    novo_time = Time(nome = time_schema.nome, cidade = time_schema.cidade)
    session.add(novo_time)
    session.commit()    
    return {"message": "Time criado com sucesso!"}

