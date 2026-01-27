from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    password: str
    nombre: str
    apellido: str
    direccion: str
    telefono: int
    correo: str

class ShowUser(BaseModel):
    username: str
    nombre: str
    correo: str

    class Config:
        orm_mode = True

class UpdateUser(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[int] = None
    correo: Optional[str] = None
    estado: Optional[bool] = None
