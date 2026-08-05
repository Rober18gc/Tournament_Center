from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, scoped_session

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