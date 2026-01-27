from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas import User, ShowUser, UpdateUser
from app.db.database import get_db
from app.db import models

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.post("/")
def crear_usuario(user: User, db: Session = Depends(get_db)):
    nuevo_usuario = models.Usuario(**user.dict())
    try:
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return {"mensaje": "Usuario creado correctamente"}
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Usuario o correo ya existente")

@router.get("/", response_model=List[ShowUser])
def obtener_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()

@router.get("/{id}", response_model=ShowUser)
def obtener_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.delete("/{id}")
def eliminar_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()
    return {"mensaje": "Usuario eliminado"}

@router.patch("/{id}")
def actualizar_usuario(id: int, user: UpdateUser, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    for key, value in user.dict(exclude_unset=True).items():
        setattr(usuario, key, value)

    db.commit()
    db.refresh(usuario)
    return {"mensaje": "Usuario actualizado"}
