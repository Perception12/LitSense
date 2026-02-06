import json
import tempfile
from inference_engine.engine import BookInferenceEngine
from inference_engine.data_models import UserInfo
from utils.file_utils import save_temp_image

engine = BookInferenceEngine()

def run_inference(image_file, user_info_json):
    image_path = save_temp_image(image_file)
    
    user_info_dict = json.loads(user_info_json)
    user_info = UserInfo(**user_info_dict)
    
    book_info = engine.extract_book_information(image_path)
    
    if book_info.confidence < 0.5:
        raise ValueError("Low confidence in extracted book information.")

    inference_response = engine.check_if_book_fits_preferences(book_info, user_info)
    
    return {
        "book_information": book_info.dict(),
        "recommendation": inference_response.dict()
    }