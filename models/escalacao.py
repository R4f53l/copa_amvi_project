from sqlalchemy import Column, Integer, ForeignKey, Boolean
from database import Base

class Escalacao(Base):
    __tablename__ = "escalacoes"

    id_escalacao = Column(Integer, primary_key=True, index=True)
    id_jogo = Column(ForeignKey("jogos.id_jogo"), nullable=False)
    id_jogador = Column(ForeignKey("jogadores_times.id_jogador_time"), nullable=False)
    titular = Column(Boolean, default = False)  # 1 para titular, 0 para reserva

    #relationship
    