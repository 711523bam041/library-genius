"""Check transactions table structure"""
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def check_transactions_table():
    print("=" * 60)
    print("CHECKING TRANSACTIONS TABLE")
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
        
        # Check transactions table structure
        print("\nTransactions table columns:")
        cursor.execute("DESCRIBE transactions")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[0]} ({col[1]})")
        
        # Check students table
        print("\nStudents table columns:")
        cursor.execute("DESCRIBE students")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[0]} ({col[1]})")
        
        # Check books table
        print("\nBooks table columns:")
        cursor.execute("DESCRIBE books")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[0]} ({col[1]})")
        
        # Test the query that dashboard uses
        print("\n" + "-" * 60)
        print("Testing recent transactions query...")
        query = """
            SELECT t.*, s.student_name, b.title as book_title
            FROM transactions t
            JOIN students s ON t.student_id = s.student_id
            JOIN books b ON t.book_id = b.book_id
            ORDER BY t.borrow_date DESC
            LIMIT 10
        """
        
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            print(f"✅ Query successful! Found {len(results)} transactions")
            
            if results:
                print(f"\nSample transaction:")
                for col_name, value in results[0].items():
                    print(f"  {col_name}: {value}")
        except Exception as e:
            print(f"❌ Query failed: {e}")
            print("\nThis is the error causing the dashboard issue!")
        
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_transactions_table()
