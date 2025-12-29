"""
ExamGenie - Text Extraction Module
Extracts text from PDF and image files with better OCR handling
"""

import PyPDF2
import pytesseract
from PIL import Image
import pdfplumber
import os

def extract_text_from_pdf(filepath):
    """Extract text from PDF using PyPDF2 and pdfplumber fallback"""
    text = ""
    try:
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
        
        if not text.strip():  # fallback to pdfplumber
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
        
        return text.strip() or "No text could be extracted from this PDF."
    
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"

def extract_text_from_image(filepath):
    """Extract text from image using pytesseract OCR"""
    try:
        image = Image.open(filepath)
        text = pytesseract.image_to_string(image)
        return text.strip() or "No text could be extracted from this image."
    
    except Exception as e:
        if "tesseract" in str(e).lower():
            return ("Tesseract OCR is not installed. Please install it:\n"
                    "Windows: https://github.com/UB-Mannheim/tesseract/wiki\n"
                    "Linux: sudo apt-get install tesseract-ocr\n"
                    "Mac: brew install tesseract")
        return f"Error extracting text from image: {str(e)}"
