from pydantic import BaseModel
from typing import List, Optional, Dict

class UserInfoRequest(BaseModel):
    favorite_genres: List[str]
    reading_history: List[Dict[str, str]] = []
    age: Optional[int] = None
    occupation: Optional[str] = None
    location: Optional[str] = None