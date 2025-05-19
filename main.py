from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid
from fpdf import FPDF

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/read', methods=['POST'])
def read_palm():
    left_hand = request.files.get('left_hand')
    right_hand = request.files.get('right_hand')
    language = request.form.get('language', 'en')

    if not left_hand or not right_hand:
        return jsonify({'error': 'Both hand images are required'}), 400

    # Save files temporarily
    left_filename = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{secure_filename(left_hand.filename)}")
    right_filename = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{secure_filename(right_hand.filename)}")
    left_hand.save(left_filename)
    right_hand.save(right_filename)

    # Simulate palmistry reading
    reading = generate_reading(language)

    # Generate PDF
    pdf_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_reading.pdf")
    create_pdf(reading, pdf_path)

    # Clean up images
    os.remove(left_filename)
    os.remove(right_filename)

    return jsonify({
        'reading': reading,
        'pdf_url': f"/api/download/{os.path.basename(pdf_path)}"
    })


@app.route('/api/download/<filename>')
def download_pdf(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'}), 404


def generate_reading(language):
    # This would be replaced with AI/jyotish logic
    if language == 'hi':
        return "आपकी हथेली बताती है कि आपके जीवन में ऊर्जा और साहस भरा हुआ है।"
    else:
        return "Your palm shows signs of energy, determination, and a successful future."

def create_pdf(text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.multi_cell(0, 10, text)
    pdf.output(filename)

if __name__ == '__main__':
    app.run(debug=True)
