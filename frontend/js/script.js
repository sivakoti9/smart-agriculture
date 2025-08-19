// API Configuration
const API_BASE_URL = 'http://localhost:5000';

// DOM Elements
const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('.section');
const loadingSpinner = document.getElementById('loadingSpinner');

// Navigation functionality
navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        
        // Remove active class from all links and sections
        navLinks.forEach(l => l.classList.remove('active'));
        sections.forEach(s => s.classList.remove('active'));
        
        // Add active class to clicked link
        link.classList.add('active');
        
        // Show corresponding section
        const targetSection = document.getElementById(link.getAttribute('href').substring(1));
        if (targetSection) {
            targetSection.classList.add('active');
        }
    });
});

// Yield Prediction Form
const yieldForm = document.getElementById('yieldForm');
const yieldResults = document.getElementById('yieldResults');
const yieldOutput = document.getElementById('yieldOutput');

yieldForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(yieldForm);
    const data = Object.fromEntries(formData.entries());
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/predict_yield`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayYieldResults(result);
        } else {
            showError('Error predicting yield: ' + result.error);
        }
    } catch (error) {
        showError('Connection error. Please check if the server is running.');
    }
    
    hideLoading();
});

function displayYieldResults(result) {
    yieldOutput.innerHTML = `
        <div class="result-item">
            <h4><i class="fas fa-chart-bar"></i> Predicted Yield</h4>
            <p class="yield-value">${result.predicted_yield.toFixed(2)} ${result.unit}</p>
        </div>
        <div class="result-item">
            <h4><i class="fas fa-lightbulb"></i> Recommendations</h4>
            <ul class="recommendation-list">
                ${result.recommendations.map(rec => `<li><i class="fas fa-arrow-right"></i> ${rec}</li>`).join('')}
            </ul>
        </div>
    `;
    
    yieldResults.style.display = 'block';
}

// Disease Detection
const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');
const imagePreview = document.getElementById('imagePreview');
const previewImg = document.getElementById('previewImg');
const analyzeBtn = document.getElementById('analyzeBtn');
const diseaseResults = document.getElementById('diseaseResults');
const diseaseOutput = document.getElementById('diseaseOutput');

uploadArea.addEventListener('click', () => {
    imageInput.click();
});

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.background = 'rgba(102, 126, 234, 0.15)';
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.background = 'rgba(102, 126, 234, 0.05)';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.background = 'rgba(102, 126, 234, 0.05)';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleImageUpload(files[0]);
    }
});

imageInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleImageUpload(e.target.files[0]);
    }
});

function handleImageUpload(file) {
    if (!file.type.startsWith('image/')) {
        showError('Please select an image file');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImg.src = e.target.result;
        imagePreview.style.display = 'block';
        uploadArea.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

analyzeBtn.addEventListener('click', async () => {
    const file = imageInput.files[0];
    if (!file) {
        showError('Please select an image first');
        return;
    }
    
    const formData = new FormData();
    formData.append('image', file);
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/detect_disease`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayDiseaseResults(result);
        } else {
            showError('Error detecting disease: ' + result.error);
        }
    } catch (error) {
        showError('Connection error. Please check if the server is running.');
    }
    
    hideLoading();
});

function displayDiseaseResults(result) {
    let medicineHtml = '';
    if (result.medicine_suggestions.medicines && result.medicine_suggestions.medicines.length > 0) {
        medicineHtml = `
            <div class="medicines">
                <h5><i class="fas fa-pills"></i> Recommended Medicines</h5>
                ${result.medicine_suggestions.medicines.map(med => `
                    <div class="medicine-item">
                        <strong>${med.name}</strong>
                        <p>Dosage: ${med.dosage}</p>
                        <p>Application: ${med.application}</p>
                        <p class="precaution">⚠️ ${med.precautions}</p>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    let organicHtml = '';
    if (result.medicine_suggestions.organic_alternatives && result.medicine_suggestions.organic_alternatives.length > 0) {
        organicHtml = `
            <div class="organic-alternatives">
                <h5><i class="fas fa-leaf"></i> Organic Alternatives</h5>
                <ul class="recommendation-list">
                    ${result.medicine_suggestions.organic_alternatives.map(alt => `<li>${alt}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    diseaseOutput.innerHTML = `
        <div class="result-item">
            <h4><i class="fas fa-microscope"></i> Disease Detection Results</h4>
            <p><strong>Detected Disease:</strong> ${result.disease.replace('_', ' ').toUpperCase()}</p>
            <p><strong>Confidence:</strong> ${(result.confidence * 100).toFixed(1)}%</p>
            <div class="confidence-bar">
                <div class="confidence-fill" style="width: ${result.confidence * 100}%"></div>
            </div>
        </div>
        
        ${medicineHtml}
        ${organicHtml}
        
        <div class="result-item">
            <h4><i class="fas fa-first-aid"></i> Treatment Tips</h4>
            <ul class="recommendation-list">
                ${result.treatment_tips.map(tip => `<li>${tip}</li>`).join('')}
            </ul>
        </div>
    `;
    
    diseaseResults.style.display = 'block';
}

// Recommendations Form
const recommendationForm = document.getElementById('recommendationForm');
const recommendationResults = document.getElementById('recommendationResults');
const recommendationOutput = document.getElementById('recommendationOutput');

recommendationForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(recommendationForm);
    const data = Object.fromEntries(formData.entries());
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/get_recommendations`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayRecommendations(result.recommendations);
        } else {
            showError('Error getting recommendations: ' + result.error);
        }
    } catch (error) {
        showError('Connection error. Please check if the server is running.');
    }
    
    hideLoading();
});

function displayRecommendations(recommendations) {
    let html = '';
    
    Object.entries(recommendations).forEach(([category, items]) => {
        if (Array.isArray(items) && items.length > 0) {
            html += `
                <div class="result-item">
                    <h4><i class="fas fa-list"></i> ${category.replace('_', ' ').toUpperCase()}</h4>
                    <ul class="recommendation-list">
                        ${items.map(item => `<li>${item}</li>`).join('')}
                    </ul>
                </div>
            `;
        }
    });
    
    recommendationOutput.innerHTML = html;
    recommendationResults.style.display = 'block';
}

// Utility Functions
function showLoading() {
    loadingSpinner.style.display = 'flex';
}

function hideLoading() {
    loadingSpinner.style.display = 'none';
}

function showError(message) {
    alert('Error: ' + message);
}

// Reset image upload when switching sections
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        if (link.getAttribute('href') !== '#disease') {
            uploadArea.style.display = 'block';
            imagePreview.style.display = 'none';
            diseaseResults.style.display = 'none';
            imageInput.value = '';
        }
    });
});