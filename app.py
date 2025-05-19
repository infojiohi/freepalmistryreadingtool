from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'temp_uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Sample palmistry + jyotish responses (mocked)
readings = [
    "You have a strong life line, indicating good health and energy.\nYour heart line suggests emotional sensitivity and deep love.",
    "Your palm shows a great career path ahead with creative strengths.\nJyotish analysis reveals a strong Mars influence — leadership qualities are high.",
    "You may face minor financial struggles in the near term, but Jupiter's position shows long-term success.",
    "A long fate line indicates stability in career.\nSaturn's influence shows growth after age 32.",
    "You are intuitive and have spiritual energy.\nMoon mount is active — imagination and emotional depth are your strengths."
]

@app.route('/api/palmistry', methods=['POST'])
def palmistry():
    if 'palmImage' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files['palmImage']
    filename = secure_filename(image.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(filepath)

    # Simulate processing delay
    print(f"Image received: {filename}, processing...")

    # Select a random reading (for now)
    reading = random.choice(readings)

    # Delete the uploaded file after use
    os.remove(filepath)

    return jsonify({"result": reading})

if __name__ == '__main__':
    app.run(debug=True)
