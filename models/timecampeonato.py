from sqlalchemy import Column, ForeignKey, Integer, String, Date
from database import Base

class TimeCampeonato(Base):
    __tablename__ = "times_campeonato"
    id_time_campeonato = Column(Integer, primary_key=True, index=True)
    id_time = Column(ForeignKey("times.id_time"), nullable=False)
    id_campeonato = Column(ForeignKey("campeonatos.id_campeonato"), nullable=False)
    grupo = Column(String, nullable=False)