from fastapi import APIRouter, Depends, HTTPException
from main import bcrypt_context, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from database import get_db
from core.security import verificar_token
from sqlalchemy.orm import Session
from models.usuario import Usuario
from schemas.usuario_schema import UsuarioSchema
from schemas.login_schema import LoginSchema
from schemas.refreshschema import RefreshSchema
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix = "/auth", tags=["auth"])

def create_access_token(id_usuario: int, role: str, duracao_token = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    payload = {"sub": str(id_usuario), "role": role, "iat": datetime.now(timezone.utc), "type": "access", "exp": data_expiracao}
    token = jwt.encode (payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def create_refresh_token(id_usuario: int, role: str, duracao_token = timedelta(days=7)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    payload = {"sub": str(id_usuario), "role": role, "iat": datetime.now(timezone.utc), "type": "refresh", "exp": data_expiracao}
    token = jwt.encode (payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def autenticar_usuario(email: str, senha: str, session: Session = Depends(get_db)):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario or not bcrypt_context.verify(senha, usuario.senha_hash):
        return None
    return usuario

@auth_router.post("/users")
async def create_user(usuario_schema: UsuarioSchema, session: Session = Depends(get_db)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code = 400, detail = "Email já cadastrado!")  
    new_password = bcrypt_context.hash(usuario_schema.senha)
    novo_usuario = Usuario(nome=usuario_schema.nome, email=usuario_schema.email, senha_hash=new_password, is_admin=usuario_schema.is_admin, ativo=usuario_schema.ativo, criado_em=usuario_schema.criado_em)
    session.add(novo_usuario)
    session.commit()    
    return {"message": "Usuário criado com sucesso!", "usuario": usuario_schema.email}

@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_db)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code = 401, detail = "Email ou senha inválidos!")
    access_token = create_access_token(usuario.id, role = "admin" if usuario.is_admin else "user")
    refresh_token = create_refresh_token(usuario.id, role = "admin" if usuario.is_admin else "user") #token de refresh tem duração maior
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"} #basicamente segue um padrao OAuth2

@auth_router.post("/login_forms")
async def login_form(dados_forms: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    usuario = autenticar_usuario(dados_forms.username, dados_forms.password, session)
    if not usuario:
        raise HTTPException(status_code = 401, detail = "Email ou senha inválidos!")
    access_token = create_access_token(usuario.id, role = "admin" if usuario.is_admin else "user")    
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/refresh")
async def refresh_token(session: Session = Depends(get_db), usuario: Usuario = Depends(verificar_token)):
    access_token = create_access_token(usuario.id, role = "admin" if usuario.is_admin else "user")
    return {"access_token": access_token, "token_type": "bearer"}


