// ISBN Scanner handlers

document.addEventListener('DOMContentLoaded', function() {
    const scanBtn = document.getElementById('scanIsbnBtn');
    const fileInput = document.getElementById('isbnFileInput');
    const scannerArea = document.getElementById('scannerArea');
    
    if (scanBtn && fileInput) {
        // Click to upload
        scanBtn.addEventListener('click', function() {
            fileInput.click();
        });
        
        // Drag and drop
        if (scannerArea) {
            scannerArea.addEventListener('click', function() {
                fileInput.click();
            });
            
            scannerArea.addEventListener('dragover', function(e) {
                e.preventDefault();
                scannerArea.style.borderColor = '#0d6efd';
                scannerArea.style.backgroundColor = '#e7f1ff';
            });
            
            scannerArea.addEventListener('dragleave', function(e) {
                e.preventDefault();
                scannerArea.style.borderColor = '#dee2e6';
                scannerArea.style.backgroundColor = '#f8f9fa';
            });
            
            scannerArea.addEventListener('drop', function(e) {
                e.preventDefault();
                scannerArea.style.borderColor = '#dee2e6';
                scannerArea.style.backgroundColor = '#f8f9fa';
                
                if (e.dataTransfer.files.length > 0) {
                    handleFileUpload(e.dataTransfer.files[0]);
                }
            });
        }
        
        // File input change
        fileInput.addEventListener('change', function(e) {
            if (e.target.files.length > 0) {
                handleFileUpload(e.target.files[0]);
            }
        });
    }
});

async function handleFileUpload(file) {
    if (!file.type.startsWith('image/')) {
        showAlert('Please upload an image file', 'warning');
        return;
    }
    
    const resultDiv = document.getElementById('scanResult');
    resultDiv.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"></div><p class="mt-2">Scanning barcode...</p></div>';
    
    const formData = new FormData();
    formData.append('image', file);
    
    try {
        const response = await fetch('/api/scan-isbn', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultDiv.innerHTML = `
                <div class="alert alert-success">
                    <i class="fas fa-check-circle me-2"></i>
                    <strong>ISBN Detected:</strong> ${data.isbn}
                </div>
            `;
            
            // Fill ISBN in form
            const isbnInput = document.getElementById('isbn');
            if (isbnInput) {
                isbnInput.value = data.isbn;
            }
            
            // Auto-fetch book details
            setTimeout(() => {
                document.getElementById('fetchBookBtn').click();
            }, 500);
        } else {
            resultDiv.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-circle me-2"></i>
                    ${data.message || 'No barcode detected'}
                </div>
            `;
        }
    } catch (error) {
        console.error('Error scanning ISBN:', error);
        resultDiv.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-circle me-2"></i>
                Error scanning barcode
            </div>
        `;
    }
}
