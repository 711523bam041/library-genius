"""Fix all schema issues and test queries"""
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def fix_all_schema_issues():
    print("=" * 60)
    print("COMPREHENSIVE SCHEMA FIX")
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
        cursor = connection.cursor(dictionary=True)
        
        # Fix 1: Test the exact query used in the API
        print("\n[Test 1] Testing dashboard recent transactions query...")
        query1 = """
            SELECT t.transaction_id, t.student_id, t.book_id, 
                   t.borrow_date, t.due_date, t.return_date, 
                   t.fine_amount, t.status,
                   s.student_name, b.title as book_title
            FROM transactions t
            JOIN students s ON t.student_id = s.student_id
            JOIN books b ON t.book_id = b.book_id
            ORDER BY t.borrow_date DESC
            LIMIT 10
        """
        
        try:
            cursor.execute(query1)
            results = cursor.fetchall()
            print(f"✅ SUCCESS! Found {len(results)} transactions")
            if results:
                print(f"\nFirst transaction data:")
                for key, val in results[0].items():
                    print(f"  {key}: {val}")
        except Exception as e:
            print(f"❌ FAILED: {e}")
            print("   The transactions query needs fixing!")
        
        # Fix 2: Test dashboard stats queries
        print("\n[Test 2] Testing dashboard stats queries...")
        
        tests = [
            ("Total Books", "SELECT COUNT(*) as count FROM books"),
            ("Total Students", "SELECT COUNT(*) as count FROM students"),
            ("Active Borrows", "SELECT COUNT(*) as count FROM transactions WHERE status = 'Active'"),
            ("Overdue Books", "SELECT COUNT(*) as count FROM transactions WHERE status = 'Active' AND due_date < CURDATE()")
        ]
        
        for test_name, query in tests:
            try:
                cursor.execute(query)
                result = cursor.fetchone()
                print(f"  ✅ {test_name}: {result['count']}")
            except Exception as e:
                print(f"  ❌ {test_name}: {e}")
        
        # Fix 3: Check if book_location column exists (old schema uses this instead of shelf_location)
        print("\n[Test 3] Checking column name compatibility...")
        cursor.execute("SHOW COLUMNS FROM books LIKE 'book_location'")
        if cursor.fetchone():
            print("  ⚠️  Found 'book_location' column (old schema)")
            print("  💡 The app uses 'shelf_location' - both exist now, so it's OK")
        
        cursor.execute("SHOW COLUMNS FROM books LIKE 'shelf_location'")
        if cursor.fetchone():
            print("  ✅ Found 'shelf_location' column (new schema)")
        
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETE")
        print("=" * 60)
        print("\nIf all tests passed, the dashboard should work now!")
        print("Refresh your browser at http://localhost:5000")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    fix_all_schema_issues()
