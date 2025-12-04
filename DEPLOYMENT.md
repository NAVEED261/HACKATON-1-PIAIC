# Physical AI & Humanoid Robotics - Deployment Guide

Complete deployment instructions for the Physical AI & Humanoid Robotics textbook system with RAG chatbot.

## 🎯 System Overview

This project consists of:
- **Docusaurus Book UI** - Static textbook website with chatbot widget
- **FastAPI Backend** - API server with RAG, Auth, Personalization, Translation
- **Qdrant** - Vector database for RAG
- **Neon Postgres** - User data and authentication
- **OpenAI** - Embeddings, LLM responses, translations

## 📋 Prerequisites

### Required Services

1. **OpenAI API Key**
   - Sign up at https://platform.openai.com/
   - Create API key from dashboard
   - Ensure credits available

2. **Qdrant Cloud** (or self-hosted)
   - Sign up at https://cloud.qdrant.io/
   - Create a cluster
   - Get host URL and API key

3. **Neon Postgres**
   - Sign up at https://neon.tech/
   - Create database
   - Get connection string

4. **GitHub Account** (for deployment)
   - Repository with GitHub Pages enabled

### Local Development Tools

- Node.js 20+
- Python 3.9+
- Git

## 🚀 Quick Start (Local Development)

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd hackaton_1
```

### 2. Configure Environment Variables

Create `.env` file in `apps/backend/`:

```bash
cd apps/backend
cp .env.template .env
```

Edit `.env` with your credentials:

```env
# OpenAI
OPENAI_API_KEY=sk-your-key-here

# Neon Postgres
DATABASE_URL=postgresql://user:password@host/dbname

# Qdrant
QDRANT_HOST=your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key

# JWT Authentication
SECRET_KEY=generate-a-strong-random-secret-key-here
ALGORITHM=HS256
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Backend Setup

```bash
cd apps/backend

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate
# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create database tables
python -c "from database import create_db_tables; create_db_tables()"

# Run server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend now running at `http://localhost:8000`

### 4. Ingest Book Content into RAG

```bash
# From project root
cd scripts
python ingest_book.py
```

This will:
- Read all markdown files from `apps/book-ui/docs`
- Generate embeddings via OpenAI
- Store in Qdrant collection

Expected output:
```
🚀 RAG Ingestion - Physical AI & Humanoid Robotics
📁 Reading from: D:\...\apps\book-ui\docs
✅ Collection exists: book_chunks
📚 Found 15 files
[1/15] intro.md
  📄 12 chunks
  ✅ Uploaded 12 chunks
...
✅ Success: 156 chunks
```

### 5. Frontend Setup

```bash
cd apps/book-ui

# Install dependencies
npm install

# Start development server
npm run start
```

Book UI now running at `http://localhost:3000`

### 6. Test the System

1. Open `http://localhost:3000`
2. Click the purple chatbot button (bottom-right)
3. Ask: "What is Physical AI?"
4. Verify you get a response from the textbook content

## 🐳 Docker Deployment

### Build and Run with Docker Compose

```bash
cd apps/backend

# Ensure .env file is configured
# Build and start
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

Backend accessible at `http://localhost:8000`

## 📦 GitHub Pages Deployment (Book UI)

### Setup GitHub Pages

1. Go to repository Settings → Pages
2. Source: "GitHub Actions"
3. Save

### Deploy Workflow

The workflow `.github/workflows/deploy-book.yml` automatically deploys on push to `master`:

```bash
git add .
git commit -m "Deploy textbook"
git push origin master
```

GitHub Actions will:
1. Build Docusaurus site
2. Deploy to GitHub Pages
3. Site available at: `https://<username>.github.io/<repo-name>/`

### Configure Backend URL

Update Docusaurus config to point to your deployed backend:

**File:** `apps/book-ui/docusaurus.config.ts`

```typescript
customFields: {
  backendUrl: 'https://your-backend-url.com'
}
```

Or set environment variable:
```bash
REACT_APP_BACKEND_URL=https://your-backend-url.com npm run build
```

## ☁️ Production Backend Deployment

### Option 1: Railway/Render

1. Create account on [Railway](https://railway.app/) or [Render](https://render.com/)
2. Create new service from GitHub repo
3. Set root directory: `apps/backend`
4. Add environment variables (all from `.env`)
5. Deploy

### Option 2: AWS/GCP/Azure

1. Build Docker image:
   ```bash
   cd apps/backend
   docker build -t physical-ai-backend .
   ```

2. Push to container registry
3. Deploy to container service (ECS, Cloud Run, Container Apps)
4. Configure environment variables
5. Expose port 8000

### Required Environment Variables (Production)

```
OPENAI_API_KEY
DATABASE_URL
QDRANT_HOST
QDRANT_API_KEY
SECRET_KEY
ALGORITHM
```

## 🧪 Testing Endpoints

### Health Check
```bash
curl http://localhost:8000/
```

### RAG Query
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is ROS 2?"}'
```

### User Signup
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123",
    "learning_preferences": "hands-on",
    "hardware_software_background": "intermediate Python"
  }'
```

### Translation
```bash
curl -X POST http://localhost:8000/chapter/translate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{"chapter_content": "# Hello\nThis is a test chapter."}'
```

## 🔧 Troubleshooting

### Backend won't start

**Error:** `DATABASE_URL environment variable is not set`
- Solution: Ensure `.env` file exists in `apps/backend/` with all variables

**Error:** `Failed to connect to Qdrant`
- Solution: Check `QDRANT_HOST` and `QDRANT_API_KEY` are correct

### RAG returns no results

- Run ingestion script: `python scripts/ingest_book.py`
- Verify Qdrant collection exists: Check Qdrant dashboard
- Check OpenAI API key is valid and has credits

### Chatbot not appearing

- Check browser console for errors
- Verify backend URL is correct
- Ensure CORS is enabled (FastAPI handles this)

### GitHub Pages 404

- Check repository Settings → Pages is enabled
- Verify workflow ran successfully (Actions tab)
- Check `docusaurus.config.ts` `baseUrl` matches repo name

## 📊 Monitoring

### Backend Logs

```bash
# Docker
docker-compose logs -f backend

# Local
# Check terminal where uvicorn is running
```

### Check Database

```bash
# Connect to Neon Postgres
psql $DATABASE_URL

# List users
SELECT * FROM users;
```

### Check Qdrant

- Visit Qdrant Cloud dashboard
- Check collection `book_chunks`
- Verify point count matches ingested chunks

## 🔐 Security Checklist

- [ ] Change `SECRET_KEY` to strong random value
- [ ] Never commit `.env` to Git
- [ ] Use HTTPS in production
- [ ] Enable rate limiting (add to FastAPI)
- [ ] Rotate API keys regularly
- [ ] Monitor OpenAI usage/costs
- [ ] Backup Neon database regularly

## 📈 Scaling

### High Traffic

- Deploy multiple backend instances behind load balancer
- Use Redis for session management
- Enable CDN for static assets (book UI)
- Scale Qdrant cluster (more nodes)

### Cost Optimization

- Cache frequent RAG queries (Redis)
- Use smaller OpenAI models for non-critical features
- Monitor and set OpenAI spending limits
- Use Qdrant local mode for development

## 🎓 Next Steps

1. ✅ Deploy book to GitHub Pages
2. ✅ Deploy backend to cloud service
3. ✅ Run ingestion script
4. ✅ Test all features
5. ✅ Monitor usage and costs
6. Add more book content
7. Improve RAG accuracy
8. Add analytics
9. Implement user feedback

## 🆘 Support

- Issues: Open GitHub issue
- Documentation: See `README.md` and `CLAUDE.md`
- Constitution: `.specify/memory/constitution.md`

## ✅ Deployment Checklist

- [ ] Environment variables configured
- [ ] Backend running and accessible
- [ ] RAG ingestion completed
- [ ] Book UI deployed to GitHub Pages
- [ ] Chatbot widget functional
- [ ] Auth (signup/signin) working
- [ ] Translation working
- [ ] Personalization working
- [ ] All API endpoints tested
- [ ] Public URLs documented

**🎉 Congratulations! Your Physical AI & Humanoid Robotics system is deployed!**