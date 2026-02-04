from flask import Blueprint, request, jsonify
from services.inference_service import run_inference

inference_bp = Blueprint('inference', __name__)

@inference_bp.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({"error": "Missing image file"}), 400
    
    
    try:
        user_info_json = request.form.get('user_info')
        if not user_info_json:
            return jsonify({"error": "Missing user info"}), 400
        
        result = run_inference(request.files['image'], user_info_json)
        
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({"INFERENCE ERROR": str(e)}), 400
    
    except Exception as e:
        return jsonify({"error": "INTERNAL SERVER ERROR"}), 500
    
    