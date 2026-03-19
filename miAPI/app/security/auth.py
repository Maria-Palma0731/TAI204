#Seguridad con HTTP BASIC
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()
def verificar_peticion(credenciales:HTTPBasicCredentials = Depends(security)):
    usuarioAuth= secrets.compare_digest(credenciales.username,"maria")
    contraAuth = secrets.compare_digest(credenciales.password, "123456")

    if not (usuarioAuth and contraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas",
        )
    return credenciales.username