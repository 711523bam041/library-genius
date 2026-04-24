from flask import Flask, render_template, session, redirect, url_for, request
from functools import wraps
from config import FLASK_SECRET_KEY, FLASK_ENV, DEBUG
from routes.api import api_bp
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

# Production settings
app.config['ENV'] = FLASK_ENV
app.config['DEBUG'] = DEBUG

# Register API blueprint
app.register_blueprint(api_bp)


# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# ==================== PAGE ROUTES ====================

@app.route('/')
@login_required
def index():
    """Dashboard page"""
    return render_template('dashboard.html')


@app.route('/login')
def login():
    """Login page"""
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/register')
def register():
    """Register page"""
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/books')
@login_required
def books():
    """Books list page"""
    return render_template('books/list.html')


@app.route('/books/add')
@login_required
def add_book():
    """Add book page"""
    return render_template('books/add.html')


@app.route('/borrow')
@login_required
def borrow():
    """Borrow book page"""
    return render_template('transactions/borrow.html')


@app.route('/return')
@login_required
def return_book():
    """Return book page"""
    return render_template('transactions/return.html')


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    if 'user_id' in session:
        return render_template('base.html'), 404
    return redirect(url_for('login'))


@app.errorhandler(500)
def internal_error(error):
    return "Internal Server Error", 500


# ==================== MAIN ====================

if __name__ == '__main__':
    print("=" * 50)
    print("LibraryGenius - AI-Powered Library Management System")
    print("=" * 50)
    print("Starting Flask server...")
    print("Access the application at: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
