from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class Jogo(Base):
    __tablename__ = "jogos"
    id_jogo = Column(Integer, primary_key=True, index=True)
    id_time_casa = Column(ForeignKey("times.id_time"), nullable = False)
    id_time_visitante = Column(ForeignKey("times.id_time"), nullable = False)
    id_campeonato = Column(ForeignKey("campeonatos.id_campeonato"), nullable = False)
    data_hora = Column(DateTime, nullable = False)
    fase = Column(String, nullable = False)
    grupo = Column(String, nullable = True)
    gols_time_casa = Column(Integer, default = 0)
    gols_time_visitante = Column(Integer, default = 0)
    id_estadio = Column(ForeignKey("estadio.id_estadio"), nullable = False)
    criado_por = Column(ForeignKey("usuarios.id"), nullable = False)

    # novos campos: status -> "agendado", "em_andamento", "finalizado" e hora_inicio_real
    status = Column(String, default="agendado", nullable=False)
    inicio_real = Column(DateTime, nullable=True)
    fim_real = Column(DateTime, nullable=True)

    time_casa = relationship("Time", foreign_keys=[id_time_casa]) #isso permite acessar o time usando jogo.time_casa
    time_visitante = relationship("Time", foreign_keys=[id_time_visitante])

    eventos = relationship("EventoJogo", back_populates="jogo") #isso permite acessar os eventos do jogo usando jogo.eventos e posteriormente acessar jogo usando evento.jogo
