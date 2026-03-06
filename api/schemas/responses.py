from pydantic import BaseModel
from typing import List


class BookInfoResponse(BaseModel):
    title: str
    genres: List[str]
    authors: List[str]
    description: str = None
    

class BookRecommendationResponse(BaseModel):
    fit_with_preferences: bool
    match_score: float
    reason_for_fit: str
    