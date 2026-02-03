from typing import Optional, Dict, List
from pydantic.v1 import BaseModel, Field


class BookInformation(BaseModel):
    "Information about the book cover image."
    title: str = Field(..., description="The title of the book.")
    authors: List[str] = Field(..., description="List of authors of the book.")
    genre: str = Field(..., description="The genre of the book.")
    confidence: float = Field(..., description="Model's confidence in the extracted information.", ge=0.0, le=1.0)
    
class InferenceResponse(BaseModel):
    "Infer if the book fits the user's preferences."
    fit_with_preferences: bool = Field(..., description="Whether the book fits the user's preferences.")
    reason_for_fit: str = Field(..., description="Reason why the book fits the user's preferences.")
    match_score: float = Field(..., description="A score indicating how well the book matches the user's preferences.", ge=0.0, le=1.0)

class UserInfo(BaseModel):
    """Information about the user and their reading preferences."""
    user_id: str = Field(..., description="Unique identifier for the user.")
    name: str = Field(..., description="Name of the user.")
    age: Optional[int] = Field(None, description="Age of the user.")
    occupation: Optional[str] = Field(None, description="Occupation of the user.")
    location: Optional[str] = Field(None, description="Location of the user.")
    reading_history: List[Dict[str, str]] = Field(default_factory=list)
    favorite_genres: List[str] = Field(default_factory=list)
 