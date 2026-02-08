import base64
from langchain_core.runnables import RunnableLambda
from pathlib import Path
from jinja2 import Template

def load_image(inputs: dict) -> dict:
    """Load an image from the given path and encode it in base64 format."""
    
    image_path = inputs.get("image_path")
    
    def encode_image(image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string

    image_base64 = encode_image(image_path)

    return {**inputs, "image": image_base64}


def load_image_chain() -> RunnableLambda:
    """Create a chain that loads an image and encodes it in base64 format."""
    return RunnableLambda(load_image)


def get_prompt_from_template(template_name:str) -> str:
    """Load a prompt template from a file."""
    base_path = Path(__file__).parent / "prompts"
    full_path = base_path / template_name
    if not full_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {full_path}")
    return Template(full_path.read_text())