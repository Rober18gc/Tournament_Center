from datetime import date
from sqlalchemy import Integer, String, Boolean, Date, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
import db
from typing import Optional


# Tabla Rol
class Rol(db.base):
    __tablename__ = 'rol'
    __table_args__ = {'sqlite_autoincrement': True}

    id_rol: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre_rol: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)

    usuarios: Mapped[list["Usuario"]] = relationship("Usuario", back_populates="rol_obj")

    def __init__(self, nombre_rol):
        self.nombre_rol = nombre_rol



# Tabla Usuario
class Usuario(db.base):
    __tablename__ = 'usuario'
    __table_args__ = {'sqlite_autoincrement': True}

    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(50), nullable=False)
    fecha_nacimiento: Mapped[date] = mapped_column(Date, nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    nombre_usuario: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    fecha_registro: Mapped[date] = mapped_column(Date, nullable=False, default=date.today())
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    id_rol: Mapped[int] = mapped_column(Integer, ForeignKey("rol.id_rol"), nullable=False, default=2)

    # Relaciones
    rol_obj: Mapped["Rol"] = relationship("Rol", back_populates="usuarios")
    creador_torneos: Mapped[list["Torneo"]] = relationship("Torneo", back_populates="usuario_obj")
    participaciones: Mapped[list["Participante_torneo"]] = relationship("Participante_torneo", back_populates="usuario_obj")
    estadisticas_global: Mapped[list["Estadistica_global"]] = relationship("Estadistica_global", back_populates="usuario_obj")
    estadisticas_juego: Mapped[list["Estadistica_juego"]] = relationship("Estadistica_juego", back_populates="usuario_obj")
    ranking: Mapped[list["Ranking_global"]] = relationship("Ranking_global", back_populates="usuario_obj")
    avisos_juegos_borrados: Mapped[list["Aviso_juego_borrado"]] = relationship("Aviso_juego_borrado", back_populates="usuario_obj")
    equipos_capitan: Mapped[list["Equipo"]] = relationship("Equipo", back_populates="capitan_obj", foreign_keys="Equipo.id_capitan")
    membresias: Mapped[list["Miembro_equipo"]] = relationship("Miembro_equipo", back_populates="usuario_obj")

    # Constructor simple sin id_rol
    def __init__(self, nombre, apellidos, fecha_nacimiento, email, nombre_usuario, password, rol_obj=None):
        self.nombre = nombre
        self.apellidos = apellidos
        self.fecha_nacimiento = fecha_nacimiento
        self.email = email
        self.nombre_usuario = nombre_usuario
        self.password = password
        if rol_obj:
            self.rol_obj = rol_obj

# Tabla Genero
class Genero(db.base):
    __tablename__ = 'genero'
    __table_args__ = {'sqlite_autoincrement': True}

    id_genero: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre_genero: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    juegos: Mapped[list["Juego"]] = relationship("Juego", back_populates="genero_obj")

    def __init__(self, nombre_genero):
        self.nombre_genero = nombre_genero



# Tabla Juego
class Juego(db.base):
    __tablename__ = 'juego'
    __table_args__ = {'sqlite_autoincrement': True}

    id_juego: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre_juego: Mapped[str] = mapped_column(String(50), nullable=False)
    id_genero: Mapped[int] = mapped_column(Integer, ForeignKey("genero.id_genero"), nullable=False)
    portada: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    tipo_elemento: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    es_equipo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    genero_obj: Mapped["Genero"] = relationship("Genero", back_populates="juegos")
    torneos: Mapped[list["Torneo"]] = relationship("Torneo", back_populates="juego_obj")
    personajes: Mapped[list["Personaje"]] = relationship("Personaje", back_populates="juego_obj")
    clubes: Mapped[list["Club"]] = relationship("Club", back_populates="juego_obj")
    armas: Mapped[list["Armas"]] = relationship("Armas", back_populates="juego_obj")
    juego_personaje_arma: Mapped[list["Personaje_arma"]] = relationship("Personaje_arma", back_populates="juego_obj")
    estadisticas_global: Mapped[list["Estadistica_global"]] = relationship("Estadistica_global", back_populates="juego_obj")
    estadisticas_juego: Mapped[list["Estadistica_juego"]] = relationship("Estadistica_juego", back_populates="juego_obj")
    ranking: Mapped[list["Ranking_global"]] = relationship("Ranking_global", back_populates="juego_obj")

    def __init__(self, nombre_juego, id_genero, portada=None, tipo_elemento=None, es_equipo=False):
        self.nombre_juego = nombre_juego
        self.id_genero = id_genero
        self.portada = portada
        self.tipo_elemento = tipo_elemento
        self.es_equipo = es_equipo


class Grupo(db.base):
    __tablename__ = 'grupo'
    __table_args__ = {'sqlite_autoincrement': True}

    id_grupo: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(1), nullable=False)  # A, B, C...
    id_torneo: Mapped[int] = mapped_column(Integer, ForeignKey("torneo.id_torneo"), nullable=False)

    # 🔗 Relaciones
    torneo_obj: Mapped["Torneo"] = relationship("Torneo", back_populates="grupos")
    participantes: Mapped[list["Participante_torneo"]] = relationship("Participante_torneo",back_populates="grupo_obj")
    def __init__(self, nombre, id_torneo):
        self.nombre = nombre
        self.id_torneo = id_torneo


# Tabla Torneo
class Torneo(db.base):
    __tablename__ = 'torneo'
    __table_args__ = {'sqlite_autoincrement': True}

    id_torneo: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(500), nullable=False)
    fecha_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_final: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[str] = mapped_column(String(30), nullable=False, default="activo")
    max_participantes: Mapped[int] = mapped_column(Integer, nullable=False)
    max_miembros_equipo: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    id_juego: Mapped[int] = mapped_column(Integer, ForeignKey("juego.id_juego"), nullable=False)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    juego_obj: Mapped["Juego"] = relationship("Juego", back_populates="torneos")
    usuario_obj: Mapped["Usuario"] = relationship("Usuario", back_populates="creador_torneos")
    participantes: Mapped[list["Participante_torneo"]] = relationship("Participante_torneo", back_populates="torneo_obj")
    partidas: Mapped[list["Partida"]] = relationship("Partida", back_populates="torneo_obj")
    grupos: Mapped[list["Grupo"]] = relationship("Grupo", back_populates="torneo_obj")

    def __init__(self, nombre, descripcion, fecha_inicio, fecha_final, estado, max_participantes,
                 id_juego, id_usuario, max_miembros_equipo=None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_final = fecha_final
        self.estado = estado
        self.max_participantes = max_participantes
        self.max_miembros_equipo = max_miembros_equipo
        self.id_juego = id_juego
        self.id_usuario = id_usuario


# Tabla Personaje
class Personaje(db.base):
    __tablename__ = 'personaje'
    __table_args__ = {'sqlite_autoincrement': True}

    id_personaje: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre_personaje: Mapped[str] = mapped_column(String(50), nullable=False)
    id_juego: Mapped[int] = mapped_column(Integer, ForeignKey("juego.id_juego"), nullable=False)

    juego_obj: Mapped["Juego"] = relationship("Juego", back_populates="personajes")
    personaje_arma: Mapped[list["Personaje_arma"]] = relationship("Personaje_arma", back_populates="personaje_obj")
    participaciones: Mapped[list["Participante_torneo"]] = relationship("Participante_torneo", back_populates="personaje_obj")
    estadisticas_global: Mapped[list["Estadistica_global"]] = relationship("Estadistica_global", back_populates="personaje_obj")
    estadisticas_juego: Mapped[list["Estadistica_juego"]] = relationship("Estadistica_juego", back_populates="personaje_obj")

    def __init__(self, nombre_personaje, id_juego):
        self.nombre_personaje = nombre_personaje
        self.id_juego = id_juego


# Tabla Club
class Club(db.base):
    __tablename__ = 'club'
    __table_args__ = {'sqlite_autoincrement': True}

    id_club: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre_club: Mapped[str] = mapped_column(String(50), nullable=False)
    id_juego: Mapped[int] = mapped_column(Integer, ForeignKey("juego.id_juego"), nullable=False)

    juego_obj: Mapped["Juego"] = relationship("Juego", back_populates="clubes")
    participaciones: Mapped[list["Participante_torneo"]] = relationship("Participante_torneo", back_populates="club_obj")
    estadisticas_global: Mapped[list["Estadistica_global"]] = relationship("Estadistica_global", back_populates="club_obj")
    estadisticas_juego: Mapped[list["Estadistica_juego"]] = relationship("Estadistica_juego", back_populates="club_obj")

    def __init__(self, nombre_club, id_juego):
        self.nombre_club = nombre_club
        self.id_juego = id_juego



# Tabla Armas
class Armas(db.base):
    __tablename__ = 'armas'
    __table_args__ = {'sqlite_autoincrement': True}

    id_armas: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre_arma: Mapped[str] = mapped_column(String(100), nullable=False)
    tipo_arma: Mapped[str] = mapped_column(String(50), nullable=False)
    id_juego: Mapped[int] = mapped_column(Integer, ForeignKey("juego.id_juego"), nullable=False)

    juego_obj: Mapped["Juego"] = relationship("Juego", back_populates="armas")
    arma_personaje: Mapped[list["Personaje_arma"]] = relationship("Personaje_arma", back_populates="arma_obj")
    estadisticas_global: Mapped[list["Estadistica_global"]] = relationship("Estadistica_global", back_populates="arma_obj")
    estadisticas_juego: Mapped[list["Estadistica_juego"]] = relationship("Estadistica_juego", back_populates="arma_obj")

    def __init__(self, nombre_arma, tipo_arma, id_juego):
        self.nombre_arma = nombre_arma
        self.tipo_arma = tipo_arma
        self.id_juego = id_juego

class Personaje_arma(db.base):

    __tablename__ = 'personaje_arma'
    __table_args__ = {'sqlite_autoincrement': True}

    id_juego: Mapped[int] = mapped_column(Integer, ForeignKey("juego.id_juego"), primary_key=True)
    juego_obj: Mapped["Juego"] = relationship("Juego", back_populates="juego_personaje_arma")
    id_personaje: Mapped[int] = mapped_column(Integer, ForeignKey("personaje.id_personaje"), primary_key=True)
    personaje_obj: Mapped["Personaje"] = relationship("Personaje", back_populates="personaje_arma")
    id_armas: Mapped[int] = mapped_column(Integer, ForeignKey("armas.id_armas"), primary_key=True)
    arma_obj: Mapped["Armas"] = relationship("Armas", back_populates="arma_personaje")
    habilidad: Mapped[str] = mapped_column(String(100), nullable=True)

    def __init__(self, id_juego ,id_personaje, id_armas, habilidad):
        self.id_juego = id_juego
        self.id_personaje = id_personaje
        self.id_armas = id_armas
        self.habilidad = habilidad


# Tabla Participante_torneo
class Participante_torneo(db.base):
    __tablename__ = 'participante_torneo'
    __table_args__ = {'sqlite_autoincrement': True}

    id_participante: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_torneo: Mapped[int] = mapped_column(Integer, ForeignKey("torneo.id_torneo"), nullable=False)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    fecha_inscripcion: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False)
    id_personaje: Mapped[int] = mapped_column(Integer, ForeignKey("personaje.id_personaje"), nullable=True)
    id_club: Mapped[int] = mapped_column(Integer, ForeignKey("club.id_club"), nullable=True)
    id_arma_principal: Mapped[int] = mapped_column(Integer, ForeignKey("armas.id_armas"), nullable=True)
    id_arma_secundaria: Mapped[int] = mapped_column(Integer, ForeignKey("armas.id_armas"), nullable=True)
    id_arma_arrojadiza: Mapped[int] = mapped_column(Integer, ForeignKey("armas.id_armas"), nullable=True)
    id_grupo: Mapped[int] = mapped_column(Integer, ForeignKey("grupo.id_grupo"), nullable=True)
    id_equipo: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("equipo.id_equipo"), nullable=True)

    grupo_obj: Mapped["Grupo"] = relationship("Grupo", back_populates="participantes")
    equipo_obj: Mapped[Optional["Equipo"]] = relationship("Equipo", foreign_keys=[id_equipo])
    victorias: Mapped[int] = mapped_column(Integer, nullable=False)
    derrotas: Mapped[int] = mapped_column(Integer, nullable=False)
    empate: Mapped[int] = mapped_column(Integer, nullable=False)
    rondas_ganadas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rondas_perdidas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    diferencia_rondas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    puntos_totales: Mapped[int] = mapped_column(Integer, nullable=False)
    posicion_grupo: Mapped[int] = mapped_column(Integer, nullable=True)
    ranking_final: Mapped[int] = mapped_column(Integer, nullable=True)
    aceptar_organizador: Mapped[bool] = mapped_column(Boolean, nullable=True, default=None)

    torneo_obj: Mapped["Torneo"] = relationship("Torneo", back_populates="participantes")
    usuario_obj: Mapped["Usuario"] = relationship("Usuario", back_populates="participaciones")
    personaje_obj: Mapped["Personaje"] = relationship("Personaje", back_populates="participaciones")
    club_obj: Mapped["Club"] = relationship("Club", back_populates="participaciones")
    partidas: Mapped[list["Participante_partida"]] = relationship("Participante_partida", back_populates="participante_obj")
    partidas_ganadas: Mapped[list["Partida"]] = relationship("Partida",foreign_keys="Partida.ganador_id",back_populates="ganador")
    miembros_participantes: Mapped[list["Miembro_participante"]] = relationship("Miembro_participante", back_populates="participante_obj", cascade="all, delete-orphan")

    def __init__(self, id_torneo, id_usuario, fecha_inscripcion, estado, id_personaje, id_club,
                 id_arma_principal, id_arma_secundaria , id_arma_arrojadiza , victorias, derrotas, empate,
                 ronda_ganadas,rondas_perdidas,diferencia_rondas, puntos_totales,
                 posicion_grupo=None, ranking_final=None, id_equipo=None):

        self.id_torneo = id_torneo
        self.id_usuario = id_usuario
        self.fecha_inscripcion = fecha_inscripcion
        self.estado = estado
        self.id_personaje = id_personaje
        self.id_club = id_club
        self.id_arma_principal = id_arma_principal
        self.id_arma_secundaria = id_arma_secundaria
        self.id_arma_arrojadiza = id_arma_arrojadiza
        self.id_equipo = id_equipo
        self.victorias = victorias
        self.derrotas = derrotas
        self.empate = empate
        self.ronda_ganadas = ronda_ganadas
        self.rondas_perdidas = rondas_perdidas
        self.diferencia_rondas = diferencia_rondas
        self.puntos_totales = puntos_totales
        self.posicion_grupo = posicion_grupo
        self.ranking_final = ranking_final

# Tabla Partida
class Partida(db.base):
    __tablename__ = 'partida'
    __table_args__ = {'sqlite_autoincrement': True}

    id_partida: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_torneo: Mapped[int] = mapped_column(Integer, ForeignKey("torneo.id_torneo"), nullable=False)
    tipo_partida: Mapped[str] = mapped_column(String(50), nullable=False)
    estado: Mapped[str] = mapped_column(String(30), nullable=False)
    ganador_id: Mapped[int] = mapped_column(Integer,ForeignKey("participante_torneo.id_participante"),nullable=True)
    ganador: Mapped["Participante_torneo"] = relationship("Participante_torneo",back_populates="partidas_ganadas",foreign_keys=[ganador_id])
    siguiente_partida_id: Mapped[int] = mapped_column(Integer, ForeignKey("partida.id_partida"), nullable=True)
    resultado_final: Mapped[str] = mapped_column(String(5), nullable=True)

    torneo_obj: Mapped["Torneo"] = relationship("Torneo", back_populates="partidas")
    siguiente_partida: Mapped["Partida"] = relationship("Partida", remote_side=[id_partida], backref="partidas_previas")
    participantes: Mapped[list["Participante_partida"]] = relationship("Participante_partida", back_populates="partida_obj")

    def __init__(self, id_torneo, tipo_partida, estado, ganador_id=None, siguiente_partida_id=None,
                 resultado_final= None):
        self.id_torneo = id_torneo
        self.tipo_partida = tipo_partida
        self.estado = estado
        self.ganador_id = ganador_id
        self.siguiente_partida_id = siguiente_partida_id
        self.resultado_final = resultado_final



# Tabla Participante_partida
class Participante_partida(db.base):
    __tablename__ = 'participante_partida'
    __table_args__ = {'sqlite_autoincrement': True}

    id_participante_partida: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_partida: Mapped[int] = mapped_column(Integer, ForeignKey("partida.id_partida"), nullable=False)
    id_participante_torneo: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("participante_torneo.id_participante"), nullable=True)
    posicion: Mapped[int] = mapped_column(Integer, nullable=False)
    puntos: Mapped[int] = mapped_column(Integer, nullable=False)
    eliminacion: Mapped[bool] = mapped_column(Boolean, nullable=False)
    resultado_usuario: Mapped[str] = mapped_column(Integer, nullable=True)
    resultado_rival: Mapped[int] = mapped_column(Integer, nullable=True)
    captura_resultado: Mapped[int] = mapped_column( String(255),nullable=True)
    confirmar_resultados: Mapped[bool] = mapped_column(Boolean,nullable=False,default=False)

    partida_obj: Mapped["Partida"] = relationship("Partida", back_populates="participantes")
    participante_obj: Mapped["Participante_torneo"] = relationship("Participante_torneo", back_populates="partidas")

    def __init__(self,id_partida,id_participante_torneo,posicion=0,
            puntos=0,eliminacion=False,resultado_usuario=None, resultado_rival=None,
                 captura_resultado=None, confirmar_resultado=False):

        self.id_partida = id_partida
        self.id_participante_torneo = id_participante_torneo
        self.posicion = posicion
        self.puntos = puntos
        self.eliminacion = eliminacion
        self.resultado_usuario = resultado_usuario
        self.resultado_rival = resultado_rival
        self.captura_resultado = captura_resultado
        self.confirmar_resultados = confirmar_resultado



# Tabla Ranking_global
class Ranking_global(db.base):
    __tablename__ = 'ranking_global'

    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id_usuario"), primary_key=True)
    id_juego: Mapped[int] = mapped_column(Integer, ForeignKey("juego.id_juego"), primary_key=True)

    usuario_obj: Mapped["Usuario"] = relationship("Usuario", back_populates="ranking")
    juego_obj: Mapped["Juego"] = relationship("Juego", back_populates="ranking")

    puntos_ranking: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    torneos_jugados: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    torneos_ganados: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    partidas_ganadas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    partidas_perdidas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    partidas_empatadas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rondas_ganadas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rondas_perdidas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    diferencia_rondas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    winrate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    posicion_global: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    def __init__(self, id_usuario, id_juego):
        self.id_usuario = id_usuario
        self.id_juego = id_juego
        self.puntos_ranking = 0
        self.torneos_jugados = 0
        self.torneos_ganados = 0
        self.partidas_ganadas = 0
        self.partidas_perdidas = 0
        self.partidas_empatadas = 0
        self.rondas_ganadas = 0
        self.rondas_perdidas = 0
        self.diferencia_rondas = 0
        self.winrate = 0.0
        self.posicion_global = 0



# Tabla Ranking_equipo
class Ranking_equipo(db.base):
    __tablename__ = 'ranking_equipo'

    id_equipo: Mapped[int] = mapped_column(Integer, ForeignKey("equipo.id_equipo"), primary_key=True)
    id_juego: Mapped[int] = mapped_column(Integer, ForeignKey("juego.id_juego"), primary_key=True)

    equipo_obj: Mapped["Equipo"] = relationship("Equipo")
    juego_obj: Mapped["Juego"] = relationship("Juego")

    puntos_ranking: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    torneos_jugados: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    torneos_ganados: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    partidas_ganadas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    partidas_perdidas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    partidas_empatadas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rondas_ganadas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rondas_perdidas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    diferencia_rondas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    winrate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    posicion_global: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    def __init__(self, id_equipo, id_juego):
        self.id_equipo = id_equipo
        self.id_juego = id_juego
        self.puntos_ranking = 0
        self.torneos_jugados = 0
        self.torneos_ganados = 0
        self.partidas_ganadas = 0
        self.partidas_perdidas = 0
        self.partidas_empatadas = 0
        self.rondas_ganadas = 0
        self.rondas_perdidas = 0
        self.diferencia_rondas = 0
        self.winrate = 0.0
        self.posicion_global = 0


# Tabla Estadistica_global
class Estadistica_global(db.base):
    __tablename__ = 'estadistica_global'
    __table_args__ = {'sqlite_autoincrement': True}

    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id_usuario"), primary_key=True)
    usuario_obj: Mapped["Usuario"] = relationship("Usuario", back_populates="estadisticas_global")

    partida_totales: Mapped[int] = mapped_column(Integer, nullable=False)
    victorias_totales: Mapped[int] = mapped_column(Integer, nullable=False)
    derrotas_totales: Mapped[int] = mapped_column(Integer, nullable=False)
    empates_totales: Mapped[int] = mapped_column(Integer, nullable=False)

    id_juego: Mapped[int] = mapped_column(Integer, ForeignKey("juego.id_juego"), nullable=False)
    juego_obj: Mapped["Juego"] = relationship("Juego", back_populates="estadisticas_global")
    id_personaje: Mapped[int] = mapped_column(Integer, ForeignKey("personaje.id_personaje"), nullable=True)
    personaje_obj: Mapped["Personaje"] = relationship("Personaje", back_populates="estadisticas_global")
    id_club: Mapped[int] = mapped_column(Integer, ForeignKey("club.id_club"), nullable=True)
    club_obj: Mapped["Club"] = relationship("Club", back_populates="estadisticas_global")
    id_armas: Mapped[int] = mapped_column(Integer, ForeignKey("armas.id_armas"), nullable=True)
    arma_obj: Mapped["Armas"] = relationship("Armas", back_populates="estadisticas_global")


# Tabla Estadistica_juego
class Estadistica_juego(db.base):
    __tablename__ = 'estadistica_juego'
    __table_args__ = {'sqlite_autoincrement': True}

    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id_usuario"), primary_key=True)
    id_juego: Mapped[int] = mapped_column(Integer, ForeignKey("juego.id_juego"), primary_key=True)

    usuario_obj: Mapped["Usuario"] = relationship("Usuario", back_populates="estadisticas_juego")
    juego_obj: Mapped["Juego"] = relationship("Juego", back_populates="estadisticas_juego")

    partida_totales: Mapped[int] = mapped_column(Integer, nullable=False)
    victorias_totales: Mapped[int] = mapped_column(Integer, nullable=False)
    derrotas_totales: Mapped[int] = mapped_column(Integer, nullable=False)
    empates_totales: Mapped[int] = mapped_column(Integer, nullable=False)

    id_personaje: Mapped[int] = mapped_column(Integer, ForeignKey("personaje.id_personaje"), nullable=True)
    personaje_obj: Mapped["Personaje"] = relationship("Personaje", back_populates="estadisticas_juego")
    id_club: Mapped[int] = mapped_column(Integer, ForeignKey("club.id_club"), nullable=True)
    club_obj: Mapped["Club"] = relationship("Club", back_populates="estadisticas_juego")
    id_armas: Mapped[int] = mapped_column(Integer, ForeignKey("armas.id_armas"), nullable=True)
    arma_obj: Mapped["Armas"] = relationship("Armas", back_populates="estadisticas_juego")


# Tabla Juego_borrado
class Juego_borrado(db.base):
    __tablename__ = 'juego_borrado'
    __table_args__ = {'sqlite_autoincrement': True}

    id_juego_borrado: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre_juego: Mapped[str] = mapped_column(String(50), nullable=False)
    motivo: Mapped[str] = mapped_column(String(500), nullable=False)
    fecha_borrado: Mapped[date] = mapped_column(Date, nullable=False)

    avisos: Mapped[list["Aviso_juego_borrado"]] = relationship("Aviso_juego_borrado", back_populates="juego_borrado_obj")

    def __init__(self, nombre_juego, motivo, fecha_borrado):
        self.nombre_juego = nombre_juego
        self.motivo = motivo
        self.fecha_borrado = fecha_borrado


# Tabla Aviso_juego_borrado
class Aviso_juego_borrado(db.base):
    __tablename__ = 'aviso_juego_borrado'
    __table_args__ = {'sqlite_autoincrement': True}

    id_aviso: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    id_juego_borrado: Mapped[int] = mapped_column(Integer, ForeignKey("juego_borrado.id_juego_borrado"), nullable=False)
    visto: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    usuario_obj: Mapped["Usuario"] = relationship("Usuario", back_populates="avisos_juegos_borrados")
    juego_borrado_obj: Mapped["Juego_borrado"] = relationship("Juego_borrado", back_populates="avisos")

    def __init__(self, id_usuario, id_juego_borrado):
        self.id_usuario = id_usuario
        self.id_juego_borrado = id_juego_borrado
        self.visto = False


# Tabla Equipo
class Equipo(db.base):
    __tablename__ = 'equipo'
    __table_args__ = {'sqlite_autoincrement': True}

    id_equipo: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    descripcion: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    max_miembros: Mapped[int] = mapped_column(Integer, nullable=False)
    id_capitan: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    fecha_creacion: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)

    capitan_obj: Mapped["Usuario"] = relationship("Usuario", back_populates="equipos_capitan", foreign_keys=[id_capitan])
    miembros: Mapped[list["Miembro_equipo"]] = relationship("Miembro_equipo", back_populates="equipo_obj", cascade="all, delete-orphan")

    def __init__(self, nombre, max_miembros, id_capitan, descripcion=None):
        self.nombre = nombre
        self.max_miembros = max_miembros
        self.id_capitan = id_capitan
        self.descripcion = descripcion
        self.fecha_creacion = date.today()


# Tabla Miembro_equipo
class Miembro_equipo(db.base):
    __tablename__ = 'miembro_equipo'
    __table_args__ = {'sqlite_autoincrement': True}

    id_miembro: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_equipo: Mapped[int] = mapped_column(Integer, ForeignKey("equipo.id_equipo"), nullable=False)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    rol: Mapped[str] = mapped_column(String(10), nullable=False, default="miembro")  # 'capitan' o 'miembro'
    fecha_union: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)

    equipo_obj: Mapped["Equipo"] = relationship("Equipo", back_populates="miembros")
    usuario_obj: Mapped["Usuario"] = relationship("Usuario", back_populates="membresias")

    def __init__(self, id_equipo, id_usuario, rol="miembro"):
        self.id_equipo = id_equipo
        self.id_usuario = id_usuario
        self.rol = rol
        self.fecha_union = date.today()


# Tabla Miembro_participante (miembros de equipo seleccionados para un torneo)
class Miembro_participante(db.base):
    __tablename__ = 'miembro_participante'
    __table_args__ = {'sqlite_autoincrement': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_participante_torneo: Mapped[int] = mapped_column(Integer, ForeignKey("participante_torneo.id_participante"), nullable=False)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)

    participante_obj: Mapped["Participante_torneo"] = relationship("Participante_torneo", back_populates="miembros_participantes")
    usuario_obj: Mapped["Usuario"] = relationship("Usuario")

    def __init__(self, id_participante_torneo, id_usuario):
        self.id_participante_torneo = id_participante_torneo
        self.id_usuario = id_usuario