from sqlalchemy import Column, Date, Integer, ForeignKey
from database import Base

class JogadorTime(Base):
    __tablename__ = "jogadores_times"

    id_jogador_time = Column(Integer, primary_key=True, index=True)
    id_jogador = Column(ForeignKey("jogadores.id_jogador"), nullable=False)
    id_time = Column(ForeignKey("times.id_time"), nullable=False)
    id_campeonato = Column(ForeignKey("campeonatos.id_campeonato"), nullable=False)
    numero_camisa = Column(Integer, nullable=False)
    data_inicio = Column(Date, nullable = False)
    data_fim = Column(Date, nullable = True)