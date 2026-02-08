from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.runnables import chain
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from inference_engine.utils import load_image_chain, get_prompt_from_template
from inference_engine.data_models import BookInformation, InferenceResponse, UserInfo


class BookInferenceEngine:
    def __init__(self):
        _ = load_dotenv()
        self.llm = ChatOpenAI(
                model="gpt-4o",
                temperature=0,
                max_tokens=1024
            )
            
        
        
        
    def extract_book_information(self, image_path:str):
        input_prompt_template = get_prompt_from_template("extract_book_information_template.jinja")
        parser = JsonOutputParser(pydantic_object=BookInformation)
        input_prompt = input_prompt_template.render(
            format_instructions=parser.get_format_instructions()
        )
        
        if not input_prompt:
            raise ValueError("Prompt template could not be rendered or is empty")
        
        @chain
        def image_model(inputs: dict) -> str | list[str]:
            """Invoke model with image and prompt"""
            
            if "prompt" not in inputs:
                raise ValueError("Missing 'prompt' in input dictionary")
            
            msg = self.llm.invoke([
                HumanMessage(
                    content=[
                        {"type": "text", "text": inputs["prompt"]},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64, {inputs['image']}"}}
                    ]
                )
            ])
            
            return msg.content
        
        
        vision_chain = load_image_chain() | image_model | parser
        
        return vision_chain.invoke({"image_path": image_path, "prompt": input_prompt})
    
    def check_if_book_fits_preferences(self, book_info: BookInformation, user_info: UserInfo):
        input_prompt_template = get_prompt_from_template("preference_prompt.jinja")
        
        parser = JsonOutputParser(pydantic_object=InferenceResponse)
        
        input_prompt = input_prompt_template.render(
            book_info=book_info,
            user_info=user_info,
            format_instructions=parser.get_format_instructions()
        )
        
        if not input_prompt:
            raise ValueError("Prompt template could not be rendered or is empty")
        
        @chain
        def preference_model(inputs: dict) -> str | list[str]:
            """Invoke model with book info and user preferences"""
            if "prompt" not in inputs:
                raise ValueError("Missing 'prompt' in input dictionary")
            
            msg = self.llm.invoke([
                HumanMessage(
                    content=[
                        {"type": "text", "text": inputs["prompt"]},
                        {"type": "text", "text": f"Book Information: {inputs['book_info']}"},
                        {"type": "text", "text": f"User Info: {inputs['user_info']}"}
                    ]
                )
            ])
            
            return msg.content
        
        preference_chain = preference_model | parser
        
        return preference_chain.invoke({
            "book_info": book_info,
            "user_info": user_info,
            "prompt": input_prompt
        })
    
            

        
        
    