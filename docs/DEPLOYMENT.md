# 🚀 Deployment Guide

## Quick Deployment Checklist

### ✅ Pre-Deployment
- [ ] All features tested locally
- [ ] Environment variables configured
- [ ] Build passes without errors
- [ ] Database configured (if using)
- [ ] API keys secured

---

## 🎯 Deployment Options

### Option 1: Vercel (Recommended for Frontend)

**Frontend Deployment**:
```bash
cd frontend
npm run build
vercel --prod
```

**Environment Variables** (Add in Vercel dashboard):
```
NEXT_PUBLIC_API_URL=https://your-backend.com
```

**Steps**:
1. Install Vercel CLI: `npm i -g vercel`
2. Login: `vercel login`
3. Deploy: `vercel --prod`
4. Done! ✅

---

### Option 2: AWS/DigitalOcean (Backend)

**Backend Deployment**:
```bash
cd backend
pip install -r requirements.txt
gunicorn main:app --workers 4 --bind 0.0.0.0:8000
```

**Environment Setup**:
```bash
export PORT=8000
export PYTHON_ENV=production
```

---

### Option 3: Docker (Full Stack)

**Create Docker Compose** (coming soon):
```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
```

---

## 📋 Environment Variables

### Frontend (.env.local):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env):
```
PORT=8000
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

---

## 🧪 Testing Before Deployment

```bash
# Frontend
cd frontend
npm run build
npm start

# Backend
cd backend
pytest
python -m uvicorn main:app --port 8000
```

---

## 🔒 Security Checklist

- [ ] Environment variables not in code
- [ ] CORS properly configured
- [ ] API rate limiting enabled
- [ ] HTTPS enforced
- [ ] Secrets in vault/secure storage

---

## 📊 Post-Deployment

1. **Monitor Logs**
2. **Check Performance**
3. **Test All Features**
4. **Setup Alerts**
5. **Document API endpoints**

---

## 🆘 Troubleshooting

**Build Fails**:
```bash
rm -rf node_modules .next
npm install
npm run build
```

**API Not Connecting**:
- Check CORS settings
- Verify API URL in environment
- Check firewall/ports

---

Last Updated: October 29, 2025
