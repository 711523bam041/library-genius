from flask import Blueprint, request, jsonify, session
from modules.auth import AuthManager
from modules.book_manager import BookManager
from modules.isbn_scanner import ISBNScanner
from modules.ai_integration import AIBookAssistant
from modules.transaction import TransactionManager
from modules.student_manager import StudentManager
from modules.database import DatabaseConnection
from functools import wraps

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Initialize managers
auth_mgr = AuthManager()
book_mgr = BookManager()
isbn_scanner = ISBNScanner()
ai_assistant = AIBookAssistant()
txn_mgr = TransactionManager()
student_mgr = StudentManager()
db = DatabaseConnection()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function


# ==================== AUTHENTICATION ENDPOINTS ====================

@api_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email', '')
    role = data.get('role', 'librarian')
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password required'}), 400
    
    success, message = auth_mgr.register_user(username, password, email, role)
    return jsonify({'success': success, 'message': message}), 200 if success else 400


@api_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password required'}), 400
    
    success, user, message = auth_mgr.authenticate_user(username, password)
    
    if success:
        session['user_id'] = user['user_id']
        session['username'] = user['username']
        session['role'] = user['role']
        return jsonify({
            'success': True,
            'message': message,
            'user': {
                'user_id': user['user_id'],
                'username': user['username'],
                'email': user.get('email', ''),
                'role': user['role']
            }
        })
    else:
        return jsonify({'success': False, 'message': message}), 401


@api_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})


@api_bp.route('/session', methods=['GET'])
def check_session():
    """Check if user is logged in"""
    if 'user_id' in session:
        return jsonify({
            'logged_in': True,
            'user': {
                'user_id': session['user_id'],
                'username': session['username'],
                'role': session.get('role', 'librarian')
            }
        })
    return jsonify({'logged_in': False})


# ==================== BOOK ENDPOINTS ====================

@api_bp.route('/books', methods=['GET'])
@login_required
def get_books():
    """Get all books with pagination"""
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    offset = (page - 1) * limit
    
    books = book_mgr.get_all_books(limit, offset)
    total = book_mgr.get_books_count()
    
    return jsonify({
        'success': True,
        'books': books,
        'total': total,
        'page': page,
        'pages': (total + limit - 1) // limit
    })


@api_bp.route('/books/search', methods=['GET'])
@login_required
def search_books():
    """Search books by query"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({'success': False, 'message': 'Search query required'}), 400
    
    results = book_mgr.search_books(query)
    return jsonify({
        'success': True,
        'books': results,
        'count': len(results)
    })


@api_bp.route('/books/<int:book_id>', methods=['GET'])
@login_required
def get_book_detail(book_id):
    """Get single book details"""
    book = book_mgr.get_book_by_id(book_id)
    if book:
        return jsonify({'success': True, 'book': book})
    return jsonify({'success': False, 'message': 'Book not found'}), 404


@api_bp.route('/books/add', methods=['POST'])
@login_required
def add_book():
    """Add a new book"""
    try:
        data = request.get_json()
        print(f"Adding book with data: {data}")  # Debug log
        
        required_fields = ['title', 'author']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields (title, author)'}), 400
        
        success = book_mgr.add_book(data)
        if success:
            return jsonify({'success': True, 'message': 'Book added successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to add book. Check database connection and try again.'}), 500
    except Exception as e:
        print(f"Error in add_book endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Error adding book: {str(e)}'}), 500


# ==================== ISBN SCAN ENDPOINTS ====================

@api_bp.route('/scan-isbn', methods=['POST'])
@login_required
def scan_isbn():
    """Scan ISBN from uploaded image"""
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No image provided'}), 400
    
    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'success': False, 'message': 'No image selected'}), 400
    
    isbn = isbn_scanner.scan_from_image(image_file)
    
    if isbn:
        return jsonify({'success': True, 'isbn': isbn})
    return jsonify({'success': False, 'message': 'No barcode detected in image'}), 400


@api_bp.route('/fetch-book-details/<isbn>', methods=['GET'])
@login_required
def fetch_book_details(isbn):
    """Fetch book details from Google Books API"""
    book_data = isbn_scanner.fetch_from_google_books(isbn)
    
    if book_data:
        book_data['isbn'] = isbn
        return jsonify({'success': True, 'book': book_data})
    return jsonify({'success': False, 'message': 'Book not found in Google Books API'}), 404


# ==================== AI ENDPOINTS ====================

@api_bp.route('/ai/generate-summary', methods=['POST'])
@login_required
def generate_summary():
    """Generate AI book summary"""
    data = request.get_json()
    title = data.get('title', '')
    author = data.get('author', '')
    description = data.get('description', '')
    
    if not title or not author:
        return jsonify({'success': False, 'message': 'Title and author required'}), 400
    
    summary = ai_assistant.generate_summary(title, author, description)
    return jsonify({'success': True, 'summary': summary})


@api_bp.route('/ai/suggest-genres', methods=['POST'])
@login_required
def suggest_genres():
    """Suggest AI book genres"""
    data = request.get_json()
    title = data.get('title', '')
    author = data.get('author', '')
    description = data.get('description', '')
    
    if not title or not author:
        return jsonify({'success': False, 'message': 'Title and author required'}), 400
    
    genres = ai_assistant.suggest_genres(title, author, description)
    return jsonify({'success': True, 'genres': genres})


@api_bp.route('/ai/save-book-data', methods=['POST'])
@login_required
def save_ai_book_data():
    """Save AI-generated data to book record"""
    data = request.get_json()
    book_id = data.get('book_id')
    summary = data.get('summary', '')
    genres = data.get('genres', '')
    
    if not book_id:
        return jsonify({'success': False, 'message': 'Book ID required'}), 400
    
    success = book_mgr.update_book_ai_data(book_id, summary, genres)
    if success:
        return jsonify({'success': True, 'message': 'AI data saved successfully'})
    return jsonify({'success': False, 'message': 'Failed to save AI data'}), 500


# ==================== TRANSACTION ENDPOINTS ====================

@api_bp.route('/borrow', methods=['POST'])
@login_required
def borrow_book():
    """Borrow a book"""
    data = request.get_json()
    student_id = data.get('student_id')
    book_id = data.get('book_id')
    
    if not student_id or not book_id:
        return jsonify({'success': False, 'message': 'Student ID and Book ID required'}), 400
    
    success, message = txn_mgr.borrow_book(student_id, book_id)
    return jsonify({'success': success, 'message': message}), 200 if success else 400


@api_bp.route('/return', methods=['POST'])
@login_required
def return_book():
    """Return a book"""
    data = request.get_json()
    student_id = data.get('student_id')
    book_id = data.get('book_id')
    condition = data.get('condition', 'Good')
    
    if not student_id or not book_id:
        return jsonify({'success': False, 'message': 'Student ID and Book ID required'}), 400
    
    success, message = txn_mgr.return_book(student_id, book_id, condition)
    return jsonify({'success': success, 'message': message}), 200 if success else 400


# ==================== STUDENT ENDPOINTS ====================

@api_bp.route('/students/<student_id>', methods=['GET'])
@login_required
def get_student(student_id):
    """Get student details and borrowed books"""
    student = student_mgr.get_student(student_id)
    
    if not student:
        return jsonify({'success': False, 'message': 'Student not found'}), 404
    
    borrowed_books = txn_mgr.get_student_borrowed_books(student_id)
    
    return jsonify({
        'success': True,
        'student': student,
        'borrowed_books': borrowed_books
    })


# ==================== DASHBOARD ENDPOINTS ====================

@api_bp.route('/dashboard/stats', methods=['GET'])
@login_required
def dashboard_stats():
    """Get dashboard statistics"""
    stats = db.get_dashboard_stats()
    return jsonify({'success': True, 'stats': stats})


@api_bp.route('/dashboard/recent-transactions', methods=['GET'])
@login_required
def recent_transactions():
    """Get recent transactions"""
    limit = request.args.get('limit', 10, type=int)
    
    query = """
        SELECT t.*, s.student_name, b.title as book_title
        FROM transactions t
        JOIN students s ON t.student_id = s.student_id
        JOIN books b ON t.book_id = b.book_id
        ORDER BY t.borrow_date DESC
        LIMIT %s
    """
    
    transactions = db.execute_query(query, (limit,))
    return jsonify({'success': True, 'transactions': transactions})
