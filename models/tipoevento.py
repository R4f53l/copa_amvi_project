from sqlalchemy import Column, Integer, String, Date
from database import Base

class TipoEvento(Base):
    __tablename__ = "tipos_evento"

    id_tipo_evento = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    acao_slug = Column(String, nullable = False) # coluna para saber qual acao tomar: ex -> atualizar placar, adicionar cartao, etc