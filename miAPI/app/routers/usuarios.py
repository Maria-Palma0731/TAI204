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

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def consultaUno(id: int, db: Session = Depends(get_db)):
    queryUsuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    if queryUsuario is None:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario no encontrado"
        )
    return {
        "mensaje": "Usuario encontrado",
        "usuario": queryUsuario
    }

@router.post("/", status_code=status.HTTP_201_CREATED)
async def agregar_usuario(usuarioP: crear_usuario, db: Session = Depends(get_db)):
    usuarioNuevo = usuarioDB(nombre=usuarioP.nombre, edad=usuarioP.edad)
    db.add(usuarioNuevo)
    db.commit()
    db.refresh(usuarioNuevo)
    return {
        "mensaje": "Usuario agregado", 
        "usuario": usuarioP, 
    }

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_usuario(id: int, usuarioP: crear_usuario, db: Session = Depends(get_db)):
    queryUsuario = db.query(usuarioDB).filter(usuarioDB.id == id). first()
    if queryUsuario is None:
            raise HTTPException(
                status_code=404,
                detail=f"Usuario no encontrado"
            )
    queryUsuario.nombre = usuarioP.nombre
    queryUsuario.edad = usuarioP.edad
    db.commit()
    db.refresh(queryUsuario)
    return {
                "mensaje": "Usuario actualizado",
                "usuario": queryUsuario,
            }

@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_usuario_parcial(id: int, usuarioP: dict, db: Session = Depends(get_db)):
    queryUsuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    if queryUsuario is None:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario no encontrado"
        )
    for campo, valor in usuarioP.items():
        setattr(queryUsuario, campo, valor)
    db.commit()
    db.refresh(queryUsuario)
    return {
        "mensaje": "Usuario se actualizo parcialmente",
        "usuario": queryUsuario
    }

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, usuario: str = Depends(verificar_peticion), db: Session = Depends (get_db)):
    queryUsuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    if queryUsuario is None:
            raise HTTPException(
                 status_code=404,
                 detail=f"Usuario no encontrado"
            )
    db.delete(queryUsuario)
    db.commit()
    return  {
         "mensaje": f"Usuario eliminado por {usuario}"
    }

