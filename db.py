from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, scoped_session
import os

# Creamos la carpeta database si no existe (solo necesario para SQLite local)
os.makedirs("database", exist_ok=True)

# En producción se usa DATABASE_URL (PostgreSQL), en local SQLite
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///database/TorneoJuegos.db")

# Render proporciona "postgres://" pero SQLAlchemy necesita "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# check_same_thread solo es necesario para SQLite
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Sesión segura por hilo
Session = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False))
db_session = Session

# Base para modelos
class base(DeclarativeBase):
    pass
