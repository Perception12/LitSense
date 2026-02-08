import json
from inference_engine.engine import BookInferenceEngine
from inference_engine.data_models import UserInfo
from api.utils.file_utils import save_temp_image
from api.schemas.responses import BookInfoResponse, BookRecommendationResponse

engine = BookInferenceEngine()

def run_inference(image_file, user_info_json):
    image_path = save_temp_image(image_file)
    
    user_info_dict = json.loads(user_info_json)
    user_info = UserInfo(**user_info_dict)
    
    book_info = engine.extract_book_information(image_path)
    
    if book_info['confidence'] < 0.5:
        raise ValueError("Low confidence in extracted book information.")

    inference_response = engine.check_if_book_fits_preferences(book_info, user_info)
    
    book_info_response = BookInfoResponse(
        title=book_info['title'],
        authors=book_info['authors'],
        genre=book_info['genre'],
    )
    
    recommendation_response = BookRecommendationResponse(
        fit_with_preferences=inference_response['fit_with_preferences'],
        match_score=inference_response['match_score'],
        reason_for_fit=inference_response['reason_for_fit']
    )
    
    return {
        "book_information": book_info_response.model_dump_json(),
        "recommendation": recommendation_response.model_dump_json()
    }