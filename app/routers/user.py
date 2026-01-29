from fastapi import APIRouter, Depends
from app.schemas import User, UserId, ShowUser, UpdateUser
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.db import models
from typing import List

usuarios = []

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

"""

# Metodos sin BD

@router.ger("/ruta1")
def ruta1():
    return {"Mensaje" : "Hemos creado nuestra primera API"}

@router.post("/user")
def obtener_usuarios():
    return usuarios

@router.post("/user")
def crear_usuario(user:User):
    usuario = user.model_dump()
    usuarios.append(usuario)
    return {"Respuesta": "Usuario creado"}

@router.post("/user/{user_id}")
def obtener_usuario(user_id:int):
    for user in usuarios:
        if user["id"] == user_id:
            return{"Usuario" : user}
        return {"Respuesta": "Usuario no encontrado"}
    
@router.post("/userjson")
def obtener_usuario_json(user_id:UserId):
    for user in usuarios:
        if user["id"] == user_id.id:
            return{"usuario": user}
        return{"Respuesta": "Usuario no encontrado"}
    
@router.delete("/user/{user_id}")
def eliminar_usuario(user_id:int):
    for index, user in enumerate(usuarios):
        if user["id"] == user_id:
            usuarios.pop(index)
            return {"Respuesta": "Usuario eliminado"}
        return{"Respuesta": "Usuario no encontrado"}
    
@router.put("/user/{user_id}")
def actualizar_usuario(user_id:int, updateUser:User):
    for index, user in enumerate(usuarios):
        if user["id"] == user_id:
            usuarios[index]["id"] = updateUser.model_dump()["id"]
            usuarios[index]["nombre"] = updateUser.model_dump()["nombre"]
            usuarios[index]["apellido"] = updateUser.model_dump()["apellido"]
            usuarios[index]["direccion"] = updateUser.model_dump()["direccion"]
            usuarios[index]["telefono"] = updateUser.model_dump()["telefono"]
            return{"Respuesta": "Usuario actualizado correctamente"}
        return {"Respuesta": "Usuario NO encontrado"}
    
"""

# Metodos BD

@router.get("/", response_model=List[ShowUser])
def obtener_usuarios(db:Session=Depends(get_db)):
    data = db.query(models.User).all()
    print(data)
    return usuarios

@router.post("/")
def crear_usuario(user:User, db:Session=Depends(get_db)):
    usuario = user.model_dump()
    nuevo_usuario = models.User(
        username = usuario["username"],
        password = usuario["password"],
        nombre = usuario["nombre"],
        apellido = usuario["apellido"],
        direccion = usuario["direccion"],
        telefono = usuario["telefono"],
        correo = usuario["correo"],
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return{"Respuesta": "Usuario creado"}

@router.get("/{user_id}", response_model=ShowUser)
def obtener_usuario(user_id:int, db:Session=Depends(get_db)):
    usuario = db.query(models.User).filter(models.User.id == user_id).first()
    if not usuario:
        return {"Respuesta": "Usuario no encontrado"}
    return usuario

@router.delete("/{user_id}")
def eliminar_usuario(user_id:int, db:Session=Depends(get_db)):
    usuario = db.query(models.User).filter(models.User.id == user_id).first()
    if not usuario:
        return {"Respuesta": "Usuario no encontrado"}
    db.delete(usuario)
    db.commit()
    return {"Respuesta": "Usuario eliminado correctamente"}

@router.patch("/{user_id}")
def actualizar_usuario(user_id:int, updateUser:UpdateUser, db:Session=Depends(get_db)):
    usuario = db.query(models.User).filter(models.User.id == user_id)
    if not usuario.first():
        return {"Respuesta": "Usuario no encontrado"}
    usuario.update(updateUser.model_dump(exclude_unset=True))
    db.commit()
    return {"Respuesta", "Usuario actualizado correctamente"}