import requests

def test_google_books_api():
    """Test Google Books API with a known ISBN"""
    
    test_isbns = [
        '9780743273565',  # The Great Gatsby
        '9780061120084',  # To Kill a Mockingbird
        '9780451524935',  # 1984
    ]
    
    print("Testing Google Books API...")
    print("=" * 60)
    
    for isbn in test_isbns:
        print(f"\nTesting ISBN: {isbn}")
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
        
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data.get('totalItems', 0) > 0:
                book = data['items'][0]['volumeInfo']
                print(f"✅ Found: {book.get('title')}")
                print(f"   Author: {', '.join(book.get('authors', ['Unknown']))}")
                print(f"   Publisher: {book.get('publisher', 'N/A')}")
            else:
                print(f"❌ Not found in Google Books")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("Test complete!")

if __name__ == '__main__':
    test_google_books_api()
