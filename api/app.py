import json
from flask import Flask, request, jsonify
from routes.inference import inference_bp


app = Flask(__name__)

app.register_blueprint(inference_bp, url_prefix='/inference')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
    