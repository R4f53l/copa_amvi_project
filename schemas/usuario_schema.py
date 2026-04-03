from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UsuarioSchema(BaseModel):  
    nome: str
    email: str
    senha: str
    is_admin: bool
    ativo: Optional[bool] = True
    criado_em: datetime
    class Config: 
        from_attributes = True

