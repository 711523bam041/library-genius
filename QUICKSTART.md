# Quick Start Guide - LibraryGenius

## 🚀 Get Started in 3 Steps

### Step 1: Setup Database

Open MySQL and run:
```bash
mysql -u root -p
```

Then execute:
```sql
source schema.sql
```

Or manually copy-paste the contents of `schema.sql` into MySQL.

### Step 2: Configure .env File

Open `.env` and update:
```env
DB_PASSWORD=your_mysql_password
FLASK_SECRET_KEY=any-random-secret-key
OPENAI_API_KEY=your-openai-key (optional)
```

### Step 3: Run the App

```bash
python app.py
```

Open browser: **http://localhost:5000**

Login with:
- Username: `admin`
- Password: `admin123`

---

## 📚 Quick Tour

1. **Dashboard** - View statistics and recent activity
2. **Books** - Browse and search your catalog
3. **Add Book** - Add books manually, scan ISBN, or fetch from Google
4. **Borrow** - Issue books to students
5. **Return** - Process returns with automatic fine calculation

---

## ✨ Key Features to Try

### ISBN Scanning
1. Go to "Add Book"
2. Click "Upload Barcode Image" 
3. Upload any book barcode photo
4. Watch as ISBN is auto-detected!

### Google Books Integration
1. Enter any ISBN (e.g., 9780143127550)
2. Click "Fetch"
3. All book details auto-filled!

### AI Summary Generation
1. Enter book title and author
2. Click "Generate Summary"
3. AI creates a professional summary!

---

## 🆘 Common Issues

**Can't connect to database?**
- Make sure MySQL is running
- Check password in `.env`

**ISBN scan not working?**
- Install Tesseract OCR
- Use clear, well-lit barcode images

**AI features not working?**
- Add your OpenAI API key to `.env`
- Features work without it but show warnings

---

## 📖 Full Documentation

See `SETUP.md` for complete documentation, API reference, and troubleshooting.

---

**Enjoy your AI-powered library system! 🎉**
