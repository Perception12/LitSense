import requests
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")


def get_book_metadata(title, author):
    url = "https://www.googleapis.com/books/v1/volumes"

    # handle author list or string
    if isinstance(author, list):
        author = author[0]

    query = f"intitle:{title}+inauthor:{author}"

    params = {
        "q": query,
        "key": GOOGLE_BOOKS_API_KEY,
        "maxResults": 1
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("totalItems", 0) == 0:
        return None

    volume = data["items"][0]["volumeInfo"]

    return {
        "title": volume.get("title"),
        "authors": volume.get("authors", []),
        "genres": volume.get("categories", []),
        "description": volume.get("description")
    }