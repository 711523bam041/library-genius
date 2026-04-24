# 🚀 Quick Deploy - LibraryGenius

Choose your deployment method:

---

## Option 1: Deploy to Railway (EASIEST - 5 minutes, FREE)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Railway:**
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub"
   - Select your repository

3. **Add MySQL:**
   - Click "+ New" → "Add Database" → "MySQL"
   - Copy connection details

4. **Set Environment Variables:**
   ```
   DB_HOST=<railway-mysql-host>
   DB_USER=root
   DB_PASSWORD=<your-mysql-password>
   DB_NAME=library_management
   FLASK_SECRET_KEY=<generate-a-random-key>
   ```

5. **Done!** Your app is live at `https://your-project.railway.app`

---

## Option 2: Deploy to PythonAnywhere (EASY - 10 minutes, FREE)

1. **Sign up:** https://www.pythonanywhere.com

2. **Upload code** via Git or file upload

3. **Create database** in Databases tab

4. **Configure web app** in Web tab

5. **Set environment variables** and reload

Full guide: See `DEPLOYMENT.md` → Option 2

---

## Option 3: Deploy to VPS (ADVANCED - 30 minutes, $6/month)

**One-command deployment on Ubuntu/Debian:**

```bash
# SSH into your server
ssh user@your-server-ip

# Make deployment script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

The script will:
- ✅ Install all dependencies
- ✅ Set up MySQL database
- ✅ Configure Gunicorn
- ✅ Set up Nginx reverse proxy
- ✅ Create systemd service
- ✅ Start your application

---

## Option 4: Deploy with Docker

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f
```

Your app will be at: `http://localhost:5000`

---

## ⚡ Pre-Deployment Checklist

Before deploying, make sure to:

- [ ] Change default admin password
- [ ] Generate a strong `FLASK_SECRET_KEY`
- [ ] Add your OpenAI API key (optional)
- [ ] Test all features locally
- [ ] Set up database backups
- [ ] Configure HTTPS/SSL

---

## 📚 Full Documentation

Detailed deployment guides for all platforms: **[DEPLOYMENT.md](DEPLOYMENT.md)**

---

## 🆘 Need Help?

Common issues and solutions are in the [DEPLOYMENT.md](DEPLOYMENT.md) troubleshooting section.

---

**Ready to deploy? Choose your platform and follow the steps above!** 🎯
