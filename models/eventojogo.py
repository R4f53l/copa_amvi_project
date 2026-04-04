from sqlalchemy import Column, Integer, ForeignKey, String
from database import Base
from sqlalchemy.orm import relationship

class EventoJogo(Base):
    __tablename__ = "eventos_jogo"
    id_evento_jogo = Column(Integer, primary_key=True, index=True)
    id_jogo = Column(ForeignKey("jogos.id_jogo"), nullable=False)    
    id_tipo_evento = Column(ForeignKey("tipos_evento.id_tipo_evento"), nullable=False)    
    minuto_ocorrido = Column(Integer, nullable=False)
    descricao = Column(String, nullable=True)
    criado_por = Column(ForeignKey("usuarios.id"), nullable=False)

    jogo = relationship("Jogo", back_populates="eventos")

    # Vai para o Tipo de Evento (Gol, Cartão, etc)
    tipo_evento = relationship("TipoEvento")

    # Vai para os Participantes (Quem fez o gol, etc)
    participantes = relationship("EventoParticipante", back_populates="eventos")