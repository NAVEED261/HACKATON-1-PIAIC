# 🚀 Quick Start Guide - Physical AI & Humanoid Robotics

**Project Status:** ✅ Code deployed to GitHub! Now ready for final deployment steps.

---

## 📍 YOUR URLS

### Frontend (GitHub Pages)
**URL:** https://naveed261.github.io/HACKATON-1-PIAIC/

**Status:** 🔄 Deploying now via GitHub Actions (check: https://github.com/NAVEED261/HACKATON-1-PIAIC/actions)

**Expected:** Live in 2-3 minutes after workflow completes

### Backend (Needs Vercel Deployment)
**Current:** Not deployed yet
**Target:** Will be on Vercel after you complete Step 2 below

---

## ⚡ 3 STEPS TO COMPLETE DEPLOYMENT

### Step 1: Wait for GitHub Pages (2-3 minutes)
1. Go to: https://github.com/NAVEED261/HACKATON-1-PIAIC/actions
2. Wait for "pages build and deployment" to complete (green checkmark)
3. Visit: https://naveed261.github.io/HACKATON-1-PIAIC/
4. ✅ Frontend is live!

### Step 2: Deploy Backend to Vercel (5 minutes)
1. Go to: https://vercel.com/
2. Sign up/Login with GitHub
3. Click "Import Project"
4. Select: `NAVEED261/HACKATON-1-PIAIC`
5. **IMPORTANT - Configure:**
   - **Root Directory:** `apps/backend`
   - **Framework Preset:** Other
   - **Build Command:** Leave empty
   - **Output Directory:** Leave empty

6. **Add Environment Variables:**
   ```
   OPENAI_API_KEY=your-openai-api-key-here
   DATABASE_URL=postgresql://username:password@host/database?sslmode=require
   QDRANT_HOST=https://your-cluster.cloud.qdrant.io
   QDRANT_API_KEY=your-qdrant-api-key
   SECRET_KEY=6vCP5y2dqD-IjLV6pZ1SOuRKKxPMS-D15AQm2OxOZdQ
   ALGORITHM=HS256
   ```

   ⚠️ **CRITICAL:** Use your REAL API keys here (the ones in your .env file locally)

7. Click "Deploy"
8. Wait 2-3 minutes
9. Copy your backend URL (e.g., `https://your-app.vercel.app`)

### Step 3: Connect Frontend to Backend (3 minutes)

After you get your Vercel backend URL:

1. Create file: `apps/book-ui/.env.production`
2. Add this line:
   ```
   REACT_APP_BACKEND_URL=https://your-actual-vercel-url.vercel.app
   ```
3. Commit and push:
   ```bash
   git add apps/book-ui/.env.production
   git commit -m "Add production backend URL"
   git push origin master
   ```
4. Wait 2 minutes for GitHub Pages to redeploy
5. ✅ Frontend now connected to backend!

### Step 4: Ingest Book Content (5 minutes)

Run locally to populate your RAG database:

```bash
cd scripts
python ingest_book.py
```

Wait for completion (3-5 minutes). You should see:
```
✅ Successfully ingested 45+ chunks
```

---

## 🎯 FINAL CHECKLIST

After completing all steps:

- [ ] Frontend live at: https://naveed261.github.io/HACKATON-1-PIAIC/
- [ ] Backend live on Vercel (your URL)
- [ ] Chatbot button visible (purple, bottom-right)
- [ ] Click chatbot → Ask "What is Physical AI?" → Get response
- [ ] RAG content ingested (45+ chunks)

---

## 🔐 SECURITY NOTE

**IMPORTANT:** The API keys in your `.env` file were exposed earlier in our conversation. For production use, you should:

1. **Regenerate OpenAI API Key:**
   - Go to: https://platform.openai.com/api-keys
   - Revoke old key
   - Create new key
   - Update in Vercel environment variables

2. **Reset Neon Database Password:**
   - Go to: https://neon.tech/
   - Reset password
   - Update DATABASE_URL in Vercel

3. **Regenerate Qdrant API Key (if possible):**
   - Check Qdrant dashboard
   - Regenerate if option available
   - Update in Vercel

---

## 🎓 TESTING YOUR DEPLOYED SYSTEM

Once everything is deployed:

1. **Test Chatbot:**
   - Visit frontend URL
   - Click purple chatbot button
   - Type: "What is Physical AI?"
   - Should get detailed response from textbook

2. **Test Signup/Signin:**
   - Click "Auth" in navigation (if available)
   - Create account
   - Login
   - View profile

3. **Test Translation:**
   - Navigate to any chapter
   - Click "Translate to Urdu" (if button is visible)
   - Should see Urdu translation

---

## 🆘 TROUBLESHOOTING

**Frontend not loading?**
- Check GitHub Actions: https://github.com/NAVEED261/HACKATON-1-PIAIC/actions
- Ensure workflow completed successfully

**Chatbot not responding?**
- Check backend is deployed on Vercel
- Check REACT_APP_BACKEND_URL is set correctly
- Check browser console for errors (F12)

**Backend errors?**
- Check Vercel logs: https://vercel.com/dashboard
- Ensure all environment variables are set
- Check DATABASE_URL is correct
- Run database setup: `python -c "from database import create_db_tables; create_db_tables()"`

**RAG ingestion failed?**
- Check OpenAI API key is valid
- Check Qdrant credentials are correct
- Check internet connection
- Look for error messages in terminal

---

## 📞 NEXT STEPS AFTER DEPLOYMENT

1. **Add More Content:**
   - Edit markdown files in `apps/book-ui/docs/`
   - Re-run ingestion script
   - Push to GitHub

2. **Monitor Costs:**
   - OpenAI: https://platform.openai.com/usage
   - Qdrant: Check dashboard
   - Neon: Check dashboard
   - Vercel: Free tier should be sufficient

3. **Share Your Work:**
   - Share frontend URL with students
   - Add to portfolio
   - Include in hackathon submission

---

## 🎉 SUCCESS!

Your Physical AI & Humanoid Robotics textbook with RAG-based chatbot is now live!

**Frontend:** https://naveed261.github.io/HACKATON-1-PIAIC/
**Backend:** [Your Vercel URL after Step 2]

Built with Claude Code 🤖
