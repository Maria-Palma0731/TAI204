from fastapi import status, HTTPException, Depends, APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as usuarioDB

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["CRUD HTTP"]
)

@router.get("/", status_code=status.HTTP_200_OK)
async def consultaT(db: Session = Depends(get_db)):
    queryUsuarios = db.query(usuarioDB).all()
    return {
            "total":len(queryUsuarios),
            "Usuarios":queryUsuarios
            }

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuarioP: crear_usuario, db: Session = Depends(get_db)):
    usuarioNuevo = usuarioDB(nombre=usuarioP.nombre, edad=usuarioP.edad)
    db.add(usuarioNuevo)
    db.commit()
    db.refresh(usuarioNuevo)
    return {
        "mensaje": "Usuario agregado", 
        "usuario": usuarioP, 
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