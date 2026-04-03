from sqlalchemy import Column, Integer, ForeignKey, String
from database import Base

class PapelEvento(Base):
    __tablename__ = "papeis_evento_participante"
    id_papel = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)