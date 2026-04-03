from sqlalchemy import Column, ForeignKey, Integer, String, Date
from database import Base

class Time(Base): 
    __tablename__ = "times"
    id_time = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cidade = Column(String, nullable=False)