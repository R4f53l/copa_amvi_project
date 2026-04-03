from sqlalchemy import Column, Integer, String, Date
from database import Base

class Jogador(Base):
    __tablename__ = "jogadores"

    id_jogador = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    posicao = Column(String, nullable=False)
    data_nascimento = Column(Date, nullable=True)
    #criar um campo na tabela para armazenar o status do jogador (ativo ou aposentado)

