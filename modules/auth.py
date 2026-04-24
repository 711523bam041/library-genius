from modules.database import DatabaseConnection
from werkzeug.security import generate_password_hash, check_password_hash

class AuthManager:
    def __init__(self):
        self.db = DatabaseConnection()
        self.db.connect()

    def register_user(self, username, password, email=None, role='librarian'):
        """Register a new user with hashed password"""
        # Check if username already exists
        existing = self.db.execute_query(
            "SELECT user_id FROM users WHERE username = %s",
            (username,)
        )
        if existing:
            return False, "Username already exists"
        
        # Hash password and insert
        password_hash = generate_password_hash(password)
        query = """
            INSERT INTO users (username, password_hash, email, role)
            VALUES (%s, %s, %s, %s)
        """
        try:
            user_id = self.db.execute_insert_get_id(
                query, (username, password_hash, email, role)
            )
            if user_id:
                return True, "User registered successfully"
            return False, "Failed to register user"
        except Exception as e:
            return False, str(e)

    def authenticate_user(self, username, password):
        """Authenticate user and return user data if successful"""
        rows = self.db.execute_query(
            "SELECT * FROM users WHERE username = %s",
            (username,)
        )
        if not rows:
            return False, None, "Invalid username or password"
        
        user = rows[0]
        if check_password_hash(user['password_hash'], password):
            # Remove password_hash from returned data
            user.pop('password_hash', None)
            return True, user, "Login successful"
        
        return False, None, "Invalid username or password"

    def get_user_by_id(self, user_id):
        """Get user details by user ID"""
        rows = self.db.execute_query(
            "SELECT user_id, username, email, role, created_at FROM users WHERE user_id = %s",
            (user_id,)
        )
        return rows[0] if rows else None

    def validate(self, username: str, password: str) -> bool:
        """Legacy method for backward compatibility"""
        success, user, msg = self.authenticate_user(username, password)
        return success
