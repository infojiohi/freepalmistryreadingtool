from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configure upload folder and allowed extensions (no saving to disk actually)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return "Free Palmistry Reading Tool API is running."

@app.route('/api/read', methods=['POST'])
def read_palm():
    if 'palm_image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['palm_image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed. Use png, jpg, jpeg"}), 400

    filename = secure_filename(file.filename)

    # Here you would process the image file (in memory)
    # For now, just a dummy combined reading result
    result = {
        "palmistry_reading": "You have a strong life line and a balanced heart line. Prosperity awaits.",
        "jyotishshastra_reading": "Your planetary positions suggest success in career and good health.",
        "advice": "Stay positive and maintain good health for a prosperous life."
    }

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
