from fastapi import status, HTTPException, Depends, APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["CRUD HTTP"]
)

@router.get("/")
async def consultaT():
    return {
            "status":"200",
            "total":len(usuarios),
            "Usuarios":usuarios
            }

@router.post("/")
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

@router.put("/{id}")
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

@router.delete("/{id}")
async def eliminar_usuario(id: int, usuario: str = Depends(verificar_peticion)):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario_eliminado = usuarios.pop(idx)
            return {
                "mensaje": f"Usuario eliminado por {usuario}"
            }
    
    raise HTTPException(
        status_code=404,
        detail=f"Usuario con id {id} no encontrado"
    )