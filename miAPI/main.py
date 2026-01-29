#importaciones 
from fastapi import FastAPI 
import asyncio


#Instancia del servidor
app = FastAPI()

#Endpoints
@app.get("/")
async def bienvenida():
    return {"mensaje": "Bienvenido a FastAPI"}

@app.get("/holaMundo")
async def hola():
    await  asyncio.sleep(5)#peticion, consultaBD, Archivo
    return {
            "mensaje":"Hola Mundo FastAPI",
            "status":"200"
            }
