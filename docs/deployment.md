# GapWise AI — Deployment Guide

## Architecture

```
┌─────────────┐    HTTPS    ┌──────────────┐    SQL    ┌──────────────┐
│   Vercel    │ ──────────→ │    Render    │ ───────→ │     Neon     │
│  (Frontend) │             │  (Backend)   │          │ (PostgreSQL) │
│  React App  │             │  FastAPI     │          │  Database    │
└─────────────┘             └──────────────┘          └──────────────┘
```

## Step 1: Database (Neon)

1. Go to [neon.tech](https://neon.tech) and create a free account
2. Create a new project (name: `gapwise-ai`)
3. A default database is created automatically
4. Copy the connection string from the dashboard
   - It looks like: `postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require`
5. Save this for the backend deployment

## Step 2: Backend (Render)

1. Go to [render.com](https://render.com) and create a free account
2. Connect your GitHub repository
3. Click **New → Web Service**
4. Configure:
   - **Name**: `gapwise-api`
   - **Root Directory**: `backend`
   - **Runtime**: Docker
   - **Instance Type**: Free
5. Add environment variables:
   | Key | Value |
   |-----|-------|
   | `DATABASE_URL` | Your Neon connection string |
   | `SECRET_KEY` | Generate a random 32+ character string |
   | `CORS_ORIGINS` | `https://your-app.vercel.app` (update after frontend deploy) |
   | `OPENAI_API_KEY` | *(optional)* Your OpenAI API key |
6. Click **Deploy**
7. Wait for the build to complete (~3-5 minutes)
8. Note your backend URL (e.g., `https://gapwise-api.onrender.com`)
9. Test: Visit `https://gapwise-api.onrender.com/api/health`

## Step 3: Frontend (Vercel)

1. Go to [vercel.com](https://vercel.com) and create a free account
2. Click **Import Project** and select your GitHub repository
3. Configure:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Add environment variable:
   | Key | Value |
   |-----|-------|
   | `VITE_API_BASE_URL` | `https://gapwise-api.onrender.com/api` |
5. Click **Deploy**
6. Note your frontend URL (e.g., `https://gapwise-ai.vercel.app`)

## Step 4: Update CORS

1. Go back to Render dashboard
2. Update the `CORS_ORIGINS` environment variable to include your Vercel URL
3. The backend will automatically redeploy

## Step 5: Verify

1. Visit your Vercel URL
2. Login with demo credentials:
   - Student: `student@gapwise.ai` / `demo123`
   - Teacher: `teacher@gapwise.ai` / `demo123`
3. Test the full flow (assessment → report → learning path → practice → reassessment)

## Troubleshooting

### Backend won't start
- Check that `DATABASE_URL` is correct and the Neon database is accessible
- Check Render logs for specific errors

### CORS errors
- Make sure `CORS_ORIGINS` includes your frontend URL (no trailing slash)
- Format: `https://your-app.vercel.app`

### Database tables not created
- The app auto-creates tables on startup
- Check Render logs for SQLAlchemy errors

### AI Mentor not responding
- Works without `OPENAI_API_KEY` using deterministic fallback
- If you add an API key, make sure it's valid and has credits

### Render free tier cold starts
- Free tier instances sleep after 15 minutes of inactivity
- First request after sleep may take 30-60 seconds
- This is normal for free tier

## Custom Domain (Optional)

### Vercel
1. Go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

### Render
1. Go to Service Settings → Custom Domains
2. Add your custom domain
3. Follow DNS configuration instructions
