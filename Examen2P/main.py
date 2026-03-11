from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI(
    title="Sistema de turnos bancarios",
    description="Examen 2do parcial",
    version="1.0.0"
)

class Turno(BaseModel):
    Cliente: str = Field(..., min_length=8, max_length=50, example="Maria Palma")
    Tramite: Literal ["deposito", "retiro", "consulta"]
    FechaTurno: datetime = Field(..., example="2026-03-11 03:20:00")
    Atendido: bool = False

#Autenticacion
security = HTTPBasic()
def verificar_peticion(credenciales:HTTPBasicCredentials = Depends(security)):
    usuarioAuth= secrets.compare_digest(credenciales.username,"Banco")
    contraAuth = secrets.compare_digest(credenciales.password, "2468")

    if not (usuarioAuth and contraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas",
        )
    return credenciales.username



# Endpoint
turnos = [] 

#Crear turnos
@app.post("/v1/turnos/", tags=["Turnos"])
async def crear_turno(turno: Turno):
    fecha_dia = turno.FechaTurno.date()
    turnos_cliente = [t for t in turnos if t.Cliente == turno.Cliente and t.FechaTurno.date() == fecha_dia]
    if len(turnos_cliente) >= 5:
        raise HTTPException(status_code=400, detail="Solo 5 turnos por dia")
    turnos.append(turno)
    return {"mensaje": "Turno creado", "turno": turno}

#Listar turnos

@app.get("/v1/turnos/", tags=["Turnos"])
async def listar_turnos():
    return {"total": len(turnos), "turnos": turnos}

#Consultar turnos
@app.get("/v1/turnos/{id}", tags=["Turnos"])
async def consultar_turno(id: int):
    if id < len(turnos):
        return {"turno": turnos[id]}
    raise HTTPException(status_code=404, detail="Turno no encontrado")

@app.put("/v1/turnos/{id}/atender", tags=["Turnos"])
async def marcar_atendido(id: int, usuario: str = Depends(verificar_peticion)):
    if id < len(turnos):
        turnos[id].Atendido = True
        return {"mensaje": "Turno marcado como atendido", "turno": turnos[id]}
    raise HTTPException(status_code=404, detail="Turno no encontrado")

#Eliminar turno
@app.delete("/v1/turnos/{id}", tags=["Turnos"])
async def eliminar_turno(id: int, usuario: str = Depends(verificar_peticion)):
    if id < len(turnos):
        turno_eliminado = turnos.pop(id)
        return {
            "mensaje": "Turno eliminado correctamente",
            "turno": turno_eliminado,
            "status": "200"
        }
    raise HTTPException(status_code=404, detail="Turno no encontrado")


