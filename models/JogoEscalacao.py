from database import Base
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime

class JogoEscalacao(Base):
    __tablename__ = "jogo_escalacao"
    id_jogo_escalacao = Column(Integer, primary_key=True, index=True)
    id_jogo = Column(ForeignKey("jogos.id_jogo"), nullable=False)
    id_time = Column(ForeignKey("times.id_time"), nullable=False)
    id_jogador_time = Column(ForeignKey("jogadores_times.id_jogador_time"), nullable=False)
    status = Column(String, nullable=False) # "titular", "reserva", "desfalque"
    criado_por = Column(ForeignKey("usuarios.id"), nullable=False)
    
