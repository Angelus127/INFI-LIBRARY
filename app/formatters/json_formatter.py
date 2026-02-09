def format_json(info):
    library = []
    for fila in info:
        library.append({
            "id": fila[0],
            "id_registro": fila[1],
            "categoria": fila[2],
            **fila[3],
            "fecha_agregado": fila[4],
            "puntaje": fila[5],
            "estado_usuario": fila[6],
            "opinion": fila[7]
        })
    return library