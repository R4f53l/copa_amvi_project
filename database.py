import os

from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base 
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL) #conexao com o banco //usuario:senha@localhost:porta/nome_banco    
Base = declarative_base()
SessionLocal = sessionmaker(bind = engine)

def get_db():    
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()


        
