try:
    from pyzbar.pyzbar import decode
    from PIL import Image
    PYZBAR_AVAILABLE = True
except Exception as e:
    print(f"Warning: pyzbar not available. ISBN scanning will be disabled. Error: {e}")
    print("To enable ISBN scanning, install Tesseract OCR and required DLLs.")
    PYZBAR_AVAILABLE = False
    decode = None
    Image = None

import requests
from config import GOOGLE_BOOKS_API_KEY

class ISBNScanner:
    def scan_from_image(self, image_file):
        """Decode barcode/ISBN from uploaded image"""
        if not PYZBAR_AVAILABLE:
            print("ISBN scanning is not available. Please install pyzbar dependencies.")
            return None
        
        try:
            image = Image.open(image_file)
            decoded_objects = decode(image)
            
            if decoded_objects:
                # Return the first detected barcode
                return decoded_objects[0].data.decode('utf-8')
            return None
        except Exception as e:
            print(f"Error scanning image: {e}")
            return None
    
    def fetch_from_google_books(self, isbn):
        """Fetch book details from Google Books API using ISBN"""
        try:
            url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
            if GOOGLE_BOOKS_API_KEY:
                url += f"&key={GOOGLE_BOOKS_API_KEY}"
            
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data.get('totalItems', 0) > 0:
                volume = data['items'][0]['volumeInfo']
                
                # Extract image URL
                cover_image = None
                if 'imageLinks' in volume:
                    cover_image = volume['imageLinks'].get('thumbnail') or volume['imageLinks'].get('smallThumbnail')
                
                # Extract categories/genres
                categories = volume.get('categories', [])
                category = categories[0] if categories else None
                
                return {
                    'title': volume.get('title', 'Unknown'),
                    'author': ', '.join(volume.get('authors', ['Unknown'])),
                    'publisher': volume.get('publisher', 'Unknown'),
                    'published_date': volume.get('publishedDate', ''),
                    'description': volume.get('description', ''),
                    'cover_image_url': cover_image,
                    'category': category,
                    'page_count': volume.get('pageCount', 0),
                    'language': volume.get('language', 'en')
                }
            return None
        except Exception as e:
            print(f"Error fetching from Google Books: {e}")
            return None
