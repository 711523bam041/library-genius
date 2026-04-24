# LibraryGenius - AI-Powered Library Management System

A complete professional library management website with AI and ISBN scanning capabilities.

## Features

- **User Authentication**: Secure login/register with password hashing
- **ISBN Barcode Scanning**: Upload barcode images to extract ISBN using pyzbar
- **Google Books Integration**: Automatically fetch book details using ISBN
- **AI-Powered Features**: 
  - Generate book summaries using OpenAI
  - Suggest categories/genres using AI
- **Complete Library Management**:
  - Book catalog with search and pagination
  - Borrow/Return transaction management
  - Student management
  - Fine calculation
- **Professional Dashboard**: Statistics and recent transactions

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: MySQL
- **APIs**: Google Books API, OpenAI API
- **Libraries**: pyzbar, Pillow, requests, werkzeug

## Prerequisites

1. Python 3.8 or higher
2. MySQL Server 5.7 or higher
3. Tesseract OCR (for pyzbar)
4. OpenAI API key (optional, for AI features)
5. Google Books API key (optional)

## Installation & Setup

### 1. Install MySQL and Create Database

```bash
# Login to MySQL
mysql -u root -p

# Run the schema script
source schema.sql

# Or manually:
CREATE DATABASE library_management;
USE library_management;
# Then run the contents of schema.sql
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Tesseract OCR (Required for ISBN Scanning)

**Windows:**
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Add to PATH or set environment variable: `TESSDATA_PREFIX`

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

### 4. Configure Environment Variables

Edit the `.env` file:

```env
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=library_management
DB_PORT=3306

# Flask Configuration
FLASK_SECRET_KEY=change-this-to-a-random-secret-key

# API Keys (Optional but recommended)
OPENAI_API_KEY=your-openai-api-key-here
GOOGLE_BOOKS_API_KEY=your-google-books-api-key-here
```

### 5. Run the Application

```bash
python app.py
```

The application will start at: **http://localhost:5000**

## Default Credentials

- **Username**: admin
- **Password**: admin123

*Note: Change this immediately after first login in production!*

## Project Structure

```
smart-lib-copy/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── schema.sql                  # Database schema
├── .env                        # Environment variables
│
├── modules/                    # Business logic modules
│   ├── __init__.py
│   ├── auth.py                 # Authentication manager
│   ├── book_manager.py         # Book operations
│   ├── student_manager.py      # Student operations
│   ├── transaction.py          # Borrow/Return transactions
│   ├── fine_calculator.py      # Fine calculation
│   ├── database.py             # Database connection
│   ├── isbn_scanner.py         # ISBN barcode scanning
│   └── ai_integration.py       # OpenAI integration
│
├── routes/                     # API routes
│   ├── __init__.py
│   └── api.py                  # REST API endpoints
│
├── templates/                  # HTML templates
│   ├── base.html               # Base template
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── books/
│   │   ├── list.html
│   │   └── add.html
│   └── transactions/
│       ├── borrow.html
│       └── return.html
│
└── static/                     # Static files
    ├── css/
    │   └── style.css
    ├── js/
    │   ├── main.js
    │   ├── auth.js
    │   ├── books.js
    │   ├── scanner.js
    │   └── ai.js
    └── images/
```

## API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - User login
- `POST /api/logout` - User logout
- `GET /api/session` - Check session status

### Books
- `GET /api/books` - Get all books (paginated)
- `GET /api/books/search?q=query` - Search books
- `GET /api/books/<id>` - Get book details
- `POST /api/books/add` - Add new book

### ISBN Scanning
- `POST /api/scan-isbn` - Scan ISBN from image
- `GET /api/fetch-book-details/<isbn>` - Fetch from Google Books

### AI Features
- `POST /api/ai/generate-summary` - Generate book summary
- `POST /api/ai/suggest-genres` - Suggest genres
- `POST /api/ai/save-book-data` - Save AI data to book

### Transactions
- `POST /api/borrow` - Borrow a book
- `POST /api/return` - Return a book

### Students
- `GET /api/students/<id>` - Get student details

### Dashboard
- `GET /api/dashboard/stats` - Get statistics
- `GET /api/dashboard/recent-transactions` - Get recent transactions

## Usage Guide

### Adding a Book

1. Navigate to "Add Book"
2. **Option 1**: Manual Entry
   - Fill in title, author, ISBN, etc.
   
3. **Option 2**: ISBN Scan
   - Click "Upload Barcode Image"
   - Upload a photo of the book's barcode
   - ISBN will be auto-detected and filled
   
4. **Option 3**: Google Books Fetch
   - Enter ISBN
   - Click "Fetch" button
   - Book details will be auto-filled

5. **AI Assistance** (Optional)
   - Click "Generate Summary" to create AI summary
   - Click "Suggest Genres" for category suggestions

6. Click "Add Book"

### Borrowing a Book

1. Navigate to "Borrow"
2. Enter Student ID and click "Fetch"
3. Enter Book ISBN and click "Fetch"
4. Verify details
5. Click "Confirm Borrow"

### Returning a Book

1. Navigate to "Return"
2. Enter Student ID and Book ISBN
3. Select book condition
4. Click "Process Return"
5. Fine will be calculated automatically if overdue

## Database Schema

The system uses 4 main tables:
- **users**: Authentication and user management
- **books**: Book catalog with AI-generated data
- **students**: Student records
- **transactions**: Borrow/Return history

See `schema.sql` for complete schema.

## Security Notes

1. **Change default admin password** immediately after first login
2. Use a strong `FLASK_SECRET_KEY` in production
3. Never commit `.env` file to version control
4. Use HTTPS in production
5. Regularly backup MySQL database
6. Keep dependencies updated

## Troubleshooting

### MySQL Connection Error
- Verify MySQL is running
- Check credentials in `.env`
- Ensure database exists

### ISBN Scanning Not Working
- Verify Tesseract OCR is installed
- Check image quality (clear, well-lit barcode)
- Try different image formats (PNG, JPG)

### AI Features Not Working
- Verify OPENAI_API_KEY is set correctly in `.env`
- Check OpenAI API quota/billing
- Features will show warning but won't crash if key is missing

### Port Already in Use
- Change port in `app.py`: `app.run(port=5001)`
- Or kill existing process on port 5000

## Future Enhancements

- Email notifications for overdue books
- Barcode generation for books
- Advanced reporting and analytics
- Export to CSV/PDF
- Mobile responsive improvements
- Multi-language support
- Book reservation system

## License

This project is for educational purposes.

## Support

For issues or questions, please check the documentation or contact the development team.

---

**Built with ❤️ using Flask, MySQL, and AI**
