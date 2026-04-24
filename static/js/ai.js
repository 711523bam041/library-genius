// AI Assistant handlers

document.addEventListener('DOMContentLoaded', function() {
    const generateSummaryBtn = document.getElementById('generateSummaryBtn');
    const suggestGenresBtn = document.getElementById('suggestGenresBtn');
    
    if (generateSummaryBtn) {
        generateSummaryBtn.addEventListener('click', generateSummary);
    }
    
    if (suggestGenresBtn) {
        suggestGenresBtn.addEventListener('click', suggestGenres);
    }
});

async function generateSummary() {
    const title = document.getElementById('title').value;
    const author = document.getElementById('author').value;
    const description = ''; // Could add a description field if needed
    
    if (!title || !author) {
        showAlert('Please enter title and author first', 'warning');
        return;
    }
    
    const resultDiv = document.getElementById('aiResult');
    resultDiv.innerHTML = '<div class="text-center"><div class="spinner-border text-success" role="status"></div><p class="mt-2">Generating summary...</p></div>';
    
    try {
        const response = await fetch('/api/ai/generate-summary', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, author, description })
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultDiv.innerHTML = `
                <div class="alert alert-info">
                    <h6 class="fw-bold"><i class="fas fa-robot me-2"></i>AI Summary:</h6>
                    <p class="mb-0">${data.summary}</p>
                </div>
            `;
        } else {
            resultDiv.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-circle me-2"></i>
                    ${data.message || 'Error generating summary'}
                </div>
            `;
        }
    } catch (error) {
        console.error('Error generating summary:', error);
        resultDiv.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-circle me-2"></i>
                Error generating summary
            </div>
        `;
    }
}

async function suggestGenres() {
    const title = document.getElementById('title').value;
    const author = document.getElementById('author').value;
    const description = '';
    
    if (!title || !author) {
        showAlert('Please enter title and author first', 'warning');
        return;
    }
    
    const resultDiv = document.getElementById('aiResult');
    resultDiv.innerHTML = '<div class="text-center"><div class="spinner-border text-info" role="status"></div><p class="mt-2">Suggesting genres...</p></div>';
    
    try {
        const response = await fetch('/api/ai/suggest-genres', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, author, description })
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultDiv.innerHTML = `
                <div class="alert alert-info">
                    <h6 class="fw-bold"><i class="fas fa-tags me-2"></i>Suggested Genres:</h6>
                    <p class="mb-0">${data.genres}</p>
                </div>
            `;
            
            // Auto-fill category if empty
            const categoryInput = document.getElementById('category');
            if (categoryInput && !categoryInput.value) {
                categoryInput.value = data.genres.split(',')[0].trim();
            }
        } else {
            resultDiv.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-circle me-2"></i>
                    ${data.message || 'Error suggesting genres'}
                </div>
            `;
        }
    } catch (error) {
        console.error('Error suggesting genres:', error);
        resultDiv.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-circle me-2"></i>
                Error suggesting genres
            </div>
        `;
    }
}
