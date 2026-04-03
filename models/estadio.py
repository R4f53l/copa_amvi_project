from sqlalchemy import Column, Integer, ForeignKey, String
from database import Base

class Estadio(Base):
    __tablename__ = "estadio"

    id_estadio = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    capacidade = Column(Integer, nullable= True)