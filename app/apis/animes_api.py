import requests

ANILIST_URL = "https://graphql.anilist.co/"

class AnimeApiError(Exception):
    pass


def search_anilist(title, media_type):
    query = """
    query ($search: String, $type: MediaType) {
      Page(perPage: 20) {
        media(search: $search, type: $type) {
          id
          title {
            romaji
            english
          }
          countryOfOrigin
          format
          description
          averageScore
          genres
          seasonYear
          coverImage {
            large
          }
        }
      }
    }
    """

    variables = {
        "search": title,
        "type": media_type.upper()
    }

    try:
        response = requests.post(
            ANILIST_URL,
            json={"query": query, "variables": variables},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        if "errors" in data:
            raise AnimeApiError(data["errors"])

        return data["data"]["Page"]["media"]

    except requests.RequestException as e:
        raise AnimeApiError("AniList no respondió correctamente") from e
