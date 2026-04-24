# Deployment Guide - LibraryGenius

This guide covers multiple deployment options for your AI-Powered Library Management System.

---

## 📋 Pre-Deployment Checklist

### 1. Security Updates

**Change Default Admin Password:**
```sql
-- Connect to MySQL and run:
USE library_management;
UPDATE users SET password_hash = 'new_hashed_password' WHERE username = 'admin';
```

**Generate a Strong Flask Secret Key:**
```python
import secrets
print(secrets.token_hex(32))
```

Update `.env` with the new secret key.

### 2. Environment Variables for Production

Create a production `.env` file:
```env
# Database (use production MySQL credentials)
DB_HOST=your-production-db-host
DB_USER=your-db-user
DB_PASSWORD=your-secure-password
DB_NAME=library_management
DB_PORT=3306

# Flask
FLASK_SECRET_KEY=your-generated-secret-key-here

# API Keys
OPENAI_API_KEY=your-openai-api-key
GOOGLE_BOOKS_API_KEY=your-google-books-api-key

# Production Settings
FLASK_ENV=production
DEBUG=False
```

### 3. Update config.py for Production

```python
# Add to config.py
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
FLASK_ENV = os.getenv('FLASK_ENV', 'production')
```

### 4. Database Migration

Run the schema fix on your production database:
```bash
python fix_schema.py
python fix_all_schema.py
```

---

## 🚀 Deployment Option 1: Railway (Easiest - FREE)

Railway is perfect for Flask apps with MySQL.

### Step 1: Prepare Your Project

1. **Create `Procfile`** (no extension):
```
web: gunicorn app:app
```

2. **Create `runtime.txt`**:
```
python-3.13.0
```

3. **Update `requirements.txt`** - add:
```
gunicorn
```

### Step 2: Deploy to Railway

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Connect your repository
4. Railway will auto-detect Python

### Step 3: Add MySQL Database

1. In Railway dashboard, click "+ New"
2. Select "Add Database" → "MySQL"
3. Wait for it to provision
4. Copy the connection details

### Step 4: Configure Environment Variables

In Railway dashboard → Variables:
```
DB_HOST=your-railway-mysql-host
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_NAME=library_management
DB_PORT=3306
FLASK_SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
```

### Step 5: Deploy

Railway auto-deploys on push. Your app will be at:
```
https://your-project.railway.app
```

---

## 🚀 Deployment Option 2: PythonAnywhere (FREE)

### Step 1: Create Account

1. Go to https://www.pythonanywhere.com
2. Sign up for a free account

### Step 2: Upload Your Code

**Option A: Using Git**
```bash
# In PythonAnywhere Bash console:
git clone https://github.com/yourusername/smart-lib-copy.git
cd smart-lib-copy
pip install -r requirements.txt --user
```

**Option B: Using File Upload**
1. Go to Files tab
2. Upload your project as a zip
3. Extract it

### Step 3: Configure MySQL

1. Go to Databases tab
2. Set a MySQL password
3. Create database:
```sql
CREATE DATABASE yourusername$library_management;
```

4. Import your schema:
```bash
mysql -u yourusername -p yourusername$library_management < schema.sql
```

### Step 4: Configure Web App

1. Go to Web tab
2. Click "Add a new web app"
3. Select "Manual configuration" → Python 3.10+
4. Set paths:
   - Source code: `/home/yourusername/smart-lib-copy`
   - Working directory: `/home/yourusername/smart-lib-copy`

5. Configure WSGI file:
```python
import sys
path = '/home/yourusername/smart-lib-copy'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

### Step 5: Set Environment Variables

In Web tab → "Set environment variables":
```
DB_HOST=yourusername.mysql.pythonanywhere-services.com
DB_USER=yourusername
DB_PASSWORD=your-mysql-password
DB_NAME=yourusername$library_management
FLASK_SECRET_KEY=your-secret-key
```

### Step 6: Install Dependencies

In Bash console:
```bash
pip install -r requirements.txt --user
```

### Step 7: Reload Web App

Click the green "Reload" button in Web tab.

Your app will be at:
```
https://yourusername.pythonanywhere.com
```

---

## 🚀 Deployment Option 3: Heroku

### Step 1: Install Heroku CLI

Download from: https://devcenter.heroku.com/articles/heroku-cli

### Step 2: Prepare Files

**Create `Procfile`:**
```
web: gunicorn app:app
```

**Create `runtime.txt`:**
```
python-3.13.0
```

### Step 3: Deploy

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-library-app

# Add PostgreSQL or use ClearDB MySQL addon
heroku addons:create cleardb:ignite

# Set environment variables
heroku config:set FLASK_SECRET_KEY=your-secret-key
heroku config:set OPENAI_API_KEY=your-openai-key
heroku config:set DB_HOST=your-cleardb-host
heroku config:set DB_USER=your-cleardb-user
heroku config:set DB_PASSWORD=your-cleardb-password
heroku config:set DB_NAME=heroku_db

# Deploy
git push heroku main

# Run database migrations
heroku run bash
# Inside bash:
mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME < schema.sql
```

---

## 🚀 Deployment Option 4: VPS (DigitalOcean, AWS, etc.)

### Step 1: Set Up Server

**Ubuntu/Debian Server:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3 python3-pip python3-venv -y

# Install MySQL
sudo apt install mysql-server -y

# Install Nginx
sudo apt install nginx -y
```

### Step 2: Configure MySQL

```bash
# Secure MySQL
sudo mysql_secure_installation

# Create database and user
sudo mysql -u root
```

```sql
CREATE DATABASE library_management;
CREATE USER 'library_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON library_management.* TO 'library_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

```bash
# Import schema
mysql -u library_user -p library_management < schema.sql
```

### Step 3: Deploy Application

```bash
# Create app directory
sudo mkdir -p /var/www/library-app
cd /var/www/library-app

# Clone your repo
git clone https://github.com/yourusername/smart-lib-copy.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn
```

### Step 4: Configure Environment

```bash
# Create .env file
sudo nano .env
```

Add your production environment variables.

### Step 5: Configure Gunicorn

Create `gunicorn_config.py`:
```python
bind = "127.0.0.1:8000"
workers = 3
timeout = 120
accesslog = "/var/log/library-app/access.log"
errorlog = "/var/log/library-app/error.log"
```

### Step 6: Create Systemd Service

```bash
sudo nano /etc/systemd/system/library-app.service
```

Add:
```ini
[Unit]
Description=LibraryGenius Flask Application
After=network.target mysql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/library-app
Environment="PATH=/var/www/library-app/venv/bin"
ExecStart=/var/www/library-app/venv/bin/gunicorn -c gunicorn_config.py app:app

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable library-app
sudo systemctl start library-app
sudo systemctl status library-app
```

### Step 7: Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/library-app
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/library-app/static;
        expires 30d;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/library-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 8: SSL Certificate (HTTPS)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is set up automatically
```

---

## 🚀 Deployment Option 5: Docker

### Step 1: Create Dockerfile

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create logs directory
RUN mkdir -p logs

# Expose port
EXPOSE 5000

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "app:app"]
```

### Step 2: Create docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DB_HOST=db
      - DB_USER=root
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_NAME=library_management
      - FLASK_SECRET_KEY=${FLASK_SECRET_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - db
    volumes:
      - ./logs:/app/logs

  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=${DB_PASSWORD}
      - MYSQL_DATABASE=library_management
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./schema.sql:/docker-entrypoint-initdb.d/schema.sql

volumes:
  mysql_data:
```

### Step 3: Run with Docker

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 📊 Post-Deployment Steps

### 1. Import Sample Data (Optional)

```bash
mysql -u username -p library_management < sample_data.sql
```

### 2. Test All Features

- ✅ Login/Register
- ✅ Add books
- ✅ Search books
- ✅ Borrow/Return
- ✅ Dashboard statistics
- ✅ AI features (if API key configured)

### 3. Set Up Backups

**MySQL Backup Script:**
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u username -p'password' library_management > backup_$DATE.sql
```

**Cron job for daily backups:**
```bash
0 2 * * * /path/to/backup.sh
```

### 4. Monitor Logs

```bash
# Flask logs
tail -f logs/app.log

# Gunicorn logs
tail -f /var/log/library-app/error.log

# Nginx logs
tail -f /var/log/nginx/error.log
```

### 5. Set Up Monitoring

Consider using:
- **Sentry** for error tracking
- **New Relic** for performance monitoring
- **Uptime Robot** for uptime monitoring

---

## 🔒 Security Best Practices

1. **Use HTTPS** - Always use SSL certificates
2. **Strong Passwords** - For database and admin accounts
3. **Environment Variables** - Never commit `.env` to Git
4. **Regular Updates** - Keep dependencies updated
5. **Firewall** - Only open necessary ports (80, 443)
6. **Database Access** - Restrict to localhost only
7. **Rate Limiting** - Prevent API abuse
8. **Backups** - Regular automated backups

---

## 🆘 Troubleshooting

### App Won't Start
```bash
# Check logs
journalctl -u library-app -f

# Check if port is in use
sudo lsof -i :5000
```

### Database Connection Failed
```bash
# Test MySQL connection
mysql -u username -p -h hostname database_name

# Check MySQL status
sudo systemctl status mysql
```

### Static Files Not Loading
```nginx
# In Nginx config, ensure correct path
location /static {
    alias /var/www/library-app/static;
}
```

---

## 💰 Cost Comparison

| Platform | Cost | Difficulty | Best For |
|----------|------|------------|----------|
| **Railway** | FREE (with limits) | Easy | Quick deployment |
| **PythonAnywhere** | FREE | Easy | Beginners |
| **Heroku** | FREE tier discontinued | Medium | Testing |
| **DigitalOcean** | $6/month | Medium | Production |
| **AWS** | $5-10/month | Hard | Enterprise |
| **VPS (Self)** | $5/month | Hard | Full control |

---

## 🎯 Recommended for You

**For testing/demo:** Railway or PythonAnywhere (FREE)

**For production:** DigitalOcean VPS ($6/month)

**For enterprise:** AWS or dedicated server

---

**Need help with a specific deployment option? Let me know which one you prefer!** 🚀
