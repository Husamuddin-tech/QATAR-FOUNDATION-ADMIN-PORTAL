# 🚀 VERCEL DEPLOYMENT - STEP BY STEP

**Platform**: Vercel
**Time**: 15 minutes
**Difficulty**: Medium
**Result**: Live API on vercel.app

---

## ⚠️ IMPORTANT

Vercel is optimized for **Node.js/Next.js**, not Python/Flask. 

**Better alternatives**: Railway, Render, Heroku (easier for Flask)

But if you need Vercel, follow this guide.

---

## 📋 STEP 1: PREPARE FILES

### Create `vercel.json`
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

Already created ✓

### Update `requirements.txt`

Add gunicorn (for production):
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

---

## 📋 STEP 2: COMMIT TO GITHUB

```bash
cd c:\Projects\CertifyMe
git add vercel.json requirements.txt
git commit -m "Add Vercel deployment configuration"
git push origin main
```

**Expected Output**:
```
✓ Files added
✓ Committed
✓ Pushed to GitHub
```

---

## 📋 STEP 3: INSTALL VERCEL CLI

### Windows (PowerShell)
```bash
npm install -g vercel
```

### Verify Installation
```bash
vercel --version
```

---

## 📋 STEP 4: DEPLOY TO VERCEL

### Login to Vercel
```bash
vercel login
```

Browser opens → Sign up/Login with GitHub → Authorize

### Deploy
```bash
cd c:\Projects\CertifyMe
vercel
```

**Interactive Setup**:
```
? Set up and deploy "~\Projects\CertifyMe"? (y/N)
  → Press Y

? Which scope do you want to deploy to?
  → Select your account

? Link to existing project? (y/N)
  → Press N (for first deployment)

? What's your project's name?
  → certifyme-api

? In which directory is your code located?
  → Press Enter (current directory)

🔨 Building...
✓ Build successful
✓ Deployment complete!

🎉 Your app is live!
🌐 https://certifyme-api-xxxx.vercel.app
```

---

## ✅ VERIFICATION

Your app is now deployed! Test it:

### Test Health Check
```bash
curl https://certifyme-api-xxxx.vercel.app/health
```

**Expected Response**:
```json
{"status": "healthy"}
```

### Test API Root
```bash
curl https://certifyme-api-xxxx.vercel.app/api
```

**Expected Response**:
```json
{"message": "CertifyMe Backend API is running"}
```

---

## 🔧 ENVIRONMENT VARIABLES (Optional)

In Vercel Dashboard:

1. Go to Settings
2. Click "Environment Variables"
3. Add variables:
   ```
   FLASK_ENV = production
   DEBUG = False
   ```

---

## 📊 DEPLOYMENT INFO

**URL**: https://certifyme-api-xxxx.vercel.app
**Status**: Active
**Logs**: `vercel logs <project-id>`

### View Logs
```bash
vercel logs
```

### Redeploy
```bash
vercel --prod
```

### List Deployments
```bash
vercel list
```

---

## 🔄 AUTO-DEPLOYMENT

**After first deployment**, just push to GitHub:

```bash
git push origin main
```

Vercel automatically redeploys! ✓

---

## ⚡ PRODUCTION CONFIGURATION

Update `config.py`:

```python
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/certifyme.db'
    
    # Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
```

---

## 🐛 TROUBLESHOOTING

### Build Fails: "ModuleNotFoundError"
```bash
# Ensure requirements.txt has all packages
pip install -r requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push origin main
vercel --prod
```

### API Returns 404
```bash
# Check vercel.json configuration
# Ensure app.py exports app correctly
# Verify: app = create_app() at module level
```

### Database Issues
```bash
# SQLite on Vercel may not persist
# Solution: Use PostgreSQL from provider
# Or add database connection string to environment variables
```

### Custom Domain
```
Vercel Dashboard → Project Settings → Domains → Add Custom Domain
```

---

## 📱 API ENDPOINTS LIVE

Once deployed, all endpoints are live:

### Authentication
```
POST   https://certifyme-api-xxxx.vercel.app/api/auth/signup
POST   https://certifyme-api-xxxx.vercel.app/api/auth/login
POST   https://certifyme-api-xxxx.vercel.app/api/auth/forgot
POST   https://certifyme-api-xxxx.vercel.app/api/auth/logout
```

### Opportunities
```
GET    https://certifyme-api-xxxx.vercel.app/api/opportunities
POST   https://certifyme-api-xxxx.vercel.app/api/opportunities
PUT    https://certifyme-api-xxxx.vercel.app/api/opportunities/<id>/edit
DELETE https://certifyme-api-xxxx.vercel.app/api/opportunities/<id>
```

---

## 🎯 COMMON ISSUES & SOLUTIONS

| Issue | Solution |
|-------|----------|
| Port error | Vercel manages ports automatically |
| Database error | Use environment variables for DB URL |
| Timeout | Check function timeout settings |
| CORS error | Verify CORS configuration in app.py |
| 500 error | Check Vercel logs: `vercel logs` |

---

## 📞 DEPLOYMENT CHECKLIST

- [x] vercel.json created
- [x] requirements.txt updated
- [x] GitHub repository updated
- [x] Vercel CLI installed
- [x] vercel login executed
- [x] vercel deploy command run
- [x] Public URL obtained
- [x] Health endpoint tested
- [x] API responding correctly
- [x] Auto-deployment working

---

## 🚀 VERCEL DASHBOARD

Access at: https://vercel.com/dashboard

### View:
- Deployments
- Environment variables
- Function logs
- Analytics
- Custom domains
- Team settings

---

## 📈 AFTER DEPLOYMENT

1. **Share URL**: 
   ```
   Your API is live at:
   https://certifyme-api-xxxx.vercel.app
   ```

2. **Update Frontend**:
   ```javascript
   const API_URL = 'https://certifyme-api-xxxx.vercel.app'
   ```

3. **Connect Frontend**: Frontend can now call deployed backend

4. **Monitor**: Check Vercel dashboard for logs/errors

---

## 🎉 YOU'RE DONE!

Your CertifyMe Backend is now **live on Vercel**! 🚀

**Your API URL**: https://certifyme-api-xxxx.vercel.app

**Next Steps**:
- Test endpoints
- Update frontend API URL
- Deploy frontend
- Share with reviewers

---

**Questions?** Check:
- Vercel docs: https://vercel.com/docs
- Flask deployment: https://flask.palletsprojects.com/en/2.3.x/deploying/
- Troubleshooting logs: `vercel logs --follow`
