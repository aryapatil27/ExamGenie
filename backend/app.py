"""
ExamGenie - Flask Backend Application
Main application file that initializes Flask, serves frontend, and registers routes
"""

import os
import sys
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

# ------------------ Paths ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))        # backend/
PROJECT_ROOT = os.path.dirname(BASE_DIR)                     # EXAMGENIE/
FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend')        # frontend folder
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')            # backend/uploads
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')           # backend/outputs
DB_PATH = os.path.join(BASE_DIR, 'users.db')                # SQLite DB

# Add modules to path
sys.path.append(os.path.join(BASE_DIR, 'modules'))

# ------------------ Import Modules ------------------
from extractor import extract_text_from_pdf, extract_text_from_image
from predictor import PaperPredictor

# ------------------ Flask App ------------------
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)

# ------------------ Config ------------------
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create folders if not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Initialize predictor
predictor = PaperPredictor()

# ------------------ Database Setup ------------------
def init_db():
    """Create users table if not exists"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ------------------ Helper ------------------
def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ------------------ Frontend Routes ------------------
@app.route('/')
def serve_index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)

# ------------------ API Endpoints ------------------
@app.route('/register', methods=['POST'])
def register():
    """Handle user registration"""
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not all([username, email, password]):
            return jsonify({'error': 'All fields are required'}), 400

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            return jsonify({'error': 'Email already registered'}), 400

        cursor.execute(
            "INSERT INTO users (username, email, password, created_at) VALUES (?, ?, ?, ?)",
            (username, email, hashed_password, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Registration successful'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    """Handle user login"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not all([email, password]):
            return jsonify({'error': 'Email and password required'}), 400

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, password FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {'id': user[0], 'name': user[1], 'email': user[2]}
            })
        else:
            return jsonify({'error': 'Invalid email or password'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file uploads and extract text"""
    try:
        if 'files[]' not in request.files:
            return jsonify({'error': 'No files provided'}), 400

        files = request.files.getlist('files[]')
        extracted_texts = []

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_filename = f"{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)

                ext = filename.rsplit('.', 1)[1].lower()
                if ext == 'pdf':
                    text = extract_text_from_pdf(filepath)
                else:
                    text = extract_text_from_image(filepath)

                extracted_texts.append({
                    'filename': filename,
                    'text': text,
                    'filepath': filepath
                })

        return jsonify({
            'success': True,
            'message': f'{len(extracted_texts)} file(s) processed successfully',
            'data': extracted_texts
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict_paper():
    """Generate predicted exam paper"""
    try:
        data = request.json
        texts = data.get('texts', [])

        if not texts:
            return jsonify({'error': 'No texts provided'}), 400

        predicted_paper = predictor.predict_future_paper(texts)
        pdf_path = predictor.generate_pdf(predicted_paper)

        return jsonify({
            'success': True,
            'predicted_paper': predicted_paper,
            'pdf_path': os.path.basename(pdf_path)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download predicted paper PDF"""
    try:
        filepath = os.path.join(OUTPUT_FOLDER, filename)
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

# ------------------ Run App ------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
