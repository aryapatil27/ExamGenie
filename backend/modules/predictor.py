"""
ExamGenie - Paper Prediction Module
Predicts future exam questions using previous papers.
"""

import re
from collections import Counter
from datetime import datetime
from fpdf import FPDF
import os
import random

class PaperPredictor:
    """Class to predict future exam papers based on previous papers"""
    
    def __init__(self):
        self.question_patterns = [
            r'Q\d+[.\):]',       # Q1. Q2) Q3:
            r'\d+[.\):]',        # 1. 2) 3:
            r'Question\s+\d+',   # Question 1
        ]
    
    def extract_questions(self, text):
        """Extract individual questions from text more reliably"""
        questions = []
        for pattern in self.question_patterns:
            splits = re.split(pattern, text, flags=re.IGNORECASE)
            for q in splits[1:]:
                sub_qs = [s.strip() for s in q.split('\n') if len(s.strip()) > 5]
                questions.extend(sub_qs)
        if not questions:
            questions = [q.strip() for q in text.split('\n\n') if len(q.strip()) > 5]
        return questions
    
    def extract_topics(self, text):
        """Extract meaningful topics/keywords from questions"""
        cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
        words = cleaned_text.split()
        
        # Stop words + generic verbs often used in questions
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'what', 'which', 'who', 'when', 'where', 'why', 'how', 'question',
            'their', 'explain', 'describe', 'concept', 'provide', 'discuss',
            'compare', 'contrast', 'relate', 'show', 'analyze', 'demonstrate',
            'apply', 'address', 'give', 'list', 'application', 'case', 'study'
        }

        # Only take words longer than 3 letters and not in stop words
        keywords = [w for w in words if len(w) > 3 and w not in stop_words]
        
        # Return unique keywords
        return list(set(keywords))
    
    def predict_future_paper(self, texts):
        """
        Predict future exam paper based on previous papers.
        Args:
            texts: List of extracted texts from previous papers
        Returns:
            Dictionary containing predicted paper details
        """
        all_questions = []
        all_keywords = []
        
        for text in texts:
            questions = self.extract_questions(text)
            all_questions.extend(questions)
            
            keywords = self.extract_topics(text)
            all_keywords.extend(keywords)
        
        keyword_freq = Counter(all_keywords)
        top_topics = keyword_freq.most_common(10)
        
        predicted_questions = self.generate_predicted_questions(all_questions, top_topics)
        
        return {
            'total_papers_analyzed': len(texts),
            'total_questions_found': len(all_questions),
            'top_topics': top_topics,
            'predicted_questions': predicted_questions,
            'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def generate_predicted_questions(self, all_questions, top_topics):
        """
        Generate predicted questions based on analysis
        Args:
            all_questions: List of actual questions from previous papers
            top_topics: List of top topics (word frequency)
        Returns:
            List of sections with questions
        """
        predictions = []

        # SECTION A - Top 5 actual questions (high probability)
        predictions.append({
            'section': 'Section A - High Probability Questions',
            'questions': []
        })
        question_freq = Counter(all_questions)
        top_questions = [q for q, _ in question_freq.most_common(5)]
        for i, question in enumerate(top_questions, 1):
            predictions[0]['questions'].append(f"Q{i}. {question}")

        # SECTION B - Realistic Analytical / Comparison Questions
        predictions.append({
            'section': 'Section B - Analytical & Comparison Questions',
            'questions': []
        })
        if len(top_topics) >= 4:
            b_questions = [
                f"Q6. How would you integrate {top_topics[0][0]} with {top_topics[1][0]} in a practical scenario?",
                f"Q7. Compare the effects of {top_topics[2][0]} and {top_topics[3][0]} in system performance.",
                f"Q8. Propose a method to optimize {top_topics[0][0]} using principles of {top_topics[2][0]}."
            ]
            predictions[1]['questions'].extend(b_questions)

        # SECTION C - Realistic Application Questions
        predictions.append({
            'section': 'Section C - Application-Based Questions',
            'questions': []
        })
        generic_words = {'their', 'explain', 'describe', 'concept', 'provide', 
                         'discuss', 'compare', 'contrast', 'address', 'application', 'case', 'study'}
        valid_topics = [t for t, _ in top_topics if t not in generic_words]
        c_questions = []
        for i, topic in enumerate(valid_topics[:4], 9):
            question_templates = [
                f"Q{i}. Design a scenario where {topic} can solve a real-world problem.",
                f"Q{i}. Explain how {topic} can be applied in a practical project or experiment.",
                f"Q{i}. Discuss a real-life example where {topic} is used effectively."
            ]
            c_questions.append(random.choice(question_templates))
        predictions[2]['questions'].extend(c_questions)

        return predictions

    def generate_pdf(self, prediction_data):
        """Generate PDF of predicted paper"""
        if not os.path.exists('outputs'):
            os.makedirs('outputs')

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        
        # Title
        pdf.cell(0, 10, 'ExamGenie - Predicted Exam Paper', 0, 1, 'C')
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 10, f"Generated on: {prediction_data['generated_date']}", 0, 1, 'C')
        pdf.ln(5)
        
        # Analysis Summary
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Analysis Summary:', 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 6, f"Papers Analyzed: {prediction_data['total_papers_analyzed']}", 0, 1)
        pdf.cell(0, 6, f"Questions Found: {prediction_data['total_questions_found']}", 0, 1)
        pdf.ln(5)
        
        # Top Topics
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Most Frequent Topics:', 0, 1)
        pdf.set_font('Arial', '', 10)
        for topic, freq in prediction_data['top_topics']:
            pdf.cell(0, 6, f"- {topic.capitalize()} (frequency: {freq})", 0, 1)
        pdf.ln(5)
        
        # Predicted Questions
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Predicted Exam Questions:', 0, 1)
        pdf.ln(3)
        
        for section_data in prediction_data['predicted_questions']:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, section_data['section'], 0, 1)
            pdf.set_font('Arial', '', 10)
            
            for question in section_data['questions']:
                pdf.multi_cell(0, 6, question)
                pdf.ln(2)
            
            pdf.ln(3)
        
        # Save PDF
        filename = f"predicted_paper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join('outputs', filename)
        pdf.output(filepath)
        
        return filename
