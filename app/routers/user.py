### Continuar pag 36


from fastapi import APIRouter, Depends
from app.schemas import User,UserId,usuarios
from app.db.database import get_db
from sqlalchemy import Session
from app.db import models

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.get("/ruta1")
def ruta1():
    return{"mensaje": "Hemos creado nuestra primera API!!"}

@router.get("/obtener_usuario")
def ruta2(user:User):
    print(user)
    print(user.nombre)
    print(user.model_dump())
    return True

@router.post("/crar_usuario")
def crear_usuario(user:User):
    usuario = user.model_dump()
    usuarios.append(usuario)
    return {"Respuesta": "Usuario creado!"}

@router.get("/")
def obtener_usuarios(db:Session=Depends(get_db)):
    data=db.query(models.User).all()
    print(data)
    return usuarios

@router.get("/users/{user_id}")
def obtener_usuario(user_id:int):
    for user in usuarios:
        if user["id"] == user_id:
            print(user, type(user))
            return user
        return {"Respuesta": "Usuario no encontrado"}
    
@router.post("/userjson")
def obtener_usuario_json(user_id:UserId):
    for user in usuarios:
        if user["id"] == user_id.id:
            return{"usuario":user}
        return{"respuesta":"Usuario no encontrado"}
    
@router.delete("/user/{user_id}")
def eliminar_usuario(user_id:int):
    for index,user in enumerate(usuarios):
        if user["id"] == user_id:
            print(index,user)
            usuarios.pop(index)
            return {"Respuesta": "Usuario eliminado correctamente"}
        return {"Respuesta": "Usuario no encontrado"}
       
@router.put("/user/{user_id}")
def actualizar_usuario(user_id:int, updateUser:User):
    for index, user in enumerate(usuarios):
        if user["id"] == user_id:
            usuarios[index]["id"] = updateUser.model_dump()["id"]
            usuarios[index]["nombre"] = updateUser.model_dump()["nombre"]
            usuarios[index]["apellido"] = updateUser.model_dump()["apellido"]
            usuarios[index]["direccion"] = updateUser.model_dump()["direccion"]
            usuarios[index]["telefono"] = updateUser.model_dump()["telefono"]
            return {"Respuesta": "Usuario actualizado correctamente"}
    return {"Respuesta": "Usuario no encontrado"}