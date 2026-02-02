from dataclasses import dataclass, asdict, field
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional, Dict, List


class BookInformation(BaseModel):
    "Information about the book cover image."
    title: str = Field(..., description="The title of the book.")
    authors: list[str] = Field(..., description="List of authors of the book.")
    genre: str = Field(..., description="The genre of the book.")
    
class InferenceResponse(BaseModel):
    "Infer if the book fits the user's preferences."
    book_info: BookInformation = Field(..., description="Extracted information about the book.")
    fit_with_preferences: bool = Field(..., description="Whether the book fits the user's preferences.")
    reason_for_fit: str = Field(..., description="Reason why the book fits the user's preferences.")

@dataclass
class UserInfo:
    """Information about the user and their reading preferences."""
    user_id: str
    name: str
    age: Optional[int] = None
    occupation: Optional[str] = None
    location: Optional[str] = None
    reading_history: List[Dict[str, str]] = field(default_factory=list)
    favorite_genres: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return asdict(self)