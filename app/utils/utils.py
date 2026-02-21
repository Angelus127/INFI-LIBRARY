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