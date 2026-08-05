import string
from random import random

from db import db_session
from models import *
from datetime import  timedelta, date
import random


def seed_roles():
#Roles que queremos tener
    roles = ["Administrador", "Usuario", "Organizador"]

    for nombre in roles:
# Verificamos si ya existe el rol
        existe = db_session.query(Rol).filter(Rol.nombre_rol == nombre).first()

        if not existe:
# Si no existe, lo creamos
            nuevo_rol = Rol(nombre_rol=nombre)
            db_session.add(nuevo_rol)
            print(f"Rol creado: {nombre}")

    db_session.commit()
    print("Seed de roles completado.")

#Seed para los generos
def seed_generos():

#Guardamos en una lista los generos
    generos = ["Lucha", "Deportes", "Shooter"]

#Recorremos la lista de los generos
    for nombre in generos:

#Llamamos a los generos para ver si existe
        existe = db_session.query(Genero).filter(Genero.nombre_genero == nombre).first()

#Si el genero no existe se crea un nuevo genero
        if not existe:
            nuevo_genero = Genero(nombre_genero=nombre)
            db_session.add(nuevo_genero)
            print(f"Genero creado: {nombre}")

    db_session.commit()
    print("Seed de generos completado.")


#Seeds de juegos
def seed_juegos():

#Guardamos los datos de los juegos en un diccionario dentro de una lista
    juegos = [
        {"nombre_juego": "Tekken 8",                  "id_genero": 1, "portada": "tekken8.png",      "tipo_elemento": "Personajes",        "es_equipo": False},
        {"nombre_juego": "Street Fighter 6",           "id_genero": 1, "portada": "streetfighter.png","tipo_elemento": "Personajes",        "es_equipo": False},
        {"nombre_juego": "Mortal Kombat 11",           "id_genero": 1, "portada": "mortal.png",       "tipo_elemento": "Personajes",        "es_equipo": False},
        {"nombre_juego": "Fifa Fc26",                  "id_genero": 2, "portada": "fifa.png",         "tipo_elemento": "Equipos",           "es_equipo": False},
        {"nombre_juego": "Nba 2K26",                   "id_genero": 2, "portada": "2k26.png",         "tipo_elemento": "Equipos",           "es_equipo": False},
        {"nombre_juego": "Nfl Madden 26",              "id_genero": 2, "portada": "madden.png",       "tipo_elemento": "Equipos",           "es_equipo": False},
        {"nombre_juego": "Battlefield 6",              "id_genero": 3, "portada": "batt.png",         "tipo_elemento": "Armas",             "es_equipo": True},
        {"nombre_juego": "Call of duty Black ops 7",   "id_genero": 3, "portada": "call.png",         "tipo_elemento": "Armas",             "es_equipo": True},
        {"nombre_juego": "Rainbow Six",                "id_genero": 3, "portada": "six.png",          "tipo_elemento": "Personajes y Armas","es_equipo": True},
    ]

#Recorremos la lista de los juegos
    for juego in juegos:

#Llamamos a los generos para ver si estan en la bd del juego
        genero = db_session.query(Genero).filter(Genero.id_genero == juego["id_genero"]).first()

#Si no es un genero se da el aviso de que este no se encuentra en la bd
        if not genero:
            print(f"El genero del juego: {juego['nombre_juego']} no existe")
            continue

#Llamamos a los juegos para ver si este se encuentra en la bd
        existe = db_session.query(Juego).filter(Juego.nombre_juego == juego["nombre_juego"]).first()

#Si este no se encuentra en la base de datos se crea el juego
        if not existe:
            nuevo_juego = Juego(
                nombre_juego=juego["nombre_juego"],
                id_genero=juego["id_genero"],
                portada=juego["portada"],
                tipo_elemento=juego["tipo_elemento"],
                es_equipo=juego.get("es_equipo", False)
            )

            db_session.add(nuevo_juego)

            print(f"Juego creado {juego['nombre_juego']}")


    db_session.commit()
    print("Seed de juegos completado.")

#Seed de personajes
def seed_personajes():
#Guardamos en listas los personajes con sus respectivos juegoss
    personajes_tekken8 = [
        {"nombre_personaje": "Jin Kazama", "id_juego": 1},
        {"nombre_personaje": "Kazuya Mishima", "id_juego": 1},
        {"nombre_personaje": "Jun Kazama", "id_juego": 1},
        {"nombre_personaje": "Paul Phoenix", "id_juego": 1},
        {"nombre_personaje": "Law", "id_juego": 1},
        {"nombre_personaje": "King", "id_juego": 1},
        {"nombre_personaje": "Lars Alexandersson", "id_juego": 1},
        {"nombre_personaje": "Alisa Bosconovitch", "id_juego": 1},
        {"nombre_personaje": "Hwoarang", "id_juego": 1},
        {"nombre_personaje": "Ling Xiaoyu", "id_juego": 1},
        {"nombre_personaje": "Asuka Kazama", "id_juego": 1},
        {"nombre_personaje": "Lili", "id_juego": 1},
        {"nombre_personaje": "Bryan Fury", "id_juego": 1},
        {"nombre_personaje": "Claudio Serafino", "id_juego": 1},
        {"nombre_personaje": "Raven", "id_juego": 1},
        {"nombre_personaje": "Steve Fox", "id_juego": 1},
        {"nombre_personaje": "Leo", "id_juego": 1},
        {"nombre_personaje": "Yoshimitsu", "id_juego": 1},
        {"nombre_personaje": "Sergei Dragunov", "id_juego": 1},
        {"nombre_personaje": "Shaheen", "id_juego": 1},
        {"nombre_personaje": "Azucena", "id_juego": 1},
        {"nombre_personaje": "Victor Chevalier", "id_juego": 1},
        {"nombre_personaje": "Reina", "id_juego": 1},
        {"nombre_personaje": "Jack-8", "id_juego": 1},
        {"nombre_personaje": "Devil Jin", "id_juego": 1}
    ]

    personajes_sf6 = [
        {"nombre_personaje": "Ryu", "id_juego": 2},
        {"nombre_personaje": "Ken", "id_juego": 2},
        {"nombre_personaje": "Chun-Li", "id_juego": 2},
        {"nombre_personaje": "Guile", "id_juego": 2},
        {"nombre_personaje": "Blanka", "id_juego": 2},
        {"nombre_personaje": "Dhalsim", "id_juego": 2},
        {"nombre_personaje": "E. Honda", "id_juego": 2},
        {"nombre_personaje": "Zangief", "id_juego": 2},
        {"nombre_personaje": "Cammy", "id_juego": 2},
        {"nombre_personaje": "Dee Jay", "id_juego": 2},
        {"nombre_personaje": "Juri", "id_juego": 2},
        {"nombre_personaje": "Luke", "id_juego": 2},
        {"nombre_personaje": "Jamie", "id_juego": 2},
        {"nombre_personaje": "Kimberly", "id_juego": 2},
        {"nombre_personaje": "Manon", "id_juego": 2},
        {"nombre_personaje": "Marisa", "id_juego": 2},
        {"nombre_personaje": "Lily", "id_juego": 2},
        {"nombre_personaje": "JP", "id_juego": 2}
    ]

    personajes_mk = [
        {"nombre_personaje": "Scorpion", "id_juego": 3},
        {"nombre_personaje": "Sub-Zero", "id_juego": 3},
        {"nombre_personaje": "Raiden", "id_juego": 3},
        {"nombre_personaje": "Liu Kang", "id_juego": 3},
        {"nombre_personaje": "Kung Lao", "id_juego": 3},
        {"nombre_personaje": "Kitana", "id_juego": 3},
        {"nombre_personaje": "Mileena", "id_juego": 3},
        {"nombre_personaje": "Johnny Cage", "id_juego": 3},
        {"nombre_personaje": "Sonya Blade", "id_juego": 3},
        {"nombre_personaje": "Jax Briggs", "id_juego": 3},
        {"nombre_personaje": "Kenshi", "id_juego": 3},
        {"nombre_personaje": "Baraka", "id_juego": 3},
        {"nombre_personaje": "Reptile", "id_juego": 3},
        {"nombre_personaje": "Smoke", "id_juego": 3},
        {"nombre_personaje": "Rain", "id_juego": 3},
        {"nombre_personaje": "Shang Tsung", "id_juego": 3},
        {"nombre_personaje": "Quan Chi", "id_juego": 3},
        {"nombre_personaje": "Sindel", "id_juego": 3},
        {"nombre_personaje": "Shao Kahn", "id_juego": 3}
    ]

    personajes_rainbow = [
        {"nombre_personaje": "Sledge", "id_juego": 9},
        {"nombre_personaje": "Thatcher", "id_juego": 9},
        {"nombre_personaje": "Ash", "id_juego": 9},
        {"nombre_personaje": "Thermite", "id_juego": 9},
        {"nombre_personaje": "Twitch", "id_juego": 9},
        {"nombre_personaje": "Montagne", "id_juego": 9},
        {"nombre_personaje": "Glaz", "id_juego": 9},
        {"nombre_personaje": "Fuze", "id_juego": 9},
        {"nombre_personaje": "Blitz", "id_juego": 9},
        {"nombre_personaje": "IQ", "id_juego": 9},
        {"nombre_personaje": "Buck", "id_juego": 9},
        {"nombre_personaje": "Blackbeard", "id_juego": 9},
        {"nombre_personaje": "Capitao", "id_juego": 9},
        {"nombre_personaje": "Hibana", "id_juego": 9},
        {"nombre_personaje": "Jackal", "id_juego": 9},
        {"nombre_personaje": "Ying", "id_juego": 9},
        {"nombre_personaje": "Zofia", "id_juego": 9},
        {"nombre_personaje": "Dokkaebi", "id_juego": 9},
        {"nombre_personaje": "Lion", "id_juego": 9},
        {"nombre_personaje": "Finka", "id_juego": 9},
        {"nombre_personaje": "Maverick", "id_juego": 9},
        {"nombre_personaje": "Nomad", "id_juego": 9},
        {"nombre_personaje": "Gridlock", "id_juego": 9},
        {"nombre_personaje": "Nokk", "id_juego": 9},
        {"nombre_personaje": "Amaru", "id_juego": 9},
        {"nombre_personaje": "Kali", "id_juego": 9},
        {"nombre_personaje": "Iana", "id_juego": 9},
        {"nombre_personaje": "Ace", "id_juego": 9},
        {"nombre_personaje": "Zero", "id_juego": 9},
        {"nombre_personaje": "Flores", "id_juego": 9},
        {"nombre_personaje": "Osa", "id_juego": 9},
        {"nombre_personaje": "Sens", "id_juego": 9},
        {"nombre_personaje": "Grim", "id_juego": 9},
        {"nombre_personaje": "Brava", "id_juego": 9},

        {"nombre_personaje": "Smoke", "id_juego": 9},
        {"nombre_personaje": "Mute", "id_juego": 9},
        {"nombre_personaje": "Castle", "id_juego": 9},
        {"nombre_personaje": "Pulse", "id_juego": 9},
        {"nombre_personaje": "Doc", "id_juego": 9},
        {"nombre_personaje": "Rook", "id_juego": 9},
        {"nombre_personaje": "Kapkan", "id_juego": 9},
        {"nombre_personaje": "Tachanka", "id_juego": 9},
        {"nombre_personaje": "Jager", "id_juego": 9},
        {"nombre_personaje": "Bandit", "id_juego": 9},
        {"nombre_personaje": "Frost", "id_juego": 9},
        {"nombre_personaje": "Valkyrie", "id_juego": 9},
        {"nombre_personaje": "Caveira", "id_juego": 9},
        {"nombre_personaje": "Echo", "id_juego": 9},
        {"nombre_personaje": "Mira", "id_juego": 9},
        {"nombre_personaje": "Lesion", "id_juego": 9},
        {"nombre_personaje": "Ela", "id_juego": 9},
        {"nombre_personaje": "Vigil", "id_juego": 9},
        {"nombre_personaje": "Maestro", "id_juego": 9},
        {"nombre_personaje": "Alibi", "id_juego": 9},
        {"nombre_personaje": "Clash", "id_juego": 9},
        {"nombre_personaje": "Kaid", "id_juego": 9},
        {"nombre_personaje": "Mozzie", "id_juego": 9},
        {"nombre_personaje": "Warden", "id_juego": 9},
        {"nombre_personaje": "Goyo", "id_juego": 9},
        {"nombre_personaje": "Wamai", "id_juego": 9},
        {"nombre_personaje": "Oryx", "id_juego": 9},
        {"nombre_personaje": "Melusi", "id_juego": 9},
        {"nombre_personaje": "Aruni", "id_juego": 9},
        {"nombre_personaje": "Thunderbird", "id_juego": 9},
        {"nombre_personaje": "Thorn", "id_juego": 9},
        {"nombre_personaje": "Azami", "id_juego": 9},
        {"nombre_personaje": "Solis", "id_juego": 9},
        {"nombre_personaje": "Fenrir", "id_juego": 9}
    ]
#Guardamos todos los personajes juntos
    personajes = personajes_tekken8 + personajes_sf6 + personajes_mk + personajes_rainbow

#Recorremos todas la listas de personajes
    for personaje in personajes:

#Llamaos a los juegos para ver si pertenece a algun personaje
        juego = db_session.query(Juego).filter(Juego.id_juego == personaje["id_juego"]).first()

#Si no hay ningun juego asignado a personajes salta el aviso
        if not juego:
            print(f"El Juego del personaje: {personaje['nombre_personaje']} no existe")
            continue

#Llamamos a los personajes para ver si se encuentran en la bd
        existe = db_session.query(Personaje).filter(Personaje.nombre_personaje == personaje["nombre_personaje"]).first()

#Si no existe se crea un personaje nuevo
        if not existe:
            nuevo_personaje = Personaje(
                nombre_personaje = personaje["nombre_personaje"],
                id_juego = personaje["id_juego"],
            )

            db_session.add(nuevo_personaje)
            print(f"Personaje creado {personaje['nombre_personaje']}")


    db_session.commit()
    print("Seed de personajes completada")

#Seed de clubs
def seed_clubs():
#Se guarda en lista todos los clubes  con sus respectivos juegos
    equipos_fifa = [
        {"nombre_club": "Real Madrid", "id_juego": 4},
        {"nombre_club": "FC Barcelona", "id_juego": 4},
        {"nombre_club": "Atlético de Madrid", "id_juego": 4},
        {"nombre_club": "Sevilla FC", "id_juego": 4},
        {"nombre_club": "Manchester City", "id_juego": 4},
        {"nombre_club": "Manchester United", "id_juego": 4},
        {"nombre_club": "Liverpool", "id_juego": 4},
        {"nombre_club": "Chelsea", "id_juego": 4},
        {"nombre_club": "Arsenal", "id_juego": 4},
        {"nombre_club": "Tottenham Hotspur", "id_juego": 4},
        {"nombre_club": "Paris Saint-Germain", "id_juego": 4},
        {"nombre_club": "Olympique Lyon", "id_juego": 4},
        {"nombre_club": "AS Monaco", "id_juego": 4},
        {"nombre_club": "Bayern Munich", "id_juego": 4},
        {"nombre_club": "Borussia Dortmund", "id_juego": 4},
        {"nombre_club": "RB Leipzig", "id_juego": 4},
        {"nombre_club": "Bayer Leverkusen", "id_juego": 4},
        {"nombre_club": "Juventus", "id_juego": 4},
        {"nombre_club": "AC Milan", "id_juego": 4},
        {"nombre_club": "Inter Milan", "id_juego": 4},
        {"nombre_club": "Napoli", "id_juego": 4},
        {"nombre_club": "Fiorentina", "id_juego": 4},
        {"nombre_club": "Benfica", "id_juego": 4},
        {"nombre_club": "Porto", "id_juego": 4},
        {"nombre_club": "Sporting CP", "id_juego": 4},
        {"nombre_club": "Ajax", "id_juego": 4},
        {"nombre_club": "PSV Eindhoven", "id_juego": 4},
        {"nombre_club": "Club Brugge", "id_juego": 4},
        {"nombre_club": "Celtic FC", "id_juego": 4},
        {"nombre_club": "RB Salzburg", "id_juego": 4},
        {"nombre_club": "Shakhtar Donetsk", "id_juego": 4},
        {"nombre_club": "Dinamo Zagreb", "id_juego": 4},
        {"nombre_club": "Galatasaray", "id_juego": 4},
        {"nombre_club": "Fenerbahçe", "id_juego": 4},
        {"nombre_club": "Spartak Moscow", "id_juego": 4},
        {"nombre_club": "Lokomotiv Moscow", "id_juego": 4},
        {"nombre_club": "Young Boys", "id_juego": 4},
        {"nombre_club": "Copenhagen", "id_juego": 4},
        {"nombre_club": "Club América", "id_juego": 4},
        {"nombre_club": "Boca Juniors", "id_juego": 4},
        {"nombre_club": "River Plate", "id_juego": 4},
        {"nombre_club": "Corinthians", "id_juego": 4},
        {"nombre_club": "Flamengo", "id_juego": 4},
        {"nombre_club": "Santos FC", "id_juego": 4},
        {"nombre_club": "LA Galaxy", "id_juego": 4},
        {"nombre_club": "Seattle Sounders", "id_juego": 4},
        {"nombre_club": "Vancouver Whitecaps", "id_juego": 4}
    ]

    equipos_nba = [
        {"nombre_club": "Los Angeles Lakers", "id_juego": 5},
        {"nombre_club": "Golden State Warriors", "id_juego": 5},
        {"nombre_club": "Brooklyn Nets", "id_juego": 5},
        {"nombre_club": "Milwaukee Bucks", "id_juego": 5},
        {"nombre_club": "Boston Celtics", "id_juego": 5},
        {"nombre_club": "Chicago Bulls", "id_juego": 5},
        {"nombre_club": "Miami Heat", "id_juego": 5},
        {"nombre_club": "Philadelphia 76ers", "id_juego": 5},
        {"nombre_club": "Phoenix Suns", "id_juego": 5},
        {"nombre_club": "Dallas Mavericks", "id_juego": 5},
        {"nombre_club": "Denver Nuggets", "id_juego": 5},
        {"nombre_club": "Utah Jazz", "id_juego": 5},
        {"nombre_club": "Toronto Raptors", "id_juego": 5},
        {"nombre_club": "Cleveland Cavaliers", "id_juego": 5},
        {"nombre_club": "Sacramento Kings", "id_juego": 5},
        {"nombre_club": "New York Knicks", "id_juego": 5},
        {"nombre_club": "Orlando Magic", "id_juego": 5},
        {"nombre_club": "Atlanta Hawks", "id_juego": 5},
        {"nombre_club": "Indiana Pacers", "id_juego": 5},
        {"nombre_club": "Washington Wizards", "id_juego": 5},
        {"nombre_club": "Portland Trail Blazers", "id_juego": 5},
        {"nombre_club": "Minnesota Timberwolves", "id_juego": 5},
        {"nombre_club": "New Orleans Pelicans", "id_juego": 5},
        {"nombre_club": "Memphis Grizzlies", "id_juego": 5},
        {"nombre_club": "Charlotte Hornets", "id_juego": 5},
        {"nombre_club": "Detroit Pistons", "id_juego": 5},
        {"nombre_club": "Oklahoma City Thunder", "id_juego": 5},
        {"nombre_club": "San Antonio Spurs", "id_juego": 5},
        {"nombre_club": "Houston Rockets", "id_juego": 5}
    ]

    equipos_nfl = [
        {"nombre_club": "Buffalo Bills", "id_juego": 6},
        {"nombre_club": "Miami Dolphins", "id_juego": 6},
        {"nombre_club": "New England Patriots", "id_juego": 6},
        {"nombre_club": "New York Jets", "id_juego": 6},
        {"nombre_club": "Baltimore Ravens", "id_juego": 6},
        {"nombre_club": "Cincinnati Bengals", "id_juego": 6},
        {"nombre_club": "Cleveland Browns", "id_juego": 6},
        {"nombre_club": "Pittsburgh Steelers", "id_juego": 6},
        {"nombre_club": "Houston Texans", "id_juego": 6},
        {"nombre_club": "Indianapolis Colts", "id_juego": 6},
        {"nombre_club": "Jacksonville Jaguars", "id_juego": 6},
        {"nombre_club": "Tennessee Titans", "id_juego": 6},
        {"nombre_club": "Denver Broncos", "id_juego": 6},
        {"nombre_club": "Kansas City Chiefs", "id_juego": 6},
        {"nombre_club": "Las Vegas Raiders", "id_juego": 6},
        {"nombre_club": "Los Angeles Chargers", "id_juego": 6},
        {"nombre_club": "Dallas Cowboys", "id_juego": 6},
        {"nombre_club": "New York Giants", "id_juego": 6},
        {"nombre_club": "Philadelphia Eagles", "id_juego": 6},
        {"nombre_club": "Washington Commanders", "id_juego": 6},
        {"nombre_club": "Chicago Bears", "id_juego": 6},
        {"nombre_club": "Detroit Lions", "id_juego": 6},
        {"nombre_club": "Green Bay Packers", "id_juego": 6},
        {"nombre_club": "Minnesota Vikings", "id_juego": 6},
        {"nombre_club": "Atlanta Falcons", "id_juego": 6},
        {"nombre_club": "Carolina Panthers", "id_juego": 6},
        {"nombre_club": "New Orleans Saints", "id_juego": 6},
        {"nombre_club": "Tampa Bay Buccaneers", "id_juego": 6},
        {"nombre_club": "Arizona Cardinals", "id_juego": 6},
        {"nombre_club": "Los Angeles Rams", "id_juego": 6},
        {"nombre_club": "San Francisco 49ers", "id_juego": 6},
        {"nombre_club": "Seattle Seahawks", "id_juego": 6}
    ]

#Se juntan todas las listas de clubes
    clubs = equipos_fifa + equipos_nba + equipos_nfl

#Se recorre todas las listas de clubes
    for club in clubs:

#Llamaos a los juegos para ver si pertenece a algun club
        juego = db_session.query(Juego).filter(Juego.id_juego == club["id_juego"]).first()

#si no esta el juego en la bd salta un aviso
        if not juego:
            print(f"El Juego del club: {club['nombre_club']} no existe")
            continue

#Llamamos a los clubs para ver si esta en la bd
        existe = db_session.query(Club).filter(Club.nombre_club == club["nombre_club"]).first()

#Si no se encuentra en la bd se crea el club
        if not existe:
            nuevo_club = Club(
                nombre_club =club["nombre_club"],
                id_juego=club["id_juego"],
            )

            db_session.add(nuevo_club)
            print(f"Club creado {club['nombre_club']}")

    db_session.commit()
    print("Seed de clubes completada")

#Seed de armas
def seed_armas():
#Tiene el mismo funcionamiento que los seeds de personajes y clubes

    armas_batt = [
        {"nombre_arma": "M16A4", "tipo_arma": "Rifle de asalto", "id_juego": 7},
        {"nombre_arma": "AK-47", "tipo_arma": "Rifle de asalto", "id_juego": 7},
        {"nombre_arma": "M4A1", "tipo_arma": "Rifle de asalto", "id_juego": 7},
        {"nombre_arma": "MP5", "tipo_arma": "Subfusil", "id_juego": 7},
        {"nombre_arma": "UMP45", "tipo_arma": "Subfusil", "id_juego": 7},
        {"nombre_arma": "Glock 17", "tipo_arma": "Pistola", "id_juego": 7},
        {"nombre_arma": "Desert Eagle", "tipo_arma": "Pistola", "id_juego": 7},
        {"nombre_arma": "M1911", "tipo_arma": "Pistola", "id_juego": 7},
        {"nombre_arma": "M24", "tipo_arma": "Francotirador", "id_juego": 7},
        {"nombre_arma": "AWP", "tipo_arma": "Francotirador", "id_juego": 7},
        {"nombre_arma": "RPG-7", "tipo_arma": "Misil", "id_juego": 7},
        {"nombre_arma": "Grenade", "tipo_arma": "Arrojadiza", "id_juego": 7},
        {"nombre_arma": "M249", "tipo_arma": "Ametralladora ligera", "id_juego": 7},
        {"nombre_arma": "PKM", "tipo_arma": "Ametralladora ligera", "id_juego": 7},
        {"nombre_arma": "M870", "tipo_arma": "Escopeta", "id_juego": 7},
        {"nombre_arma": "SPAS-12", "tipo_arma": "Escopeta", "id_juego": 7},
        {"nombre_arma": "M67 Grenade", "tipo_arma": "Explosivo", "id_juego": 7},
        {"nombre_arma": "C4", "tipo_arma": "Explosivo", "id_juego": 7},
        {"nombre_arma": "Barrett M82", "tipo_arma": "Francotirador pesado", "id_juego": 7},
        {"nombre_arma": "MG42", "tipo_arma": "Ametralladora pesada", "id_juego": 7}
    ]

    armas_call = [
        {"nombre_arma": "AK-47", "tipo_arma": "Rifle de asalto", "id_juego": 8},
        {"nombre_arma": "M4", "tipo_arma": "Rifle de asalto", "id_juego": 8},
        {"nombre_arma": "FAMAS", "tipo_arma": "Rifle de asalto", "id_juego": 8},
        {"nombre_arma": "MP5", "tipo_arma": "Subfusil", "id_juego": 8},
        {"nombre_arma": "UMP45", "tipo_arma": "Subfusil", "id_juego": 8},
        {"nombre_arma": "P90", "tipo_arma": "Subfusil", "id_juego": 8},
        {"nombre_arma": "M1911", "tipo_arma": "Pistola", "id_juego": 8},
        {"nombre_arma": "Desert Eagle", "tipo_arma": "Pistola", "id_juego": 8},
        {"nombre_arma": "Barrett .50cal", "tipo_arma": "Francotirador pesado", "id_juego": 8},
        {"nombre_arma": "M21", "tipo_arma": "Francotirador", "id_juego": 8},
        {"nombre_arma": "RPG-7", "tipo_arma": "Misil", "id_juego": 8},
        {"nombre_arma": "Grenade", "tipo_arma": "Arrojadiza", "id_juego": 8},
        {"nombre_arma": "Claymore", "tipo_arma": "Explosivo", "id_juego": 8},
        {"nombre_arma": "C4", "tipo_arma": "Explosivo", "id_juego": 8},
        {"nombre_arma": "MG42", "tipo_arma": "Ametralladora ligera", "id_juego": 8},
        {"nombre_arma": "M60", "tipo_arma": "Ametralladora pesada", "id_juego": 8},
        {"nombre_arma": "SPAS-12", "tipo_arma": "Escopeta", "id_juego": 8},
        {"nombre_arma": "Remington 870", "tipo_arma": "Escopeta", "id_juego": 8},
        {"nombre_arma": "Crossbow", "tipo_arma": "Especial", "id_juego": 8},
        {"nombre_arma": "Thompson", "tipo_arma": "Rifle de asalto clásico", "id_juego": 8}
    ]

    armas_rainbow = [
        {"nombre_arma": "L85A2", "tipo_arma": "Rifle de asalto", "id_juego": 9},
        {"nombre_arma": "AR33", "tipo_arma": "Rifle de asalto", "id_juego": 9},
        {"nombre_arma": "G36C", "tipo_arma": "Rifle de asalto", "id_juego": 9},
        {"nombre_arma": "R4-C", "tipo_arma": "Rifle de asalto", "id_juego": 9},
        {"nombre_arma": "556xi", "tipo_arma": "Rifle de asalto", "id_juego": 9},
        {"nombre_arma": "F2", "tipo_arma": "Rifle de asalto", "id_juego": 9},
        {"nombre_arma": "AK-12", "tipo_arma": "Rifle de asalto", "id_juego": 9},
        {"nombre_arma": "AUG A2", "tipo_arma": "Rifle de asalto", "id_juego": 9},
        {"nombre_arma": "552 Commando", "tipo_arma": "Rifle de asalto", "id_juego": 9},
        {"nombre_arma": "416-C Carbine", "tipo_arma": "Rifle de asalto", "id_juego": 9},
        {"nombre_arma": "C8-SFW", "tipo_arma": "Rifle de asalto", "id_juego": 9},
        {"nombre_arma": "Mk17 CQB", "tipo_arma": "Rifle de asalto", "id_juego": 9},
        {"nombre_arma": "Para-308", "tipo_arma": "Rifle de asalto", "id_juego": 9},
        {"nombre_arma": "Type-89", "tipo_arma": "Rifle de asalto", "id_juego": 9},
        {"nombre_arma": "C7E", "tipo_arma": "Rifle de asalto", "id_juego": 9},
        {"nombre_arma": "M762", "tipo_arma": "Rifle de asalto", "id_juego": 9},
        {"nombre_arma": "V308", "tipo_arma": "Rifle de asalto", "id_juego": 9},
        {"nombre_arma": "ARX200", "tipo_arma": "Rifle de asalto", "id_juego": 9},
        {"nombre_arma": "F90", "tipo_arma": "Rifle de asalto", "id_juego": 9},
        {"nombre_arma": "MP5", "tipo_arma": "Subfusil", "id_juego": 9},
        {"nombre_arma": "MP5K", "tipo_arma": "Subfusil", "id_juego": 9},
        {"nombre_arma": "UMP45", "tipo_arma": "Subfusil", "id_juego": 9},
        {"nombre_arma": "P90", "tipo_arma": "Subfusil", "id_juego": 9},
        {"nombre_arma": "MP7", "tipo_arma": "Subfusil", "id_juego": 9},
        {"nombre_arma": "FMG-9", "tipo_arma": "Subfusil", "id_juego": 9},
        {"nombre_arma": "Vector .45 ACP", "tipo_arma": "Subfusil", "id_juego": 9},
        {"nombre_arma": "T-5 SMG", "tipo_arma": "Subfusil", "id_juego": 9},
        {"nombre_arma": "K1A", "tipo_arma": "Subfusil", "id_juego": 9},
        {"nombre_arma": "PDW9", "tipo_arma": "Subfusil", "id_juego": 9},
        {"nombre_arma": "MPX", "tipo_arma": "Subfusil", "id_juego": 9},
        {"nombre_arma": "Mx4 Storm", "tipo_arma": "Subfusil", "id_juego": 9},
        {"nombre_arma": "SPSMG9", "tipo_arma": "Subfusil", "id_juego": 9},
        {"nombre_arma": "6P41", "tipo_arma": "Ametralladora ligera", "id_juego": 9},
        {"nombre_arma": "G8A1", "tipo_arma": "Ametralladora ligera", "id_juego": 9},
        {"nombre_arma": "M249", "tipo_arma": "Ametralladora ligera", "id_juego": 9},
        {"nombre_arma": "T-95 LSW", "tipo_arma": "Ametralladora ligera", "id_juego": 9},
        {"nombre_arma": "LMG-E", "tipo_arma": "Ametralladora ligera", "id_juego": 9},
        {"nombre_arma": "ALDA 5.56", "tipo_arma": "Ametralladora ligera", "id_juego": 9},
        {"nombre_arma": "M590A1", "tipo_arma": "Escopeta", "id_juego": 9},
        {"nombre_arma": "M1014", "tipo_arma": "Escopeta", "id_juego": 9},
        {"nombre_arma": "M870", "tipo_arma": "Escopeta", "id_juego": 9},
        {"nombre_arma": "SG-CQB", "tipo_arma": "Escopeta", "id_juego": 9},
        {"nombre_arma": "SASG-12", "tipo_arma": "Escopeta", "id_juego": 9},
        {"nombre_arma": "ACS12", "tipo_arma": "Escopeta", "id_juego": 9},
        {"nombre_arma": "ITA12S", "tipo_arma": "Escopeta", "id_juego": 9},
        {"nombre_arma": "ITA12L", "tipo_arma": "Escopeta", "id_juego": 9},
        {"nombre_arma": "P226 Mk 25", "tipo_arma": "Pistola", "id_juego": 9},
        {"nombre_arma": "M45 MEUSOC", "tipo_arma": "Pistola", "id_juego": 9},
        {"nombre_arma": "5.7 USG", "tipo_arma": "Pistola", "id_juego": 9},
        {"nombre_arma": "P12", "tipo_arma": "Pistola", "id_juego": 9},
        {"nombre_arma": "P9", "tipo_arma": "Pistola", "id_juego": 9},
        {"nombre_arma": "LFP586", "tipo_arma": "Pistola", "id_juego": 9},
        {"nombre_arma": "GSh-18", "tipo_arma": "Pistola", "id_juego": 9},
        {"nombre_arma": "PMM", "tipo_arma": "Pistola", "id_juego": 9},
        {"nombre_arma": "Mk1 9mm", "tipo_arma": "Pistola", "id_juego": 9},
        {"nombre_arma": "D-50", "tipo_arma": "Pistola", "id_juego": 9},
        {"nombre_arma": "PRB92", "tipo_arma": "Pistola", "id_juego": 9},
        {"nombre_arma": "USP40", "tipo_arma": "Pistola", "id_juego": 9},
        {"nombre_arma": "SDP 9mm", "tipo_arma": "Pistola", "id_juego": 9}
    ]

    armas = armas_batt + armas_call + armas_rainbow

    for arma in armas:

        juego = db_session.query(Juego).filter(Juego.id_juego == arma["id_juego"]).first()

        if not juego:
            print(f"El Juego del personaje: {arma['nombre_arma']} no existe")
            continue

        existe = db_session.query(Armas).filter(
            Armas.nombre_arma == arma["nombre_arma"],
            Armas.id_juego == arma["id_juego"]
        ).first()

        if not existe:
            nuevo_arma = Armas(
                nombre_arma = arma["nombre_arma"],
                tipo_arma= arma["tipo_arma"],
                id_juego = arma["id_juego"],
            )

            db_session.add(nuevo_arma)
            print(f"Arma creada {arma['nombre_arma']}")

    db_session.commit()
    print("Seed de armas completada")


#Seed para la creacion del administrados
def seed_admin():
#Se guarda en una los usuarios con el rol de administrador
    admin = [{
        "nombre": "Roberto",
        "apellidos": "Garcia Crespo",
        "fecha_nacimiento": date(1998, 4, 29),
        "email": "admin2@gmail.com",
        "nombre_usuario": "RobertoAdmin2",
        "password": "admin",
        "id_rol": 1
    }]

#Recorremos la lista de admin
    for a in admin:
#Buscamos el rol directamente con get
        rol = db.db_session.get(Rol, a["id_rol"])

#Si no hay ningun rol salta un aviso
        if not rol:
            print(f"Rol {a['id_rol']} no encontrado, admin no creado")
            continue

#Comprobamos si el usuario existe
        existe = db.db_session.query(Usuario).filter_by(nombre_usuario=a["nombre_usuario"]).first()

        if existe:
            print(f"Usuario {a['nombre_usuario']} ya existe")
            continue

        nuevo_usuario = Usuario(
            nombre=a["nombre"],
            apellidos=a["apellidos"],
            fecha_nacimiento=a["fecha_nacimiento"],
            email=a["email"],
            nombre_usuario=a["nombre_usuario"],
            password=a["password"]
        )
#asignamos el rol
        nuevo_usuario.rol_obj = rol

        db.db_session.add(nuevo_usuario)
        print(f"Admin creado: {a['nombre']}")

    try:
        db.db_session.commit()
        print("Seed de administrador completado")
    except Exception as e:
        db.db_session.rollback()
        print("Error en seed_admin:", e)

#Seed para los usuarios
def seed_usuarios():

#Validamos a los usuarios
    letras = list(string.ascii_lowercase[:10])  # a-j

    usuarios = []

    for i, letra in enumerate(letras):

#Creamos a los usuarios
        usuarios.append({
            "nombre": letra * 3,          # aaa, bbb, ccc...
            "apellidos": letra * 3,
            "fecha_nacimiento": date.today() - timedelta(days=random.randint(7000, 15000)),
            "email": f"{letra}@gmail.com",
            "nombre_usuario": letra * 3,
            "password": letra * 3,
            "id_rol": 2   # usuario normal
        })

#Recorremos la lista de los usuarios
    for u in usuarios:

# comprobamos los roles
        rol = db.db_session.get(Rol, u["id_rol"])
        if not rol:
            print(f"Rol {u['id_rol']} no encontrado")
            continue

#evitar duplicados mirando si el usuario existe
        existe = db.db_session.query(Usuario).filter_by(
            nombre_usuario=u["nombre_usuario"]
        ).first()

        if existe:
            print(f"Usuario {u['nombre_usuario']} ya existe")
            continue

        nuevo_usuario = Usuario(
            nombre=u["nombre"],
            apellidos=u["apellidos"],
            fecha_nacimiento=u["fecha_nacimiento"],
            email=u["email"],
            nombre_usuario=u["nombre_usuario"],
            password=u["password"]
        )

#Asignamos los roles
        nuevo_usuario.rol_obj = rol

        db.db_session.add(nuevo_usuario)

        print(f"Usuario creado: {u['nombre_usuario']}")

    try:
        db.db_session.commit()
        print("Seed de usuarios completado correctamente")

    except Exception as e:
        db.db_session.rollback()
        print("Error en seed_usuarios:", e)

#Seed de personajes con sus armas con el mismo funcionamiento del seed de personajes, clubes y armas
def seed_personaje_armas():
    rainbow = [
        {"id_juego": 9, "id_personaje": 63, "id_arma": 41, "habilidad": "Martillo demoledor"},
        {"id_juego": 9, "id_personaje": 63, "id_arma": 79, "habilidad": "Martillo demoledor"},
        {"id_juego": 9, "id_personaje": 63, "id_arma": 89, "habilidad": "Martillo demoledor"},

        {"id_juego": 9, "id_personaje": 64, "id_arma": 41, "habilidad": "Granada PEM"},
        {"id_juego": 9, "id_personaje": 64, "id_arma": 42, "habilidad": "Granada PEM"},
        {"id_juego": 9, "id_personaje": 64, "id_arma": 89, "habilidad": "Granada PEM"},

        {"id_juego": 9, "id_personaje": 65, "id_arma": 44, "habilidad": "Proyectil de brecha"},
        {"id_juego": 9, "id_personaje": 65, "id_arma": 43, "habilidad": "Proyectil de brecha"},
        {"id_juego": 9, "id_personaje": 65, "id_arma": 90, "habilidad": "Proyectil de brecha"},

        {"id_juego": 9, "id_personaje": 66, "id_arma": 45, "habilidad": "Carga exotérmica"},
        {"id_juego": 9, "id_personaje": 66, "id_arma": 80, "habilidad": "Carga exotérmica"},
        {"id_juego": 9, "id_personaje": 66, "id_arma": 91, "habilidad": "Carga exotérmica"},

        {"id_juego": 9, "id_personaje": 67, "id_arma": 46, "habilidad": "Dron de choque"},
        {"id_juego": 9, "id_personaje": 67, "id_arma": 81, "habilidad": "Dron de choque"},
        {"id_juego": 9, "id_personaje": 67, "id_arma": 92, "habilidad": "Dron de choque"},

        {"id_juego": 9, "id_personaje": 68, "id_arma": 92, "habilidad": "Escudo extensible"},
        {"id_juego": 9, "id_personaje": 68, "id_arma": 93, "habilidad": "Escudo extensible"},

        {"id_juego": 9, "id_personaje": 69, "id_arma": 83, "habilidad": "Mira térmica"},
        {"id_juego": 9, "id_personaje": 69, "id_arma": 88, "habilidad": "Mira térmica"},

        {"id_juego": 9, "id_personaje": 70, "id_arma": 47, "habilidad": "Carga de racimo"},
        {"id_juego": 9, "id_personaje": 70, "id_arma": 74, "habilidad": "Carga de racimo"},
        {"id_juego": 9, "id_personaje": 70, "id_arma": 88, "habilidad": "Carga de racimo"},

        {"id_juego": 9, "id_personaje": 71, "id_arma": 94, "habilidad": "Escudo cegador"},

        {"id_juego": 9, "id_personaje": 72, "id_arma": 48, "habilidad": "Detector electrónico"},
        {"id_juego": 9, "id_personaje": 72, "id_arma": 49, "habilidad": "Detector electrónico"},
        {"id_juego": 9, "id_personaje": 72, "id_arma": 95, "habilidad": "Detector electrónico"},

        {"id_juego": 9, "id_personaje": 73, "id_arma": 51, "habilidad": "Escopeta táctica"},
        {"id_juego": 9, "id_personaje": 73, "id_arma": 96, "habilidad": "Escopeta táctica"},

        {"id_juego": 9, "id_personaje": 74, "id_arma": 52, "habilidad": "Escudo balístico"},
        {"id_juego": 9, "id_personaje": 74, "id_arma": 97, "habilidad": "Escudo balístico"},

        {"id_juego": 9, "id_personaje": 75, "id_arma": 53, "habilidad": "Ballesta táctica"},
        {"id_juego": 9, "id_personaje": 75, "id_arma": 98, "habilidad": "Ballesta táctica"},

        {"id_juego": 9, "id_personaje": 76, "id_arma": 54, "habilidad": "Lanzador X-Kairos"},
        {"id_juego": 9, "id_personaje": 76, "id_arma": 99, "habilidad": "Lanzador X-Kairos"},

        {"id_juego": 9, "id_personaje": 77, "id_arma": 55, "habilidad": "Visor de rastreo"},
        {"id_juego": 9, "id_personaje": 77, "id_arma": 97, "habilidad": "Visor de rastreo"},

        {"id_juego": 9, "id_personaje": 78, "id_arma": 56, "habilidad": "Granada candela"},
        {"id_juego": 9, "id_personaje": 78, "id_arma": 94, "habilidad": "Granada candela"},

        {"id_juego": 9, "id_personaje": 79, "id_arma": 57, "habilidad": "Lanzador KS79"},
        {"id_juego": 9, "id_personaje": 79, "id_arma": 95, "habilidad": "Lanzador KS79"},

        {"id_juego": 9, "id_personaje": 80, "id_arma": 58, "habilidad": "Bomba lógica"},
        {"id_juego": 9, "id_personaje": 80, "id_arma": 96, "habilidad": "Bomba lógica"},

        {"id_juego": 9, "id_personaje": 81, "id_arma": 59, "habilidad": "EE-UNO-D"},
        {"id_juego": 9, "id_personaje": 81, "id_arma": 97, "habilidad": "EE-UNO-D"},

        {"id_juego": 9, "id_personaje": 82, "id_arma": 60, "habilidad": "Impulso adrenal"},
        {"id_juego": 9, "id_personaje": 82, "id_arma": 98, "habilidad": "Impulso adrenal"},

        {"id_juego": 9, "id_personaje": 83, "id_arma": 61, "habilidad": "Soplete táctico"},
        {"id_juego": 9, "id_personaje": 83, "id_arma": 99, "habilidad": "Soplete táctico"},

        {"id_juego": 9, "id_personaje": 97, "id_arma": 65, "habilidad": "Granada de gas remoto"},
        {"id_juego": 9, "id_personaje": 97, "id_arma": 90, "habilidad": "Granada de gas remoto"},

        {"id_juego": 9, "id_personaje": 98, "id_arma": 66, "habilidad": "Inhibidor de señal"},
        {"id_juego": 9, "id_personaje": 98, "id_arma": 91, "habilidad": "Inhibidor de señal"},

        {"id_juego": 9, "id_personaje": 99, "id_arma": 67, "habilidad": "Panel blindado"},
        {"id_juego": 9, "id_personaje": 99, "id_arma": 92, "habilidad": "Panel blindado"},

        {"id_juego": 9, "id_personaje": 100, "id_arma": 68, "habilidad": "Sensor cardíaco"},
        {"id_juego": 9, "id_personaje": 100, "id_arma": 93, "habilidad": "Sensor cardíaco"},

        {"id_juego": 9, "id_personaje": 101, "id_arma": 69, "habilidad": "Pistola estimulante"},
        {"id_juego": 9, "id_personaje": 101, "id_arma": 94, "habilidad": "Pistola estimulante"},

        {"id_juego": 9, "id_personaje": 102, "id_arma": 70, "habilidad": "Placas blindadas"},
        {"id_juego": 9, "id_personaje": 102, "id_arma": 95, "habilidad": "Placas blindadas"},

        {"id_juego": 9, "id_personaje": 103, "id_arma": 71, "habilidad": "Trampa explosiva"},
        {"id_juego": 9, "id_personaje": 103, "id_arma": 96, "habilidad": "Trampa explosiva"},

        {"id_juego": 9, "id_personaje": 104, "id_arma": 72, "habilidad": "Torreta montada"},
        {"id_juego": 9, "id_personaje": 104, "id_arma": 97, "habilidad": "Torreta montada"},

        {"id_juego": 9, "id_personaje": 105, "id_arma": 73, "habilidad": "Sistema ADS"},
        {"id_juego": 9, "id_personaje": 105, "id_arma": 98, "habilidad": "Sistema ADS"},

        {"id_juego": 9, "id_personaje": 106, "id_arma": 74, "habilidad": "Batería de choque"},
        {"id_juego": 9, "id_personaje": 106, "id_arma": 99, "habilidad": "Batería de choque"}
    ]

    for per_arm in rainbow:

        juego = db_session.query(Juego).filter(Juego.id_juego == per_arm["id_juego"]).first()

        if not juego:
            continue

        personaje = db_session.query(Personaje).filter(Personaje.id_personaje == per_arm["id_personaje"]).first()

        if not personaje:
            continue

        arma = db_session.query(Armas).filter(Armas.id_armas == per_arm["id_arma"]).first()

        if not arma:
            continue

        existe = db_session.query(Personaje_arma).filter(
            Personaje_arma.id_juego == per_arm["id_juego"],
            Personaje_arma.id_personaje == per_arm["id_personaje"],
            Personaje_arma.id_armas == per_arm["id_arma"]
        ).first()

        if not existe:
            nuevo_personaje_arma = Personaje_arma(
                id_juego=per_arm["id_juego"],
                id_personaje=per_arm["id_personaje"],
                id_armas = per_arm["id_arma"],
                habilidad = per_arm["habilidad"]
            )

            db_session.add(nuevo_personaje_arma)

    db_session.commit()
    print("Seed de personjes_armas completada")

#Seed para guardar y llamar a los demas seeds
def seed_all():
    seed_roles()
    seed_generos()
    seed_juegos()
    seed_personajes()
    seed_clubs()
    seed_armas()
    seed_admin()
    #seed_usuarios()
    seed_personaje_armas()