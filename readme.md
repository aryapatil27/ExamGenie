🧞 ExamGenie - AI-Powered Exam Paper Predictor
ExamGenie is a full-stack web application that helps college students predict future exam papers by analyzing previous question papers using AI and pattern recognition.

✨ Features
Multiple File Upload: Upload multiple PDFs and images simultaneously
Text Extraction: Extracts text from PDFs and images using OCR
AI Prediction: Analyzes patterns and predicts future exam questions
Dark/Light Mode: Toggle between themes for comfortable viewing
Fully Responsive: Works seamlessly on desktop, tablet, and mobile
PDF Export: Download predicted papers as PDF files
Modern UI: Beautiful, gradient-based design with flip card animations
📁 Project Structure
project_root/
├── backend/
│   ├── app.py                 # Flask main application
│   ├── modules/
│   │   ├── extractor.py       # Text extraction (PDF/Image)
│   │   └── predictor.py       # Prediction algorithm
│   ├── requirements.txt       # Python dependencies
│   ├── uploads/               # Temporary file storage (auto-created)
│   └── outputs/               # Generated PDFs (auto-created)
├── frontend/
│   ├── index.html            # Main page
│   ├── login.html            # Login page
│   ├── css/
│   │   ├── style.css         # Main stylesheet
│   │   └── dark.css          # Dark mode styles
│   └── js/
│       └── main.js           # Frontend logic
└── README.md                 # This file
🚀 Installation & Setup
Prerequisites
Python 3.8 or higher
pip (Python package manager)
Tesseract OCR (for image text extraction)
Step 1: Install Tesseract OCR
Windows:

Download from: https://github.com/UB-Mannheim/tesseract/wiki
Install and add to PATH
Linux (Ubuntu/Debian):

bash
sudo apt-get update
sudo apt-get install tesseract-ocr
macOS:

bash
brew install tesseract
Step 2: Clone/Download the Project
Download all the files and organize them according to the folder structure above.

Step 3: Install Python Dependencies
Navigate to the backend folder and install requirements:

bash
cd backend
pip install -r requirements.txt
Step 4: Create Required Folders
The application will auto-create these, but you can create them manually:

bash
# In backend folder
mkdir uploads outputs
mkdir modules
Step 5: Run the Backend
From the backend folder:

bash
python app.py
The Flask server will start on http://localhost:5000

Step 6: Run the Frontend
Navigate to the frontend folder
Open index.html in your web browser
OR use a simple HTTP server:

bash
# Python 3
python -m http.server 8000

# Then visit: http://localhost:8000
📖 Usage Guide
1. Upload Papers
Click "Choose Files" or drag & drop PDF/image files
Multiple files can be uploaded at once
Supported formats: PDF, PNG, JPG, JPEG
2. Extract Text
Click "Upload & Extract Text" button
Wait for processing (loading spinner will appear)
Extracted text will be displayed on the page
3. Generate Prediction
Click "🔮 Predict Future Paper" button
AI will analyze patterns and generate predictions
View predicted questions organized by sections
4. Download PDF
Click "📥 Download as PDF" to save the predicted paper
PDF includes analysis summary and all predicted questions
5. Login (Optional)
Click "Login" button in header
Use any email/password (basic implementation)
Demonstrates authentication flow
🎨 Features in Detail
Prediction Algorithm
The prediction algorithm analyzes:

Topic Frequency: Identifies most repeated topics/keywords
Question Patterns: Recognizes common question formats
Trend Analysis: Predicts high-probability topics
Question Generation: Creates new questions based on patterns
Dark Mode
Click the moon/sun icon in the header
Preference is saved in browser localStorage
Smooth transition between themes
Responsive Design
Mobile-first approach
Breakpoints: 480px, 768px, 1200px
Touch-friendly interface
🔧 Configuration
Backend API URL
To change the API URL, edit frontend/js/main.js:

javascript
const API_BASE_URL = 'http://localhost:5000';
File Upload Limits
To change file size limits, edit backend/app.py:

python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
🐛 Troubleshooting
Issue: "Error connecting to server"
Solution: Make sure Flask backend is running on port 5000

Issue: "Tesseract not found"
Solution: Install Tesseract OCR and ensure it's in system PATH

Issue: CORS errors
Solution: Flask-CORS is installed and configured. Check if backend is running.

Issue: PDF extraction returns no text
Solution: Ensure PDF contains selectable text (not scanned images)

Issue: Image extraction fails
Solution: Verify Tesseract installation and image quality

🎯 API Endpoints
GET /
Home endpoint - Returns API status

POST /upload
Upload and extract text from files

Body: FormData with files[]
Returns: Extracted text data
POST /predict
Generate predicted exam paper

Body: JSON with texts array
Returns: Predicted questions and PDF path
GET /download/<filename>
Download generated PDF

Params: filename
Returns: PDF file
POST /login
Basic login authentication

Body: JSON with email and password
Returns: User data
📚 Technologies Used
Backend
Flask - Web framework
PyPDF2 - PDF text extraction
Pytesseract - OCR for images
FPDF - PDF generation
Flask-CORS - Cross-origin support
Frontend
HTML5 - Structure
CSS3 - Styling (Flexbox, Grid, Animations)
Vanilla JavaScript - Logic and API calls
Modern ES6+ syntax
🔐 Security Notes
Current login is basic (frontend only)
For production: Implement proper authentication (JWT, OAuth)
Add server-side validation
Use HTTPS
Implement rate limiting
Sanitize file uploads
🚀 Future Enhancements
 User accounts and history
 Machine learning model integration
 Subject-specific predictions
 Collaborative filtering
 Question difficulty analysis
 Study schedule generator
 Mobile app version
📝 License
This project is created for educational purposes. Feel free to modify and use as needed.

👨‍💻 Developer Notes
Code Structure
Modular design: Separate concerns (extraction, prediction, routing)
Error handling: Try-catch blocks throughout
Comments: Inline documentation for clarity
Responsive: Mobile-first CSS approach
Best Practices
Clean, readable code
Consistent naming conventions
Proper file organization
Minimal dependencies
🤝 Contributing
Feel free to fork, modify, and submit pull requests. This is an educational project meant to help students.

📞 Support
For issues or questions:

Check troubleshooting section
Ensure all dependencies are installed
Verify backend is running on port 5000
Check browser console for errors
Made with ❤️ for students everywhere. Good luck with your exams! 🎓

