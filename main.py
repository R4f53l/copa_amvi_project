from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os 

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from routers import auth, campeonatos, jogo_eventos, times, jogadores, estadio, jogos, timesjogadores

app.include_router(auth.auth_router) #importa o router do auth e inclui ele na aplicação
app.include_router(times.times_router) #inclui as rotas do times na aplicacao 
app.include_router(jogadores.jogadores_router) #inclui as rotas dos jogadores na aplicacao
app.include_router(estadio.estadio_router)
app.include_router(jogos.jogos_router)
app.include_router(campeonatos.campeonatos_router)
app.include_router(jogo_eventos.jogo_eventos_router)
app.include_router(timesjogadores.timesjogadores_router)
app.include_router(times.times_router)
#rodar o codigo: uvicorn main:app --reload