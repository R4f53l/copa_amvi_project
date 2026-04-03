from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False) #inicialmente, todos os usuários serão admin. Não há necessidade de aba para  usuários comuns.
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime(timezone = True), server_default=func.now()) #basicamente, pega o horario do meu banco.