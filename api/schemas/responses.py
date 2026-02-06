from pydantic import BaseModel
from typing import List


class BookInfoResponse(BaseModel):
    title: str
    genre: str
    authors: List[str]
    

class BookRecommendationResponse(BaseModel):
    fit_with_preferences: bool
    match_score: float
    reason_for_fit: str
    