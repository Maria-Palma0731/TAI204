
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#1 Definir URL conexion
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://admin:123456@postgres:5432/DB_miapi"
                         )

#2 Crear motor de conexion
engine= create_engine(DATABASE_URL)

#3 Creamos gestion de sesiones
Sessionlocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

#4. Base declarativa para Modelo
Base = declarative_base()

#5. Funcion para trabajar sessiones con las funciones.
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

        