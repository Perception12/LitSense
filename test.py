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
    "favorite_authors": [ "George Orwell", "F. Scott Fitzgerald", "Albert Einstein"]
}

with open("assets/book cover 2.jpg", "rb") as f:
    response = requests.post(
        url,
        files={"image": f},
        data={"user_info": json.dumps(user_info)}
    )

print(response.status_code)
print(response.json())
