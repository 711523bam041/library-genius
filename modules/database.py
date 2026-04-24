import mysql.connector
from mysql.connector import Error
import logging
import os
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT, LOG_FILE, LOG_LEVEL

# Create logs directory if it doesn't exist
log_dir = os.path.dirname(LOG_FILE)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

# Configure logging with fallback
try:
    logging.basicConfig(filename=LOG_FILE, level=getattr(logging, LOG_LEVEL))
except Exception:
    # If file logging fails, use console logging
    logging.basicConfig(level=getattr(logging, LOG_LEVEL))
    logging.warning(f"Could not write to {LOG_FILE}, using console logging instead")
logger = logging.getLogger(__name__)

class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                port=DB_PORT
            )
            return self.connection.is_connected()
        except Error as e:
            print("DB connect error:", e)
            logger.error(f"Error connecting to database: {e}")
            self.connection = None
            return False

    def execute_query(self, query, params=None):
        try:
            # Reconnect if connection is lost
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return None
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            print(f"Database query error: {e}")
            # Try to reconnect
            self.connection = None
            if self.connect():
                try:
                    cursor = self.connection.cursor(dictionary=True)
                    cursor.execute(query, params or ())
                    rows = cursor.fetchall()
                    cursor.close()
                    return rows
                except Exception as e2:
                    logger.error(f"Error executing query after reconnect: {e2}")
                    print(f"Database query error after reconnect: {e2}")
                    return None
            return None

    def execute_update(self, query, params=None):
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return 0
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            count = cursor.rowcount
            cursor.close()
            return count
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            logger.error(f"Error executing update: {e}")
            print(f"Database update error: {e}")
            # Try to reconnect
            self.connection = None
            if self.connect():
                try:
                    cursor = self.connection.cursor()
                    cursor.execute(query, params or ())
                    self.connection.commit()
                    count = cursor.rowcount
                    cursor.close()
                    return count
                except Exception as e2:
                    if self.connection:
                        self.connection.rollback()
                    logger.error(f"Error executing update after reconnect: {e2}")
                    print(f"Database update error after reconnect: {e2}")
                    return 0
            return 0

    def execute_insert_get_id(self, query, params=None):
        """Execute INSERT and return the last inserted ID"""
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                return None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            last_id = cursor.lastrowid
            cursor.close()
            return last_id
        except Error as e:
            self.connection.rollback()
            logger.error(f"Error executing insert: {e}")
            return None

    def get_dashboard_stats(self):
        """Get statistics for dashboard"""
        stats = {}
        try:
            # Total books
            result = self.execute_query("SELECT COUNT(*) as count FROM books")
            stats['total_books'] = result[0]['count'] if result else 0
            
            # Total students
            result = self.execute_query("SELECT COUNT(*) as count FROM students")
            stats['total_students'] = result[0]['count'] if result else 0
            
            # Active borrows
            result = self.execute_query("SELECT COUNT(*) as count FROM transactions WHERE status = 'Active'")
            stats['active_borrows'] = result[0]['count'] if result else 0
            
            # Overdue books
            result = self.execute_query("SELECT COUNT(*) as count FROM transactions WHERE status = 'Active' AND due_date < CURDATE()")
            stats['overdue_books'] = result[0]['count'] if result else 0
            
            return stats
        except Exception as e:
            logger.error(f"Error getting dashboard stats: {e}")
            return stats

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
