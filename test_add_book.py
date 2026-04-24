"""Test adding a book directly"""
from modules.book_manager import BookManager

def test_add_book():
    print("=" * 60)
    print("TEST: Adding a book directly via BookManager")
    print("=" * 60)
    
    book_mgr = BookManager()
    
    # Test book data
    book_data = {
        "title": "Test Book Direct",
        "author": "Test Author",
        "isbn": "1234567890123",
        "category": "Fiction",
        "shelf_location": "A1-01",
        "available_copies": 1
    }
    
    print(f"\nBook data to add:")
    for key, value in book_data.items():
        print(f"  {key}: {value}")
    
    print("\nAttempting to add book...")
    try:
        success = book_mgr.add_book(book_data)
        
        if success:
            print("✅ SUCCESS: Book added!")
            
            # Verify it was added
            book = book_mgr.get_book("1234567890123")
            if book:
                print(f"\nVerified - Book found in database:")
                print(f"  ID: {book['book_id']}")
                print(f"  Title: {book['title']}")
                print(f"  Author: {book['author']}")
            else:
                print("⚠️  Warning: Book was not found after adding")
        else:
            print("❌ FAILED: add_book returned False")
            print("\nPossible reasons:")
            print("  - Database table structure mismatch")
            print("  - Missing columns in books table")
            print("  - Constraint violation")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    test_add_book()
