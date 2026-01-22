from openai import OpenAI
import os
from dotenv import load_dotenv
from jinja2 import Template
from pathlib import Path


class BookInferenceEngine:
    def __init__(self):
        _ = load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def extract_book_information(self, book_cover):
        system_template_path = Path("prompts/system_prompt_template.jinja")
        system_template_content = system_template_path.read_text()
        system_prompt = Template(system_template_content).render()
    