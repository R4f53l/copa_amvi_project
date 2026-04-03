from main import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from models.usuario import Usuario
from sqlalchemy.orm import Session
from fastapi.params import Depends
from fastapi import HTTPException
from database import get_db

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login_forms")

def verificar_token(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Token inválido")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    user_id = int(payload.get("sub"))
    if user_id is None:
        raise HTTPException(status_code=401, detail="Token inválido")

    usuario = session.query(Usuario).filter(Usuario.id == user_id).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return usuario

def verificar_admin(usuario: Usuario = Depends(verificar_token)):
    if not usuario.is_admin:
        raise HTTPException(status_code=403, detail="Acesso negado: Admins apenas")
    return usuario

    