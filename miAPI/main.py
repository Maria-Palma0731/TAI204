#importaciones 
from fastapi import FastAPI 
import asyncio
from typing import Optional

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

@app.get("/v1/usuario/{id}", tags=["Parametro obligatorio"])
async def consultauno(id:int):

    return {"mensaje": "Usuario encontrado", 
            "usuario":id,
            "status":"200"
            }

@app.get("/v1/usuarios/", tags=["Parametro opcional"])
async def consultatodos(id:Optional[int]=None):
    if id is not None: 
        for usuariok in usuarios:
            if usuariok["id"] == id:
                return {"mensaje":"Usuario encontrado","usuario":usuariok,"status":"200"}
        return {"mensaje":"Usuario no encontrado","status":"200"}
    else:
        return {"mensaje":"No se proporciono un id","status":"200"}
