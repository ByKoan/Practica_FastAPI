from app.db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    nombre = Column(String)
    apellido = Column(String)
    direccion = Column(String)
    telefono = Column(Integer)
    correo = Column(String, unique=True)
    estado = Column(Boolean, default=False)
    creacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    ventas = relationship("Venta", back_populates="usuario")


class Venta(Base):
    __tablename__ = "venta"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    usuario = relationship("Usuario", back_populates="ventas")
