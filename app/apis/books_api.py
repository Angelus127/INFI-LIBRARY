import requests, os

class BookApiError(Exception):
    pass

def search_books(title):
    query = """
    query GetEditionsFromTitle ($titulo: String!) {
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
    
    try:
        response = requests.post(
            "https://api.hardcover.app/v1/graphql",
            headers = {
                "Authorization": f"Bearer {os.getenv('BOOKS_API')}",
                "Content-Type": "application/json"
            },
            json={"query": query, "variables": {"titulo": title}},
            timeout=10
        )
        response.raise_for_status()
        return response.json()["data"]["books"]
    except Exception as e:
        raise BookApiError("Hardcover no respondio correctamente") from e