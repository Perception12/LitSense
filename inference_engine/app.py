from engine import BookInferenceEngine
from data_models import UserInfo

engine = BookInferenceEngine()

book_info = engine.extract_book_information("../assets/book cover 2.jpg")
print("Extracted Book Information:", book_info)

user_info = UserInfo(
    user_id="user_123",
    name="Alice",
    age=30,
    occupation="Engineer",
    location="New York",
    reading_history=[
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
        {"title": "1984", "author": "George Orwell"}
    ],
    favorite_genres=["Science Fiction", "Classics"])


inference_response = engine.check_if_book_fits_preferences(book_info, user_info)
print("Inference Response:", inference_response)