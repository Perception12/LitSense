import json
from flask import Flask, request, jsonify



app = Flask(__name__)


@app.route('/inference', methods=['POST'])
def get_inference_on_image():
    data = json.loads(request.data)
    image_file = data.get('image')
    if not image_file:
        return jsonify({'error': 'No image file provided'}), 400
    



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
    