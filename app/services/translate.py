TRADUCCION_GENEROS = {
    "Action": "Acción",
    "Adventure": "Aventura",
    "Fantasy": "Fantasía",
    "Romance": "Romance",
    "Comedy": "Comedia",
    "Drama": "Drama",
    "Ecchi": "Ecchi",
    "Sci-Fi": "Ciencia ficción",
    "Science fiction": "Ciencia ficción",
    "Horror": "Terror",
    "Mystery": "Misterio",
    "Psychological": "Psicológico",
    "Supernatural": "Sobrenatural",
    "Mecha": "Mecha",
    "Slice of Life": "Recuentos de la vida",
    "Music": "Música",
    "Hentai": "Hentai",
    "Thriller": "Suspenso",
    "Fiction": "Ficción",
    "Juvenile Fiction": "Ficción juvenil",
    "Young Adult Fiction": "Ficción juvenil adulta",
    "Literary Criticism": "Crítica literaria",
    "History": "Historia",
    "Courts and courtiers": "Cortes y cortesanos",
    "Angels": "Ángeles",
}

TRADUCCION_TEMPORADAS = {
    "WINTER": "Invierno",
    "SPRING": "Primavera",
    "SUMMER": "Verano",
    "FALL": "Otoño",
    None: None
}

TRADUCCION_ESTADOS = {
    "FINISHED": "Finalizado",
    "RELEASING": "En emisión",
    "NOT_YET_RELEASED": "Próximo",
    "CANCELLED": "Cancelado",
    "HIATUS": "En pausa",
    None: None
}

def traducir(valor, tabla):
    return tabla.get(valor, valor)

def traducir_generos(lista):
    return [traducir(g, TRADUCCION_GENEROS) for g in lista]

def traducir_temporada(v):
    return traducir(v, TRADUCCION_TEMPORADAS)

def traducir_estado(v):
    return traducir(v, TRADUCCION_ESTADOS)
