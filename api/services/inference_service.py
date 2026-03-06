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

    book_info_response = BookInfoResponse(
        title=book_info.get('title', ""),
        authors=book_info.get('authors', []),
        genres=book_info.get('genres', []),
        description=book_info.get('description', "")
    )

    inference_response = engine.check_if_book_fits_preferences(
        book_info, user_info)

    recommendation_response = BookRecommendationResponse(
        fit_with_preferences=inference_response.get('fit_with_preferences', False),
        match_score=inference_response.get('match_score'),
        reason_for_fit=inference_response.get('reason_for_fit')
    )

    return {
        "book_information": book_info_response.model_dump_json(),
        "recommendation": recommendation_response.model_dump_json()
    }
