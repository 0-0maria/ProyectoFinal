from pydantic import BaseModel
from datetime import date

class UsuarioRegistro(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ServicioCreate(BaseModel):
    nombre: str
    precio: float

class ClienteServicioCreate(BaseModel):
    idservicio: int
    fecha: date
    cliente: str