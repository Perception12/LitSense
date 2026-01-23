from openai import OpenAI
import os
from dotenv import load_dotenv
from jinja2 import Template
from pathlib import Path
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain import globals
from langchain_core.runnables import chain
from langchain_core.messages import HumanMessage
from utils import load_image_chain, get_prompt_from_template


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

class BookInferenceEngine:
    def __init__(self):
        _ = load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        globals.set_debug(True)
        
    @chain    
    def extract_book_information(self, book_cover):
        system_prompt = get_prompt_from_template("prompts/system_prompt_template.jinja")
        extract_book_information_prompt = get_prompt_from_template("prompts/extract_book_information_template.jinja")

        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            max_tokens=1024
        )
        
        return llm.invoke([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": extract_book_information_prompt}
        ])
            

        
        
    