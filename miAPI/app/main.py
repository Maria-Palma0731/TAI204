#importaciones 
from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional
from pydantic import BaseModel, Field

#Instancia del servidor
app = FastAPI(
title="Mi Primer API",
description="MARIA PALMA TORRES",
version="1.0.0"
)

#TB Ficticia de usuarios
usuarios = [
    {"id":1, "nombre":"Maria", "edad":24},
    {"id":2, "nombre":"Guadalupe", "edad":20},
    {"id":3, "nombre":"Artemio", "edad":21}
]

#Modelo de pydantic de validacion.

class crear_usuario(BaseModel):
    id: int=Field(...,gt = 0, description= "identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juanito Doe")
    edad: int = Field(..., ge=1, le= 125, description= "Edad validad entre 1 y 125")



#Endpoints
@app.get("/", tags=["Inicio"])
async def bienvenida():
    return {"mensaje": "Bienvenido a FastAPI"}

@app.get("/holaMundo", tags=["Asincronia"])
async def hola():
    await  asyncio.sleep(5)#peticion, consultaBD, Archivo.
    return {
            "mensaje":"Hola Mundo FastAPI",
            "status":"200"
            }

@app.get("/v1/ParametroOb/{id}", tags=["Parametro obligatorio"])
async def consultauno(id:int):

    return {"mensaje": "Usuario encontrado", 
            "usuario":id,
            "status":"200"
            }

@app.get("/v1/ParametroOp/", tags=["Parametro opcional"])
async def consultatodos(id:Optional[int]=None):
    if id is not None: 
        for usuariok in usuarios:
            if usuariok["id"] == id:
                return {"mensaje":"Usuario encontrado","usuario":usuariok,"status":"200"}
        return {"mensaje":"Usuario no encontrado","status":"200"}
    else:
        return {"mensaje":"No se proporciono un id","status":"200"}

@app.get("/v1/usuarios/", tags=["CRUD HTTP"])
async def consultaT():
    return {
            "status":"200",
            "total":len(usuarios),
            "Usuarios":usuarios
            }


@app.post("/v1/usuarios/", tags=["CRUD HTTP"])
async def crear_usuario(usuario: crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail=f"El id ya existe"
            )
    usuarios.append(usuario)
    return {
        "mensaje": "Usuario agregado", 
        "usuario": usuario, 
        "status": "200"
    }

@app.put("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def actualizar_usuario(id: int, usuario: dict):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario["id"] = id
            usuarios[idx] = usuario
            return {
                "mensaje": "Usuario actualizado",
                "usuario": usuario,
                "status": "200"
            }
    
    raise HTTPException(
        status_code=404,
        detail=f"Usuario con id {id} no encontrado"
    )


@app.delete("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def eliminar_usuario(id: int):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario_eliminado = usuarios.pop(idx)
            return {
                "mensaje": "Usuario eliminado",
                "usuario": usuario_eliminado,
                "status": "200"
            }
    
    raise HTTPException(
        status_code=404,
        detail=f"Usuario con id {id} no encontrado"
    )