TRADUCCION_GENEROS = {
    "Action": "Accion",
    "Adventure": "Aventura",
    "Fantasy": "Fantasía",
    "Romance": "Romance",
    "Comedy": "Comedia",
    "Drama": "Drama",
    "Ecchi": "Ecchi",
    "Sci-Fi": "Ciencia ficcion",
    "Science fiction": "Ciencia ficcion",
    "Horror": "Terror",
    "Mystery": "Misterio",
    "Psychological": "Psicologico",
    "Supernatural": "Sobrenatural",
    "Mecha": "Mecha",
    "Slice of Life": "Recuentos de la vida",
    "Music": "Musica",
    "Hentai": "Hentai",
    "Thriller": "Suspenso",
    "Fiction": "Ficcion",
    "Juvenile Fiction": "Ficción juvenil",
    "Young Adult": "Adulto Joven",
    "Young Adult Fiction": "Ficción juvenil adulta",
    "Literary Criticism": "Crítica literaria",
    "History": "Historia",
    "Angels": "Angeles",
    "Magic": "Magia",
    "Spicy": "Spicy",
    "Philosophy": "Filosofia",
    "Classics": "Clasico",
    "Treasure": "Tesoro",
    "Dystopian": "Distopia",
    "Spirituality": "Espiritual",
    "Self-Help": "Auto-Ayuda",
    "Urban Fantasy": "Fantasia Urbana",
    "Dark Fantasy": "Fantasia Oscura"
}

def display_genre():  
    return {g for g in TRADUCCION_GENEROS.values()}

def traducir_generos(lista):
    return [TRADUCCION_GENEROS.get(g, g) for g in lista]