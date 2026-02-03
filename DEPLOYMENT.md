# 🚀 CropGuard - Deployment Guide

## 📦 Deploy to GitHub

### Step 1: Initialize Git Repository

```bash
cd D:\Hack\N1\CropGuard
git init
git add .
git commit -m "Initial commit: CropGuard crop health monitoring system"
```

### Step 2: Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `CropGuard`
3. Description: `Satellite-based crop health monitoring using Sentinel-2 imagery and NDVI analysis`
4. Choose: **Public** (for free Streamlit deployment)
5. **Don't** initialize with README (we already have one)
6. Click "Create repository"

### Step 3: Push to GitHub

```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/CropGuard.git
git branch -M main
git push -u origin main
```

---

## ☁️ Deploy to Streamlit Cloud (Free!)

### Prerequisites
- GitHub account (done above)
- Streamlit Cloud account (free)

### Step 1: Sign Up for Streamlit Cloud

1. Go to: https://streamlit.io/cloud
2. Click "Sign up"
3. Sign in with GitHub
4. Authorize Streamlit

### Step 2: Deploy App

1. Click "New app"
2. Select your repository: `YOUR_USERNAME/CropGuard`
3. Branch: `main`
4. Main file path: `app.py`
5. Click "Deploy!"

### Step 3: Add Secrets (Optional)

If you want to pre-configure credentials:

1. Go to app settings (⚙️)
2. Click "Secrets"
3. Add:
   ```toml
   SENTINEL_CLIENT_ID = "your_client_id"
   SENTINEL_CLIENT_SECRET = "your_client_secret"
   ```

Then update `app.py` to read from secrets:
```python
import streamlit as st

# Try to load from secrets first
try:
    client_id = st.secrets.get("SENTINEL_CLIENT_ID", "")
    client_secret = st.secrets.get("SENTINEL_CLIENT_SECRET", "")
except:
    client_id = ""
    client_secret = ""
```

---

## 🌐 Your Deployed App URL

After deployment, your app will be available at:
```
https://YOUR_USERNAME-cropguard-app-RANDOM.streamlit.app
```

Example:
```
https://johndoe-cropguard-app-abc123.streamlit.app
```

---

## 🔄 Update Deployed App

Whenever you make changes:

```bash
git add .
git commit -m "Description of changes"
git push
```

Streamlit Cloud will **automatically redeploy** within 1-2 minutes!

---

## 📊 Alternative Deployment Options

### 1. Heroku (Free Tier)

**Procfile:**
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**Deploy:**
```bash
heroku create cropguard-app
git push heroku main
```

### 2. Docker

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

**Build & Run:**
```bash
docker build -t cropguard .
docker run -p 8501:8501 cropguard
```

### 3. AWS EC2

1. Launch EC2 instance (Ubuntu)
2. Install Python and dependencies
3. Clone repository
4. Run with `streamlit run app.py`
5. Configure security group for port 8501

### 4. Google Cloud Run

```bash
gcloud run deploy cropguard \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 🔒 Security Best Practices

### 1. Never Commit Credentials

✅ Use `.env` file (already in `.gitignore`)
✅ Use Streamlit secrets
✅ Use environment variables

❌ Don't hardcode in `app.py`
❌ Don't commit `.env` file

### 2. Environment Variables

For local development:
```bash
# Create .env file
SENTINEL_CLIENT_ID=your_id
SENTINEL_CLIENT_SECRET=your_secret
```

Update `app.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("SENTINEL_CLIENT_ID", "")
client_secret = os.getenv("SENTINEL_CLIENT_SECRET", "")
```

---

## 📈 Monitoring & Analytics

### Streamlit Cloud Dashboard

- View app usage
- Check logs
- Monitor performance
- See error reports

### Google Analytics (Optional)

Add to `app.py`:
```python
# Add Google Analytics tracking
st.markdown("""
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
""", unsafe_allow_html=True)
```

---

## 🐛 Troubleshooting Deployment

### "Module not found" error
→ Check `requirements.txt` has all dependencies
→ Run `pip freeze > requirements.txt` locally

### "Port already in use"
→ Streamlit Cloud handles this automatically
→ For local: use `--server.port=8502`

### "Out of memory"
→ Reduce area size limit in `config.py`
→ Optimize image processing

### "Slow loading"
→ Add caching with `@st.cache_data`
→ Reduce default area size

---

## 🎯 Post-Deployment Checklist

- [ ] App loads successfully
- [ ] Map displays correctly
- [ ] Drawing tools work
- [ ] Manual input works
- [ ] Search works
- [ ] Analysis runs successfully
- [ ] Results display properly
- [ ] Mobile responsive
- [ ] Share link with others

---

## 🌟 Promote Your App

### Share on Social Media

**Twitter/X:**
```
🌾 Just deployed CropGuard - a free satellite-based crop health monitoring tool!

✨ Features:
📍 Interactive map with GPS
🛰️ Real Sentinel-2 data
🧮 NDVI analysis
📊 Health classification

Try it: [YOUR_URL]

#AgTech #RemoteSensing #OpenSource
```

**LinkedIn:**
```
Excited to share CropGuard - an open-source crop health monitoring system using Sentinel-2 satellite imagery!

Built with Python, Streamlit, and the Sentinel Hub API, it provides:
- Interactive map-based area selection
- Automated NDVI computation
- 3-tier health classification
- Real-time satellite data processing

Perfect for farmers, agronomists, and researchers.

Live demo: [YOUR_URL]
GitHub: [YOUR_REPO]
```

### Add Badges to README

```markdown
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
```

---

## 📞 Support

**Issues?**
- Check Streamlit Cloud logs
- Review GitHub Issues
- Check Sentinel Hub status

**Questions?**
- Streamlit Community Forum
- Stack Overflow
- GitHub Discussions

---

**🎉 Your app is now live and accessible worldwide!**

Share the link and help farmers monitor their crops! 🌾
