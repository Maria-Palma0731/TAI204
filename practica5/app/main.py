from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

app = FastAPI(
    title="Biblioteca Digital",
    description="MARIA PALMA TORRES - Practica 5",
    version="1.0.0"
)

# TB Ficticia
libros = [
    {"id": 1, "nombre": "El libro de la almohada", "autor": "Sei Shonagon", "anio": 1002, "paginas": 320, "estado": "disponible"},
    {"id": 2, "nombre": "Kokoro", "autor": "Natsume Soseki", "anio": 1914, "paginas": 248, "estado": "disponible"},
    {"id": 3, "nombre": "Nieve de primavera", "autor": "Yukio Mishima", "anio": 1969, "paginas": 389, "estado": "disponible"},
    {"id": 4, "nombre": "Haiku: antologia de poesia japonesa", "autor": "Matsuo Basho", "anio": 1689, "paginas": 180, "estado": "disponible"},
    {"id": 5, "nombre": "El mar de la fertilidad", "autor": "Yukio Mishima", "anio": 1970, "paginas": 420, "estado": "disponible"}
]
prestamos = [
    {"id": 3, "nombre": "Nieve de primavera", "autor": "Yukio Mishima", "anio": 1969, "paginas": 389, "estado": "prestado"},
{"id": 5, "nombre": "El mar de la fertilidad", "autor": "Yukio Mishima", "anio": 1970, "paginas": 420, "estado": "prestado"}
]

# Modelos de validacion con pydantic
class Libro(BaseModel):
    id: int = Field(..., gt=0, description="Identificador del libro")
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre del libro")
    autor: str = Field(..., min_length=3, max_length=100, description="Autor del libro")
    anio: int = Field(..., gt=1450, le=datetime.now().year, description="Anio de publicacion")
    paginas: int = Field(..., gt=1, description="Numero de paginas")
    estado: Literal["disponible", "prestado"] = "disponible"

class Prestamo(BaseModel):
    id: int = Field(..., gt=0, description="Identificador del prestamo")
    libro_id: int = Field(..., gt=0, description="Id del libro a prestar")
    usuario_nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del usuario")
    usuario_correo: str = Field(..., min_length=5, max_length=100, description="Correo del usuario")

# Endpoints Libros
@app.get("/v1/libros/", tags=["Libros"])
async def listar_libros():
    disponibles = []
    for l in libros:
        if l["estado"] == "disponible":
            disponibles.append(l)
    return {
        "status": "200",
        "total": len(disponibles),
        "libros": disponibles
    }

@app.post("/v1/libros/", tags=["Libros"], status_code=201)
async def registrar_libro(libro: Libro):
    for l in libros:
        if l["id"] == libro.id:
            raise HTTPException(status_code=400, detail="El id del libro ya existe")
    libros.append(libro.model_dump())
    return {
        "mensaje": "Libro registrado",
        "libro": libro,
        "status": "201"
    }

@app.get("/v1/libros/{nombre}", tags=["Libros"])
async def buscar_libro(nombre: str):
    resultados = []
    for l in libros:
        if nombre.lower() in l["nombre"].lower():
            resultados.append(l)
    if len(resultados) == 0:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return {
        "status": "200",
        "libros": resultados
    }

# Endpoints Prestamos
@app.post("/v1/prestamos/", tags=["Prestamos"], status_code=201)
async def registrar_prestamo(prestamo: Prestamo):
    for p in prestamos:
        if p["id"] == prestamo.id:
            raise HTTPException(status_code=400, detail="El id del prestamo ya existe")
    for l in libros:
        if l["id"] == prestamo.libro_id:
            if l["estado"] == "prestado":
                raise HTTPException(status_code=409, detail="El libro ya esta prestado")
            l["estado"] = "prestado"
            prestamos.append(prestamo.model_dump())
            return {
                "mensaje": "Prestamo registrado",
                "prestamo": prestamo,
                "status": "201"
            }
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.put("/v1/prestamos/{id}/devolver", tags=["Prestamos"])
async def devolver_libro(id: int):
    for p in prestamos:
        if p["id"] == id:
            for l in libros:
                if l["id"] == p["libro_id"]:
                    l["estado"] = "disponible"
            return {
                "mensaje": "Libro devuelto",
                "prestamo": p,
                "status": "200"
            }
    raise HTTPException(status_code=409, detail="El registro de prestamo no existe")

@app.delete("/v1/prestamos/{id}", tags=["Prestamos"])
async def eliminar_prestamo(id: int):
    for idx, p in enumerate(prestamos):
        if p["id"] == id:
            prestamo_eliminado = prestamos.pop(idx)
            return {
                "mensaje": "Prestamo eliminado",
                "prestamo": prestamo_eliminado,
                "status": "200"
            }
    raise HTTPException(status_code=409, detail="El registro de prestamo no existe")
