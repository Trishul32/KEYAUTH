# KeyAuth Cloud Deployment Guide

This guide covers deploying KeyAuth to various cloud platforms with PostgreSQL.

## Database Configuration

The app now supports both SQLite (local) and PostgreSQL (production):

```bash
# Local development (default)
DATABASE_URL=sqlite://db.sqlite3

# PostgreSQL production
DATABASE_URL=postgresql://user:password@host:5432/database_name
```

---

## Option 1: Railway (Recommended - Easiest)

Railway offers the easiest deployment with free PostgreSQL.

### Steps:

1. **Push to GitHub** (if not already)

2. **Deploy on Railway:**
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your KeyAuth repository
   - Railway auto-detects the Dockerfile

3. **Add PostgreSQL:**
   - Click "New" → "Database" → "PostgreSQL"
   - Railway automatically sets `DATABASE_URL`

4. **Set Environment Variables:**
   - Go to your service → Variables
   - Add:
     ```
     SMTP_EMAIL=your_email@gmail.com
     SMTP_PASSWORD=your_app_password
     ```

5. **Deploy!** Railway handles the rest.

**Free Tier:** 500 hours/month, 1GB PostgreSQL

---

## Option 2: Render

### Steps:

1. **Push to GitHub**

2. **Deploy the render.yaml:**
   - Go to [render.com](https://render.com)
   - Click "New" → "Blueprint"
   - Connect your repository
   - Render reads `render.yaml` and creates:
     - PostgreSQL database
     - Web service

3. **Set Environment Variables:**
   - Go to your web service → Environment
   - Add `SMTP_EMAIL` and `SMTP_PASSWORD`

**Free Tier:** 750 hours/month, free PostgreSQL (90-day expiry)

---

## Option 3: Heroku

### Steps:

1. **Install Heroku CLI:**
   ```bash
   # Windows
   winget install Heroku.HerokuCLI
   ```

2. **Login and Create App:**
   ```bash
   heroku login
   heroku create keyauth-app
   ```

3. **Add PostgreSQL:**
   ```bash
   heroku addons:create heroku-postgresql:essential-0
   ```

4. **Set Config Vars:**
   ```bash
   heroku config:set SMTP_EMAIL=your_email@gmail.com
   heroku config:set SMTP_PASSWORD=your_app_password
   ```

5. **Deploy:**
   ```bash
   git push heroku main
   ```

**Note:** Heroku no longer has a free tier. Starts at ~$5/month.

---

## Option 4: Docker (Any Cloud Provider)

Works with AWS, GCP, Azure, DigitalOcean, etc.

### Build and Run:

```bash
# Build image
docker build -t keyauth .

# Run with PostgreSQL connection
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e SMTP_EMAIL=your_email@gmail.com \
  -e SMTP_PASSWORD=your_app_password \
  keyauth
```

### Docker Compose (Local Testing with PostgreSQL):

```bash
docker-compose up --build
```

This starts:
- PostgreSQL on port 5432
- KeyAuth API on port 8000

---

## Option 5: Fly.io

### Steps:

1. **Install flyctl:**
   ```bash
   # Windows
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. **Deploy:**
   ```bash
   fly launch
   fly postgres create
   fly postgres attach <postgres-app-name>
   fly secrets set SMTP_EMAIL=your_email@gmail.com
   fly secrets set SMTP_PASSWORD=your_app_password
   fly deploy
   ```

**Free Tier:** 3 shared VMs, free PostgreSQL

---

## Post-Deployment Checklist

1. ✅ Test the API: `https://your-app-url.com/`
2. ✅ Test registration: `POST /register`
3. ✅ Verify database connection in logs
4. ✅ Update frontend URLs to point to your deployed API
5. ✅ Update CORS origins in `main.py` for production

---

## Updating CORS for Production

Edit `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-domain.com",
        "chrome-extension://your-extension-id"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Common Issues

### "relation does not exist" error
Tortoise ORM creates tables automatically on first run. If you see this error, restart the service.

### Connection timeout
Ensure your database allows connections from your app's IP. Check firewall/security group settings.

### "postgres://" vs "postgresql://"
Some providers use `postgres://`. The app automatically converts this to `postgresql://` for asyncpg compatibility.
