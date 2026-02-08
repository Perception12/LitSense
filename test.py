import json
import requests

url = "http://127.0.0.1:8080/api/inference"

user_info = {
    "user_id": "user_123",
    "name": "Alice",
    "age": 30,
    "occupation": "Engineer",
    "location": "New York",
    "favorite_genres": ["Science Fiction", "Classics"],
    "reading_history": [
        {"title": "1984", "author": "George Orwell"},
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}
    ]
}

with open("assets/book cover 2.jpg", "rb") as f:
    response = requests.post(
        url,
        files={"image": f},
        data={"user_info": json.dumps(user_info)}
    )

print(response.status_code)
print(response.json())
