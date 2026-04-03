from sqlalchemy import Column, Integer, String, Date
from database import Base

class Campeonato(Base):
    __tablename__ = "campeonatos"

    id_campeonato = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=True)
    ano = Column(Integer, nullable=False)
    status = Column(String, default="ativo") #ativo, finalizado, cancelado