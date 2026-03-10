from titlecase import titlecase

def round_num(value, decim=2):
    try:
        return str(round(float(value), decim))
    except (TypeError, ValueError):
        return None

def format_title(titulo: str) -> str:
    titulo = titulo.strip()
    return titlecase(titulo)

def isIsbn(valor: str) -> bool:
    valor = valor.replace("-", "").strip()
    return valor.isdigit and len(valor) in (10, 13)

def normaliza_books(result, is_isbn=False):
    if is_isbn:
        return [edition["book"] for edition in result["data"]["editions"] if edition.get("book")]
    else:
        return result["data"]["books"]

def construccion_sql(sql, count, titulo, tipo, estado, orden="id", limite=20, offset=0):
    condiciones = []
    parametros = []

    if titulo:
        condiciones.append("datos->>'titulo' ILIKE %s")
        parametros.append(f"%{titulo}%")

    if tipo:
        if tipo != "todos":
            condiciones.append("tipo = %s")
            parametros.append(tipo)
        else:
            condiciones.append("1=1")

    if estado:
        condiciones.append("estado = %s")
        parametros.append(estado)

    if condiciones:
        sql += " WHERE " + " AND ".join(condiciones) 

    if count:
        return sql, parametros   
    
    if orden:
        orden_sql = {
            'antiguos': " ORDER BY id ASC",
            'unpopular': " ORDER BY puntuacion ASC",
            'popular': " ORDER BY puntuacion DESC"
        }.get(orden, " ORDER BY id DESC")

        sql += orden_sql

    sql += " LIMIT %s OFFSET %s"
    parametros.append(limite)
    parametros.append(offset)

    return sql, parametros
