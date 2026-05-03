# 🚀 VERCEL DEPLOYMENT GUIDE - CertifyMe Backend

**Deployment Service**: Vercel
**Application**: Flask REST API with SQLite
**Status**: Ready for deployment

---

## ⚠️ IMPORTANT NOTE

Vercel is optimized for Node.js/Next.js. For Flask, consider these alternatives:
- **Heroku** (Easy, best for Flask)
- **Railway** (Modern, simple)
- **Render** (Free tier available)
- **PythonAnywhere** (Python-specific)

But if you want Vercel, follow this guide.

---

## 📋 OPTION 1: DEPLOY TO VERCEL (Recommended Alternative)

### Step 1: Convert to Vercel-Compatible Format

Create `vercel.json`:
```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### Step 2: Update app.py

Add this at the very end of `app.py`:
```python
# Vercel serverless function export
app = create_app()
```

### Step 3: Create requirements.txt (Already Done)
```
Flask==2.3.2
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.2
Flask-CORS==4.0.0
Werkzeug==2.3.6
itsdangerous==2.1.2
python-dotenv==1.0.0
```

### Step 4: Install Vercel CLI
```bash
npm install -g vercel
# or
npm i -g vercel
```

### Step 5: Deploy to Vercel
```bash
vercel
```

Follow the prompts:
- Link to GitHub project? Yes
- Deploy to account? Select your account
- Function root directory? ./

---

## 📌 OPTION 2: HEROKU DEPLOYMENT (EASIEST FOR FLASK)

### Step 1: Install Heroku CLI
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Create `Procfile`
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT app:create_app()
```

### Step 3: Add Gunicorn to requirements.txt
```bash
pip install gunicorn
pip freeze > requirements.txt
```

### Step 4: Login to Heroku
```bash
heroku login
```

### Step 5: Create Heroku App
```bash
heroku create certifyme-app
```

### Step 6: Deploy
```bash
git push heroku main
```

---

## 🚀 OPTION 3: RAILWAY DEPLOYMENT (MODERN & EASY)

### Step 1: Go to Railway
Visit: https://railway.app

### Step 2: Connect GitHub
- Click "New Project"
- Click "Deploy from GitHub repo"
- Select your repository
- Click "Deploy"

### Step 3: Configure Environment Variables
```
DATABASE_URL (auto-created)
FLASK_ENV=production
DEBUG=False
```

### Step 4: Done!
Railway automatically detects Python/Flask and deploys.

---

## 📝 BEST PRACTICE: RENDER DEPLOYMENT

### Step 1: Visit Render
https://render.com

### Step 2: Connect GitHub
- Click "New +"
- Select "Web Service"
- Connect to GitHub
- Select repository

### Step 3: Configure
```
Name: certifyme-api
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT app:create_app()
```

### Step 4: Deploy
- Click "Create Web Service"
- Wait for deployment
- Get public URL

---

## ✅ COMPLETE VERCEL SETUP (STEP-BY-STEP)

### Prerequisites
- Node.js installed
- GitHub account with repository
- Vercel account (https://vercel.com)

### Step 1: Add Vercel Configuration Files

Create `vercel.json`:
```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production",
    "DEBUG": "False"
  }
}
```

### Step 2: Update requirements.txt

Add these packages:
```
Flask==2.3.2
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.2
Flask-CORS==4.0.0
Werkzeug==2.3.6
itsdangerous==2.1.2
python-dotenv==1.0.0
gunicorn==21.2.0
```

### Step 3: Modify app.py

Change the last lines from:
```python
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
```

To:
```python
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Step 4: Commit Changes
```bash
cd c:\Projects\CertifyMe
git add vercel.json requirements.txt app.py
git commit -m "Add Vercel deployment configuration"
git push origin main
```

### Step 5: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 6: Deploy
```bash
cd c:\Projects\CertifyMe
vercel login
vercel
```

**Expected Output**:
```
🔗  Connected to https://github.com/sriramselvaraj9/Certify-Me-Project-Assessment
🔨  Building...
✓ Production build generated
✓ Deployment ready!
✓ Live URL: https://certifyme-xxx.vercel.app
```

### Step 7: Configure Environment Variables (Optional)

In Vercel Dashboard:
1. Go to project settings
2. Click "Environment Variables"
3. Add:
   - Key: `FLASK_ENV` | Value: `production`
   - Key: `DEBUG` | Value: `False`

---

## 🔧 VERCEL PYTHON RUNTIME REQUIREMENTS

Update `requirements.txt` with deployment packages:

```
Flask==2.3.2
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.2
Flask-CORS==4.0.0
Werkzeug==2.3.6
itsdangerous==2.1.2
python-dotenv==1.0.0
gunicorn==21.2.0
```

### Install locally first:
```bash
pip install -r requirements.txt
```

---

## 📊 DEPLOYMENT COMPARISON

| Platform | Difficulty | Cost | Best For |
|----------|-----------|------|----------|
| **Vercel** | Medium | Free tier | Node.js/Next.js |
| **Heroku** | Easy | Free (limited) | Flask/Python |
| **Railway** | Easy | Generous free | Modern Python apps |
| **Render** | Easy | Free tier | Quick deployment |
| **PythonAnywhere** | Easy | Free tier | Python-only |

---

## 🎯 RECOMMENDED: HEROKU (EASIEST)

### Quick Heroku Deploy

```bash
# 1. Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# 2. Add Procfile
echo "web: gunicorn -w 4 -b 0.0.0.0:\$PORT app:create_app()" > Procfile

# 3. Add gunicorn to requirements
pip install gunicorn
pip freeze > requirements.txt

# 4. Commit
git add Procfile requirements.txt
git commit -m "Add Heroku configuration"
git push origin main

# 5. Deploy
heroku login
heroku create certifyme-app
git push heroku main

# 6. View logs
heroku logs --tail
```

**Result**: App deployed to `https://certifyme-app.herokuapp.com`

---

## 🚀 QUICK RAILWAY DEPLOY

**Easiest Option** - Just 3 steps:

1. **Visit**: https://railway.app/new
2. **Select**: "Deploy from GitHub repo"
3. **Connect & Deploy**: One click!

Railway automatically:
- Detects Python
- Installs dependencies
- Deploys Flask app
- Provides public URL

**That's it!** No configuration needed.

---

## 💾 DATABASE CONSIDERATIONS

### Current Setup
- **SQLite** (local file-based)
- **Problem**: Vercel deletes files after each deployment
- **Solution**: Use PostgreSQL or MongoDB

### Add PostgreSQL

1. **Using Heroku**:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

2. **Using Railway/Render**:
   - Auto-creates PostgreSQL
   - Connection string provided

3. **Update config.py**:
   ```python
   import os
   
   DATABASE_URL = os.environ.get('DATABASE_URL')
   if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
       DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
   
   class ProductionConfig(Config):
       SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///certifyme.db'
   ```

---

## ✅ DEPLOYMENT CHECKLIST

### Before Deploying
- [ ] All code committed to GitHub
- [ ] requirements.txt updated with all packages
- [ ] vercel.json created (if using Vercel)
- [ ] Procfile created (if using Heroku)
- [ ] Environment variables documented
- [ ] Database strategy decided
- [ ] Tests passing locally

### During Deployment
- [ ] CLI tool installed (Vercel/Heroku)
- [ ] Logged in to service
- [ ] Environment variables configured
- [ ] Build completed successfully
- [ ] No errors in logs

### After Deployment
- [ ] Public URL accessible
- [ ] API endpoints responding
- [ ] Database connected
- [ ] Tests passing on deployed version
- [ ] CORS configured correctly
- [ ] Frontend can access API

---

## 🔗 DEPLOYMENT LINKS

| Service | Link | CLI Command |
|---------|------|------------|
| **Vercel** | https://vercel.com | `vercel login` |
| **Heroku** | https://heroku.com | `heroku login` |
| **Railway** | https://railway.app | Connect GitHub |
| **Render** | https://render.com | Connect GitHub |
| **PythonAnywhere** | https://pythonanywhere.com | Web portal |

---

## 📝 PRODUCTION CONFIGURATION

Update `config.py` for production:

```python
import os

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    
    # Database
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    
    # Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
```

---

## 🎯 RECOMMENDATION

**For Flask, I recommend (in order)**:

1. **🥇 Railway** - Easiest, modern, just connect GitHub
2. **🥈 Heroku** - Proven, reliable, free tier limited
3. **🥉 Render** - Simple, good free tier, reliable

**Vercel** is designed for Node.js. While possible, the above are better.

---

## 📞 WHICH DEPLOYMENT?

**Choose based on:**

| If You Want | Choose |
|-------------|--------|
| Easiest setup | Railway ✅ |
| Most reliable | Heroku |
| Free tier | Render or Railway |
| Vercel specifically | See Step-by-Step above |
| Production ready | Railway + PostgreSQL |

---

**Ready to deploy?** Choose a platform from the options above and follow the guide! 🚀
