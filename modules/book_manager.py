from modules.database import DatabaseConnection

class BookManager:
    def __init__(self):
        self.db = DatabaseConnection()
        self.db.connect()

    # fetch using ISBN (for UI)
    def get_book(self, isbn: str):
        rows = self.db.execute_query(
            "SELECT * FROM books WHERE isbn_13 = %s OR isbn_10 = %s",
            (isbn, isbn)
        )
        return rows[0] if rows else None

    # if you ever need by numeric id
    def get_book_by_id(self, book_id: int):
        rows = self.db.execute_query(
            "SELECT * FROM books WHERE book_id = %s",
            (book_id,)
        )
        return rows[0] if rows else None

    def search_by_isbn(self, isbn: str):
        rows = self.db.execute_query(
            "SELECT * FROM books WHERE isbn_13 = %s OR isbn_10 = %s",
            (isbn, isbn)
        )
        return rows[0] if rows else None

    def search_by_title(self, title: str):
        return self.db.execute_query(
            "SELECT * FROM books WHERE title LIKE %s",
            (f"%{title}%",)
        )

    def get_all_books(self, limit=20, offset=0):
        """Get all books with pagination"""
        return self.db.execute_query(
            "SELECT * FROM books ORDER BY created_at DESC LIMIT %s OFFSET %s",
            (limit, offset)
        )

    def get_books_count(self):
        """Get total number of books"""
        result = self.db.execute_query("SELECT COUNT(*) as count FROM books")
        return result[0]['count'] if result else 0

    def check_availability(self, book_id: int):
        book = self.get_book_by_id(book_id)
        if not book:
            return False, "Book not found"
        if book["available_copies"] <= 0:
            return False, "No copies available"
        return True, "Available"

    def update_available_copies(self, book_id: int, borrow: bool = True):
        delta = -1 if borrow else 1
        return self.db.execute_update(
            "UPDATE books SET available_copies = available_copies + %s "
            "WHERE book_id = %s",
            (delta, book_id)
        ) > 0

    def add_book(self, book_data: dict):
        # We assume book_data contains title, author, isbn (13 or 10), category, shelf_location, available_copies
        isbn = book_data.get("isbn", "")
        # Very simple distinction: if length == 13, it's ISBN-13, else assume ISBN-10 or generalized.
        isbn_clean = str(isbn).replace('-', '')
        isbn_13 = isbn if len(isbn_clean) == 13 else None
        isbn_10 = isbn if len(isbn_clean) == 10 else (isbn if not isbn_13 else None)
        
        query = """
            INSERT INTO books (title, author, isbn_13, isbn_10, category, shelf_location, available_copies, total_copies)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            book_data.get("title", "Unknown"),
            book_data.get("author", "Unknown"),
            isbn_13,
            isbn_10,
            book_data.get("category", ""),
            book_data.get("shelf_location", ""),
            book_data.get("available_copies", 1),
            book_data.get("available_copies", 1)
        )
        return self.db.execute_update(query, params) > 0

    def add_book_from_api(self, book_data: dict):
        """Add book with data from Google Books API"""
        isbn = book_data.get("isbn", "")
        isbn_clean = str(isbn).replace('-', '')
        isbn_13 = isbn if len(isbn_clean) == 13 else None
        isbn_10 = isbn if len(isbn_clean) == 10 else (isbn if not isbn_13 else None)
        
        query = """
            INSERT INTO books (title, author, isbn_13, isbn_10, publisher, category, 
                             cover_image_url, available_copies, total_copies)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            book_data.get("title", "Unknown"),
            book_data.get("author", "Unknown"),
            isbn_13,
            isbn_10,
            book_data.get("publisher", ""),
            book_data.get("category", ""),
            book_data.get("cover_image_url", ""),
            book_data.get("available_copies", 1),
            book_data.get("available_copies", 1)
        )
        return self.db.execute_update(query, params) > 0

    def update_book_ai_data(self, book_id: int, summary: str, genres: str):
        """Update AI-generated summary and genres for a book"""
        return self.db.execute_update(
            "UPDATE books SET ai_summary = %s, ai_suggested_genres = %s WHERE book_id = %s",
            (summary, genres, book_id)
        ) > 0

    def search_books(self, query: str):
        """Search books by title, author, or ISBN"""
        return self.db.execute_query(
            """SELECT * FROM books 
               WHERE title LIKE %s OR author LIKE %s OR isbn_13 LIKE %s OR isbn_10 LIKE %s
               ORDER BY title""",
            (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%")
        )
