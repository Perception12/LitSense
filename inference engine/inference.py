from openai import OpenAI
import os
from dotenv import load_dotenv
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain import globals
from langchain_core.runnables import chain
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputParser
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
        
        
    def extract_book_information(self, image_path: str):
        input_prompt = get_prompt_from_template("prompts/extract_book_information_template.jinja")
        
        parser = JsonOutputParser(pydantic_object=BookInformation)
        
        @chain
        def image_model(inputs: dict) -> str | list[str]:
            """Invoke model with image and prompt"""
            llm = ChatOpenAI(
                model="gpt-4o",
                temperature=0,
                max_tokens=1024
            )
            
            msg = llm.invoke([
                HumanMessage(
                    content=[
                        {"type": "text", "text": inputs["prompt"]},
                        {"type": "text", "text": parser.get_format_instructions()},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{inputs['image_base64']}"}}
                    ]
                )
            ])
            
            return msg.content
        
        vision_chain = load_image_chain() | image_model | parser
        
        return vision_chain.invoke({"image_path": image_path, "prompt": input_prompt})
    
            

        
        
    