from flask import Flask, render_template, request, jsonify, session, redirect, flash
from werkzeug.utils import secure_filename
from models import *
import db
import re
import os
import string
import random
from seed_data import *
from datetime import datetime, date as date_type
from sqlalchemy import inspect, text
import json as json_mod

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "clave-local-desarrollo")

db_session = db.db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.Session.remove()

# ===============================
# CONTEXT PROCESSOR
# ===============================
@app.context_processor
def inject_usuario():
    rol_usuario = None
    nombre_usuario = session.get("nombre_usuario")

    if nombre_usuario:
        usuario = db_session.query(Usuario).filter_by(nombre_usuario=nombre_usuario).first()
        if usuario and usuario.rol_obj:
            rol_usuario = usuario.rol_obj.nombre_rol

    generos = db_session.query(Genero).order_by(Genero.id_genero).all()

    return {"nombre_usuario": nombre_usuario, "rol_usuario": rol_usuario, "generos": generos}

# HOME

@app.route('/')
def home():
    juegos = db_session.query(Juego).order_by(Juego.id_juego).all()
    return render_template('index.html', pagina_actual='index', juegos=juegos)

# ===============================
# FORM USUARIO
# ===============================
@app.route("/formusuario")
def formusuario():
    return render_template("formusuario.html")


# VALIDACIÓN DE CONTRASEÑA

#Validamos las conteaseñas de manera que sean mas de 6 caracteres, que tenga 1 mayuscula y un simbolo
def validar_password(password):
    if len(password) < 6:
        return "La contraseña debe tener al menos 6 caracteres, 1 mayuscula y 1 simbolo (. , ! @ # ...)"
    if not re.search(r"[A-Z]", password):
        return "La contraseña debe tener al menos 6 caracteres, 1 mayuscula y 1 simbolo (. , ! @ # ...)"
    if not re.search(r"[a-z]", password):
        return "La contraseña debe tener al menos 6 caracteres, 1 mayuscula y 1 simbolo (. , ! @ # ...)"
    if not re.search(r"[^A-Za-z0-9]", password):
        return "La contraseña debe tener al menos 6 caracteres, 1 mayuscula y 1 simbolo (. , ! @ # ...)"
    return None



# CREAR USUARIO

#Una funcion para crear usuarios
@app.route("/crear_usuario", methods=["POST"])
def crear_usuario():
    data = request.json

    try:

#Sirve para las validaciones en el cual solo se puedan usur letras en el nombre
        solo_letras = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$")
#Sirve para las validaciones del correo con el simbolo de @ y . con algo de texto
        email_regex = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

#Validacion para que solo sean letras en nombre y apellidos
        if len(data["nombre"]) < 2 or not solo_letras.match(data["nombre"]):
            return jsonify({"error": "Nombre inválido"}), 400

        if len(data["apellidos"]) < 2 or not solo_letras.match(data["apellidos"]):
            return jsonify({"error": "Apellidos inválidos"}), 400

        try:
#Guardamos la fecha de nacimiento como un date, que sea inferior a la actual
            fecha_nacimiento = datetime.strptime(
            data["fecha_nacimiento"], "%Y-%m-%d"
        ).date()

        except ValueError:
            return jsonify({"error": "Formato de fecha inválido"}), 400

#Verificamos que sea la fecha inferior a la fecha actual
        if fecha_nacimiento > datetime.now().date():
            return jsonify({"error": "Fecha de nacimiento inválida"}), 400

#Validamos que sea un email con la @ y punto
        if not email_regex.match(data["email"]):
            return jsonify({"error": "Email inválido"}), 400

#Validamos que el nombre del usuario tenga por lo menos 3 digitos
        if len(data["nombre_usuario"]) < 3:
            return jsonify({"error": "Nombre de usuario demasiado corto"}), 400

#Validamos la contraseña con la funcion de validar_password
        error_password = validar_password(data.get("password", ""))
        if error_password:
            return jsonify({"error": error_password}), 400

#Guardamos los datos del formulario en sus respectivos campos
        nuevo_usuario = Usuario(
            nombre=data["nombre"],
            apellidos=data["apellidos"],
            fecha_nacimiento=fecha_nacimiento,
            email=data["email"],
            nombre_usuario=data["nombre_usuario"],
            password=data["password"]
        )

#El usuario creado se guarda automaticamente en el rol de "Usuario"
        rol_usuario = db_session.get(Rol, 2)
        nuevo_usuario.rol_obj = rol_usuario

#Guardamos el usuario nuevo creado
        db_session.add(nuevo_usuario)
        db_session.commit()

#Se le guarda en la session
        session["nombre_usuario"] = nuevo_usuario.nombre_usuario

        return jsonify({"mensaje": "Usuario creado correctamente"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

#PERFIL

#Funcion para ver los perfiles de los usuarios
@app.route("/perfil")
def perfil():

#si el usuario no tiene sesion te redirige a la misma pagina
    if "nombre_usuario" not in session:
        return redirect("/")

#Se llama al usuario
    usuario = db_session.query(Usuario).filter_by(
        nombre_usuario=session["nombre_usuario"]
    ).first()

#Si no es un usuario se redirige a la misma pagina
    if not usuario:
        return redirect("/")

#Llamamos a todas las participaciones del usuario
    participaciones = db_session.query(Participante_torneo).filter_by(
        id_usuario=usuario.id_usuario
    ).all()

#Cogemos el juego favorito, es decir, en el que mas a participado y lo guardamos en el diccionario
    conteo_por_juego = {}
#Cada vez que participa en un torneo de ese juego se guarda en el diccionario y se le suma 1
    for participacion in participaciones:
        id_juego = participacion.torneo_obj.id_juego
        conteo_por_juego[id_juego] = conteo_por_juego.get(id_juego, 0) + 1

    juego_favorito = None
    elemento_mas_usado = None
    etiqueta_elemento = None

#Se coge el conteo por juegos y se muestra el juego con el conte mas alto
    if conteo_por_juego:
        id_juego_favorito = max(conteo_por_juego, key=lambda id_juego: conteo_por_juego[id_juego])
        juego_favorito = db_session.get(Juego, id_juego_favorito)

        participaciones_juego_favorito = [
            participacion for participacion in participaciones
            if participacion.torneo_obj.id_juego == id_juego_favorito
        ]

#Aqui decimos que tabla va a usar segun el juego que ya se encuentran creados
#El primer caso guarda a los personajes de sus respectivos juegos
        if id_juego_favorito in [1, 2, 3, 9]:
#Se guarda el personaje mas usado dentro de ese juego
            etiqueta_elemento = "Personaje más usado"
            conteo_personajes = {}
#Recorremos las participaciones dentro del diccionarioy cogemos el valor de participaciones
            for participacion in participaciones_juego_favorito:
                if participacion.id_personaje:
                    conteo_personajes[participacion.id_personaje] = conteo_personajes.get(participacion.id_personaje, 0) + 1

#Buscamos el personaje mas usado
            if conteo_personajes:
                id_personaje_mas_usado = max(conteo_personajes, key=lambda id_p: conteo_personajes[id_p])
                personaje = db_session.get(Personaje, id_personaje_mas_usado)
                if personaje:
                    elemento_mas_usado = personaje.nombre_personaje

#Mismo proceso que el de personajes pero usado con la base de datos de club
        elif id_juego_favorito in [4, 5, 6]:
            etiqueta_elemento = "Club más usado"
            conteo_clubs = {}
            for participacion in participaciones_juego_favorito:
                if participacion.id_club:
                    conteo_clubs[participacion.id_club] = conteo_clubs.get(participacion.id_club, 0) + 1

            if conteo_clubs:
                id_club_mas_usado = max(conteo_clubs, key=lambda id_c: conteo_clubs[id_c])
                club = db_session.get(Club, id_club_mas_usado)
                if club:
                    elemento_mas_usado = club.nombre_club

#Mismo proceso que el de personaje y club pero ahora con la base de datos de armas
        elif id_juego_favorito in [7, 8]:
            etiqueta_elemento = "Arma más usada"
            conteo_armas = {}
            for participacion in participaciones_juego_favorito:
                if participacion.id_arma_principal:
                    conteo_armas[participacion.id_arma_principal] = conteo_armas.get(participacion.id_arma_principal, 0) + 1
            if conteo_armas:
                id_arma_mas_usada = max(conteo_armas, key=lambda id_a: conteo_armas[id_a])
                arma = db_session.get(Armas, id_arma_mas_usada)
                if arma:
                    elemento_mas_usado = arma.nombre_arma

#Torneos en los que ha participado un usuario cogemos el id y comprbamos en cuantos ha participado ese id
    torneos_participados = [
        {"nombre": participacion.torneo_obj.nombre, "id": participacion.torneo_obj.id_torneo}
        for participacion in participaciones
    ]

#Torneos ganados los mismo recorremos en cuantos participa el id y en cuantos tiene el ranking final 1
    torneos_ganados = [
        {"nombre": participacion.torneo_obj.nombre, "id": participacion.torneo_obj.id_torneo}
        for participacion in participaciones
        if participacion.ranking_final == 1
    ]

#Torneos creados por el usuario
    torneos_creados = db_session.query(Torneo).filter_by(
        id_usuario=usuario.id_usuario
    ).all()

#Recorremos todos los torneos en el que el id de creador es este y cogemos los que no tienen el estado Finalizado
    torneos_creados_activos = [
        {"nombre": torneo.nombre, "id": torneo.id_torneo}
        for torneo in torneos_creados
        if torneo.estado != "Finalizado"
    ]

#Lo mismo que el anterior pero cogiendo los torneos con el estado Finalizado
    torneos_creados_finalizados = [
        {"nombre": torneo.nombre, "id": torneo.id_torneo}
        for torneo in torneos_creados
        if torneo.estado == "Finalizado"
    ]

# Renderiza el perfil con estadísticas calculadas con los datos del perfil y de estadisticas de juego
    return render_template(
        "perfil.html",
        usuario=usuario,
        juego_favorito=juego_favorito,
        elemento_mas_usado=elemento_mas_usado,
        etiqueta_elemento=etiqueta_elemento,
        torneos_participados=torneos_participados,
        torneos_ganados=torneos_ganados,
        torneos_creados_activos=torneos_creados_activos,
        torneos_creados_finalizados=torneos_creados_finalizados
    )


# PERFIL
@app.route("/perfil_usuario")
def perfil_usuario():

#Verifica que el usuario tiene la sesion activa
    if "nombre_usuario" not in session:
        return jsonify({"error": "No autorizado"}), 401

#Se llama al usuario de la bd
    usuario = db_session.query(Usuario).filter_by(
        nombre_usuario=session["nombre_usuario"]
    ).first()

#Si no es un usuario salta el error
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

#Se devuelven los datos de los usuarios
    return jsonify({
        "nombre": usuario.nombre,
        "apellidos": usuario.apellidos,
        "email": usuario.email,
        "nombre_usuario": usuario.nombre_usuario,
        "fecha_nacimiento": usuario.fecha_nacimiento.strftime("%Y-%m-%d"),
        "fecha_registro": usuario.fecha_registro.strftime("%Y-%m-%d"),
        "rol": usuario.rol_obj.nombre_rol
    })


# LOGIN
@app.route("/login", methods=["POST"])
def login():

#Se guarda el nombre del usuario y la password
    usuario_form = request.form["nombre_usuario"]
    password_form = request.form["password"]

#Se redirige a la pagina tras el login
    next_page = request.args.get("next")

#Se llama al usuario desde la bd
    usuario = db_session.query(Usuario).filter_by(
        nombre_usuario=usuario_form
    ).first()

#Se comprueba si el usuario y la password dada es igual a la que hay en la bd
    if usuario and usuario.password == password_form:
        session['nombre_usuario'] = usuario.nombre_usuario
        return redirect(next_page or "/")

#Error que salta cuando no coinciden las credenciales
    flash("Usuario o contraseña incorrectos", "error")
    return redirect(next_page or "/")


# LOGOUT
@app.route("/logout")
def logout():
#Saca el usario de la sesion
    session.pop("nombre_usuario", None)
    return redirect("/")


# JUEGO
@app.route('/juego/<int:id_juego>')
def plantilla_juego(id_juego):

#Llamamos de a los juegos desde la bd
    juego = db_session.query(Juego).filter_by(
        id_juego=id_juego
    ).first()

#Si no esta en la bd salta el error de no encontrado
    if not juego:
        return jsonify({"error": "Juego no encontrado"}), 404

#Llamamos a los personajes del juego desde la bd
    personajes = db_session.query(Personaje).filter_by(
        id_juego=juego.id_juego
    ).all()

#Llamamos a los torneos que se crean en los juego
    torneos = db_session.query(Torneo).filter_by(
        id_juego=juego.id_juego
    ).all()

#Comprobamos si es creador o no
    es_creador = False

#Comprobamos si el usuario tiene la sesion activa y le llamamos desde la bd
    if "nombre_usuario" in session:
        usuario_actual_obj = db_session.query(Usuario).filter_by(
            nombre_usuario=session["nombre_usuario"]
        ).first()

#Comprobamos si el usuario que hemos cogido es Administrador gestiona todos los torneos
        if usuario_actual_obj:
            if usuario_actual_obj.rol_obj and usuario_actual_obj.rol_obj.nombre_rol == "Administrador":
                es_creador = True
# Si no es Administrador, solo tiene permisos sobre los torneos que el usuario a creado
            else:
                es_creador = any(
                    torneo.id_usuario == usuario_actual_obj.id_usuario
                    for torneo in torneos
                )

#Comprobamos si el usuario tiene la sesion activa
    usuario_logueado = "nombre_usuario" in session
    usuario_id = None
#Si el usuario esta logueado llamamos a este desde la bd
    if usuario_logueado:
        user = db_session.query(Usuario).filter_by(nombre_usuario=session["nombre_usuario"]).first()
        if user:
            usuario_id = user.id_usuario

#Renderizamos los datos de los juegos
    return render_template(
        'juegos.html',
        juego=juego,
        personajes=personajes,
        torneos=torneos,
        es_creador=es_creador,
        usuario_logueado=usuario_logueado,
        usuario_id=usuario_id
    )

# CREAR TORNEO
@app.route("/crear_torneo", methods=["GET", "POST"])
def crear_torneo():

#POST → CREAR TORNEO
    if request.method == "POST":

        data = request.form

        try:
#comprobar si el usuario tiene la sesion activa
            if "nombre_usuario" not in session:
                return jsonify({"error": "Debes iniciar sesión"}), 401

#Cogemos el usuario desde la bd
            usuario = db_session.query(Usuario).filter_by(
                nombre_usuario=session["nombre_usuario"]
            ).first()

#Si no se encuentra en la bd nos salta el error
            if not usuario:
                return jsonify({"error": "Usuario no encontrado"}), 404

#Gestionamos las fechas
            fecha_inicio = datetime.strptime(
                data["fecha_inicio"], "%Y-%m-%d"
            ).date()

            fecha_final = datetime.strptime(
                data["fecha_final"], "%Y-%m-%d"
            ).date()

            max_participantes = int(data["max_participantes"])
            hoy = datetime.now().date()

# máximo participantes que sean siempre par
            if max_participantes < 2 or max_participantes % 2 != 0:
                return jsonify({"error": "El número máximo debe ser par y mayor que 1"}), 400

#Verificacion para que la fecha inicio no puede ser inferior a la actual
            if fecha_inicio < hoy:
                return jsonify({"error": "La fecha de inicio no puede ser anterior a hoy"}), 400

#Verificamos que la fecha final sea superior fecha inicio
            if fecha_final < fecha_inicio:
                return jsonify({"error": "La fecha final no puede ser anterior a la fecha de inicio"}), 400

#cambia el rol si no es admin y te lo cambia de usuario a Organizador
            if usuario.rol_obj.nombre_rol != "Administrador":
                rol_organizador = db_session.query(Rol).filter_by(
                    nombre_rol="Organizador"
                ).first()

                if rol_organizador:
                    usuario.rol_obj = rol_organizador

#creamos el torneo, si el torneo consta de equipos este coge el maximo de miembros si es 1 vs 1 se queda en none
            juego_torneo = db_session.get(Juego, int(data["id_juego"]))
            max_miembros_equipo = None
            if juego_torneo and juego_torneo.es_equipo:
                mme = data.get("max_miembros_equipo", "").strip()
                if mme:
                    max_miembros_equipo = int(mme)

#Damos los datos del torneo creado
            nuevo_torneo = Torneo(
                nombre=data["nombre"],
                descripcion=data["descripcion"],
                fecha_inicio=fecha_inicio,
                fecha_final=fecha_final,
                estado="Activo",
                max_participantes=int(data["max_participantes"]),
                id_juego=int(data["id_juego"]),
                id_usuario=usuario.id_usuario,
                max_miembros_equipo=max_miembros_equipo
            )

#Creamos el torneo y guardamos los cambios
            db_session.add(nuevo_torneo)
            db_session.commit()

#Verificamos si es administrador te redirigue a los torneos directamente si es usuario te lleva a la pagina juego
            if usuario.rol_obj and usuario.rol_obj.nombre_rol == "Administrador":
                return redirect("/admin/torneos")
            return redirect(f"/juego/{data['id_juego']}")

        except Exception as e:
            return jsonify({"error": str(e)}), 500

#GET → FORMULARIO
    id_juego = request.args.get("juego")

#Obtiene el juego, las imagenes del juego y si es equipo o no
    juego = db_session.get(Juego, int(id_juego)) if id_juego else None
    juego_imagen = juego.portada if juego and juego.portada else "Logo.png"
    es_equipo = juego.es_equipo if juego else False

#Renderizamos los datos del formulario
    return render_template(
        "formtorneo.html",
        id_juego=id_juego,
        juego_imagen=juego_imagen,
        es_equipo=es_equipo
    )

# SELECCIONAR JUEGO
@app.route("/seleccionar_juego")
def seleccionar_juego():

#Cogemos los juegos de la bd y nos lleva a select.html con los datos de ese juego para la pagina
    juegos = db_session.query(Juego).all()
    return render_template("select.html", juegos=juegos)


# MOSTRAR TORNEOS
@app.route("/mostrar_torneo/<int:id_juego>")
def mostrar_torneo(id_juego):

#Obtenemos el usuario de la sesion
    usuario_actual = session.get("nombre_usuario")
    usuario = None

#Comprobamos el usuario y lo cogemos de la bd
    if usuario_actual:
        usuario = db_session.query(Usuario).filter_by(
            nombre_usuario=usuario_actual
        ).first()

#Llamamos a los torneos desde la bd
    torneos = db_session.query(Torneo).filter_by(id_juego=id_juego).all()

#Ordenamos los torneos poniendo primero los Activos y abajo los finalizados
    torneos.sort(key=lambda torneo: (
        1 if torneo.estado == "Finalizado" else 0,
        -torneo.id_torneo
    ))

#Creamos una lista para los resultados
    resultado = []

#Recorremos todos los torneos
    for t in torneos:

#guardamos los creadores y los inscrito con esto
        es_creador = False
        ya_inscrito = False

#Si es un usuario se ve si es un organizador o un Organizador
        if usuario:
            es_creador = _es_organizador_o_admin(t, usuario)

#Cogemos de la base de datos los usuario que ya estan inscritos
            ya_inscrito = db_session.query(Participante_torneo).filter_by(
                id_torneo=t.id_torneo,
                id_usuario=usuario.id_usuario
            ).first() is not None

#Aqui guardaremos al ganador del torneo
        ganador_nombre = None

#Si el torneo esta finalizado, cogemos al ganador con el torneo y su ranking siendo 1
        if t.estado == "Finalizado":
            participante_ganador = db_session.query(Participante_torneo).filter_by(
                id_torneo=t.id_torneo,
                ranking_final=1
            ).first()

#Se guarda el ganador del torneo
            if participante_ganador and participante_ganador.usuario_obj:
                ganador_nombre = participante_ganador.usuario_obj.nombre_usuario

#Guardamos los datos del torneo en la lista de resultados
        resultado.append({
            "id_torneo": t.id_torneo,
            "nombre": t.nombre,
            "descripcion": t.descripcion,
            "fecha_inicio": t.fecha_inicio.strftime("%Y-%m-%d"),
            "fecha_final": t.fecha_final.strftime("%Y-%m-%d"),
            "estado": t.estado,
            "participantes_totales": len(t.participantes),
            "max_participantes": t.max_participantes,
            "es_creador": es_creador,
            "ya_inscrito": ya_inscrito,
            "ganador": ganador_nombre,
            "portada": t.juego_obj.portada or "Logo.png",
            "es_equipo": t.juego_obj.es_equipo
        })

    return jsonify(resultado)

#CREACION GRUPOS
def crear_grupos_automaticos(torneo, lista_participantes):
#Randomizamos la lista de participantes
    random.shuffle(lista_participantes)
#Guardamos el total de la lista de participantes
    total_participantes = len(lista_participantes)

#Limitamos el numero de grupos segun el numero de participantes
    if total_participantes <= 4:
        numero_grupos = 1
    elif total_participantes <= 8:
        numero_grupos = 2
    elif total_participantes <= 16:
        numero_grupos = 4
    elif total_participantes <= 32:
        numero_grupos = 8
    elif total_participantes <= 64:
        numero_grupos = 16
    elif total_participantes <= 128:
        numero_grupos = 32
    else:
        numero_grupos = 64

#Creamos los grupos con letras es decir... A,B.C... y lo guardamos en la lista
    letras_grupos = list(string.ascii_uppercase)
    grupos_creados = []

#creamos los grupos
    for indice_grupo in range(numero_grupos):

        nuevo_grupo = Grupo(
            nombre=letras_grupos[indice_grupo],
            id_torneo=torneo.id_torneo
        )

#Guardamos los grupos en la lista de grupos_creados
        db_session.add(nuevo_grupo)
        grupos_creados.append(nuevo_grupo)

#Generamos las ids
    db_session.flush()

#asignamos los participantes a los grupos
    for indice_participante, participante in enumerate(lista_participantes):

#Selecciona el grupo donde va a ir ese participante
        grupo_asignado = grupos_creados[indice_participante % numero_grupos]
        participante.id_grupo = grupo_asignado.id_grupo

    return grupos_creados

#GENERAMOS PARTIDAS
def generar_partidos_por_grupo(grupo, participantes_del_torneo):

#Guardamos en una lista las partidas
    partidos_generados = []

#Guardamos en una lista los participantes de sus grupos
    jugadores_del_grupo = [
        participante
        for participante in participantes_del_torneo
        if participante.id_grupo == grupo.id_grupo
    ]

#Recorremos el rango de los jugadores del grupo y genera las partidas
    for indice_local in range(len(jugadores_del_grupo)):
#Guardamos el primer jugador
        jugador_local = jugadores_del_grupo[indice_local]

        for indice_visitante in range(indice_local + 1, len(jugadores_del_grupo)):
#Guardamos el segundo jugador
            jugador_visitante = jugadores_del_grupo[indice_visitante]

#Creamos las partidas con sus datos
            nueva_partida = Partida(
                id_torneo=grupo.id_torneo,
                tipo_partida=f"Fase de grupos - Grupo {grupo.nombre}",
                estado="pendiente",
                ganador_id=None
            )

#Se guarda la partida nueva y se le da un id a este
            db_session.add(nueva_partida)
            db_session.flush()

#Crea los datos del jugador local en la partida con sus estadisticas a 0 al principio
            registro_local = Participante_partida(
                id_partida=nueva_partida.id_partida,
                id_participante_torneo=jugador_local.id_participante,
                posicion=0,
                puntos=0,
                eliminacion=False,
                resultado_usuario=None,
                resultado_rival= None
            )

#Crea los datos del jugador visitante en la partida con sus estadisticas a 0 al principio
            registro_visitante = Participante_partida(
                id_partida=nueva_partida.id_partida,
                id_participante_torneo=jugador_visitante.id_participante,
                posicion=0,
                puntos=0,
                eliminacion=False,
                resultado_usuario=None,
                resultado_rival=None
            )

#Se añade cada participante
            db_session.add(registro_local)
            db_session.add(registro_visitante)
#Guardamos la partida generada
            partidos_generados.append(nueva_partida)

    return partidos_generados

#FASE DE GRUPOS
def generar_fase_grupos(id_torneo):

#Obtenemos el torneo desde la bd
    torneo = db_session.get(Torneo, id_torneo)

#Obtenemos todos lo participantes del torneo
    participantes_torneo = db_session.query(Participante_torneo)\
        .filter_by(id_torneo=id_torneo)\
        .all()

#Si el numero de participantes es inferior a 4 no se crean los grupos
    if len(participantes_torneo) < 4:
        return "No hay suficientes jugadores para crear grupos"

#Genera los grupos automáticamente con los participantes del torneo
    grupos_creados = crear_grupos_automaticos(torneo, participantes_torneo)

#Se asigna un id
    db_session.flush()

#Guardamos las partidas en la lista
    todos_los_partidos = []

#Recorremos todos los grupos
    for grupo_actual in grupos_creados:

#Genera todos los partidos del grupo actual
        partidos_grupo = generar_partidos_por_grupo(
            grupo_actual,
            participantes_torneo
        )

#Añadimos las partidas del grupo a la lista total de partidos
        todos_los_partidos.extend(partidos_grupo)
#Guardamos los cambios
    db_session.commit()

    return {
        "mensaje": "Fase de grupos generada correctamente",
        "grupos": len(grupos_creados),
        "partidos": len(todos_los_partidos)
    }

#VER GRUPO
@app.route("/torneo/<int:id_torneo>/grupos")
def ver_grupos_torneo(id_torneo):

#Obtenemos el torneo y comprobamos si el juego es de equipo
    torneo_obj = db_session.get(Torneo, id_torneo)
    es_juego_equipo = torneo_obj.juego_obj.es_equipo if torneo_obj else False

#Obtenemos todos los grupos del torneo
    grupos = db_session.query(Grupo).filter_by(id_torneo=id_torneo).all()

#Creamos una lista de resutados
    resultado = []

#Recorremos los grupos
    for grupo in grupos:

#Obtenemos los participantes asignados a este grupo
        participantes_grupo = db_session.query(Participante_torneo).filter_by(id_grupo=grupo.id_grupo).all()

#Obtenemos las partidas de este grupo filtrando por su nombre
        partidas = db_session.query(Partida)\
            .filter(
                Partida.id_torneo == id_torneo,
                Partida.tipo_partida.like(f"%Grupo {grupo.nombre}%")
            ).all()

        partidas_json = []

#Recorremos todas las partidas
        for p in partidas:

#Obtenemos los participantes de cada partida
            participantes_partida = db_session.query(Participante_partida)\
                .filter_by(id_partida=p.id_partida)\
                .all()

#Creamos una lista de jugadores
            jugadores = []

            for pp in participantes_partida:

#Si es torneo de equipo obtenemos el nombre del equipo, si no el del usuario
                if es_juego_equipo:
                    nombre = pp.participante_obj.equipo_obj.nombre \
                        if (pp.participante_obj and pp.participante_obj.equipo_obj) \
                        else "Equipo eliminado"
                elif pp.participante_obj and pp.participante_obj.usuario_obj:
                    nombre = pp.participante_obj.usuario_obj.nombre_usuario
                else:
                    nombre = "Usuario eliminado"

#Añadimos los nombres a la lista de jugadores
                jugadores.append(nombre)

            partidas_json.append({
                "id_partida": p.id_partida,
                "jugadores": jugadores
            })

        participantes_json = []

        for participante in participantes_grupo:

#Según el tipo de torneo extraemos nombre e id de equipo o de usuario
            if es_juego_equipo:
                nombre_usuario = participante.equipo_obj.nombre if participante.equipo_obj else "Equipo eliminado"
                id_usuario = None
                id_equipo = participante.equipo_obj.id_equipo if participante.equipo_obj else None
            else:
                nombre_usuario = None
                id_usuario = None
                id_equipo = None
                if participante.usuario_obj:
                    nombre_usuario = participante.usuario_obj.nombre_usuario
                    id_usuario = participante.usuario_obj.id_usuario
                if nombre_usuario is None:
                    nombre_usuario = "Usuario eliminado"

            participantes_json.append({
                "id_usuario": id_usuario,
                "id_equipo": id_equipo,
                "usuario": nombre_usuario
            })

#Añadimos el grupo con sus participantes y partidas al resultado
        resultado.append({
            "grupo": grupo.nombre,
            "participantes": participantes_json,
            "partidas": partidas_json
        })

#Devolvemos el resultado completo en formato JSON
    return jsonify(resultado)

def generar_encuentros(participantes):
#Mezclamos los participantes aleatoriamente para que los emparejamientos sean al azar
    random.shuffle(participantes)

#Lista donde guardamos los encuentros generados
    encuentros = []

#Recorremos los participantes de dos en dos para emparejarlos
    for i in range(0, len(participantes), 2):
        if i + 1 < len(participantes):
            encuentros.append({
                "jugador_a": participantes[i].usuario_obj.nombre_usuario,
                "jugador_b": participantes[i+1].usuario_obj.nombre_usuario
            })
        else:
#Si el número de participantes es impar el último recibe un bye automático
            encuentros.append({
                "jugador_a": participantes[i].usuario_obj.nombre_usuario,
                "jugador_b": "BYE"
            })

    return encuentros

def obtener_nombre_rondas(total_partidas):
#Diccionario que relaciona el número de partidas con el nombre de la ronda
    rondas = {
        1: "Final",
        2: "Semifinal",
        4: "Cuartos",
        8: "Octavos",
        16: "Dieciseisavos",
        32: "Treintaidosavos"
    }

#Devolvemos el nombre de la ronda o uno genérico si no está en el diccionario
    return rondas.get(
        total_partidas,
        f"Ronda {total_partidas}"
    )


#PARTICIPAR TORNEO
@app.route("/participar_torneo/<int:id_torneo>", methods=["GET", "POST"])
def participar_torneo(id_torneo):

    # Si no hay sesión activa redirigimos al inicio
    if "nombre_usuario" not in session:
        return redirect("/")

#Comprbamos si el usuario esta logeado
    usuario = db_session.query(Usuario).filter_by(
        nombre_usuario=session["nombre_usuario"]
    ).first()

#Comprobamos si es el torneo en el que se realiza todo
    torneo = db_session.query(Torneo).filter_by(id_torneo=id_torneo).first()

#Si el torneo no existe devolvemos un error 404
    if not torneo:
        return "Torneo no encontrado", 404

#Evitamos que la gente entre al torneo cuando este está cerrado
    if torneo.estado == "Cerrado":
        flash("El torneo está cerrado")
        return redirect(f"/torneo/{id_torneo}")

#Evitamos que entre la gente al torneo cuando este ya está lleno
    if len(torneo.participantes) >= torneo.max_participantes:
        flash("El torneo está lleno")
        return redirect(f"/torneo/{id_torneo}")

#Evitamos duplicados comprobando si el usuario ya está inscrito
    existe = db_session.query(Participante_torneo).filter_by(
        id_usuario=usuario.id_usuario,
        id_torneo=id_torneo
    ).first()

    if existe and request.method == "POST":
        return jsonify({"error": "Ya estás inscrito en este torneo"}), 400

#Comprobamos si el juego del torneo es de equipo
    es_juego_equipo = torneo.juego_obj.es_equipo

#Sirve para la incripcion de equipos a torneos
    if request.method == "POST" and es_juego_equipo:
        data = request.form

#Obtenemos el equipo e ids de miembros seleccionados del formulario
        id_equipo_sel = data.get("id_equipo")
        miembros_ids = request.form.getlist("miembros")

#Verificamos que se ha seleccionado un equipo
        if not id_equipo_sel:
            flash("Debes seleccionar un equipo")
            return redirect(f"/participar_torneo/{id_torneo}")

#Verificamos que el equipo existe
        equipo_sel = db_session.get(Equipo, int(id_equipo_sel))
        if not equipo_sel:
            flash("Equipo no encontrado")
            return redirect(f"/participar_torneo/{id_torneo}")

#Solo el capitán puede inscribir al equipo
        if equipo_sel.id_capitan != usuario.id_usuario:
            flash("Solo el capitán del equipo puede inscribirlo en un torneo")
            return redirect(f"/participar_torneo/{id_torneo}")

#El equipo necesita al menos 5 miembros para participar
        if len(equipo_sel.miembros) < 5:
            flash("El equipo necesita al menos 5 miembros para participar")
            return redirect(f"/participar_torneo/{id_torneo}")

#Evitamos que el mismo equipo se inscriba dos veces
        equipo_ya_inscrito = db_session.query(Participante_torneo).filter_by(
            id_equipo=int(id_equipo_sel), id_torneo=id_torneo
        ).first()
        if equipo_ya_inscrito:
            flash("Este equipo ya está inscrito en el torneo")
            return redirect(f"/participar_torneo/{id_torneo}")

#Verificamos que se han seleccionado miembros participantes
        if not miembros_ids:
            flash("Debes seleccionar al menos un miembro participante")
            return redirect(f"/participar_torneo/{id_torneo}")

#Verificamos que no se supera el límite de miembros permitido
        max_m = torneo.max_miembros_equipo or len(equipo_sel.miembros)
        if len(miembros_ids) > max_m:
            flash(f"Solo puedes llevar un máximo de {max_m} miembros")
            return redirect(f"/participar_torneo/{id_torneo}")

#Comprobación final de plazas disponibles
        if len(torneo.participantes) >= torneo.max_participantes:
            return "Torneo lleno", 400

#Creamos el participante del torneo y lo añadimos a la base de datos
        participante = Participante_torneo(
            id_torneo=id_torneo,
            id_usuario=usuario.id_usuario,
            fecha_inscripcion=datetime.now().date(),
            estado="Activo",
            id_personaje=None, id_club=None,
            id_arma_principal=None, id_arma_secundaria=None, id_arma_arrojadiza=None,
            victorias=0, derrotas=0, empate=0,
            ronda_ganadas=0, rondas_perdidas=0, diferencia_rondas=0,
            puntos_totales=0, ranking_final=0,
            id_equipo=int(id_equipo_sel)
        )
        db_session.add(participante)
        db_session.flush()

#Añadimos cada miembro seleccionado como Miembro_participante
        for id_m in miembros_ids:
            db_session.add(Miembro_participante(
                id_participante_torneo=participante.id_participante,
                id_usuario=int(id_m)
            ))

        db_session.commit()
        return redirect(f"/torneo/{id_torneo}")

#INSCRIPCIÓN SIN EQUIPO

#Obtenemos el tipo de elemento del juego para saber qué campos mostrar
    tipo_elemento = torneo.juego_obj.tipo_elemento or ""

    if request.method == "POST":

        data = request.form

#Verificamos que se han seleccionado los elementos obligatorios según el tipo de juego
        if tipo_elemento in ("Personajes", "Personajes y Armas") and not data.get("id_personaje"):
            flash("Debes seleccionar un personaje")
            return redirect(f"/participar_torneo/{id_torneo}")

        if tipo_elemento == "Equipos" and not data.get("id_club"):
            flash("Debes seleccionar un club")
            return redirect(f"/participar_torneo/{id_torneo}")

        if tipo_elemento in ("Armas", "Personajes y Armas") and not data.get("id_arma_principal"):
            flash("Debes seleccionar un arma principal")
            return redirect(f"/participar_torneo/{id_torneo}")

#Comprobación final de plazas disponibles
        if len(torneo.participantes) >= torneo.max_participantes:
            return "Torneo lleno", 400

#Creamos el participante con los elementos seleccionados y lo guardamos
        participante = Participante_torneo(
            id_torneo=id_torneo,
            id_usuario=usuario.id_usuario,
            fecha_inscripcion=datetime.now().date(),
            estado="Activo",
            id_personaje=data.get("id_personaje") or None,
            id_club=data.get("id_club") or None,
            id_arma_principal=data.get("id_arma_principal") or None,
            id_arma_secundaria=data.get("id_arma_secundaria") or None,
            id_arma_arrojadiza=data.get("id_arma_arrojadiza") or None,
            victorias=0, derrotas=0, empate=0,
            ronda_ganadas=0, rondas_perdidas=0, diferencia_rondas=0,
            puntos_totales=0, ranking_final=0
        )

#Añadimos y guardamos los cambios
        db_session.add(participante)
        db_session.commit()

        return redirect(f"/torneo/{id_torneo}")

#FORMULARIO DINAMICO

#Caso equipos
    if es_juego_equipo:
#Lista de equipos donde el usuario es capitán y cumplen los requisitos
        equipos_disponibles = []
        equipos_capitan = db_session.query(Equipo).filter_by(id_capitan=usuario.id_usuario).all()
        for eq in equipos_capitan:
#Descartamos equipos con menos de 5 miembros o ya inscritos
            if len(eq.miembros) < 5:
                continue
            ya_inscrito = db_session.query(Participante_torneo).filter_by(
                id_equipo=eq.id_equipo, id_torneo=id_torneo
            ).first()
            if ya_inscrito:
                continue
            equipos_disponibles.append({
                "equipo": eq,
                "miembros": [
                    {"id": mb.id_usuario, "nombre": mb.usuario_obj.nombre_usuario, "rol": mb.rol}
                    for mb in eq.miembros
                ]
            })

#Mostramos a los participantes del torneo
        return render_template(
            "participar.html",
            usuario=usuario,
            torneo=torneo,
            id_torneo=id_torneo,
            es_equipo=True,
            equipos_disponibles=equipos_disponibles,
            max_miembros=torneo.max_miembros_equipo or 999
        )

#Caso 1v1
#Listas de elementos seleccionables según el tipo de juego
    personajes = []
    clubs = []
    arma_principal = []
    arma_secundaria = []
    arma_arrojadiza = []

#Comprobamos los elementos y los llamamos a la bd
    if tipo_elemento in ("Personajes", "Personajes y Armas"):
        personajes = db_session.query(Personaje).filter_by(id_juego=torneo.id_juego).all()

    if tipo_elemento == "Equipos":
        clubs = db_session.query(Club).filter_by(id_juego=torneo.id_juego).all()

    if tipo_elemento in ("Armas", "Personajes y Armas"):
        todas_las_armas = db_session.query(Armas).filter_by(id_juego=torneo.id_juego).all()

        tipos_principal = {"Rifle de asalto", "Rifle de asalto clásico", "Ametralladora ligera",
                           "Ametralladora pesada", "Escopeta", "Francotirador", "Francotirador pesado"}
        tipos_secundaria = {"Pistola", "Misil"}
        tipos_arrojadiza = {"Arrojadiza", "Explosivo"}

        armas_clasificadas = [a for a in todas_las_armas if a.tipo_arma in tipos_principal | tipos_secundaria | tipos_arrojadiza]

#Si hay armas clasificadas las separamos por tipo, si no usamos todas como principal
        if armas_clasificadas:
            arma_principal = [a for a in todas_las_armas if a.tipo_arma in tipos_principal]
            arma_secundaria = [a for a in todas_las_armas if a.tipo_arma in tipos_secundaria]
            arma_arrojadiza = [a for a in todas_las_armas if a.tipo_arma in tipos_arrojadiza]
        else:
            arma_principal = todas_las_armas

#Mostramos los elementos disponibles según el juego
    return render_template(
        "participar.html",
        usuario=usuario,
        torneo=torneo,
        personajes=personajes,
        clubs=clubs,
        arma_principal=arma_principal,
        arma_secundaria=arma_secundaria,
        arma_arrojadiza=arma_arrojadiza,
        id_torneo=id_torneo,
        es_equipo=False
    )

@app.route("/torneo/<int:id_torneo>")
def ver_torneo(id_torneo):

#Obtenemos el torneo de la base de datos
    torneo = db_session.query(Torneo).filter_by(id_torneo=id_torneo).first()

#Si el torneo no existe devolvemos un error 404
    if not torneo:
        return "Torneo no encontrado", 404

    mostrar_modal_organizador = False
    es_obligatorio = False

#Un torneo es huérfano si lo tiene el admin pero el admin no es participante
    organizador_es_admin = (
        torneo.usuario_obj is not None and
        torneo.usuario_obj.rol_obj.id_rol == 1
    )
    admin_es_participante = db_session.query(Participante_torneo).filter_by(
        id_torneo=id_torneo,
        id_usuario=torneo.id_usuario
    ).first() is not None

    torneo_huerfano = organizador_es_admin and not admin_es_participante

#Si el torneo es huérfano y hay un usuario logueado le preguntamos si quiere ser organizador
    if torneo_huerfano and "nombre_usuario" in session:

        usuario_actual = db_session.query(Usuario).filter_by(
            nombre_usuario=session["nombre_usuario"]
        ).first()

        if usuario_actual:
#Comprobamos si el usuario participa en el torneo y aún no ha respondido
            participacion_actual = db_session.query(Participante_torneo).filter_by(
                id_torneo=id_torneo,
                id_usuario=usuario_actual.id_usuario
            ).first()

            if participacion_actual and participacion_actual.aceptar_organizador is None:
                mostrar_modal_organizador = True

#Contamos cuántos otros participantes hay y cuántos aún no han respondido
                total_otros = db_session.query(Participante_torneo).filter(
                    Participante_torneo.id_torneo == id_torneo,
                    Participante_torneo.id_usuario != usuario_actual.id_usuario,
                ).count()

                otros_sin_responder = db_session.query(Participante_torneo).filter(
                    Participante_torneo.id_torneo == id_torneo,
                    Participante_torneo.id_usuario != usuario_actual.id_usuario,
                    Participante_torneo.aceptar_organizador.is_(None)
                ).count()

#Si todos los demás ya rechazaron el cargo este usuario debe aceptar obligatoriamente
                es_obligatorio = (total_otros > 0 and otros_sin_responder == 0)

#Obtenemos los participantes y partidas del torneo
    participantes = db_session.query(Participante_torneo).filter_by(
        id_torneo=id_torneo
    ).all()

    partidas = db_session.query(Partida).filter_by(
        id_torneo=id_torneo
    ).all()

#Obtenemos el usuario de la sesión si está logueado
    usuario_sesion = None
    if "nombre_usuario" in session:
        usuario_sesion = db_session.query(Usuario).filter_by(
            nombre_usuario=session["nombre_usuario"]
        ).first()

#Comprobamos si el usuario es organizador o admin y si el torneo es de equipo
    es_organizador_o_admin = _es_organizador_o_admin(torneo, usuario_sesion)
    es_equipo = torneo.juego_obj.es_equipo

#Obtenemos los ids de participación del usuario para saber en qué partidas puede subir resultado
    ids_participante_usuario = set()
    if usuario_sesion:
        if es_equipo:
#Solo el capitán puede subir resultados
            participaciones_equipo = db_session.query(Participante_torneo)\
                .join(Equipo, Participante_torneo.id_equipo == Equipo.id_equipo)\
                .filter(
                    Participante_torneo.id_torneo == id_torneo,
                    Equipo.id_capitan == usuario_sesion.id_usuario
                ).all()
            ids_participante_usuario = {p.id_participante for p in participaciones_equipo}
        else:
            pt = db_session.query(Participante_torneo).filter_by(
                id_torneo=id_torneo,
                id_usuario=usuario_sesion.id_usuario
            ).first()
            if pt:
                ids_participante_usuario = {pt.id_participante}

#Mostramos los datos necesarios a la plantilla del torneo
    return render_template(
        "torneo.html",
        torneo=torneo,
        participantes=participantes,
        partidas=partidas,
        mostrar_modal_organizador=mostrar_modal_organizador,
        es_obligatorio=es_obligatorio,
        es_organizador_o_admin=es_organizador_o_admin,
        es_equipo=es_equipo,
        ids_participante_usuario=ids_participante_usuario
    )

@app.route("/torneo/<int:id_torneo>/aceptar_organizador", methods=["POST"])
def aceptar_ser_organizador(id_torneo):

#Si no hay sesión activa devolvemos un error
    if "nombre_usuario" not in session:
        return jsonify({"error": "No autorizado"}), 401

#Obtenemos el usuario actual de la sesión
    usuario_actual = db_session.query(Usuario).filter_by(
        nombre_usuario=session["nombre_usuario"]
    ).first()

#Si no es el usuario actual salta un error 404
    if not usuario_actual:
        return jsonify({"error": "Usuario no encontrado"}), 404

#Verificamos que el usuario es participante del torneo
    participacion = db_session.query(Participante_torneo).filter_by(
        id_torneo=id_torneo,
        id_usuario=usuario_actual.id_usuario
    ).first()

#Si no eres participante del torneo salta un error 403
    if not participacion:
        return jsonify({"error": "No eres participante de este torneo"}), 403

#Obtenemos el torneo
    torneo = db_session.get(Torneo, id_torneo)
    if not torneo:
        return jsonify({"error": "Torneo no encontrado"}), 404

#Asignamos al usuario como nuevo organizador del torneo
    torneo.id_usuario = usuario_actual.id_usuario
    participacion.aceptar_organizador = True

#Si el usuario es un usuario normal le ascendemos a organizador
    if usuario_actual.rol_obj.nombre_rol == "Usuario":
        rol_organizador = db_session.query(Rol).filter_by(nombre_rol="Organizador").first()
        if rol_organizador:
            usuario_actual.rol_obj = rol_organizador

#Guardamos el cambio
    db_session.commit()
    return jsonify({"mensaje": "Ahora eres el organizador del torneo"})


@app.route("/torneo/<int:id_torneo>/rechazar_organizador", methods=["POST"])
def rechazar_ser_organizador(id_torneo):

#Si no hay sesión activa devolvemos un error
    if "nombre_usuario" not in session:
        return jsonify({"error": "No autorizado"}), 401

#Obtenemos el usuario actual de la sesión
    usuario_actual = db_session.query(Usuario).filter_by(
        nombre_usuario=session["nombre_usuario"]
    ).first()

#Si no es el usuario actual se devuelve un error 404
    if not usuario_actual:
        return jsonify({"error": "Usuario no encontrado"}), 404

#Verificamos que el usuario es participante del torneo
    participacion = db_session.query(Participante_torneo).filter_by(
        id_torneo=id_torneo,
        id_usuario=usuario_actual.id_usuario
    ).first()

#Si no es participante del torneo nos salta un error 403
    if not participacion:
        return jsonify({"error": "No eres participante de este torneo"}), 403

#Marcamos la participación como rechazada y guardamos
    participacion.aceptar_organizador = False
    db_session.commit()

    return jsonify({"mensaje": "Has rechazado ser el organizador"})


@app.route("/cerrar_torneo/<int:id_torneo>", methods=["POST"])
def cerrar_torneo(id_torneo):

    try:
#Obtenemos el torneo de la base de datos
        torneo = db_session.get(Torneo, id_torneo)

#Si no es un torneo nos salta el error 404
        if not torneo:
            return jsonify({"error": "Torneo no encontrado"}), 404

#Si el torneo ya está cerrado no hacemos nada
        if torneo.estado == "Cerrado":
            return jsonify({"mensaje": "El torneo ya está cerrado"}), 200

#Comprobamos que hay sesión activa
        if "nombre_usuario" not in session:
            return jsonify({"error": "No autorizado"}), 401

#Obtenemos el usuario de la sesión
        usuario = db_session.query(Usuario).filter_by(
            nombre_usuario=session["nombre_usuario"]
        ).first()

#Si no obtenemos usuario nos salta el error 404
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

#Solo el organizador o un administrador pueden cerrar el torneo
        if not _es_organizador_o_admin(torneo, usuario):
            return jsonify({"error": "No tienes permiso para cerrar este torneo"}), 403

#Obtenemos los participantes del torneo
        participantes = db_session.query(Participante_torneo)\
            .filter_by(id_torneo=id_torneo)\
            .all()

#Se necesitan al menos 5 jugadores para generar la fase de grupos
        if len(participantes) < 5:
            return jsonify({"error": "Se necesitan al menos 5 jugadores para fase de grupos"}), 400

#Limpiamos los datos anteriores por si el torneo se había cerrado antes
        db_session.query(Participante_partida)\
            .filter(Participante_partida.id_partida.in_(
                db_session.query(Partida.id_partida).filter_by(id_torneo=id_torneo)
            )).delete(synchronize_session=False)

#Elimina las partidas del torneo
        db_session.query(Partida).filter_by(id_torneo=id_torneo).delete()
#Elimina los grupos del torneo
        db_session.query(Grupo).filter_by(id_torneo=id_torneo).delete()

        db_session.flush()

#GENERAR LA FASE DE GRUPOS
        resultado = generar_fase_grupos(id_torneo)

#Si la generación falla revertimos los cambios
        if isinstance(resultado, str):
            db_session.rollback()
            return jsonify({"error": resultado}), 400

#Cerramos el torneo y guardamos los cambios
        torneo.estado = "Cerrado"
        db_session.commit()

        return jsonify({
            "mensaje": "Fase de grupos generada correctamente",
            "grupos": resultado["grupos"],
            "partidos": resultado["partidos"]
        })

    except Exception as e:
#Si ocurre cualquier error inesperado revertimos y devolvemos el mensaje
        db_session.rollback()
        return jsonify({
            "error": str(e)
        }), 500

@app.route("/torneo/<int:id_torneo>/mostrar_participante/<int:id_usuario>")
def mostrar_participante(id_torneo, id_usuario):

#Buscamos la participación del usuario en el torneo
    participante = db_session.query(Participante_torneo).filter_by(
        id_torneo=id_torneo,
        id_usuario=id_usuario
    ).first()

#Si no es un participante salta el error 404
    if not participante:
        return jsonify({"error": "Participante no encontrado"}), 404

#Devolvemos los datos del participante con sus estadísticas
    return jsonify({
        "usuario": participante.usuario_obj.nombre_usuario,
        "personaje": participante.personaje_obj.nombre_personaje if participante.personaje_obj else None,
        "club": participante.club_obj.nombre_club if participante.club_obj else None,
        "victorias": participante.victorias,
        "derrotas": participante.derrotas,
        "empates": participante.empate
    })

@app.route("/torneo/<int:id_torneo>/mostrar_equipo/<int:id_equipo>")
def mostrar_equipo(id_torneo, id_equipo):

#Buscamos la participación del equipo en el torneo
    participante = db_session.query(Participante_torneo).filter_by(
        id_torneo=id_torneo,
        id_equipo=id_equipo
    ).first()

#Si no el equipo no participa no salta el error 404
    if not participante:
        return jsonify({"error": "Equipo no encontrado en torneo"}), 404

#Obtenemos el equipo y la lista de nombres de sus miembros participantes
    equipo = participante.equipo_obj
    miembros_lista = [m.usuario_obj.nombre_usuario for m in participante.miembros_participantes if m.usuario_obj]

#Devolvemos los datos del equipo con sus estadísticas
    return jsonify({
        "es_equipo": True,
        "usuario": equipo.nombre,
        "miembros": miembros_lista,
        "victorias": participante.victorias or 0,
        "derrotas": participante.derrotas or 0,
        "empates": participante.empate or 0,
    })

@app.route("/torneo/<int:id_torneo>/mi_participante")
def mi_participante(id_torneo):

    try:
#Si no hay sesión activa devolvemos un error
        if "nombre_usuario" not in session:
            return jsonify({"error": "No autorizado"}), 401

#Obtenemos el usuario de la sesión
        usuario = db_session.query(Usuario).filter_by(
            nombre_usuario=session["nombre_usuario"]
        ).first()

        if not usuario:
            return jsonify({"error": "Usuario no existe"}), 404

#Obtenemos el torneo
        torneo_obj = db_session.get(Torneo, id_torneo)
        if not torneo_obj:
            return jsonify({"error": "Torneo no encontrado"}), 404

#Si el torneo es de equipo buscamos al usuario entre los miembros participantes
        if torneo_obj.juego_obj.es_equipo:
            miembro = db_session.query(Miembro_participante)\
                .join(Participante_torneo, Miembro_participante.id_participante_torneo == Participante_torneo.id_participante)\
                .filter(
                    Participante_torneo.id_torneo == id_torneo,
                    Miembro_participante.id_usuario == usuario.id_usuario
                ).first()

            if not miembro:
                return jsonify({"error": "No eres participante del torneo"}), 200

#Obtenemos el equipo y la lista de miembros participantes
            participante = miembro.participante_obj
            equipo = participante.equipo_obj
            miembros_lista = [m.usuario_obj.nombre_usuario for m in participante.miembros_participantes if m.usuario_obj]

#Devolvemos los datos del equipo con sus estadísticas
            return jsonify({
                "es_equipo": True,
                "usuario": equipo.nombre,
                "miembros": miembros_lista,
                "victorias": participante.victorias or 0,
                "derrotas": participante.derrotas or 0,
                "empates": participante.empate or 0,
                "puntos": participante.puntos_totales or 0
            })

#Si es torneo 1v1 buscamos directamente la participación del usuario
        participante = db_session.query(Participante_torneo).filter_by(
            id_usuario=usuario.id_usuario,
            id_torneo=id_torneo
        ).first()

#Si no es participante nos salta error
        if not participante:
            return jsonify({"error": "No eres participante del torneo"}), 200

#Devolvemos los datos del usuario con sus estadísticas
        return jsonify({
            "es_equipo": False,
            "usuario": usuario.nombre_usuario,
            "personaje": participante.personaje_obj.nombre_personaje
            if participante.personaje_obj else None,
            "club": participante.club_obj.nombre_club
            if participante.club_obj else None,
            "victorias": participante.victorias or 0,
            "derrotas": participante.derrotas or 0,
            "empates": participante.empate or 0,
            "puntos": participante.puntos_totales or 0
        })

    except Exception as e:
#Si ocurre cualquier error inesperado devolvemos el mensaje
        return jsonify({"error": str(e)}), 500

@app.route("/partida/<int:id_partida>/resultado", methods=["POST"])
def guardar_resultado(id_partida):

    try:
#Si no hay sesión activa devolvemos un error
        if "nombre_usuario" not in session:
            return jsonify({"error": "No autorizado"}), 401

#Obtenemos el usuario de la sesión y la partida
        usuario = db_session.query(Usuario).filter_by(
            nombre_usuario=session["nombre_usuario"]
        ).first()

#Obtenemos la partida que se a jugagdo
        partida = db_session.get(Partida, id_partida)

#Si no es una partida nos salta un error
        if not partida:
            return jsonify({"error": "Partida no encontrada"}), 404

# INPUTS
# Recogemos los resultados y la captura enviados por el formulario
        resultado_usuario = request.form.get("resultado_usuario", "").strip()
        resultado_rival = request.form.get("resultado_rival", "").strip()
        captura = request.files.get("captura_resultado")

#Verificamos que se han enviado ambos resultados
        if resultado_usuario == "" or resultado_rival == "":
            return jsonify({"error": "Faltan resultados"}), 400

#Verificamos que los resultados son números válidos
        if not resultado_usuario.isdigit() or not resultado_rival.isdigit():
            return jsonify({"error": "Solo se permiten números"}), 400

        resultado_usuario = int(resultado_usuario)
        resultado_rival = int(resultado_rival)

#Buscamos al participante actual en la partida por su usuario
        participante_actual = db_session.query(Participante_partida)\
            .join(Participante_torneo)\
            .filter(
                Participante_partida.id_partida == id_partida,
                Participante_torneo.id_usuario == usuario.id_usuario,
                Participante_partida.id_participante_torneo == Participante_torneo.id_participante
            ).first()

        if not participante_actual:
#En torneos de equipo comprobamos si el usuario es capitán del equipo participante
            participante_equipo = db_session.query(Participante_partida)\
                .join(Participante_torneo, Participante_partida.id_participante_torneo == Participante_torneo.id_participante)\
                .join(Equipo, Participante_torneo.id_equipo == Equipo.id_equipo)\
                .filter(
                    Participante_partida.id_partida == id_partida,
                    Equipo.id_capitan == usuario.id_usuario
                ).first()
            if participante_equipo:
                participante_actual = participante_equipo

#Si no es participante nos salta el error
        if not participante_actual:
            return jsonify({"error": "No participas en esta partida"}), 403

#Guardamos el resultado enviado por este participante
        participante_actual.resultado_usuario = resultado_usuario
        participante_actual.resultado_rival = resultado_rival
        participante_actual.confirmar_resultados = False

#Si se ha enviado una captura la guardamos en disco y registramos la ruta
        if captura and captura.filename != "":

            carpeta = "static/capturas"
            os.makedirs(carpeta, exist_ok=True)

            nombre = f"{id_partida}_{usuario.id_usuario}_{captura.filename}"
            ruta_guardado = os.path.join(carpeta, nombre)

            captura.save(ruta_guardado)

            participante_actual.captura_resultado = ruta_guardado

#Obtenemos los dos participantes de la partida en orden fijo
        participantes = db_session.query(Participante_partida).filter(
            Participante_partida.id_partida == id_partida
        ).order_by(Participante_partida.id_participante_partida.asc()).all()

#Si el numero de participanete es menor a 2 nos satla el error
        if len(participantes) < 2:
            return jsonify({"error": "Partida incompleta"}), 400

        p1 = participantes[0]
        p2 = participantes[1]

#SI AMBOS HAN ENVIADO RESULTADOS
        if (
            p1.resultado_usuario is not None and
            p2.resultado_usuario is not None and
            p1.resultado_rival is not None and
            p2.resultado_rival is not None
        ):
#Comprobamos si los resultados de ambos coinciden de forma cruzada
            coincide = (
                p1.resultado_usuario == p2.resultado_rival and
                p2.resultado_usuario == p1.resultado_rival
            )

            if coincide:

#Guardamos el resultado final siempre en orden fijo p1-p2
                resultado_final = f"{p1.resultado_usuario}-{p2.resultado_usuario}"

#Si tenemos el resultado final pasa a estar la partida finalizada y se guardan los resultados
                partida.resultado_final = resultado_final
                partida.estado = "Finalizado"

                puntos1 = p1.resultado_usuario
                puntos2 = p2.resultado_usuario

                participante1 = p1.participante_obj
                participante2 = p2.participante_obj

#En eliminatorias no se permiten empates
                if es_eliminatoria(partida) and puntos1 == puntos2:
                    return jsonify({"error": "En eliminatorias no se permiten empates"}), 400

#Asignamos el ganador según los puntos
                if puntos1 > puntos2:
                    partida.ganador_id = participante1.id_participante
                elif puntos2 > puntos1:
                    partida.ganador_id = participante2.id_participante
                else:
                    partida.ganador_id = None

#En fase de grupos actualizamos victorias, derrotas, empates y puntos
                if not es_eliminatoria(partida):
                    if puntos1 > puntos2:
                        participante1.victorias += 1
                        participante1.puntos_totales += 3
                        participante2.derrotas += 1
                    elif puntos2 > puntos1:
                        participante2.victorias += 1
                        participante2.puntos_totales += 3
                        participante1.derrotas += 1
                    else:
                        participante1.empate += 1
                        participante1.puntos_totales += 1
                        participante2.empate += 1
                        participante2.puntos_totales += 1

#Actualizamos las rondas ganadas, perdidas y la diferencia
                    participante1.rondas_ganadas += puntos1
                    participante1.rondas_perdidas += puntos2
                    participante1.diferencia_rondas = participante1.rondas_ganadas - participante1.rondas_perdidas
                    participante2.rondas_ganadas += puntos2
                    participante2.rondas_perdidas += puntos1
                    participante2.diferencia_rondas = participante2.rondas_ganadas - participante2.rondas_perdidas

#En eliminatorias hacemos avanzar al ganador y comprobamos si el torneo ha terminado
                if es_eliminatoria(partida):
                    avanzar_ganador_eliminatoria(partida)
                    verificar_fin_torneo(partida)

                p1.confirmar_resultados = True
                p2.confirmar_resultados = True

            else:
#Si los resultados no coinciden la partida queda pendiente de revisión
                partida.estado = "Pendiente de revision"

                p1.confirmar_resultados = False
                p2.confirmar_resultados = False

        else:
#Si solo uno ha enviado resultado la partida sigue pendiente
            partida.estado = "Pendiente"

#Se guardan los cambios
        db_session.commit()

#Comprobamos si la fase de grupos ha terminado tras guardar el resultado
        verificar_fin_fase_grupos(partida.id_torneo)

        return jsonify({
            "mensaje": "Resultado guardado correctamente",
            "estado": partida.estado,
            "resultado_final": partida.resultado_final
        })

    except Exception as e:
#Si ocurre cualquier error inesperado revertimos y devolvemos el mensaje
        db_session.rollback()

        return jsonify({
            "error": "Error interno",
            "detalle": str(e)
        }), 500

@app.route("/partida/<int:id_partida>/estado_resultado")
def estado_resultado_partida(id_partida):

#Obtenemos la partida de la base de datos
    partida = db_session.get(Partida, id_partida)

#Si no encontramos la partida nos salta el error
    if not partida:
        return jsonify({"error": "Partida no encontrada"}), 404

#Obtenemos los participantes de la partida en orden fijo
    participantes_partida = db_session.query(Participante_partida).filter_by(
        id_partida=id_partida
    ).order_by(Participante_partida.id_participante_partida.asc()).all()

#Filtramos los participantes que ya han enviado su resultado
    resultados_enviados = [
        participante
        for participante in participantes_partida
        if participante.resultado_usuario is not None
    ]

#Comprobamos si uno o ambos participantes ya han enviado resultado
    primer_resultado_enviado = len(resultados_enviados) >= 1
    ambos_enviaron = len(resultados_enviados) >= 2

#Devolvemos el estado de la partida y si han enviado resultados
    return jsonify({
        "estado": partida.estado,
        "primer_resultado_enviado": primer_resultado_enviado,
        "ambos_enviaron": ambos_enviaron
    })

@app.route("/conflicto/<int:id_partida>")
def obtener_conflicto(id_partida):

    try:
#Si no hay sesión activa devolvemos un error
        if "nombre_usuario" not in session:
            return jsonify({"error": "No autorizado"}), 401

#Obtenemos el usuario de la sesión
        usuario = db_session.query(Usuario).filter_by(
            nombre_usuario=session["nombre_usuario"]
        ).first()

#Si no encontramos al usuario nos salta el error
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

#Obtenemos la partida
        partida = db_session.get(Partida, id_partida)

#Si no encontramos la partida nos salta el error
        if not partida:
            return jsonify({"error": "No existe la partida"}), 404

#Solo el organizador o un administrador pueden ver el conflicto
        if not partida.torneo_obj or not _es_organizador_o_admin(partida.torneo_obj, usuario):
            return jsonify({"error": "No autorizado"}), 403

#Obtenemos los participantes de la partida
        participantes = db_session.query(Participante_partida).filter_by(
            id_partida=id_partida
        ).all()

#Lista con los datos del conflicto de cada participante
        resultado = []

        for p in participantes:

            nombre_usuario = "Usuario eliminado"

#Obtenemos el nombre del participante si existe
            if (
                p.participante_obj and
                p.participante_obj.usuario_obj
            ):
                usuario_obj = p.participante_obj.usuario_obj
                nombre_usuario = usuario_obj.nombre_usuario

#Añadimos sus resultados y captura al listado
            resultado.append({
                "usuario": nombre_usuario,
                "resultado_usuario": p.resultado_usuario,
                "resultado_rival": p.resultado_rival,
                "captura": p.captura_resultado
            })

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/resolver_conflicto/<int:id_partida>", methods=["POST"])
def resolver_conflicto(id_partida):

    try:
#Si no hay sesión activa devolvemos un error
        if "nombre_usuario" not in session:
            return jsonify({"error": "No autorizado"}), 401

#Obtenemos el usuario de la sesión y la partida
        usuario = db_session.query(Usuario).filter_by(
            nombre_usuario=session["nombre_usuario"]
        ).first()

        partida = db_session.get(Partida, id_partida)

#Si no se encuentra la partida nos salta el error
        if not partida:
            return jsonify({"error": "Partida no encontrada"}), 404

#Solo el organizador o un administrador pueden resolver conflictos
        if not _es_organizador_o_admin(partida.torneo_obj, usuario):
            return jsonify({"error": "No autorizado"}), 403

#Obtenemos el resultado final enviado por el organizador
        resultado_final = request.form.get("resultado_final")

#Si no obtenemos el resultado final nos salta el error
        if not resultado_final:
            return jsonify({"error": "Resultado inválido"}), 400

#Guardamos el resultado final y la partida pasa a finalizado
        partida.resultado_final = resultado_final
        partida.estado = "Finalizado"

#Validamos que el formato del resultado sea correcto (ej: 3-1)
        if "-" not in resultado_final:
            return jsonify({"Error" : "Formato invalido"}), 400

#Lo dividimos en dos partes con el split para coger el resultado
        partes = resultado_final.split("-")

#Si el numero de resultados es distinto a 2 nos salta el error
        if len(partes) != 2:
            return jsonify({"error": "Formato inválido"}), 400

        puntos_1 = partes[0].strip()
        puntos_2 = partes[1].strip()

#Verificamos que ambas partes son números
        if not puntos_1.isdigit() or not puntos_2.isdigit():
            return jsonify({"error": "Solo numeros"}), 400

        puntos_1 = int(puntos_1)
        puntos_2 = int(puntos_2)

#En eliminatorias no se permiten empates
        if es_eliminatoria(partida) and puntos_1 == puntos_2:
            return jsonify({
                "error": "En eliminatorias no se permiten empates"
            }), 400

#Obtenemos los participantes de la partida en orden ascendente
        participantes = db_session.query(Participante_partida).filter(
            Participante_partida.id_partida == id_partida
        ).order_by(Participante_partida.id_participante_partida.asc()).all()

#Si el numero de participantes en inferior a 2 nos salta el error
        if len(participantes) < 2:
            return jsonify({"Error" : "Resultado incompleto"}), 400

        p1 = participantes[0]
        p2 = participantes[1]

        participante1 = p1.participante_obj
        participante2 = p2.participante_obj

#Guardamos el resultado final y marcamos la partida como finalizada
        partida.resultado_final = resultado_final
        partida.estado = "Finalizado"

#Calculamos el ganador según los resultados
        if puntos_1 > puntos_2:
            partida.ganador_id = participante1.id_participante
        elif puntos_2 > puntos_1:
            partida.ganador_id = participante2.id_participante
        else:
            partida.ganador_id = None

#En fase de grupos actualizamos victorias, derrotas, empates y puntos
        if not es_eliminatoria(partida):
            if puntos_1 > puntos_2:
                participante1.victorias += 1
                participante1.puntos_totales += 3
                participante2.derrotas += 1
            elif puntos_2 > puntos_1:
                participante2.victorias += 1
                participante2.puntos_totales += 3
                participante1.derrotas += 1
            else:
                participante1.empate += 1
                participante1.puntos_totales += 1
                participante2.empate += 1
                participante2.puntos_totales += 1

#Actualizamos las rondas ganadas, perdidas y la diferencia
            participante1.rondas_ganadas += puntos_1
            participante1.rondas_perdidas += puntos_2
            participante1.diferencia_rondas = participante1.rondas_ganadas - participante1.rondas_perdidas
            participante2.rondas_ganadas += puntos_2
            participante2.rondas_perdidas += puntos_1
            participante2.diferencia_rondas = participante2.rondas_ganadas - participante2.rondas_perdidas

#En eliminatorias hacemos avanzar al ganador y comprobamos si el torneo ha terminado
        if es_eliminatoria(partida) and partida.ganador_id:
            avanzar_ganador_eliminatoria(partida)
            verificar_fin_torneo(partida)

#Confirmamos los resultados de todos los participantes
        for p in participantes:
            p.confirmar_resultados = True

#Guardamos los cambios
        db_session.commit()

#Comprobamos si la fase de grupos ha terminado tras resolver el conflicto
        verificar_fin_fase_grupos(partida.id_torneo)

        return jsonify({
            "mensaje": "Conflicto resuelto correctamente"
        })

    except Exception as e:
#Si ocurre cualquier error inesperado revertimos y devolvemos el mensaje
        db_session.rollback()

        return jsonify({
            "error": str(e)
        }), 500

@app.route("/torneo/<int:id_torneo>/eliminatorias_arbol")
def obtener_eliminatorias_arbol(id_torneo):

#Obtenemos todas las partidas eliminatorias del torneo (excluimos las de grupos)
    partidas = db_session.query(Partida).filter(
        Partida.id_torneo == id_torneo,
        ~Partida.tipo_partida.ilike("%grupo%"),
        Partida.tipo_partida != None
    ).all()

#MAPA DE NODOS
#Construimos un diccionario con cada partida como nodo del árbol
    nodos = {}

    for p in partidas:

#Obtenemos los participantes de cada partida
        participantes = db_session.query(Participante_partida)\
            .filter_by(id_partida=p.id_partida).all()

#Lista con los nombres de los jugadores o equipos de la partida
        jugadores = []

        for pp in participantes:
            if pp.participante_obj and pp.participante_obj.equipo_obj:
                jugadores.append(pp.participante_obj.equipo_obj.nombre)
            elif pp.participante_obj and pp.participante_obj.usuario_obj:
                jugadores.append(pp.participante_obj.usuario_obj.nombre_usuario)
            else:
                jugadores.append("BYE")

# Guardamos el nodo con sus datos y una lista de hijos vacía para construir el árbol después
        nodos[p.id_partida] = {
            "id_partida": p.id_partida,
            "jugadores": jugadores,
            "estado": p.estado,
            "resultado": p.resultado_final,
            "siguiente_id": p.siguiente_partida_id,
            "hijos": []
        }

#CONSTRUIR ARBOL
#Enlazamos cada nodo con su partida padre para formar el árbol eliminatorio
    raiz = None

    for p in partidas:

        nodo = nodos[p.id_partida]

        if p.siguiente_partida_id:
#Si tiene siguiente partida lo añadimos como hijo de ese nodo
            padre = nodos.get(p.siguiente_partida_id)
            if padre:
                padre["hijos"].append(nodo)
        else:
#Si no tiene siguiente partida es la final (raíz del árbol)
            raiz = nodo

#Devolvemos el árbol completo con la raíz como punto de entrada
    return jsonify({
        "torneo_id": id_torneo,
        "raiz": raiz
    })

@app.route("/torneo/<int:id_torneo>/clasificacion_grupos")
def clasificacion_grupos(id_torneo):

    try:
#Obtenemos el torneo y comprobamos si es de equipo
        torneo_clas = db_session.get(Torneo, id_torneo)
        es_equipo_clas = torneo_clas.juego_obj.es_equipo if torneo_clas else False

#Obtenemos todos los grupos del torneo
        grupos = db_session.query(Grupo).filter_by(id_torneo=id_torneo).all()

#Lista para guardar resultados
        resultado = []

        for g in grupos:

#Lista con la clasificación de cada participante del grupo
            clasificacion = []

            participantes = g.participantes or []

            for p in participantes:

                usuario = getattr(p, "usuario_obj", None)

#Obtenemos el nombre según si es torneo de equipo o individual
                if es_equipo_clas:
                    equipo_clas = getattr(p, "equipo_obj", None)
                    nombre = getattr(equipo_clas, "nombre", "Equipo eliminado") if equipo_clas else "Equipo eliminado"
                else:
                    nombre = (
                        getattr(usuario, "nombre_usuario", None)
                        if usuario else "Usuario eliminado"
                    )

#Recogemos las estadísticas del participante
                victorias = p.victorias or 0
                derrotas = p.derrotas or 0
                empates = p.empate or 0

                rg = p.rondas_ganadas or 0
                rp = p.rondas_perdidas or 0
                dr = rg - rp
                pt = p.puntos_totales or 0

#Calculamos el total de partidas jugadas
                pj = victorias + derrotas + empates

# Añadimos al listado la fila de este participante con todas sus estadísticas
                clasificacion.append({
                    "obj": p,
                    "usuario": nombre,
                    "pj": pj,
                    "pg": victorias,
                    "pd": derrotas,
                    "pe": empates,
                    "rg": rg,
                    "rp": rp,
                    "dr": dr,
                    "pt": pt
                })

#Ordenamos por puntos totales y diferencia de rondas de mayor a menor
            clasificacion.sort(key=lambda x: (x["pt"], x["dr"]), reverse=True)

#Asignamos la posición en el grupo y la guardamos en la base de datos
            for i, c in enumerate(clasificacion):
                c["pos"] = i + 1

                participante_obj = c["obj"]
                participante_obj.posicion_grupo = i + 1

#Guardamos los cambios
            db_session.commit()

#Eliminamos el objeto ORM antes de devolver el JSON
            clasificacion_limpia = [
                {k: v for k, v in c.items() if k != "obj"}
                for c in clasificacion
            ]

            resultado.append({
                "grupo": g.nombre,
                "clasificacion": clasificacion_limpia
            })

        return jsonify(resultado)

    except Exception as e:
#Si ocurre cualquier error inesperado revertimos y devolvemos el mensaje
        db_session.rollback()
        return jsonify({"error": str(e)}), 500


def verificar_fin_fase_grupos(id_torneo):
    try:
        torneo = db_session.get(Torneo, id_torneo)
        if not torneo:
            return False

#comprobamos que todas las partidas de grupos están finalizadas
        partidas_grupos = db_session.query(Partida).filter(
            Partida.id_torneo == id_torneo,
            Partida.tipo_partida.like("Fase de grupos%")
        ).all()

        if not partidas_grupos:
            return False

        if not all(p.estado == "Finalizado" for p in partidas_grupos):
            return False

#Evitamos regenerar si ya existen eliminatorias
        if db_session.query(Partida).filter(
            Partida.id_torneo == id_torneo,
            ~Partida.tipo_partida.like("Fase de grupos%")
        ).first():
            return False

#calculamos los clasificados por grupo
        clasificados = obtener_clasificados_por_grupo(id_torneo)

#creamos bracket inicial
        bracket_inicial = crear_bracket_inicial(clasificados)

#generarmos las eliminatorias
        crear_eliminatorias_desde_bracket(id_torneo, bracket_inicial)

#actualizamos el torneo
        torneo.fase_actual = "Eliminatorias"
        db_session.commit()

        return True

    except Exception as e:
        db_session.rollback()
        print("Error:", str(e))
        return False

def obtener_clasificados_por_grupo(id_torneo):

#Cogemos los grupos de la base de datos
    grupos = db_session.query(Grupo).filter_by(id_torneo=id_torneo).all()

#Creamos una lista para guardar a los clasificados
    clasificados = {}

#Recorremos todos los grupos y cogemos los participantes de estos
    for grupo in grupos:
        participantes = db_session.query(Participante_torneo).filter_by(
            id_grupo=grupo.id_grupo
        ).all()

#Cogemos a los participantes en el orden que se pide, puntos, rondas y rondas ganadas
        participantes.sort(
            key=lambda p: (
                p.puntos_totales or 0,
                p.diferencia_rondas or 0,
                p.rondas_ganadas or 0
            ),
            reverse=True
        )

#Si hay dos o mas participantes se guardan para la fase eliminatoria
        if len(participantes) >= 2:
            clasificados[grupo.nombre] = {
                "1": participantes[0],
                "2": participantes[1]
            }

    return clasificados

def crear_bracket_inicial(clasificados):
#Obtienemos los grupos ordenados y se crean dos listas para guardarlos
    nombres = sorted(clasificados.keys())
    participantes1 = []
    participantes2 = []

#Recorre los grupos de dos en dos
    for i in range(0, len(nombres), 2):
#Evita errores si queda un grupo sin pareja
        if i + 1 >= len(nombres):
            break

#Guardamos los dos grupos que se enfrentarán
        g1 = nombres[i]
        g2 = nombres[i + 1]

#Ponemos el orden de emparejamiento 1 vs 2 y vicebersa por grupos
        participantes1.append((clasificados[g1]["1"], clasificados[g2]["2"]))
        participantes2.append((clasificados[g2]["1"], clasificados[g1]["2"]))

#Devolvemos los emparejamientos
    return participantes1 + participantes2

def crear_eliminatorias_desde_bracket(id_torneo, bracket_inicial):

    rondas_actuales = []

#PRIMERA RONDA
# Obtenemos el nombre de la ronda según el número de partidas iniciales
    nombre_primera_ronda = obtener_nombre_rondas(len(bracket_inicial))

    for p1, p2 in bracket_inicial:

#Creamos la partida y la añadimos a la base de datos
        partida = Partida(
            id_torneo=id_torneo,
            tipo_partida=nombre_primera_ronda,
            estado="Pendiente"
        )

#Guardamos cambios
        db_session.add(partida)
        db_session.flush()

#Añadimos los dos participantes de la partida
        db_session.add_all([
            Participante_partida(
                id_partida=partida.id_partida,
                id_participante_torneo=p1.id_participante,
                posicion=1
            ),
            Participante_partida(
                id_partida=partida.id_partida,
                id_participante_torneo=p2.id_participante,
                posicion=2
            )
        ])

        rondas_actuales.append(partida)

#RESTO DEL ÁRBOL
#Seguimos generando rondas hasta que solo quede una partida (la final)
    while len(rondas_actuales) > 1:

        nueva_ronda = []
        nombre_ronda = obtener_nombre_rondas(len(rondas_actuales) // 2)

        for i in range(0, len(rondas_actuales), 2):

#Creamos la partida de la siguiente ronda (el ganador irá aquí)
            partida = Partida(
                id_torneo=id_torneo,
                tipo_partida=nombre_ronda,
                estado="Pendiente"
            )

            db_session.add(partida)
            db_session.flush()

#Enlazamos las partidas de la ronda actual con su partida padre
            rondas_actuales[i].siguiente_partida_id = partida.id_partida
            if i + 1 < len(rondas_actuales):
                rondas_actuales[i + 1].siguiente_partida_id = partida.id_partida

            nueva_ronda.append(partida)

        rondas_actuales = nueva_ronda

@app.route("/torneo/<int:id_torneo>/eliminatorias")
def obtener_eliminatorias(id_torneo):

#Obtenemos todas las partidas del torneo
    partidas = db_session.query(Partida).filter(Partida.id_torneo == id_torneo).all()

#Lista de resultados
    resultado = []

    for p in partidas:

#Obtenemos los participantes de cada partida
        participantes = db_session.query(Participante_partida).filter_by(id_partida=p.id_partida).all()

#Extraemos los nombres de usuario de los participantes
        jugadores = [
            pp.participante_obj.usuario_obj.nombre_usuario
            for pp in participantes
        ]

        resultado.append({
            "id_partida": p.id_partida,
            "siguiente_partida_id": p.siguiente_partida_id,
            "estado": p.estado,
            "resultado_final": p.resultado_final,
            "jugadores": jugadores
        })

    return jsonify(resultado)

def avanzar_ganador_eliminatoria(partida):

#Si no hay ganador o no hay siguiente partida no hacemos nada
    if not partida.ganador_id:
        return

    if not partida.siguiente_partida:
        return

    siguiente = db_session.get(Partida, partida.siguiente_partida_id)

    if not siguiente:
        return

#Si la siguiente partida ya tiene dos participantes no añadimos más
    participantes_actuales = db_session.query(Participante_partida).filter_by(
        id_partida=siguiente.id_partida,
    ).count()

    if participantes_actuales >= 2:
        return

#Posición según orden de creación: la partida con menor id va arriba (posicion=1)
    partidas_origen = db_session.query(Partida).filter_by(
        siguiente_partida_id=siguiente.id_partida
    ).order_by(Partida.id_partida.asc()).all()

    posicion = 1
    if len(partidas_origen) >= 2 and partidas_origen[1].id_partida == partida.id_partida:
        posicion = 2

#Añadimos el ganador como participante en la siguiente partida
    nuevo = Participante_partida(
        id_partida=siguiente.id_partida,
        id_participante_torneo=partida.ganador_id,
        posicion=posicion
    )

    db_session.add(nuevo)

def es_eliminatoria(partida):
#Devuelve True si la partida es de fase eliminatoria
    return (
        partida.tipo_partida is not None and
        not partida.tipo_partida.startswith("Fase de grupos")
    )

def recalcular_rol_organizador(id_usuario):
#Si el usuario no tiene rol de organizador no hay nada que recalcular
    usuario = db_session.get(Usuario, id_usuario)
    if not usuario or not usuario.rol_obj or usuario.rol_obj.id_rol != 3:
        return

#Si ya no organiza ningún torneo activo le devolvemos el rol de usuario normal
    otros_torneos_activos = db_session.query(Torneo).filter(
        Torneo.id_usuario == id_usuario,
        Torneo.estado != "Finalizado"
    ).count()

    if otros_torneos_activos == 0:
        rol_usuario_normal = db_session.query(Rol).filter_by(nombre_rol="Usuario").first()
        if rol_usuario_normal:
            usuario.rol_obj = rol_usuario_normal


def verificar_fin_torneo(partida):

#Solo actuamos si es la final y ya hay un ganador
    if partida.tipo_partida != "Final" or not partida.ganador_id:
        return

    participantes_partida = db_session.query(Participante_partida).filter(
        Participante_partida.id_partida == partida.id_partida
    ).order_by(Participante_partida.id_participante_partida.asc()).all()

    if len(participantes_partida) < 2:
        return

#Asignamos el ranking final: 1 al ganador, 2 al perdedor
    for participante_partida in participantes_partida:
        participante = participante_partida.participante_obj
        posicion = 1 if participante.id_participante == partida.ganador_id else 2
        participante.ranking_final = posicion

#Marcamos el torneo como finalizado y actualizamos el ranking global
    torneo = db_session.get(Torneo, partida.id_torneo)
    if torneo:
        torneo.estado = "Finalizado"
        db_session.flush()
        actualizar_ranking_global(partida.id_torneo)
        recalcular_rol_organizador(torneo.id_usuario)

# RANKING GLOBAL
def actualizar_ranking_global(id_torneo):

    torneo = db_session.get(Torneo, id_torneo)
    if not torneo:
        return

#Si es torneo de equipo delegamos en su propia función
    if torneo.juego_obj.es_equipo:
        actualizar_ranking_equipo(id_torneo)
        return

#Actualizamos las estadísticas globales de cada participante con los datos de grupos
    participantes = db_session.query(Participante_torneo).filter_by(
        id_torneo=id_torneo
    ).all()

    for participante in participantes:

#Buscamos el registro global del jugador para este juego o lo creamos si no existe
        registro = db_session.query(Ranking_global).filter_by(
            id_usuario=participante.id_usuario,
            id_juego=torneo.id_juego
        ).first()

        if not registro:
            registro = Ranking_global(
                id_usuario=participante.id_usuario,
                id_juego=torneo.id_juego
            )
            db_session.add(registro)

        registro.torneos_jugados += 1

        if participante.ranking_final == 1:
            registro.torneos_ganados += 1

#Acumulamos las estadísticas de la fase de grupos
        registro.partidas_ganadas += participante.victorias or 0
        registro.partidas_perdidas += participante.derrotas or 0
        registro.partidas_empatadas += participante.empate or 0
        registro.rondas_ganadas += participante.rondas_ganadas or 0
        registro.rondas_perdidas += participante.rondas_perdidas or 0
        registro.diferencia_rondas = registro.rondas_ganadas - registro.rondas_perdidas
        registro.puntos_ranking += participante.puntos_totales or 0

#Calculamos el winrate como porcentaje de torneos ganados sobre jugados
        registro.winrate = round(registro.torneos_ganados / registro.torneos_jugados, 2)\
            if registro.torneos_jugados > 0 else 0.0

    db_session.flush()

#Sumamos también las estadísticas de la fase eliminatoria
    partidas_eliminatorias = db_session.query(Partida).filter(
        Partida.id_torneo == id_torneo,
        Partida.estado == "Finalizado",
        ~Partida.tipo_partida.like("Fase de grupos%")
    ).all()

    for partida_eliminatoria in partidas_eliminatorias:

        if not partida_eliminatoria.resultado_final:
            continue

#Parseamos el resultado en formato "X-Y"
        partes = partida_eliminatoria.resultado_final.split("-")

        if len(partes) != 2 or not partes[0].isdigit() or not partes[1].isdigit():
            continue

        puntos_p1 = int(partes[0])
        puntos_p2 = int(partes[1])

        participantes_partida = db_session.query(Participante_partida).filter_by(
            id_partida=partida_eliminatoria.id_partida
        ).order_by(Participante_partida.id_participante_partida.asc()).all()

        if len(participantes_partida) < 2:
            continue

        pp1 = participantes_partida[0]
        pp2 = participantes_partida[1]

        participante1 = pp1.participante_obj
        participante2 = pp2.participante_obj

        if not participante1 or not participante2:
            continue

#Buscamos los registros globales de ambos jugadores
        registro1 = db_session.query(Ranking_global).filter_by(
            id_usuario=participante1.id_usuario,
            id_juego=torneo.id_juego
        ).first()

        registro2 = db_session.query(Ranking_global).filter_by(
            id_usuario=participante2.id_usuario,
            id_juego=torneo.id_juego
        ).first()

#Actualizamos rondas y partidas ganadas/perdidas en eliminatorias
        if registro1:
            registro1.rondas_ganadas += puntos_p1
            registro1.rondas_perdidas += puntos_p2
            registro1.diferencia_rondas = registro1.rondas_ganadas - registro1.rondas_perdidas
            if partida_eliminatoria.ganador_id == participante1.id_participante:
                registro1.partidas_ganadas += 1
            else:
                registro1.partidas_perdidas += 1

        if registro2:
            registro2.rondas_ganadas += puntos_p2
            registro2.rondas_perdidas += puntos_p1
            registro2.diferencia_rondas = registro2.rondas_ganadas - registro2.rondas_perdidas
            if partida_eliminatoria.ganador_id == participante2.id_participante:
                registro2.partidas_ganadas += 1
            else:
                registro2.partidas_perdidas += 1

    db_session.flush()

#Recalculamos las posiciones globales ordenando por torneos ganados, winrate y demás criterios
    todos_los_registros = db_session.query(Ranking_global).filter_by(
        id_juego=torneo.id_juego
    ).all()

    todos_los_registros.sort(key=lambda entrada: (
        -(entrada.torneos_ganados or 0),
        -(entrada.winrate or 0.0),
        -(entrada.torneos_jugados or 0),
        -(entrada.partidas_ganadas or 0),
        -(entrada.diferencia_rondas or 0)
    ))

    for posicion, entrada in enumerate(todos_los_registros, start=1):
        entrada.posicion_global = posicion


def actualizar_ranking_equipo(id_torneo):
    torneo = db_session.get(Torneo, id_torneo)
    if not torneo:
        return

#Actualizamos las estadísticas globales de cada equipo participante con los datos de grupos
    participantes = db_session.query(Participante_torneo).filter_by(id_torneo=id_torneo).all()

    for participante in participantes:
        if not participante.id_equipo:
            continue

#Buscamos el registro del equipo para este juego o lo creamos si no existe
        registro = db_session.query(Ranking_equipo).filter_by(
            id_equipo=participante.id_equipo,
            id_juego=torneo.id_juego
        ).first()

        if not registro:
            registro = Ranking_equipo(id_equipo=participante.id_equipo, id_juego=torneo.id_juego)
            db_session.add(registro)

        registro.torneos_jugados += 1
        if participante.ranking_final == 1:
            registro.torneos_ganados += 1
#Acumulamos estadísticas de la fase de grupos
        registro.partidas_ganadas += participante.victorias or 0
        registro.partidas_perdidas += participante.derrotas or 0
        registro.partidas_empatadas += participante.empate or 0
        registro.rondas_ganadas += participante.rondas_ganadas or 0
        registro.rondas_perdidas += participante.rondas_perdidas or 0
        registro.diferencia_rondas = registro.rondas_ganadas - registro.rondas_perdidas
        registro.puntos_ranking += participante.puntos_totales or 0
        registro.winrate = round(registro.torneos_ganados / registro.torneos_jugados, 2) \
            if registro.torneos_jugados > 0 else 0.0

    db_session.flush()

#Sumamos también las estadísticas de la fase eliminatoria
    partidas_eliminatorias = db_session.query(Partida).filter(
        Partida.id_torneo == id_torneo,
        Partida.estado == "Finalizado",
        ~Partida.tipo_partida.like("Fase de grupos%")
    ).all()

    for pe in partidas_eliminatorias:
        if not pe.resultado_final:
            continue

#Parseamos el resultado en formato "X-Y"
        partes = pe.resultado_final.split("-")
        if len(partes) != 2 or not partes[0].isdigit() or not partes[1].isdigit():
            continue

        pts1, pts2 = int(partes[0]), int(partes[1])
        pps = db_session.query(Participante_partida).filter_by(
            id_partida=pe.id_partida
        ).order_by(Participante_partida.id_participante_partida.asc()).all()

        if len(pps) < 2:
            continue

        p1 = pps[0].participante_obj
        p2 = pps[1].participante_obj
        if not p1 or not p2 or not p1.id_equipo or not p2.id_equipo:
            continue

#Buscamos los registros de ambos equipos
        r1 = db_session.query(Ranking_equipo).filter_by(id_equipo=p1.id_equipo, id_juego=torneo.id_juego).first()
        r2 = db_session.query(Ranking_equipo).filter_by(id_equipo=p2.id_equipo, id_juego=torneo.id_juego).first()

#Actualizamos rondas y partidas de eliminatorias para cada equipo
        if r1:
            r1.rondas_ganadas += pts1
            r1.rondas_perdidas += pts2
            r1.diferencia_rondas = r1.rondas_ganadas - r1.rondas_perdidas
            if pe.ganador_id == p1.id_participante:
                r1.partidas_ganadas += 1
            else:
                r1.partidas_perdidas += 1
        if r2:
            r2.rondas_ganadas += pts2
            r2.rondas_perdidas += pts1
            r2.diferencia_rondas = r2.rondas_ganadas - r2.rondas_perdidas
            if pe.ganador_id == p2.id_participante:
                r2.partidas_ganadas += 1
            else:
                r2.partidas_perdidas += 1

    db_session.flush()

#Recalculamos las posiciones globales de equipos para este juego
    todos = db_session.query(Ranking_equipo).filter_by(id_juego=torneo.id_juego).all()
    todos.sort(key=lambda e: (
        -(e.torneos_ganados or 0),
        -(e.winrate or 0.0),
        -(e.torneos_jugados or 0),
        -(e.partidas_ganadas or 0),
        -(e.diferencia_rondas or 0)
    ))
    for pos, e in enumerate(todos, start=1):
        e.posicion_global = pos


@app.route("/juego/<int:id_juego>/ranking")
def ranking_juego(id_juego):

    try:
        juego = db_session.get(Juego, id_juego)
        if not juego:
            return jsonify([])

        resultado = []

#Rama para torneos de equipo
        if juego.es_equipo:
            registros = db_session.query(Ranking_equipo).filter_by(
                id_juego=id_juego
            ).order_by(Ranking_equipo.posicion_global.asc()).all()

            for reg in registros:
                nombre = reg.equipo_obj.nombre if reg.equipo_obj else "Equipo eliminado"
#Calculamos las partidas jugadas sumando victorias, derrotas y empates
                pj = (reg.partidas_ganadas or 0) + (reg.partidas_perdidas or 0) + (reg.partidas_empatadas or 0)
                resultado.append({
                    "pos":     reg.posicion_global,
                    "usuario": nombre,
                    "es_equipo": True,
                    "tp":      reg.torneos_jugados or 0,
                    "tg":      reg.torneos_ganados or 0,
                    "wt":      reg.winrate or 0.0,
                    "pj":      pj,
                    "pg":      reg.partidas_ganadas or 0,
                    "pp":      reg.partidas_perdidas or 0,
                    "pe":      reg.partidas_empatadas or 0,
                    "rg":      reg.rondas_ganadas or 0,
                    "rp":      reg.rondas_perdidas or 0,
                    "dr":      reg.diferencia_rondas or 0,
                    "pts":     reg.puntos_ranking or 0
                })
        else:
#Rama para torneos individuales
            registros = db_session.query(Ranking_global).filter_by(
                id_juego=id_juego
            ).order_by(Ranking_global.posicion_global.asc()).all()
#Calculamos las partidas jugadas sumando victorias, derrotas y empates
            for registro in registros:
                nombre_usuario = registro.usuario_obj.nombre_usuario if registro.usuario_obj else "Usuario eliminado"
                pj = (registro.partidas_ganadas or 0) + (registro.partidas_perdidas or 0) + (registro.partidas_empatadas or 0)
                resultado.append({
                    "pos":      registro.posicion_global,
                    "usuario":  nombre_usuario,
                    "es_equipo": False,
                    "tp":       registro.torneos_jugados or 0,
                    "tg":       registro.torneos_ganados or 0,
                    "wt":       registro.winrate or 0.0,
                    "pj":       pj,
                    "pg":       registro.partidas_ganadas or 0,
                    "pp":       registro.partidas_perdidas or 0,
                    "pe":       registro.partidas_empatadas or 0,
                    "rg":       registro.rondas_ganadas or 0,
                    "rp":       registro.rondas_perdidas or 0,
                    "dr":       registro.diferencia_rondas or 0,
                    "pts":      registro.puntos_ranking or 0
                })

        return jsonify(resultado)

    except Exception as error:
        return jsonify({"error": str(error)}), 500

@app.route("/juego/<int:id_juego>/jugadores_activos")
def jugadores_activos(id_juego):

    try:
        juego = db_session.get(Juego, id_juego)

#Si es torneo de equipo devolvemos los equipos que han participado en este juego
        if juego and juego.es_equipo:
            equipos = db_session.query(Equipo).join(
                Participante_torneo, Participante_torneo.id_equipo == Equipo.id_equipo
            ).join(
                Torneo, Torneo.id_torneo == Participante_torneo.id_torneo
            ).filter(
                Torneo.id_juego == id_juego
            ).distinct().all()

            return jsonify([
                {"id_usuario": None, "usuario": eq.nombre}
                for eq in equipos
            ])

#Si es individual devolvemos los usuarios que han participado en torneos de este juego
        jugadores = db_session.query(
            Usuario.id_usuario,
            Usuario.nombre_usuario
        ).join(
            Participante_torneo,
            Participante_torneo.id_usuario == Usuario.id_usuario
        ).join(
            Torneo,
            Torneo.id_torneo == Participante_torneo.id_torneo
        ).filter(
            Torneo.id_juego == id_juego
        ).distinct().all()

        return jsonify([
            {"id_usuario": j.id_usuario, "usuario": j.nombre_usuario}
            for j in jugadores
        ])

    except Exception as e:
        return jsonify({"error": "Error jugadores activos", "detalle": str(e)}), 500


#BORRADO
def _ejecutar_borrado_usuario(usuario):

#Obtenemos todas las participaciones del usuario en torneos
    participaciones = db_session.query(Participante_torneo).filter_by(
        id_usuario=usuario.id_usuario
    ).all()

    torneos_afectados = set()

#Resolver partidas pendientes dando 3-0 al rival
    for participacion in participaciones:

#Buscamos todas las partidas en las que participa este usuario
        registros_en_partidas = db_session.query(Participante_partida).filter_by(
            id_participante_torneo=participacion.id_participante
        ).all()

        for registro_usuario in registros_en_partidas:

            partida = db_session.get(Partida, registro_usuario.id_partida)

#Saltamos partidas ya finalizadas
            if not partida or partida.estado == "Finalizado":
                continue

            participantes_partida = db_session.query(Participante_partida).filter_by(
                id_partida=partida.id_partida
            ).order_by(Participante_partida.id_participante_partida.asc()).all()

            if len(participantes_partida) < 2:
                continue

            primer_participante = participantes_partida[0]
            segundo_participante = participantes_partida[1]

#Determinamos si el usuario a borrar es el primero o el segundo
            usuario_es_primero = (
                primer_participante.id_participante_torneo == participacion.id_participante
            )

#Asignamos victoria 3-0 al rival según la posición del usuario
            if usuario_es_primero:
                resultado_final = "0-3"
                participante_rival = segundo_participante.participante_obj
                ganador_id = segundo_participante.id_participante_torneo
            else:
                resultado_final = "3-0"
                participante_rival = primer_participante.participante_obj
                ganador_id = primer_participante.id_participante_torneo

            partida.resultado_final = resultado_final
            partida.estado = "Finalizado"
            partida.ganador_id = ganador_id

#En fase de grupos actualizamos las estadísticas del rival
            if not es_eliminatoria(partida):
                participante_rival.victorias += 1
                participante_rival.puntos_totales += 3
                participante_rival.rondas_ganadas += 3
                participante_rival.diferencia_rondas = (
                    participante_rival.rondas_ganadas - participante_rival.rondas_perdidas
                )

#En eliminatorias hacemos avanzar al rival y comprobamos si el torneo ha terminado
            if es_eliminatoria(partida):
                avanzar_ganador_eliminatoria(partida)
                verificar_fin_torneo(partida)

            torneos_afectados.add(partida.id_torneo)

    db_session.flush()

#Poner a NULL id_participante_torneo para conservar el historial de partidas mostrando "Eliminado"
    for participacion in participaciones:
        db_session.query(Participante_partida).filter_by(
            id_participante_torneo=participacion.id_participante
        ).update({"id_participante_torneo": None}, synchronize_session='fetch')

#Poner a NULL ganador_id en partidas donde este participante era el ganador
        db_session.query(Partida).filter_by(
            ganador_id=participacion.id_participante
        ).update({"ganador_id": None}, synchronize_session='fetch')

    db_session.flush()

#Eliminar Participante_torneo (ya no hay FK que lo bloquee)
    db_session.query(Participante_torneo).filter_by(
        id_usuario=usuario.id_usuario
    ).delete(synchronize_session='fetch')

    db_session.flush()

#Comprobar si algún torneo termina la fase de grupos tras el abandono
    for id_torneo in torneos_afectados:
        verificar_fin_fase_grupos(id_torneo)

#Gestionar torneos que creó el usuario
    admin = db_session.get(Usuario, 1)
    torneos_creados = db_session.query(Torneo).filter_by(
        id_usuario=usuario.id_usuario
    ).all()

    for torneo_creado in torneos_creados:
        torneo_sin_iniciar = torneo_creado.estado not in ("Cerrado", "Finalizado")

        if torneo_sin_iniciar:
#Si el torneo aún no ha empezado lo borramos completamente
            partidas_del_torneo = db_session.query(Partida).filter_by(
                id_torneo=torneo_creado.id_torneo
            ).all()
            for partida_del_torneo in partidas_del_torneo:
                db_session.query(Participante_partida).filter_by(
                    id_partida=partida_del_torneo.id_partida
                ).delete()
            db_session.query(Partida).filter_by(
                id_torneo=torneo_creado.id_torneo
            ).delete()
            db_session.query(Participante_torneo).filter_by(
                id_torneo=torneo_creado.id_torneo
            ).delete()
            db_session.delete(torneo_creado)
        else:
#Si el torneo ya está en curso lo pasamos al admin y limpiamos el organizador
            db_session.query(Participante_torneo).filter_by(
                id_torneo=torneo_creado.id_torneo
            ).update({"aceptar_organizador": None}, synchronize_session=False)
            if admin:
                torneo_creado.id_usuario = admin.id_usuario

    db_session.flush()

#Gestionar equipos donde el usuario es capitán o miembro
    membresias = db_session.query(Miembro_equipo).filter_by(
        id_usuario=usuario.id_usuario
    ).all()

    for membresia in membresias:
        equipo = membresia.equipo_obj

        if membresia.rol == "capitan":
#Buscar el siguiente miembro más antiguo (excluye al usuario actual)
            siguiente = db_session.query(Miembro_equipo).filter(
                Miembro_equipo.id_equipo == equipo.id_equipo,
                Miembro_equipo.id_usuario != usuario.id_usuario
            ).order_by(Miembro_equipo.fecha_union.asc()).first()

            if siguiente:
                siguiente.rol = "capitan"
                equipo.id_capitan = siguiente.id_usuario
            else:
#Sin no hay mas miembros borramos el equipo
                db_session.delete(equipo)
                db_session.flush()
                continue

        db_session.delete(membresia)

    db_session.flush()

#Eliminamos su ranking global
    db_session.query(Ranking_global).filter_by(
        id_usuario=usuario.id_usuario
    ).delete()

#Eliminamos al usuario
    db_session.delete(usuario)
    db_session.commit()

#VALIDACIÓN COMPARTIDA DE DATOS DE USUARIO
def validar_campos_usuario(datos, id_usuario_excluir=None):
    # Expresiones regulares para validar nombre y email
    solo_letras = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$")
    email_regex = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

#Extraemos los campos del diccionario de datos
    nombre = datos.get("nombre")
    apellidos = datos.get("apellidos")
    email = datos.get("email")
    fecha_str = datos.get("fecha_nacimiento")
    nombre_usuario = datos.get("nombre_usuario")
    password = datos.get("password")

#Solo validamos el campo si viene en los datos permitiendo actualizaciones parciales
    if nombre is not None:
        if len(nombre) < 2 or not solo_letras.match(nombre):
            return "Nombre inválido (solo letras, mínimo 2 caracteres)"

    if apellidos is not None:
        if len(apellidos) < 2 or not solo_letras.match(apellidos):
            return "Apellidos inválidos (solo letras, mínimo 2 caracteres)"

    if email is not None:
        if not email_regex.match(email):
            return "Email inválido"
#Comprobamos que el email no esté en uso por otro usuario
        email_en_uso = db_session.query(Usuario).filter(
            Usuario.email == email,
            Usuario.id_usuario != id_usuario_excluir
        ).first()
        if email_en_uso:
            return "El email ya está en uso por otro usuario"

    if fecha_str is not None:
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except ValueError:
            return "Formato de fecha inválido, usa YYYY-MM-DD"
        if fecha > datetime.now().date():
            return "La fecha de nacimiento no puede ser futura"

    if nombre_usuario is not None:
        if len(nombre_usuario) < 3:
            return "El nombre de usuario debe tener al menos 3 caracteres"
#Comprobamos que el nombre de usuario no esté en uso por otro usuario
        nombre_en_uso = db_session.query(Usuario).filter(
            Usuario.nombre_usuario == nombre_usuario,
            Usuario.id_usuario != id_usuario_excluir
        ).first()
        if nombre_en_uso:
            return f"El nombre de usuario '{nombre_usuario}' ya está en uso"

    if password is not None:
        error_password = validar_password(password)
        if error_password:
            return error_password

#Si todos los campos son válidos devolvemos None
    return None

# EDITAR USUARIO (admin)
@app.route("/admin/editar_usuario/<int:id_usuario>", methods=["PATCH"])
def admin_editar_usuario(id_usuario):
#Verificamos que hay sesión activa y que el usuario es administrador
    if "nombre_usuario" not in session:
        return jsonify({"error": "No autorizado"}), 401

    administrador = db_session.query(Usuario).filter_by(
        nombre_usuario=session["nombre_usuario"]
    ).first()

    if not administrador or administrador.rol_obj.id_rol != 1:
        return jsonify({"error": "No autorizado"}), 403

    usuario_a_editar = db_session.get(Usuario, id_usuario)
    if not usuario_a_editar:
        return jsonify({"error": "Usuario no encontrado"}), 404

#Filtramos solo los campos que el admin puede modificar
    datos_recibidos = request.json
    campos_editables = {"nombre", "apellidos", "email", "rol", "nombre_usuario"}
    datos_a_aplicar = {campo: valor for campo, valor in datos_recibidos.items() if campo in campos_editables}

#Validamos los campos excepto el rol
    datos_para_validar = {campo: valor for campo, valor in datos_a_aplicar.items() if campo != "rol"}
    error_validacion = validar_campos_usuario(datos_para_validar, id_usuario_excluir=id_usuario)
    if error_validacion:
        return jsonify({"error": error_validacion}), 400

#Aplicamos los cambios campo a campo
    for nombre_campo, valor_campo in datos_a_aplicar.items():
        if nombre_campo == "rol":
#El rol se busca por nombre y se asigna como objeto
            rol_nuevo = db_session.query(Rol).filter_by(nombre_rol=valor_campo).first()
            if not rol_nuevo:
                return jsonify({"error": f"Rol '{valor_campo}' no existe"}), 400
            usuario_a_editar.rol_obj = rol_nuevo
        elif nombre_campo == "fecha_nacimiento":
            usuario_a_editar.fecha_nacimiento = datetime.strptime(valor_campo, "%Y-%m-%d").date()
        else:
            setattr(usuario_a_editar, nombre_campo, valor_campo)

    try:
        db_session.commit()
        return jsonify({"mensaje": "Usuario actualizado correctamente"})
    except Exception as excepcion:
        db_session.rollback()
        return jsonify({"error": str(excepcion)}), 500

# EDITAR MI PERFIL
@app.route("/editar_mi_perfil", methods=["PATCH"])
def editar_mi_perfil():
#Verificamos que hay sesión activa
    if "nombre_usuario" not in session:
        return jsonify({"error": "No autorizado"}), 401

    usuario = db_session.query(Usuario).filter_by(
        nombre_usuario=session["nombre_usuario"]
    ).first()

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

#Filtramos solo los campos que el propio usuario puede modificar
    datos_recibidos = request.json
    campos_editables = {"nombre", "apellidos", "email", "nombre_usuario", "password"}
    datos_a_aplicar = {campo: valor for campo, valor in datos_recibidos.items() if campo in campos_editables}

    error_validacion = validar_campos_usuario(datos_a_aplicar, id_usuario_excluir=usuario.id_usuario)
    if error_validacion:
        return jsonify({"error": error_validacion}), 400

#Aplicamos los cambios campo a campo
    for nombre_campo, valor_campo in datos_a_aplicar.items():
        if nombre_campo == "fecha_nacimiento":
            usuario.fecha_nacimiento = datetime.strptime(valor_campo, "%Y-%m-%d").date()
        else:
            setattr(usuario, nombre_campo, valor_campo)

#Si cambió el nombre de usuario actualizamos también la sesión
    if "nombre_usuario" in datos_a_aplicar:
        session["nombre_usuario"] = datos_a_aplicar["nombre_usuario"]

    try:
        db_session.commit()
        return jsonify({"mensaje": "Perfil actualizado correctamente"})
    except Exception as excepcion:
        db_session.rollback()
        return jsonify({"error": str(excepcion)}), 500

# BORRAR USUARIO (admin)
@app.route("/admin/borrar_usuario/<int:id_usuario>", methods=["DELETE"])
def admin_borrar_usuario(id_usuario):

#Verificamos que hay sesión activa y que el usuario es administrador
    if "nombre_usuario" not in session:
        return jsonify({"error": "No autorizado"}), 401

    administrador = db_session.query(Usuario).filter_by(
        nombre_usuario=session["nombre_usuario"]
    ).first()

    if not administrador or administrador.rol_obj.id_rol != 1:
        return jsonify({"error": "No autorizado"}), 403

    usuario_a_borrar = db_session.get(Usuario, id_usuario)

    if not usuario_a_borrar:
        return jsonify({"error": "Usuario no encontrado"}), 404

#El admin no puede borrarse a sí mismo desde este panel
    if usuario_a_borrar.id_usuario == administrador.id_usuario:
        return jsonify({"error": "No puedes borrarte a ti mismo desde aquí"}), 400

    try:
        _ejecutar_borrado_usuario(usuario_a_borrar)
        return jsonify({"mensaje": "Usuario borrado correctamente"})
    except Exception as excepcion:
        db_session.rollback()
        return jsonify({"error": str(excepcion)}), 500

#ZONA ADMIN JUEGOS
def _verificar_admin():
#Devuelve el usuario si está en sesión y es admin, o None si no lo es
    if "nombre_usuario" not in session:
        return None
    usuario = db_session.query(Usuario).filter_by(
        nombre_usuario=session["nombre_usuario"]
    ).first()
    if not usuario or usuario.rol_obj.id_rol != 1:
        return None
    return usuario

def _es_organizador_o_admin(torneo, usuario):
#Devuelve True si el usuario es admin o es el organizador del torneo
    if not usuario:
        return False
    if usuario.rol_obj and usuario.rol_obj.nombre_rol == "Administrador":
        return True
    return torneo.id_usuario == usuario.id_usuario

@app.route("/admin/juegos")
def admin_zona_juegos():

#Redirigimos si no es admin
    if not _verificar_admin():
        return redirect("/")
    return render_template("zona_juego_admin.html")

@app.route("/admin/juegos/crear")
def admin_crear_juego():
    if not _verificar_admin():
        return redirect("/")

    generos = db_session.query(Genero).order_by(Genero.id_genero).all()
    return render_template("creacion_juego_admin.html", generos=generos)

@app.route("/admin/torneos")
def admin_zona_torneos():
    if not _verificar_admin():
        return redirect("/")
    return render_template("zona_torneo_admin.html")

@app.route("/admin/torneos/ver")
def admin_ver_torneos():
    admin = _verificar_admin()
    if not admin:
        return redirect("/")

    juegos = db_session.query(Juego).order_by(Juego.nombre_juego).all()
    return render_template("torneo_admin.html", juegos=juegos, admin=admin)

@app.route("/admin/torneos/gestionar")
def admin_gestionar_torneos():
    if not _verificar_admin():
        return redirect("/")

    juegos = db_session.query(Juego).order_by(Juego.nombre_juego).all()
    return render_template("administracion_torneo.html", juegos=juegos)

@app.route("/admin/torneo/<int:id_torneo>/info", methods=["PATCH"])
def admin_editar_torneo_info(id_torneo):
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

    torneo = db_session.get(Torneo, id_torneo)

    if not torneo:
        return jsonify({"error": "Torneo no encontrado"}), 404
    data = request.get_json()
    cambios = {}

#Validamos y aplicamos cada campo editable del torneo
    if "nombre" in data:
        nombre = data["nombre"].strip()
        if len(nombre) < 3:
            return jsonify({"error": "El nombre debe tener al menos 3 caracteres"}), 400
        torneo.nombre = nombre
        cambios["nombre"] = nombre

    if "descripcion" in data:
        torneo.descripcion = data["descripcion"].strip()
        cambios["descripcion"] = torneo.descripcion

    if "estado" in data:
        torneo.estado = data["estado"]
        cambios["estado"] = torneo.estado

    if "max_participantes" in data:
        try:
            valor = int(data["max_participantes"])

            if valor not in [8, 16, 32, 64, 128]:
                return jsonify({"error": "El número de participantes debe ser 8, 16, 32, 64 o 128"}), 400

            torneo.max_participantes = valor
            cambios["max_participantes"] = valor

        except ValueError:
            return jsonify({"error": "Valor inválido para participantes"}), 400

    if "fecha_inicio" in data:
        try:
            nueva_inicio = date_type.fromisoformat(data["fecha_inicio"])

            if nueva_inicio < date_type.today():
                return jsonify({"error": "La fecha de inicio debe ser igual o posterior a hoy"}), 400

            torneo.fecha_inicio = nueva_inicio
            cambios["fecha_inicio"] = data["fecha_inicio"]
        except ValueError:
            return jsonify({"error": "Fecha inválida"}), 400

    if "fecha_final" in data:
        try:
            nueva_final = date_type.fromisoformat(data["fecha_final"])
            fecha_inicio_ref = torneo.fecha_inicio

            if nueva_final < fecha_inicio_ref:
                return jsonify({"error": "La fecha final debe ser igual o posterior a la fecha de inicio"}), 400

            torneo.fecha_final = nueva_final
            cambios["fecha_final"] = data["fecha_final"]

        except ValueError:
            return jsonify({"error": "Fecha inválida"}), 400

    db_session.commit()

    return jsonify({"ok": True, "cambios": cambios})

@app.route("/admin/torneo/<int:id_torneo>", methods=["DELETE"])
def admin_borrar_torneo(id_torneo):
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

    torneo = db_session.get(Torneo, id_torneo)

    if not torneo:
        return jsonify({"error": "Torneo no encontrado"}), 404

#Guardamos los ids afectados para recalcular roles después del borrado
    ids_usuarios = [pt.id_usuario for pt in torneo.participantes]
    id_creador = torneo.id_usuario
    _cascade_borrar_torneo(torneo)

    db_session.commit()

    for id_u in set(ids_usuarios + [id_creador]):
        recalcular_rol_organizador(id_u)

    db_session.commit()

    return jsonify({"ok": True})

@app.route("/admin/torneos/finalizados", methods=["DELETE"])
def admin_borrar_torneos_finalizados():
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403
    try:
#Borramos todos los torneos finalizados y recalculamos roles de los afectados
        torneos = db_session.query(Torneo).filter_by(estado="Finalizado").all()
        ids_usuarios = set()

        for torneo in torneos:
            ids_usuarios.update([pt.id_usuario for pt in torneo.participantes])
            ids_usuarios.add(torneo.id_usuario)
            _cascade_borrar_torneo(torneo)

        db_session.commit()

        for id_u in ids_usuarios:
            recalcular_rol_organizador(id_u)

        db_session.commit()
        return jsonify({"ok": True, "borrados": len(torneos)})

    except Exception as e:
        db_session.rollback()
        print("Error al borrar torneos finalizados:", str(e))
        return jsonify({"error": f"Error al borrar: {str(e)}"}), 500

@app.route("/admin/torneo/<int:id_torneo>/participante/<int:id_usuario>/rol", methods=["PATCH"])
def admin_cambiar_rol_participante(id_torneo, id_usuario):
#Verificamos si es administrador
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

    data = request.get_json()
    nuevo_rol_nombre = data.get("rol")
    torneo = db_session.get(Torneo, id_torneo)

    if not torneo:
        return jsonify({"error": "Torneo no encontrado"}), 404

    usuario = db_session.get(Usuario, id_usuario)

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    if usuario.rol_obj and usuario.rol_obj.nombre_rol == "Administrador":
        return jsonify({"error": "No se puede cambiar el rol de un administrador"}), 400

    id_anterior_organizador = torneo.id_usuario

    if nuevo_rol_nombre == "Organizador":
#Asignamos el nuevo organizador y actualizamos su rol
        torneo.id_usuario = id_usuario
        rol_org = db_session.query(Rol).filter_by(nombre_rol="Organizador").first()

        if rol_org:
            usuario.rol_obj = rol_org

        db_session.commit()

#Recalculamos el rol del organizador anterior si ha cambiado
        if id_anterior_organizador != id_usuario:
            recalcular_rol_organizador(id_anterior_organizador)
        db_session.commit()
    else:
#No se puede quitar al organizador sin asignar uno nuevo
        if torneo.id_usuario == id_usuario:
            return jsonify({"error": "No puedes quitar el organizador sin asignar uno nuevo"}), 400

        recalcular_rol_organizador(id_usuario)

        db_session.commit()

    return jsonify({"ok": True})

def _cascade_borrar_torneo(torneo):
#Rompemos los enlaces entre partidas antes de borrarlas para evitar errores de FK
    for partida in list(torneo.partidas):
        partida.siguiente_partida_id = None

    db_session.flush()

    for partida in list(torneo.partidas):
        for pp in list(partida.participantes):
            db_session.delete(pp)

    db_session.flush()

    for partida in list(torneo.partidas):
        partida.ganador_id = None

    db_session.flush()

    for partida in list(torneo.partidas):
        db_session.delete(partida)

    db_session.flush()

    for pt in list(torneo.participantes):
        db_session.delete(pt)

    db_session.flush()

    for grupo in list(torneo.grupos):
        db_session.delete(grupo)

    db_session.flush()
    db_session.delete(torneo)
    db_session.flush()

@app.route("/admin/juegos/gestionar")
def admin_gestionar_juegos():
    if not _verificar_admin():
        return redirect("/")

    juegos = db_session.query(Juego).order_by(Juego.id_juego).all()
    return render_template("administrador_juego.html", juegos=juegos)

@app.route("/admin/juegos/crear", methods=["POST"])
def admin_crear_juego_post():


    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

#Recogemos los datos del formulario
    nombre_juego = request.form.get("nombre_juego", "").strip()
    id_genero = request.form.get("id_genero", "").strip()
    nuevo_genero = request.form.get("nuevo_genero", "").strip()
    tipo_elemento = request.form.get("tipo_elemento", "").strip()
    archivo_portada = request.files.get("portada")

    if not nombre_juego:
        return jsonify({"error": "El nombre del juego es obligatorio"}), 400
    if not tipo_elemento:
        return jsonify({"error": "El tipo de elemento es obligatorio"}), 400

#Gestionamos el género: usamos uno existente o creamos uno nuevo
    if nuevo_genero:
        genero_existente = db_session.query(Genero).filter(
            Genero.nombre_genero.ilike(nuevo_genero)
        ).first()

        if genero_existente:
            genero_obj = genero_existente
        else:
            genero_obj = Genero(nombre_genero=nuevo_genero)
            db_session.add(genero_obj)
            db_session.flush()

    elif id_genero:
        genero_obj = db_session.get(Genero, int(id_genero))

        if not genero_obj:
            return jsonify({"error": "Género no encontrado"}), 400
    else:
        return jsonify({"error": "Debes seleccionar o crear un género"}), 400

#Guardamos la portada si se ha subido, o usamos la imagen por defecto
    nombre_portada = "Logo.png"
    if archivo_portada and archivo_portada.filename:
        nombre_seguro = secure_filename(archivo_portada.filename)
        ruta_portadas = os.path.join(app.root_path, "static", "imagenes", "portadas")
        os.makedirs(ruta_portadas, exist_ok=True)
        archivo_portada.save(os.path.join(ruta_portadas, nombre_seguro))
        nombre_portada = nombre_seguro

    es_equipo = request.form.get("es_equipo", "false") == "true"

#Creamos el juego en la base de datos
    nuevo_juego = Juego(
        nombre_juego=nombre_juego,
        id_genero=genero_obj.id_genero,
        portada=nombre_portada,
        tipo_elemento=tipo_elemento,
        es_equipo=es_equipo
    )

    db_session.add(nuevo_juego)
    db_session.flush()

    tipos_con_personajes = {"Personajes", "Personajes y Armas"}
    tipos_con_armas = {"Armas", "Personajes y Armas"}

    mapa_idx_personaje = {}
    mapa_idx_arma = {}

#Añadimos personajes si el tipo de elemento los incluye
    if tipo_elemento in tipos_con_personajes:
        personajes_json = request.form.get("personajes", "[]")
        personajes = json_mod.loads(personajes_json)
        for idx, nombre_p in enumerate(personajes):
            nombre_p = nombre_p.strip()
            if nombre_p:
                nuevo_personaje = Personaje(nombre_personaje=nombre_p, id_juego=nuevo_juego.id_juego)
                db_session.add(nuevo_personaje)
                db_session.flush()
                mapa_idx_personaje[idx] = nuevo_personaje.id_personaje

#Añadimos equipos/clubs si el tipo es "Equipos"
    if tipo_elemento == "Equipos":
        equipos_json = request.form.get("equipos", "[]")
        equipos = json_mod.loads(equipos_json)

        for nombre_e in equipos:
            nombre_e = nombre_e.strip()

            if nombre_e:
                db_session.add(Club(nombre_club=nombre_e, id_juego=nuevo_juego.id_juego))

#Añadimos armas si el tipo de elemento las incluye
    if tipo_elemento in tipos_con_armas:
        armas_json = request.form.get("armas", "[]")
        armas = json_mod.loads(armas_json)

        for idx, arma in enumerate(armas):
            nombre_a = arma.get("nombre", "").strip()
            tipo_a = arma.get("tipo_arma", "").strip()

            if nombre_a and tipo_a:
                nueva_arma = Armas(nombre_arma=nombre_a, tipo_arma=tipo_a, id_juego=nuevo_juego.id_juego)
                db_session.add(nueva_arma)
                db_session.flush()
                mapa_idx_arma[idx] = nueva_arma.id_armas

#Añadimos las relaciones personaje-arma con su habilidad
    if tipo_elemento == "Personajes y Armas":
        habilidades_json = request.form.get("habilidades", "[]")
        habilidades = json_mod.loads(habilidades_json)

        for hab in habilidades:
            personaje_idx = hab.get("personaje_idx")
            arma_idx = hab.get("arma_idx")
            habilidad = hab.get("habilidad", "").strip()
            id_personaje = mapa_idx_personaje.get(personaje_idx)
            id_arma = mapa_idx_arma.get(arma_idx)

            if id_personaje and id_arma and habilidad:
                db_session.add(Personaje_arma(
                    id_juego=nuevo_juego.id_juego,
                    id_personaje=id_personaje,
                    id_armas=id_arma,
                    habilidad=habilidad
                ))

    db_session.commit()
    return jsonify({"ok": True, "id_juego": nuevo_juego.id_juego})

# CRUD ELEMENTOS DE JUEGO (admin)
@app.route("/admin/juegos/<int:id_juego>/nombre", methods=["PATCH"])
def admin_editar_nombre_juego(id_juego):

#Verificamos si es administrador y hacemos las validaciones
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

    nuevo_nombre = request.json.get("nombre", "").strip()

    if len(nuevo_nombre) < 3:
        return jsonify({"error": "El nombre debe tener al menos 3 caracteres"}), 400

    juego = db_session.get(Juego, id_juego)

    if not juego:
        return jsonify({"error": "Juego no encontrado"}), 404

    juego.nombre_juego = nuevo_nombre
    db_session.commit()

    return jsonify({"ok": True})

@app.route("/admin/juegos/<int:id_juego>", methods=["DELETE"])
def admin_borrar_juego(id_juego):
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

    juego = db_session.get(Juego, id_juego)

    if not juego:
        return jsonify({"error": "Juego no encontrado"}), 404

    id_genero = juego.id_genero

#Borramos en cascada todos los torneos del juego
    for torneo in list(juego.torneos):
        for partida in list(torneo.partidas):
            partida.siguiente_partida_id = None

        db_session.flush()

        for partida in list(torneo.partidas):
            for pp in list(partida.participantes):
                db_session.delete(pp)
        db_session.flush()

        for partida in list(torneo.partidas):
            partida.ganador_id = None
        db_session.flush()

        for partida in list(torneo.partidas):
            db_session.delete(partida)
        db_session.flush()

        for pt in list(torneo.participantes):
            db_session.delete(pt)
        db_session.flush()

        for grupo in list(torneo.grupos):
            db_session.delete(grupo)

        db_session.flush()
        db_session.delete(torneo)
    db_session.flush()

#Borramos estadísticas, ranking y elementos del juego
    for eg in list(juego.estadisticas_global):
        db_session.delete(eg)

    for ej in list(juego.estadisticas_juego):
        db_session.delete(ej)

    for rg in list(juego.ranking):
        db_session.delete(rg)

    for pa in list(juego.juego_personaje_arma):
        db_session.delete(pa)

    db_session.flush()

    for p in list(juego.personajes):
        db_session.delete(p)

    for c in list(juego.clubes):
        db_session.delete(c)

    for a in list(juego.armas):
        db_session.delete(a)

    db_session.flush()
    db_session.delete(juego)
    db_session.commit()

#Si el género se queda sin juegos lo borramos también
    genero_borrado = False
    otros_juegos = db_session.query(Juego).filter_by(id_genero=id_genero).count()

    if otros_juegos == 0:
        genero = db_session.get(Genero, id_genero)

        if genero:
            db_session.delete(genero)
            db_session.commit()
            genero_borrado = True

    return jsonify({"ok": True, "genero_borrado": genero_borrado})

@app.route("/admin/juegos/<int:id_juego>/genero", methods=["PATCH"])
def admin_editar_genero_juego(id_juego):
#Verificamos si es administrador
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

    juego = db_session.get(Juego, id_juego)

    if not juego:
        return jsonify({"error": "Juego no encontrado"}), 404

    id_genero_antiguo = juego.id_genero
    id_genero = request.json.get("id_genero")
    nuevo_genero_nombre = request.json.get("nuevo_genero", "").strip()

#Si se pasa un nombre nuevo buscamos el género o lo creamos
    if nuevo_genero_nombre:
        genero_obj = db_session.query(Genero).filter(
            Genero.nombre_genero.ilike(nuevo_genero_nombre)
        ).first()

        if not genero_obj:
            genero_obj = Genero(nombre_genero=nuevo_genero_nombre)

            db_session.add(genero_obj)
            db_session.flush()

        juego.id_genero = genero_obj.id_genero
        nombre_resultado = genero_obj.nombre_genero

    elif id_genero:
#Si se pasa un id usamos el género existente
        juego.id_genero = id_genero
        genero_obj = db_session.get(Genero, id_genero)
        nombre_resultado = genero_obj.nombre_genero if genero_obj else ""

    else:
        return jsonify({"error": "Indica un género"}), 400

    db_session.commit()
    genero_borrado = False

#Si el género anterior se queda sin juegos lo borramos
    if id_genero_antiguo != juego.id_genero:
        otros = db_session.query(Juego).filter_by(id_genero=id_genero_antiguo).count()

        if otros == 0:
            genero_viejo = db_session.get(Genero, id_genero_antiguo)

            if genero_viejo:
                db_session.delete(genero_viejo)
                db_session.commit()
                genero_borrado = True

    return jsonify({"ok": True, "nombre_genero": nombre_resultado, "genero_borrado": genero_borrado})

@app.route("/admin/juegos/<int:id_juego>/tipo_elemento", methods=["PATCH"])
def admin_editar_tipo_elemento_juego(id_juego):
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

    juego = db_session.get(Juego, id_juego)

    if not juego:
        return jsonify({"error": "Juego no encontrado"}), 404

#Validamos que el tipo recibido sea una de las opciones permitidas
    tipo = request.json.get("tipo_elemento", "").strip()
    opciones_validas = ["Personajes", "Equipos", "Armas", "Personajes y Armas"]

    if tipo not in opciones_validas:
        return jsonify({"error": "Tipo de elemento no válido"}), 400

    juego.tipo_elemento = tipo
    db_session.commit()

    return jsonify({"ok": True})

@app.route("/admin/juegos/<int:id_juego>/portada", methods=["PATCH"])
def admin_editar_portada_juego(id_juego):

    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

    juego = db_session.get(Juego, id_juego)

    if not juego:
        return jsonify({"error": "Juego no encontrado"}), 404

    if "portada" not in request.files:
        return jsonify({"error": "No se recibió imagen"}), 400

    archivo = request.files["portada"]

    if not archivo.filename:
        return jsonify({"error": "Archivo vacío"}), 400

#Guardamos la imagen en la carpeta de portadas
    nombre_archivo = secure_filename(archivo.filename)
    ruta_portadas = os.path.join(app.root_path, "static", "imagenes", "portadas")
    os.makedirs(ruta_portadas, exist_ok=True)
    archivo.save(os.path.join(ruta_portadas, nombre_archivo))
    juego.portada = nombre_archivo

    db_session.commit()

    return jsonify({"ok": True, "portada": nombre_archivo})

@app.route("/admin/juegos/<int:id_juego>/info", methods=["PATCH"])
def admin_editar_info_juego(id_juego):
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

    juego = db_session.get(Juego, id_juego)

    if not juego:
        return jsonify({"error": "Juego no encontrado"}), 404

#Recogemos los datos enviados y guardamos el género actual por si hay que borrarlo después
    datos = request.json
    id_genero_antiguo = juego.id_genero
    respuesta = {"ok": True}

#Actualizamos el nombre si viene en los datos
    if "nombre" in datos:
        nombre = datos["nombre"].strip()

        if len(nombre) < 3:
            return jsonify({"error": "El nombre debe tener al menos 3 caracteres"}), 400

        juego.nombre_juego = nombre
        respuesta["nombre"] = nombre

#Si viene un nuevo nombre de género lo buscamos o lo creamos
    if "nuevo_genero" in datos:
        nuevo_nombre = datos["nuevo_genero"].strip()

        if len(nuevo_nombre) < 2:
            return jsonify({"error": "El nombre del género debe tener al menos 2 caracteres"}), 400

        genero_obj = db_session.query(Genero).filter(
            Genero.nombre_genero.ilike(nuevo_nombre)
        ).first()

        if not genero_obj:
            genero_obj = Genero(nombre_genero=nuevo_nombre)
            db_session.add(genero_obj)
            db_session.flush()

        juego.id_genero = genero_obj.id_genero
        respuesta["id_genero"] = genero_obj.id_genero
        respuesta["nombre_genero"] = genero_obj.nombre_genero

    elif "id_genero" in datos:
#Si viene un id de género existente lo asignamos directamente
        juego.id_genero = datos["id_genero"]
        genero_obj = db_session.get(Genero, datos["id_genero"])
        respuesta["id_genero"] = datos["id_genero"]
        respuesta["nombre_genero"] = genero_obj.nombre_genero if genero_obj else ""

#Actualizamos el tipo de elemento si viene en los datos
    if "tipo_elemento" in datos:
        tipo = datos["tipo_elemento"]

        if tipo not in ["Personajes", "Equipos", "Armas", "Personajes y Armas"]:
            return jsonify({"error": "Tipo de elemento no válido"}), 400

        juego.tipo_elemento = tipo
        respuesta["tipo_elemento"] = tipo

    db_session.commit()

#Si cambió el género comprobamos si el antiguo se ha quedado huérfano y lo borramos
    genero_borrado = False
    if "id_genero" in respuesta or "nuevo_genero" in datos:
        if id_genero_antiguo != juego.id_genero:
            otros = db_session.query(Juego).filter_by(id_genero=id_genero_antiguo).count()

            if otros == 0:
                genero_viejo = db_session.get(Genero, id_genero_antiguo)

                if genero_viejo:
                    db_session.delete(genero_viejo)
                    db_session.commit()
                    genero_borrado = True

    respuesta["genero_borrado"] = genero_borrado

    return jsonify(respuesta)

@app.route("/admin/juegos/<int:id_juego>/personaje", methods=["POST"])
def admin_anadir_personaje(id_juego):
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

#Extraemos y limpiamos el nombre del body JSON
    nombre = request.json.get("nombre", "").strip()

#Validamos que el nombre tenga una longitud mínima
    if len(nombre) < 3:
        return jsonify({"error": "El nombre debe tener al menos 3 caracteres"}), 400

#Creamos el personaje vinculado al juego y guardamos
    nuevo = Personaje(nombre_personaje=nombre, id_juego=id_juego)
    db_session.add(nuevo)
    db_session.commit()

#Devolvemos el id y nombre del nuevo registro
    return jsonify({"ok": True, "id": nuevo.id_personaje, "nombre": nuevo.nombre_personaje})

@app.route("/admin/personaje/<int:id_personaje>", methods=["PATCH"])
def admin_editar_personaje(id_personaje):
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

#Extraemos y validamos el nuevo nombre
    nombre = request.json.get("nombre", "").strip()

    if len(nombre) < 3:
        return jsonify({"error": "El nombre debe tener al menos 3 caracteres"}), 400

#Buscamos el personaje; si no existe devolvemos 404
    personaje = db_session.get(Personaje, id_personaje)
    if not personaje:
        return jsonify({"error": "Personaje no encontrado"}), 404

#Aplicamos el cambio y guardamos
    personaje.nombre_personaje = nombre
    db_session.commit()

    return jsonify({"ok": True})

@app.route("/admin/personaje/<int:id_personaje>", methods=["DELETE"])
def admin_borrar_personaje(id_personaje):
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

#Buscamos el personaje; si no existe devolvemos 404
    personaje = db_session.get(Personaje, id_personaje)
    if not personaje:
        return jsonify({"error": "Personaje no encontrado"}), 404

#Eliminamos y confirmamos la transacción
    db_session.delete(personaje)
    db_session.commit()

    return jsonify({"ok": True})

@app.route("/admin/juegos/<int:id_juego>/club", methods=["POST"])
def admin_anadir_club(id_juego):
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

#Extraemos y limpiamos el nombre del body JSON
    nombre = request.json.get("nombre", "").strip()

#Validamos que el nombre tenga una longitud mínima
    if len(nombre) < 3:
        return jsonify({"error": "El nombre debe tener al menos 3 caracteres"}), 400

#Creamos el club vinculado al juego y guardamos
    nuevo = Club(nombre_club=nombre, id_juego=id_juego)
    db_session.add(nuevo)
    db_session.commit()

#Devolvemos el id y nombre del nuevo registro
    return jsonify({"ok": True, "id": nuevo.id_club, "nombre": nuevo.nombre_club})

@app.route("/admin/club/<int:id_club>", methods=["PATCH"])
def admin_editar_club(id_club):
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

#Extraemos y validamos el nuevo nombre
    nombre = request.json.get("nombre", "").strip()

    if len(nombre) < 3:
        return jsonify({"error": "El nombre debe tener al menos 3 caracteres"}), 400

#Buscamos el club; si no existe devolvemos 404
    club = db_session.get(Club, id_club)
    if not club:
        return jsonify({"error": "Equipo no encontrado"}), 404

#Aplicamos el cambio y guardamos
    club.nombre_club = nombre
    db_session.commit()

    return jsonify({"ok": True})

@app.route("/admin/club/<int:id_club>", methods=["DELETE"])
def admin_borrar_club(id_club):
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

#Buscamos el club; si no existe devolvemos el error
    club = db_session.get(Club, id_club)
    if not club:
        return jsonify({"error": "Equipo no encontrado"}), 404

#Eliminamos y confirmamos la transacción
    db_session.delete(club)
    db_session.commit()

    return jsonify({"ok": True})

@app.route("/admin/juegos/<int:id_juego>/arma", methods=["POST"])
def admin_anadir_arma(id_juego):
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

#Extraemos nombre y tipo de arma del body JSON
    nombre = request.json.get("nombre", "").strip()
    tipo_arma = request.json.get("tipo_arma", "").strip()

#Ambos campos son obligatorios y deben tener longitud mínima
    if len(nombre) < 3 or len(tipo_arma) < 3:
        return jsonify({"error": "Nombre y tipo deben tener al menos 3 caracteres"}), 400

#Creamos el arma vinculada al juego y guardamos
    nueva = Armas(nombre_arma=nombre, tipo_arma=tipo_arma, id_juego=id_juego)
    db_session.add(nueva)
    db_session.commit()

#Devolvemos el id, nombre y tipo del nuevo registro
    return jsonify({"ok": True, "id": nueva.id_armas, "nombre": nueva.nombre_arma, "tipo_arma": nueva.tipo_arma})

@app.route("/admin/arma/<int:id_arma>", methods=["PATCH"])
def admin_editar_arma(id_arma):
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

#Extraemos los campos opcionales del body JSON
    nombre = request.json.get("nombre", "").strip()
    tipo_arma = request.json.get("tipo_arma", "").strip()

#Buscamos el arma; si no existe devolvemos 404
    arma = db_session.get(Armas, id_arma)
    if not arma:
        return jsonify({"error": "Arma no encontrada"}), 404

#Actualizamos solo los campos que vienen en la petición
    if nombre:
        arma.nombre_arma = nombre
    if tipo_arma:
        arma.tipo_arma = tipo_arma

    db_session.commit()

    return jsonify({"ok": True})

@app.route("/admin/arma/<int:id_arma>", methods=["DELETE"])
def admin_borrar_arma(id_arma):
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

#Buscamos el arma; si no existe devolvemos 404
    arma = db_session.get(Armas, id_arma)
    if not arma:
        return jsonify({"error": "Arma no encontrada"}), 404

#Eliminamos y confirmamos la transacción
    db_session.delete(arma)
    db_session.commit()

    return jsonify({"ok": True})

@app.route("/admin/juegos/<int:id_juego>/habilidad", methods=["POST"])
def admin_anadir_habilidad(id_juego):
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

#Extraemos los tres campos que forman la clave compuesta más la habilidad
    id_personaje = request.json.get("id_personaje")
    id_arma = request.json.get("id_arma")
    habilidad = request.json.get("habilidad", "").strip()

#Todos los campos son obligatorios
    if not id_personaje or not id_arma or len(habilidad) < 3:
        return jsonify({"error": "Todos los campos son obligatorios y la habilidad debe tener al menos 3 caracteres"}), 400

#Comprobamos que no exista ya esa combinación personaje-arma para este juego
    existe = db_session.query(Personaje_arma).filter_by(
        id_juego=id_juego, id_personaje=id_personaje, id_armas=id_arma
    ).first()

    if existe:
        return jsonify({"error": "Ya existe esa combinación personaje-arma"}), 400

#Creamos el registro con la clave compuesta
    nueva = Personaje_arma(id_juego=id_juego, id_personaje=id_personaje, id_armas=id_arma, habilidad=habilidad)
    db_session.add(nueva)
    db_session.commit()

    return jsonify({"ok": True})

@app.route("/admin/habilidad/<int:id_juego>/<int:id_personaje>/<int:id_arma>", methods=["PATCH"])
def admin_editar_habilidad(id_juego, id_personaje, id_arma):
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

#Extraemos y validamos la nueva descripción de habilidad
    habilidad = request.json.get("habilidad", "").strip()

    if len(habilidad) < 3:
        return jsonify({"error": "La habilidad debe tener al menos 3 caracteres"}), 400

#Buscamos la relación personaje-arma por sus tres claves; si no existe devolvemos 404
    registro = db_session.query(Personaje_arma).filter_by(
        id_juego=id_juego, id_personaje=id_personaje, id_armas=id_arma
    ).first()

    if not registro:
        return jsonify({"error": "Habilidad no encontrada"}), 404

#Actualizamos la habilidad y guardamos
    registro.habilidad = habilidad
    db_session.commit()

    return jsonify({"ok": True})

@app.route("/admin/habilidad/<int:id_juego>/<int:id_personaje>/<int:id_arma>", methods=["DELETE"])
def admin_borrar_habilidad(id_juego, id_personaje, id_arma):
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

#Buscamos la relación personaje-arma por sus tres claves; si no existe devolvemos 404
    registro = db_session.query(Personaje_arma).filter_by(
        id_juego=id_juego, id_personaje=id_personaje, id_armas=id_arma
    ).first()

    if not registro:
        return jsonify({"error": "Habilidad no encontrada"}), 404

#Eliminamos el registro y confirmamos la transacción
    db_session.delete(registro)
    db_session.commit()

    return jsonify({"ok": True})

#BORRAR MI CUENTA (propio usuario)
@app.route("/borrar_mi_cuenta", methods=["DELETE"])
def borrar_mi_cuenta():

#Verificamos que el usuario tenga sesión activa
    if "nombre_usuario" not in session:
        return jsonify({"error": "No autorizado"}), 401

#Buscamos el usuario en la BD por su nombre de sesión
    usuario = db_session.query(Usuario).filter_by(
        nombre_usuario=session["nombre_usuario"]
    ).first()

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    try:
#Ejecutamos el borrado en cascada y cerramos la sesión
        _ejecutar_borrado_usuario(usuario)
        session.pop("nombre_usuario", None)
        return jsonify({"mensaje": "Cuenta eliminada correctamente"})

    except Exception as excepcion:
#Si algo falla revertimos todos los cambios
        db_session.rollback()
        return jsonify({"error": str(excepcion)}), 500

#ADMINISTRADOR - USUARIOS
@app.route("/admin/usuarios/zona")
def admin_usuarios_zona():
#Redirigimos si no hay sesión activa
    if "nombre_usuario" not in session:
        return redirect("/")

#Buscamos el usuario en la BD
    usuario_activo = db_session.query(Usuario).filter_by(
        nombre_usuario=session["nombre_usuario"]
    ).first()

#Solo el administrador puede acceder
    if not usuario_activo or usuario_activo.rol_obj.id_rol != 1:
        return redirect("/")

    return render_template("zona_usuarios_admin.html")

@app.route("/admin/equipos")
def admin_equipos():
#Redirigimos si no hay sesión activa
    if "nombre_usuario" not in session:
        return redirect("/")

#Buscamos el usuario en la BD
    usuario_activo = db_session.query(Usuario).filter_by(
        nombre_usuario=session["nombre_usuario"]
    ).first()

#Solo el administrador puede acceder a la gestión de equipos
    if not usuario_activo or usuario_activo.rol_obj.id_rol != 1:
        return redirect("/")

#Cargamos todos los equipos ordenados por nombre
    equipos = db_session.query(Equipo).order_by(Equipo.nombre).all()
    return render_template("administrador_equipos.html", equipos=equipos)

@app.route("/admin/equipo/<int:id_equipo>/info", methods=["PATCH"])
def admin_editar_equipo(id_equipo):
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

#Buscamos el equipo; si no existe devolvemos 404
    equipo = db_session.get(Equipo, id_equipo)
    if not equipo:
        return jsonify({"error": "Equipo no encontrado"}), 404

#Extraemos el campo a editar, el nuevo valor y los límites válidos para max_miembros
    data = request.get_json()
    campo = data.get("campo")
    valor = str(data.get("valor", "")).strip()
    valores_max = {"5", "10", "15", "20", "50", "100"}

    if campo == "nombre":
#El nombre no puede estar vacío
        if not valor:
            return jsonify({"error": "El nombre no puede estar vacío"}), 400

#Verificamos que no exista otro equipo con el mismo nombre
        existente = db_session.query(Equipo).filter(
            Equipo.nombre == valor, Equipo.id_equipo != id_equipo
        ).first()
        if existente:
            return jsonify({"error": "Ya existe un equipo con ese nombre"}), 400

        equipo.nombre = valor

    elif campo == "descripcion":
        equipo.descripcion = valor or None

    elif campo == "max_miembros":
#Validamos que el valor esté entre las opciones permitidas
        if valor not in valores_max:
            return jsonify({"error": "Valor de máximo de miembros no válido"}), 400

        nuevo_max = int(valor)
        miembros_actuales = len(equipo.miembros)

#No se puede reducir el máximo por debajo de los miembros actuales
        if nuevo_max < miembros_actuales:
            return jsonify({"error": f"No puedes reducir el máximo a {nuevo_max} si hay {miembros_actuales} miembros"}), 400

        equipo.max_miembros = nuevo_max

    else:
        return jsonify({"error": "Campo no reconocido"}), 400

    db_session.commit()
    return jsonify({"ok": True})

@app.route("/admin/equipo/<int:id_equipo>", methods=["DELETE"])
def admin_borrar_equipo(id_equipo):

#Verificamos el admin, si no lo esos no esta autorizado
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

#Llamamos a los equipos de la bd
    equipo = db_session.get(Equipo, id_equipo)
#Si no encontramos el equipo nos sale que no encontrado
    if not equipo:
        return jsonify({"error": "Equipo no encontrado"}), 404

#Borramos el equipo y guardamos los cambios
    db_session.delete(equipo)
    db_session.commit()
    return jsonify({"ok": True})

@app.route("/admin/equipo/<int:id_equipo>/miembro/<int:id_usuario>", methods=["DELETE"])
def admin_expulsar_miembro_equipo(id_equipo, id_usuario):

#Verificamos al administrador si no es no hay autorización
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

#Llamamos a los equipos de la bd
    equipo = db_session.get(Equipo, id_equipo)
#Si no es un equipo no salta el error de no encontrado
    if not equipo:
        return jsonify({"error": "Equipo no encontrado"}), 404

#Si el id del usuario corresponde al del capitan del equipo, no se le permite expulsar
    if equipo.id_capitan == id_usuario:
        return jsonify({"error": "No puedes expulsar al capitán del equipo"}), 400

#Llamamos a los miembros del equipo de la bd
    miembro = db_session.query(Miembro_equipo).filter_by(
        id_equipo=id_equipo, id_usuario=id_usuario
    ).first()

#Si no es un miebro nos salta el error
    if not miembro:
        return jsonify({"error": "Miembro no encontrado"}), 404

#Borramos al miembro y guardamos los cambios
    db_session.delete(miembro)
    db_session.commit()
    return jsonify({"ok": True})

@app.route("/admin/equipo/<int:id_equipo>/capitan/<int:id_usuario>", methods=["PATCH"])
def admin_cambiar_capitan_equipo(id_equipo, id_usuario):

#Verificacion de administrador
    if not _verificar_admin():
        return jsonify({"error": "No autorizado"}), 403

#Llamamos a los miembros del equipo
    miembro = db_session.query(Miembro_equipo).filter_by(
        id_equipo=id_equipo, id_usuario=id_usuario
    ).first()

#Si no es miembro del equipo nos salta el error
    if not miembro:
        return jsonify({"error": "El usuario no es miembro del equipo"}), 404

#Alterna los roles de usuario entre miembro y capitan y se guarda el cambio
    miembro.rol = "miembro" if miembro.rol == "capitan" else "capitan"
    db_session.commit()
    return jsonify({"ok": True, "rol": miembro.rol})

@app.route("/admin/usuarios")
def admin_usuarios():
# Si no hay sesión activa redirigimos al inicio
    if "nombre_usuario" not in session:
        return redirect("/")

# Obtenemos el usuario activo de la sesión
    usuario_activo = db_session.query(Usuario).filter_by(
        nombre_usuario=session["nombre_usuario"]
    ).first()

# Si no existe o no es administrador redirigimos al inicio
    if not usuario_activo or usuario_activo.rol_obj.id_rol != 1:
        return redirect("/")

#Obtenemos todos los usuarios de la base de datos
    todos_los_usuarios = db_session.query(Usuario).all()

    lista_usuarios = []
    for usuario in todos_los_usuarios:
#Contamos los torneos en los que ha participado
        torneos_participados = db_session.query(Participante_torneo).filter_by(
            id_usuario=usuario.id_usuario
        ).count()

#Contamos los torneos que ha creado
        torneos_creados = db_session.query(Torneo).filter_by(
            id_usuario=usuario.id_usuario
        ).count()

#Contamos los torneos que ha ganado (ranking_final == 1)
        torneos_ganados = db_session.query(Participante_torneo).filter_by(
            id_usuario=usuario.id_usuario,
            ranking_final=1
        ).count()

#Definimos el orden de los roles para ordenarlos en la vista
        roles_orden = {"Administrador": 1, "Organizador": 2, "Usuario": 3}
        nombre_rol = usuario.rol_obj.nombre_rol if usuario.rol_obj else "Usuario"

#Añadimos los datos del usuario junto con sus estadísticas a la lista
        lista_usuarios.append({
            "id_usuario": usuario.id_usuario,
            "nombre_usuario": usuario.nombre_usuario,
            "nombre": usuario.nombre,
            "apellidos": usuario.apellidos,
            "email": usuario.email,
            "fecha_nacimiento": usuario.fecha_nacimiento.strftime("%Y-%m-%d"),
            "password": usuario.password,
            "rol": nombre_rol,
            "rol_orden": roles_orden.get(nombre_rol, 3),
            "torneos_participados": torneos_participados,
            "torneos_creados": torneos_creados,
            "torneos_ganados": torneos_ganados,
        })

#Enviamos la lista de usuarios a la plantilla
    return render_template("administrador_usuario.html", usuarios=lista_usuarios)


# ===============================
# EQUIPOS
# ===============================

@app.route("/equipos")
def ver_equipos():
    equipos = db_session.query(Equipo).order_by(Equipo.fecha_creacion.desc()).all()

    usuario_actual_id = None
    if "nombre_usuario" in session:
        u = db_session.query(Usuario).filter_by(nombre_usuario=session["nombre_usuario"]).first()
        if u:
            usuario_actual_id = u.id_usuario

    equipos_data = []
    for equipo in equipos:
        miembros_count = len(equipo.miembros)
        ya_es_miembro = any(m.id_usuario == usuario_actual_id for m in equipo.miembros)
        es_capitan_equipo = any(
            m.id_usuario == usuario_actual_id and m.rol == "capitan"
            for m in equipo.miembros
        )
        miembros_lista = [
            {
                "id_usuario": m.id_usuario,
                "nombre": m.usuario_obj.nombre_usuario,
                "rol": m.rol,
                "es_yo": m.id_usuario == usuario_actual_id
            }
            for m in equipo.miembros if m.usuario_obj
        ]
        equipos_data.append({
            "id_equipo": equipo.id_equipo,
            "nombre": equipo.nombre,
            "descripcion": equipo.descripcion,
            "max_miembros": equipo.max_miembros,
            "miembros_count": miembros_count,
            "ya_es_miembro": ya_es_miembro,
            "lleno": miembros_count >= equipo.max_miembros,
            "es_capitan_equipo": es_capitan_equipo,
            "miembros": miembros_lista
        })

    return render_template("equipos.html", equipos=equipos_data, usuario_actual_id=usuario_actual_id)


@app.route("/equipos/crear", methods=["GET", "POST"])
def crear_equipo():
    if "nombre_usuario" not in session:
        return redirect("/")

    if request.method == "GET":
        return render_template("formequipos.html")

    nombre = request.form.get("nombre", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    max_miembros = request.form.get("max_miembros", "").strip()

    if not nombre or not max_miembros:
        return render_template("formequipos.html", error="El nombre y el máximo de miembros son obligatorios.")

    if not max_miembros.isdigit() or int(max_miembros) < 2:
        return render_template("formequipos.html", error="El máximo de miembros debe ser al menos 2.")

    existe = db_session.query(Equipo).filter_by(nombre=nombre).first()
    if existe:
        return render_template("formequipos.html", error="Ya existe un equipo con ese nombre.")

    usuario = db_session.query(Usuario).filter_by(nombre_usuario=session["nombre_usuario"]).first()

    try:
        nuevo_equipo = Equipo(
            nombre=nombre,
            max_miembros=int(max_miembros),
            id_capitan=usuario.id_usuario,
            descripcion=descripcion or None
        )
        db_session.add(nuevo_equipo)
        db_session.flush()

        miembro_capitan = Miembro_equipo(
            id_equipo=nuevo_equipo.id_equipo,
            id_usuario=usuario.id_usuario,
            rol="capitan"
        )
        db_session.add(miembro_capitan)
        db_session.commit()

        return redirect("/equipos")

    except Exception as e:
        db_session.rollback()
        return render_template("formequipos.html", error="Error al crear el equipo. Inténtalo de nuevo.")


@app.route("/equipos/<int:id_equipo>/unirse", methods=["POST"])
def unirse_equipo(id_equipo):
    if "nombre_usuario" not in session:
        return jsonify({"error": "Debes iniciar sesión"}), 401

    usuario = db_session.query(Usuario).filter_by(nombre_usuario=session["nombre_usuario"]).first()
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    equipo = db_session.get(Equipo, id_equipo)
    if not equipo:
        return jsonify({"error": "Equipo no encontrado"}), 404

    ya_miembro = db_session.query(Miembro_equipo).filter_by(
        id_equipo=id_equipo, id_usuario=usuario.id_usuario
    ).first()
    if ya_miembro:
        return jsonify({"error": "Ya eres miembro de este equipo"}), 400

    if len(equipo.miembros) >= equipo.max_miembros:
        return jsonify({"error": "El equipo está completo"}), 400

    try:
        nuevo_miembro = Miembro_equipo(
            id_equipo=id_equipo,
            id_usuario=usuario.id_usuario,
            rol="miembro"
        )
        db_session.add(nuevo_miembro)
        db_session.commit()
        return jsonify({"mensaje": "Te has unido al equipo correctamente"})

    except Exception as e:
        db_session.rollback()
        return jsonify({"error": "Error al unirse al equipo"}), 500


@app.route("/equipos/<int:id_equipo>/salir", methods=["POST"])
def salir_equipo(id_equipo):
    if "nombre_usuario" not in session:
        return jsonify({"error": "Debes iniciar sesión"}), 401

    usuario = db_session.query(Usuario).filter_by(nombre_usuario=session["nombre_usuario"]).first()
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    miembro = db_session.query(Miembro_equipo).filter_by(
        id_equipo=id_equipo, id_usuario=usuario.id_usuario
    ).first()
    if not miembro:
        return jsonify({"error": "No eres miembro de este equipo"}), 400

    equipo = db_session.get(Equipo, id_equipo)

    try:
        if miembro.rol == "capitan":
            otros = [m for m in equipo.miembros if m.id_usuario != usuario.id_usuario]
            if otros:
                # Transferir capitanía al miembro más antiguo
                nuevo_capitan = sorted(otros, key=lambda m: m.fecha_union)[0]
                nuevo_capitan.rol = "capitan"
                equipo.id_capitan = nuevo_capitan.id_usuario

        db_session.delete(miembro)

        if len(equipo.miembros) <= 1:
            db_session.delete(equipo)

        db_session.commit()
        return jsonify({"mensaje": "Has salido del equipo"})

    except Exception as e:
        db_session.rollback()
        return jsonify({"error": "Error al salir del equipo"}), 500


@app.route("/equipos/<int:id_equipo>/expulsar/<int:id_usuario>", methods=["DELETE"])
def expulsar_miembro_equipo(id_equipo, id_usuario):
    if "nombre_usuario" not in session:
        return jsonify({"error": "No autorizado"}), 401
    capitan = db_session.query(Usuario).filter_by(nombre_usuario=session["nombre_usuario"]).first()
    if not capitan:
        return jsonify({"error": "Usuario no encontrado"}), 404
    mi_membresia = db_session.query(Miembro_equipo).filter_by(
        id_equipo=id_equipo, id_usuario=capitan.id_usuario
    ).first()
    if not mi_membresia or mi_membresia.rol != "capitan":
        return jsonify({"error": "No tienes permisos para expulsar miembros"}), 403
    if capitan.id_usuario == id_usuario:
        return jsonify({"error": "No puedes expulsarte a ti mismo"}), 400
    miembro = db_session.query(Miembro_equipo).filter_by(
        id_equipo=id_equipo, id_usuario=id_usuario
    ).first()
    if not miembro:
        return jsonify({"error": "El usuario no es miembro del equipo"}), 404
    db_session.delete(miembro)
    db_session.commit()
    return jsonify({"ok": True})

@app.route("/equipos/<int:id_equipo>/capitan/<int:id_usuario>", methods=["PATCH"])
def toggle_capitan_equipo(id_equipo, id_usuario):
    if "nombre_usuario" not in session:
        return jsonify({"error": "No autorizado"}), 401
    capitan = db_session.query(Usuario).filter_by(nombre_usuario=session["nombre_usuario"]).first()
    if not capitan:
        return jsonify({"error": "Usuario no encontrado"}), 404
    mi_membresia = db_session.query(Miembro_equipo).filter_by(
        id_equipo=id_equipo, id_usuario=capitan.id_usuario
    ).first()
    if not mi_membresia or mi_membresia.rol != "capitan":
        return jsonify({"error": "No tienes permisos para cambiar roles"}), 403
    if capitan.id_usuario == id_usuario:
        return jsonify({"error": "No puedes cambiar tu propio rol"}), 400
    miembro = db_session.query(Miembro_equipo).filter_by(
        id_equipo=id_equipo, id_usuario=id_usuario
    ).first()
    if not miembro:
        return jsonify({"error": "El usuario no es miembro del equipo"}), 404
    miembro.rol = "miembro" if miembro.rol == "capitan" else "capitan"
    db_session.commit()
    return jsonify({"ok": True, "rol": miembro.rol})

# ===============================
# MAIN
# ===============================

def aplicar_migraciones():
    inspector = inspect(db.engine)

    columnas_participante = [c['name'] for c in inspector.get_columns('participante_torneo')]
    columnas_juego = [c['name'] for c in inspector.get_columns('juego')]
    columnas_torneo = [c['name'] for c in inspector.get_columns('torneo')]

    with db.engine.connect() as conexion:
        if 'aceptar_organizador' not in columnas_participante:
            conexion.execute(text(
                'ALTER TABLE participante_torneo ADD COLUMN aceptar_organizador BOOLEAN DEFAULT NULL'
            ))
        if 'id_equipo' not in columnas_participante:
            conexion.execute(text(
                'ALTER TABLE participante_torneo ADD COLUMN id_equipo INTEGER REFERENCES equipo(id_equipo)'
            ))
        if 'es_equipo' not in columnas_juego:
            conexion.execute(text('ALTER TABLE juego ADD COLUMN es_equipo BOOLEAN DEFAULT 0'))
            conexion.execute(text(
                "UPDATE juego SET es_equipo = 1 WHERE nombre_juego IN "
                "('Battlefield 6', 'Call of duty Black ops 7', 'Rainbow Six')"
            ))
        if 'max_miembros_equipo' not in columnas_torneo:
            conexion.execute(text('ALTER TABLE torneo ADD COLUMN max_miembros_equipo INTEGER DEFAULT NULL'))
        conexion.execute(text('ALTER TABLE partida ALTER COLUMN tipo_partida TYPE VARCHAR(50)'))
        conexion.execute(text('ALTER TABLE partida ALTER COLUMN estado TYPE VARCHAR(30)'))
        conexion.execute(text(
            'ALTER TABLE participante_partida ALTER COLUMN id_participante_torneo DROP NOT NULL'
        ))
        conexion.commit()

# Inicialización de la BD (se ejecuta siempre, con Gunicorn y con el servidor de desarrollo)
db.base.metadata.create_all(bind=db.engine)
aplicar_migraciones()
seed_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=os.environ.get("FLASK_DEBUG", "0") == "1")
