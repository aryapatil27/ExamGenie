/**
 * ExamGenie - Main JavaScript File
 * Handles file uploads, API communication, UI interactions, and login/logout
 */

// ======================
// Configuration
// ======================
const API_BASE_URL = 'http://localhost:5000';

let selectedFiles = [];
let extractedTexts = [];
let currentPrediction = null;

// DOM Elements
const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const fileList = document.getElementById('fileList');
const uploadBtn = document.getElementById('uploadBtn');
const extractedSection = document.getElementById('extractedSection');
const extractedText = document.getElementById('extractedText');
const predictBtn = document.getElementById('predictBtn');
const predictionSection = document.getElementById('predictionSection');
const predictionContent = document.getElementById('predictionContent');
const downloadBtn = document.getElementById('downloadBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const themeToggle = document.getElementById('themeToggle');

// ======================
// Theme Toggle
// ======================
const body = document.body;
const themeIcon = document.querySelector('.theme-icon');

const currentTheme = localStorage.getItem('theme') || 'light';
body.classList.toggle('dark-mode', currentTheme === 'dark');
themeIcon.textContent = currentTheme === 'dark' ? '☀️' : '🌙';

themeToggle.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    const isDark = body.classList.contains('dark-mode');
    themeIcon.textContent = isDark ? '☀️' : '🌙';
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
});

// ======================
// User Login Handling
// ======================
function updateHeaderUser() {
    const nav = document.querySelector('.nav');
    const user = JSON.parse(localStorage.getItem('user'));

    if (user) {
        nav.innerHTML = `
            <span class="user-name">👤 ${user.name}</span>
            <button class="btn btn-secondary" id="logoutBtn">Logout</button>
        `;

        document.getElementById('logoutBtn').addEventListener('click', () => {
            localStorage.removeItem('user');
            window.location.reload();
        });
    } else {
        nav.innerHTML = `
            <button id="themeToggle" class="theme-toggle" aria-label="Toggle theme">
                <span class="theme-icon">${body.classList.contains('dark-mode') ? '☀️' : '🌙'}</span>
            </button>
            <button class="btn btn-primary" onclick="window.location.href='login.html'">Login</button>
        `;

        // Re-add theme toggle listener after re-render
        document.getElementById('themeToggle').addEventListener('click', () => {
            body.classList.toggle('dark-mode');
            const isDark = body.classList.contains('dark-mode');
            document.querySelector('.theme-icon').textContent = isDark ? '☀️' : '🌙';
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        });
    }
}

// Call on page load
updateHeaderUser();

// ======================
// File Upload Handling
// ======================
fileInput?.addEventListener('change', (e) => handleFiles(e.target.files));

uploadArea?.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea?.addEventListener('dragleave', () => uploadArea.classList.remove('drag-over'));

uploadArea?.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    handleFiles(e.dataTransfer.files);
});

function handleFiles(files) {
    const validFiles = Array.from(files).filter(file => {
        const ext = file.name.split('.').pop().toLowerCase();
        return ['pdf', 'png', 'jpg', 'jpeg'].includes(ext);
    });

    if (validFiles.length === 0) {
        alert('Please select valid PDF or image files.');
        return;
    }

    selectedFiles = [...selectedFiles, ...validFiles];
    displayFileList();
    uploadBtn.style.display = 'block';
}

function displayFileList() {
    if (!fileList) return;

    fileList.innerHTML = '';
    selectedFiles.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';

        const icon = file.type.includes('pdf') ? '📄' : '🖼️';
        const fileInfo = document.createElement('div');
        fileInfo.className = 'file-info';
        fileInfo.innerHTML = `
            <span class="file-icon">${icon}</span>
            <div class="file-details">
                <h4>${file.name}</h4>
                <span class="file-size">${formatFileSize(file.size)}</span>
            </div>
        `;

        const removeBtn = document.createElement('button');
        removeBtn.className = 'remove-btn';
        removeBtn.textContent = 'Remove';
        removeBtn.onclick = () => removeFile(index);

        fileItem.appendChild(fileInfo);
        fileItem.appendChild(removeBtn);
        fileList.appendChild(fileItem);
    });
}

function removeFile(index) {
    selectedFiles.splice(index, 1);
    displayFileList();
    if (selectedFiles.length === 0 && uploadBtn) uploadBtn.style.display = 'none';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// ======================
// Upload and Extract Text
// ======================
uploadBtn?.addEventListener('click', async () => {
    if (selectedFiles.length === 0) {
        alert('Please select files first.');
        return;
    }

    loadingSpinner.style.display = 'block';
    uploadBtn.disabled = true;

    try {
        const formData = new FormData();
        selectedFiles.forEach(file => formData.append('files[]', file));

        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData,
            mode: 'cors'
        });

        const data = await response.json();

        if (data.success) {
            extractedTexts = data.data.map(item => item.text);
            displayExtractedText(data.data);
            extractedSection.style.display = 'block';
            extractedSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            alert('Error: ' + (data.error || 'Failed to process files'));
        }
    } catch (error) {
        console.error('Upload error:', error);
        alert('Error connecting to server. Make sure the Flask backend is running on http://localhost:5000');
    } finally {
        loadingSpinner.style.display = 'none';
        uploadBtn.disabled = false;
    }
});

function displayExtractedText(data) {
    if (!extractedText) return;
    extractedText.innerHTML = '';
    data.forEach((item, index) => {
        const textBlock = document.createElement('div');
        textBlock.className = 'text-block';
        textBlock.innerHTML = `
            <h4>📄 ${item.filename}</h4>
            <p>${item.text.substring(0, 500)}${item.text.length > 500 ? '...' : ''}</p>
        `;
        extractedText.appendChild(textBlock);
    });
}

// ======================
// Predict Future Paper
// ======================
predictBtn?.addEventListener('click', async () => {
    if (extractedTexts.length === 0) {
        alert('No extracted text available.');
        return;
    }

    loadingSpinner.style.display = 'block';
    predictBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ texts: extractedTexts }),
            mode: 'cors'
        });

        const data = await response.json();

        if (data.success) {
            currentPrediction = data;
            displayPrediction(data.predicted_paper);
            predictionSection.style.display = 'block';
            predictionSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            alert('Error: ' + (data.error || 'Failed to generate prediction'));
        }
    } catch (error) {
        console.error('Prediction error:', error);
        alert('Error connecting to server. Make sure the Flask backend is running.');
    } finally {
        loadingSpinner.style.display = 'none';
        predictBtn.disabled = false;
    }
});

function displayPrediction(prediction) {
    if (!predictionContent) return;
    predictionContent.innerHTML = '';

    const summary = document.createElement('div');
    summary.className = 'prediction-summary';
    summary.innerHTML = `
        <h4>📊 Analysis Summary</h4>
        <p><strong>Papers Analyzed:</strong> ${prediction.total_papers_analyzed}</p>
        <p><strong>Questions Found:</strong> ${prediction.total_questions_found}</p>
        <p><strong>Generated:</strong> ${prediction.generated_date}</p>

        <h4 style="margin-top: 1rem;">🎯 Most Frequent Topics</h4>
        <ul class="topic-list">
            ${prediction.top_topics.slice(0, 5).map(([topic, freq]) => `
                <li class="topic-item">
                    <span>${topic.charAt(0).toUpperCase() + topic.slice(1)}</span>
                    <span style="font-weight:bold;color:var(--primary-color);">${freq}x</span>
                </li>`).join('')}
        </ul>
    `;
    predictionContent.appendChild(summary);

    prediction.predicted_questions.forEach(section => {
        const sectionDiv = document.createElement('div');
        sectionDiv.className = 'question-section';
        const sectionTitle = document.createElement('h3');
        sectionTitle.textContent = section.section;
        sectionDiv.appendChild(sectionTitle);

        section.questions.forEach(question => {
            const questionDiv = document.createElement('div');
            questionDiv.className = 'question-item';
            questionDiv.textContent = question;
            sectionDiv.appendChild(questionDiv);
        });

        predictionContent.appendChild(sectionDiv);
    });
}

// ======================
// Download PDF
// ======================
downloadBtn?.addEventListener('click', () => {
    if (!currentPrediction || !currentPrediction.pdf_path) {
        alert('No prediction available to download.');
        return;
    }
    const downloadUrl = `${API_BASE_URL}/download/${currentPrediction.pdf_path}`;
    window.open(downloadUrl, '_blank');
});

// ======================
// Smooth Scroll for Links
// ======================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) target.scrollIntoView({ behavior: 'smooth' });
    });
});
