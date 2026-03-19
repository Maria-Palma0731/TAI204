#importaciones 
from fastapi import FastAPI
from app.routers import usuarios, varios

#Instancia del servidor
app = FastAPI(
title="Mi Primer API",
description="MARIA PALMA TORRES",
version="1.0.0"
)
#Router de Endpoints disponibles
app.include_router(usuarios.router),
app.include_router(varios.routerV)