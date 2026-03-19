from fastapi import APIRouter
import asyncio
from typing import Optional
from app.data.database import usuarios

routerV = APIRouter(
    tags=["Inicio"]
)

#Endpoints
@routerV.get("/")
async def bienvenida():
    return {"mensaje": "Bienvenido a FastAPI"}

@routerV.get("/holaMundo")
async def hola():
    await  asyncio.sleep(5)#peticion, consultaBD, Archivo.
    return {
            "mensaje":"Hola Mundo FastAPI",
            "status":"200"
            }

@routerV.get("/v1/ParametroOb/{id}")
async def consultauno(id:int):

    return {"mensaje": "Usuario encontrado", 
            "usuario":id,
            "status":"200"
            }

@routerV.get("/v1/ParametroOp/")
async def consultatodos(id:Optional[int]=None):
    if id is not None: 
        for usuariok in usuarios:
            if usuariok["id"] == id:
                return {"mensaje":"Usuario encontrado","usuario":usuariok,"status":"200"}
        return {"mensaje":"Usuario no encontrado","status":"200"}
    else:
        return {"mensaje":"No se proporciono un id","status":"200"}
