from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, scoped_session
import os

# Creamos la carpeta database si no existe (necesario en producción)
os.makedirs("database", exist_ok=True)

engine = create_engine(
    'sqlite:///database/TorneoJuegos.db',
    connect_args={'check_same_thread': False}
)

# Sesión segura por hilo
Session = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False))
db_session = Session

# Base para modelos
class base(DeclarativeBase):
    pass