from sqlalchemy import Column, Integer, ForeignKey, String
from database import Base
from sqlalchemy.orm import relationship

class EventoParticipante(Base):
    __tablename__ = "eventos_participante"
    id_evento_participante = Column(Integer, primary_key=True, index=True)
    id_evento_jogo = Column(ForeignKey("eventos_jogo.id_evento_jogo"), nullable=False)    
    id_time = Column(ForeignKey("times.id_time"), nullable=False)
    id_jogador_time = Column(ForeignKey("jogadores_times.id_jogador_time"), nullable=True)
    papel_id = Column(ForeignKey("papeis_evento_participante.id_papel"), nullable=False)

    eventos = relationship("EventoJogo", back_populates="participantes")

    jogador = relationship("JogadorTime", foreign_keys=[id_jogador_time])

    papel = relationship("PapelEvento", foreign_keys=[papel_id])
