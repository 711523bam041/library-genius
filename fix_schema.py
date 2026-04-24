"""Fix database schema - add missing columns"""
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def fix_schema():
    print("=" * 60)
    print("FIXING DATABASE SCHEMA")
    print("=" * 60)
    
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'library_management'),
        'port': int(os.getenv('DB_PORT', '3306'))
    }
    
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        # Check current books table structure
        print("\nCurrent books table columns:")
        cursor.execute("DESCRIBE books")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[0]} ({col[1]})")
        
        # Add missing columns
        print("\nAdding missing columns...")
        
        columns_to_add = [
            ("publisher", "VARCHAR(255)"),
            ("ai_summary", "TEXT"),
            ("ai_suggested_genres", "VARCHAR(255)"),
            ("cover_image_url", "TEXT"),
            ("shelf_location", "VARCHAR(50)"),
            ("total_copies", "INT DEFAULT 1"),
            ("created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        ]
        
        for col_name, col_type in columns_to_add:
            # Check if column exists
            cursor.execute(f"SHOW COLUMNS FROM books LIKE '{col_name}'")
            if not cursor.fetchone():
                try:
                    cursor.execute(f"ALTER TABLE books ADD COLUMN {col_name} {col_type}")
                    print(f"  ✅ Added column: {col_name}")
                except Exception as e:
                    print(f"  ⚠️  Column {col_name}: {e}")
            else:
                print(f"  ✓ Column {col_name} already exists")
        
        # Check users table
        print("\nChecking users table...")
        cursor.execute("SHOW COLUMNS FROM users")
        user_cols = [col[0] for col in cursor.fetchall()]
        print(f"  Users table columns: {', '.join(user_cols)}")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 60)
        print("SCHEMA FIX COMPLETE")
        print("=" * 60)
        print("\nTry adding a book again!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    fix_schema()
