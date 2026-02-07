# Deploying Shopify Discovery Dashboard

This guide explains how to deploy the read-only public dashboard.

## Quick Deploy to Render (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add public dashboard"
   git push
   ```

2. **Deploy on Render**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect the `render.yaml` configuration
   - Click "Create Web Service"
   - Your dashboard will be live at: `https://your-app-name.onrender.com`

## Alternative: Deploy to Railway

1. **Push to GitHub** (if not already done)

2. **Deploy on Railway**
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect Flask app
   - Set environment variable: `DATABASE_PATH=shopify_leads_snapshot.db`
   - Your dashboard will be live at: `https://your-app-name.up.railway.app`

## Alternative: Deploy to Fly.io

1. **Install Fly CLI**
   ```bash
   brew install flyctl
   ```

2. **Login and deploy**
   ```bash
   fly auth login
   fly launch
   fly deploy
   ```

## Local Testing

Before deploying, test the public dashboard locally:

```bash
python3 web_dashboard_public.py
```

Open http://localhost:5002 in your browser.

## Database Snapshot

The dashboard uses `shopify_leads_snapshot.db` - a read-only snapshot of the discovery data.

To update the snapshot:
```bash
cp shopify_leads.db shopify_leads_snapshot.db
git add shopify_leads_snapshot.db
git commit -m "Update data snapshot"
git push
```

Then redeploy on your hosting platform.

## Features

The public dashboard shows:
- ✅ Total stores discovered
- ✅ Shopify Plus detection
- ✅ USA store filtering
- ✅ Top countries breakdown
- ✅ Recent discoveries
- ❌ No batch controls (read-only)
- ❌ No data modification

## Free Tier Limits

- **Render**: 750 hours/month (enough for 24/7), sleeps after 15min inactivity
- **Railway**: $5 credit/month (~500 hours)
- **Fly.io**: 3 shared-cpu VMs, 160GB bandwidth/month
