#!/bin/bash
# Quick Deployment Script for LibraryGenius
# Run this on your production server (Ubuntu/Debian)

echo "=================================="
echo "LibraryGenius Deployment Script"
echo "=================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Update system
echo -e "${YELLOW}Updating system...${NC}"
sudo apt update && sudo apt upgrade -y

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
sudo apt install -y python3 python3-pip python3-venv mysql-server nginx git

# Create application directory
echo -e "${YELLOW}Setting up application directory...${NC}"
sudo mkdir -p /var/www/library-app
sudo chown $USER:$USER /var/www/library-app
cd /var/www/library-app

# Clone repository (replace with your repo URL)
echo -e "${YELLOW}Cloning repository...${NC}"
echo "Enter your Git repository URL (or press Enter to skip if files are already here):"
read GIT_URL

if [ ! -z "$GIT_URL" ]; then
    git clone $GIT_URL .
fi

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Configure MySQL
echo -e "${YELLOW}Configuring MySQL...${NC}"
echo "Enter MySQL root password:"
read -s MYSQL_ROOT_PASSWORD
echo "Enter application database user password:"
read -s DB_PASSWORD

mysql -u root -p"$MYSQL_ROOT_PASSWORD" <<EOF
CREATE DATABASE IF NOT EXISTS library_management;
CREATE USER IF NOT EXISTS 'library_user'@'localhost' IDENTIFIED BY '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON library_management.* TO 'library_user'@'localhost';
FLUSH PRIVILEGES;
EOF

# Import schema
echo -e "${YELLOW}Importing database schema...${NC}"
mysql -u library_user -p"$DB_PASSWORD" library_management < schema.sql

# Create .env file
echo -e "${YELLOW}Creating .env file...${NC}"
cat > .env <<EOF
DB_HOST=localhost
DB_USER=library_user
DB_PASSWORD=$DB_PASSWORD
DB_NAME=library_management
DB_PORT=3306
FLASK_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
FLASK_ENV=production
DEBUG=False
EOF

echo "Enter your OpenAI API key (or press Enter to skip):"
read OPENAI_KEY
if [ ! -z "$OPENAI_KEY" ]; then
    echo "OPENAI_API_KEY=$OPENAI_KEY" >> .env
fi

# Configure Gunicorn
echo -e "${YELLOW}Configuring Gunicorn...${NC}"
cat > gunicorn_config.py <<EOF
bind = "127.0.0.1:8000"
workers = 3
timeout = 120
accesslog = "/var/log/library-app/access.log"
errorlog = "/var/log/library-app/error.log"
EOF

# Create log directory
sudo mkdir -p /var/log/library-app
sudo chown www-data:www-data /var/log/library-app

# Create systemd service
echo -e "${YELLOW}Creating systemd service...${NC}"
sudo tee /etc/systemd/system/library-app.service > /dev/null <<EOF
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
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Set proper permissions
sudo chown -R www-data:www-data /var/www/library-app
sudo chmod -R 755 /var/www/library-app

# Enable and start service
echo -e "${YELLOW}Starting application...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable library-app
sudo systemctl start library-app

# Configure Nginx
echo -e "${YELLOW}Configuring Nginx...${NC}"
echo "Enter your domain name (or press Enter for localhost):"
read DOMAIN_NAME

if [ -z "$DOMAIN_NAME" ]; then
    DOMAIN_NAME="_"
fi

sudo tee /etc/nginx/sites-available/library-app > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN_NAME;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static {
        alias /var/www/library-app/static;
        expires 30d;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/library-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

echo -e "${GREEN}=================================="
echo "Deployment Complete!"
echo "=================================="
echo -e "${GREEN}Application URL: http://$DOMAIN_NAME${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Test your application"
echo "2. Set up SSL: sudo certbot --nginx -d $DOMAIN_NAME"
echo "3. Change default admin password"
echo "4. Set up database backups"
echo ""
echo -e "${YELLOW}Useful commands:${NC}"
echo "View logs: sudo journalctl -u library-app -f"
echo "Restart app: sudo systemctl restart library-app"
echo "Check status: sudo systemctl status library-app"
echo ""
