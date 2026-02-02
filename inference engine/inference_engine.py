from openai import OpenAI
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain import globals
from langchain_core.runnables import chain
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from utils import load_image_chain, get_prompt_from_template
from data_models import BookInformation, InferenceResponse, UserInfo


class BookInferenceEngine:
    def __init__(self):
        _ = load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        globals.set_debug(True)
        
        
    def extract_book_information(self, image_path:str):
        input_prompt_template = get_prompt_from_template("prompts/extract_book_information_template.jinja")
        input_prompt = input_prompt_template.render()
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
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64, {inputs['image']}"}}
                    ]
                )
            ])
            
            return msg.content
        
        vision_chain = load_image_chain() | image_model | parser
        
        return vision_chain.invoke({"image_path": image_path, "prompt": input_prompt})
    
    def check_if_book_fits_preferences(self, book_info: BookInformation, user_info: UserInfo):
        input_prompt_template = get_prompt_from_template("prompts/preference_prompt.jinja")
        input_prompt = input_prompt_template.render(
            book_info=book_info,
            user_info=user_info.to_dict()
        )
        
        parser = JsonOutputParser(pydantic_object=InferenceResponse)
        
        @chain
        def preference_model(inputs: dict) -> str | list[str]:
            """Invoke model with book info and user preferences"""
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
                        {"type": "text", "text": f"Book Information: {inputs['book_info']}"},
                        {"type": "text", "text": f"User Info: {inputs['user_info']}"}
                    ]
                )
            ])
            
            return msg.content
        
        preference_chain = preference_model | parser
        
        return preference_chain.invoke({
            "book_info": book_info,
            "user_info": user_info.to_dict(),
            "prompt": input_prompt
        })
    
            

        
        
    