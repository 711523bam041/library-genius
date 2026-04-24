// Book management handlers

// Load books on page load
let currentPage = 1;
const booksPerPage = 20;

document.addEventListener('DOMContentLoaded', function() {
    // Check which page we're on and load appropriate data
    if (document.getElementById('booksTableBody')) {
        loadBooks(currentPage);
    }
    
    // Search handler
    const searchBtn = document.getElementById('searchBtn');
    if (searchBtn) {
        searchBtn.addEventListener('click', searchBooks);
    }
    
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchBooks();
            }
        });
    }
    
    // Add book form handler
    const addBookForm = document.getElementById('addBookForm');
    if (addBookForm) {
        addBookForm.addEventListener('submit', addBook);
    }
});

// Load books with pagination
async function loadBooks(page = 1) {
    try {
        const response = await fetch(`/api/books?page=${page}&limit=${booksPerPage}`);
        const data = await response.json();
        
        if (data.success) {
            displayBooks(data.books);
            displayPagination(data.total, page, data.pages);
        } else {
            showAlert('Error loading books', 'danger');
        }
    } catch (error) {
        console.error('Error loading books:', error);
        showAlert('Error loading books', 'danger');
    }
}

// Display books in table
function displayBooks(books) {
    const tbody = document.getElementById('booksTableBody');
    
    if (!books || books.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">No books found</td></tr>';
        return;
    }
    
    tbody.innerHTML = books.map(book => {
        const coverImg = book.cover_image_url 
            ? `<img src="${book.cover_image_url}" alt="Cover" style="width: 50px; height: 75px; object-fit: cover;">`
            : '<div style="width: 50px; height: 75px; background: #e9ecef; display: flex; align-items: center; justify-content: center;"><i class="fas fa-book text-muted"></i></div>';
        
        const isbn = book.isbn_13 || book.isbn_10 || 'N/A';
        
        return `
            <tr>
                <td>${coverImg}</td>
                <td>${book.title}</td>
                <td>${book.author}</td>
                <td>${isbn}</td>
                <td>${book.category || 'N/A'}</td>
                <td><span class="badge bg-success">${book.available_copies}/${book.total_copies}</span></td>
                <td>
                    <button class="btn btn-sm btn-info" onclick="viewBook(${book.book_id})">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

// Display pagination
function displayPagination(total, currentPage, totalPages) {
    const pagination = document.getElementById('pagination');
    if (!pagination) return;
    
    let html = '';
    
    // Previous button
    if (currentPage > 1) {
        html += `<li class="page-item"><a class="page-link" href="#" onclick="loadBooks(${currentPage - 1}); return false;">Previous</a></li>`;
    }
    
    // Page numbers
    for (let i = 1; i <= totalPages; i++) {
        if (i === currentPage) {
            html += `<li class="page-item active"><a class="page-link" href="#">${i}</a></li>`;
        } else if (i === 1 || i === totalPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
            html += `<li class="page-item"><a class="page-link" href="#" onclick="loadBooks(${i}); return false;">${i}</a></li>`;
        } else if (i === currentPage - 3 || i === currentPage + 3) {
            html += `<li class="page-item disabled"><a class="page-link">...</a></li>`;
        }
    }
    
    // Next button
    if (currentPage < totalPages) {
        html += `<li class="page-item"><a class="page-link" href="#" onclick="loadBooks(${currentPage + 1}); return false;">Next</a></li>`;
    }
    
    pagination.innerHTML = html;
}

// Search books
async function searchBooks() {
    const query = document.getElementById('searchInput').value.trim();
    
    if (!query) {
        loadBooks(1);
        return;
    }
    
    try {
        const response = await fetch(`/api/books/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (data.success) {
            displayBooks(data.books);
            document.getElementById('pagination').innerHTML = '';
        } else {
            showAlert('Error searching books', 'danger');
        }
    } catch (error) {
        console.error('Error searching books:', error);
        showAlert('Error searching books', 'danger');
    }
}

// View book details
function viewBook(bookId) {
    // Could implement a modal or navigate to detail page
    showAlert(`Viewing book ${bookId}`, 'info');
}

// Add book form handler
async function addBook(e) {
    if (e) e.preventDefault();
    
    const bookData = {
        title: document.getElementById('title').value,
        author: document.getElementById('author').value,
        isbn: document.getElementById('isbn').value,
        publisher: document.getElementById('publisher').value,
        category: document.getElementById('category').value,
        shelf_location: document.getElementById('shelf_location').value,
        available_copies: parseInt(document.getElementById('copies').value),
        cover_image_url: document.getElementById('cover_image_url').value
    };
    
    if (!bookData.title || !bookData.author) {
        showAlert('Title and Author are required', 'warning');
        return;
    }
    
    try {
        const response = await fetch('/api/books/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(bookData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('Book added successfully!', 'success');
            setTimeout(() => {
                window.location.href = '/books';
            }, 1500);
        } else {
            showAlert(data.message || 'Failed to add book', 'danger');
        }
    } catch (error) {
        console.error('Error adding book:', error);
        showAlert('Error adding book', 'danger');
    }
}

// Fetch book from Google Books
const fetchBookBtn = document.getElementById('fetchBookBtn');
if (fetchBookBtn) {
    fetchBookBtn.addEventListener('click', async function() {
        const isbn = document.getElementById('isbn').value.trim();
        
        if (!isbn) {
            showAlert('Please enter an ISBN first', 'warning');
            return;
        }
        
        try {
            const response = await fetch(`/api/fetch-book-details/${isbn}`);
            const data = await response.json();
            
            if (data.success) {
                const book = data.book;
                document.getElementById('title').value = book.title || '';
                document.getElementById('author').value = book.author || '';
                document.getElementById('publisher').value = book.publisher || '';
                document.getElementById('category').value = book.category || '';
                document.getElementById('cover_image_url').value = book.cover_image_url || '';
                
                showAlert('Book details fetched successfully! You can now add this book.', 'success');
                
                // Enable AI buttons
                document.getElementById('generateSummaryBtn').disabled = false;
                document.getElementById('suggestGenresBtn').disabled = false;
            } else {
                showAlert('Book not found in Google Books. You can still add it manually by filling in the form.', 'warning');
            }
        } catch (error) {
            console.error('Error fetching book:', error);
            showAlert('Error fetching book details', 'danger');
        }
    });
}
