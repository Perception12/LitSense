import base64
from langchain.chains import TransformChain
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

    return {"image_base64": image_base64}


def load_image_chain() -> TransformChain:
    """Create a TransformChain that loads and encodes an image."""
    
    return TransformChain(
        input_variables=["image_path"],
        output_variables=["image_base64"],
        transform=load_image
    )


def get_prompt_from_template(template_path:str) -> str:
    """Load a prompt template from a file."""
    path = Path(template_path)
    content = path.read_text()
    return Template(content).render()