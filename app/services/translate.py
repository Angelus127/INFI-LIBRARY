def traducir_generos(lista_generos):
    traduccion_generos = {
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

    return [traduccion_generos.get(g, g) for g in lista_generos]

def traducir_temporada(valor):
    traduccion_temporadas = {
        "WINTER": "Invierno",
        "SPRING": "Primavera",
        "SUMMER": "Verano",
        "FALL": "Otoño",
        None: None
    }
    return traduccion_temporadas.get(valor, valor)

def traducir_estado(valor):
    traduccion_estados = {
    "FINISHED": "Finalizado",
    "RELEASING": "En emisión",
    "NOT_YET_RELEASED": "Próximo",
    "CANCELLED": "Cancelado",
    "HIATUS": "En pausa",
    None: None
    }
    return traduccion_estados.get(valor, valor)