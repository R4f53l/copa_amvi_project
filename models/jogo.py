from sqlalchemy import Column, ForeignKey, Integer, String, Date
from database import Base

class Jogo(Base):
    __tablename__ = "jogos"
    id_jogo = Column(Integer, primary_key=True, index=True)
    id_time_casa = Column(ForeignKey("times.id_time"), nullable = False)
    id_time_visitante = Column(ForeignKey("times.id_time"), nullable = False)
    id_campeonato = Column(ForeignKey("campeonatos.id_campeonato"), nullable = False)
    data_hora = Column(Date, nullable = False)
    fase = Column(String, nullable = False)
    grupo = Column(String, nullable = True)
    gols_time_casa = Column(Integer, default = 0)
    gols_time_visitante = Column(Integer, default = 0)
    id_estadio = Column(ForeignKey("estadio.id_estadio"), nullable = False)
    criado_por = Column(ForeignKey("usuarios.id"), nullable = False)