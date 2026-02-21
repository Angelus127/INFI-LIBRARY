import requests, os
from app.utils.utils import format_title, isIsbn, normaliza_books

class BookApiError(Exception):
    pass

def search_books(title):
    if isIsbn(title):
        query = buscar_isbn()
        variables = {"isbn": title}
        key = "editions"
        books = normaliza_books(search_api(query, variables), True)

    else:
        title = format_title(title)
        query = buscar_titulo()
        variables = {"titulo": title}
        key = "books"
        books = normaliza_books(search_api(query, variables), False)
    
    return books

def search_api(query, variables):
    try:
        response = requests.post(
            "https://api.hardcover.app/v1/graphql",
            headers = {
                "Authorization": f"Bearer {os.getenv('BOOKS_API')}",
                "Content-Type": "application/json"
            },
            json={"query": query, "variables": variables},

            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise BookApiError("Hardcover no respondio correctamente") from e

def buscar_titulo():
    return """
    query ($titulo: String!) {
        books(where: { title: { _eq: $titulo } }){
            id
            title
            image {
                url
            }
            contributions {
                author {
                    name
                }
            }
            release_date
            pages
            description
            rating
            cached_tags 
        }
    }
    """

def buscar_isbn():
    return """
    query ($isbn: String!) {
        editions(where: { isbn_13: { _eq: $isbn}}) {
            book {
                id
                title
                image {
                    url
                }
                contributions {
                    author {
                        name
                    }
                }
                release_date
                pages
                description
                rating
                cached_tags 
            }
        }
    }
    """