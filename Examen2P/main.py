from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, timedelta, timezone

class Turno(BaseModel):
    Cliente: str = Field(..., min_length=8, max_length=50, example="Maria Palma")
    Tramite: Literal["deposito", "retiro", "consulta"]
    FechaTurno: datetime = Field(..., example="2025-10-10 09:30:00")
    Atendido: bool = False


# Endpoint
turnos = [] 

#Crear turnos:
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

#Cambiar a
@app.put("/v1/turnos/{id}/atender", tags=["Turnos"])
async def marcar_atendido(id: int):
    if id < len(turnos):
        turnos[id].Atendido = True
        return {"mensaje": "Turno marcado como atendido", "turno": turnos[id]}
    raise HTTPException(status_code=404, detail="Turno no encontrado")