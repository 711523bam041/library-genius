"""Database Connection Test Script"""
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def test_database_connection():
    """Test MySQL database connection"""
    
    print("=" * 60)
    print("DATABASE CONNECTION TEST")
    print("=" * 60)
    
    # Get config from .env
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'library_management'),
        'port': int(os.getenv('DB_PORT', '3306'))
    }
    
    print(f"\nConnection Details:")
    print(f"  Host: {db_config['host']}")
    print(f"  Port: {db_config['port']}")
    print(f"  User: {db_config['user']}")
    print(f"  Database: {db_config['database']}")
    print(f"  Password: {'***' + db_config['password'][-3:] if db_config['password'] else 'NOT SET'}")
    
    print("\n" + "-" * 60)
    
    # Test 1: Basic connection
    print("\n[Test 1] Testing MySQL connection...")
    try:
        connection = mysql.connector.connect(**db_config)
        
        if connection.is_connected():
            print("✅ SUCCESS: Connected to MySQL server")
            
            # Get server info
            db_info = connection.get_server_info()
            print(f"   MySQL Server Version: {db_info}")
            
            # Test 2: Check if database exists
            print("\n[Test 2] Checking if database exists...")
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            
            if db_config['database'] in databases:
                print(f"✅ Database '{db_config['database']}' exists")
                
                # Test 3: Check tables
                print(f"\n[Test 3] Checking tables in '{db_config['database']}'...")
                cursor.execute(f"USE {db_config['database']}")
                cursor.execute("SHOW TABLES")
                tables = [table[0] for table in cursor.fetchall()]
                
                if tables:
                    print(f"✅ Found {len(tables)} tables:")
                    for table in tables:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        print(f"   - {table}: {count} rows")
                else:
                    print("❌ No tables found! You need to run schema.sql")
                    
            else:
                print(f"❌ Database '{db_config['database']}' does NOT exist")
                print("   Solution: Run 'source schema.sql' in MySQL")
                print(f"   Available databases: {', '.join(databases)}")
            
            cursor.close()
            
        else:
            print("❌ FAILED: Could not establish connection")
            
    except Error as e:
        print(f"❌ FAILED: Connection error")
        print(f"   Error: {e}")
        
        # Provide solutions based on error
        error_msg = str(e).lower()
        if 'access denied' in error_msg:
            print("\n💡 Solution:")
            print("   - Check your MySQL username and password in .env file")
            print("   - Make sure the user has permission to access the database")
        elif 'unknown database' in error_msg or 'does not exist' in error_msg:
            print("\n💡 Solution:")
            print("   - Run the schema.sql file to create the database")
            print("   - Use MySQL Workbench or command line to execute schema.sql")
        elif 'can\'t connect' in error_msg or 'connection refused' in error_msg:
            print("\n💡 Solution:")
            print("   - Make sure MySQL server is running")
            print("   - Check if port 3306 is correct")
            print("   - Start MySQL service from Windows Services")
        else:
            print("\n💡 Possible Solutions:")
            print("   1. Check if MySQL server is running")
            print("   2. Verify credentials in .env file")
            print("   3. Run schema.sql to create database and tables")
            print("   4. Check MySQL service in Windows Services")
    
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("\n" + "-" * 60)
            print("Connection closed.")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == '__main__':
    test_database_connection()
