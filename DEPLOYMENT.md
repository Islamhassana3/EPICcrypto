# 🚀 Deployment Guide - Railway.app

This guide will walk you through deploying the EPICcrypto AI Crypto Prediction application on Railway.app.

## Prerequisites

- GitHub account
- Railway.app account (sign up at https://railway.app)
- This repository forked or cloned to your GitHub account

## Method 1: Deploy from GitHub (Recommended)

### Step 1: Prepare Your Repository

1. Fork this repository to your GitHub account
2. Ensure all files are committed and pushed

### Step 2: Connect to Railway

1. Go to [Railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub account
5. Select the **EPICcrypto** repository

### Step 3: Configure Deployment

Railway will automatically detect the Python application and configure it based on:
- `requirements.txt` - Python dependencies
- `Procfile` - Start command
- `runtime.txt` - Python version
- `railway.json` - Railway-specific configuration

### Step 4: Set Environment Variables (Optional)

1. In Railway dashboard, go to your project
2. Click on **"Variables"** tab
3. Add any custom environment variables:
   ```
   SECRET_KEY=your-secure-random-key-here
   FLASK_ENV=production
   ```
   
Note: `PORT` is automatically set by Railway

### Step 5: Deploy

1. Railway will automatically build and deploy your application
2. Wait for the build to complete (usually 2-5 minutes)
3. Once deployed, you'll see a **"View Logs"** option

### Step 6: Access Your Application

1. In Railway dashboard, click **"Settings"** tab
2. Scroll to **"Domains"** section
3. Click **"Generate Domain"** to get a public URL
4. Your app will be available at: `https://your-app-name.railway.app`

## Method 2: Deploy Using Railway CLI

### Step 1: Install Railway CLI

```bash
# Using npm
npm install -g @railway/cli

# Or using curl
curl -fsSL https://railway.app/install.sh | sh
```

### Step 2: Login to Railway

```bash
railway login
```

This will open a browser window for authentication.

### Step 3: Initialize Project

Navigate to your project directory:

```bash
cd EPICcrypto
railway init
```

Select **"Create new project"** when prompted.

### Step 4: Link to Existing Project (Optional)

If you already created a project on Railway dashboard:

```bash
railway link
```

### Step 5: Deploy

```bash
railway up
```

This will build and deploy your application.

### Step 6: View Logs

```bash
railway logs
```

### Step 7: Add Custom Domain (Optional)

```bash
railway domain
```

## Configuration Files Explained

### 1. `requirements.txt`
Lists all Python dependencies that Railway will install.

### 2. `Procfile`
Tells Railway how to start the application:
```
web: gunicorn app:create_app() --bind 0.0.0.0:$PORT --workers 4
```

### 3. `runtime.txt`
Specifies Python version:
```
python-3.11.6
```

### 4. `railway.json`
Railway-specific configuration:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:create_app() --bind 0.0.0.0:$PORT --workers 4",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

## Environment Variables

### Required Variables

Railway automatically sets:
- `PORT` - The port your application should listen on

### Optional Variables

You can set these in Railway dashboard:

- `SECRET_KEY` - Flask secret key for session management
  ```
  SECRET_KEY=your-super-secret-key-change-this
  ```

- `FLASK_ENV` - Flask environment
  ```
  FLASK_ENV=production
  ```

### Generating a Secret Key

Use Python to generate a secure secret key:

```python
import secrets
print(secrets.token_hex(32))
```

## Monitoring and Maintenance

### View Logs

**Via Dashboard:**
1. Go to your project in Railway dashboard
2. Click **"Deployments"** tab
3. Click on the latest deployment
4. View real-time logs

**Via CLI:**
```bash
railway logs
```

### Monitor Performance

Railway provides metrics for:
- CPU usage
- Memory usage
- Network traffic
- Request rates

Access these in the **"Metrics"** tab of your project.

### Restart Application

**Via Dashboard:**
1. Go to **"Deployments"** tab
2. Click **"Redeploy"** on the latest deployment

**Via CLI:**
```bash
railway up --detach
```

## Troubleshooting

### Build Fails

**Check Python version:**
Ensure `runtime.txt` has a supported Python version (3.9+)

**Check dependencies:**
Ensure all packages in `requirements.txt` are compatible

**View build logs:**
```bash
railway logs
```

### Application Won't Start

**Check start command:**
Verify `Procfile` has correct command:
```
web: gunicorn app:create_app() --bind 0.0.0.0:$PORT --workers 4
```

**Check port binding:**
Ensure app binds to `0.0.0.0:$PORT` not just `localhost`

**Verify environment variables:**
Check all required variables are set

### API Errors

**Rate limiting:**
CoinGecko and Binance APIs have rate limits. The app includes caching to minimize requests.

**Network issues:**
Ensure Railway can access external APIs (CoinGecko, Binance)

**Check logs for errors:**
```bash
railway logs --tail 100
```

## Performance Optimization

### 1. Worker Configuration

Adjust workers in `Procfile` based on your Railway plan:

```
web: gunicorn app:create_app() --bind 0.0.0.0:$PORT --workers 4 --timeout 120
```

### 2. Enable Caching

The application includes built-in caching. To use Redis for production:

1. Add Redis service in Railway:
   - Click **"New"** → **"Database"** → **"Redis"**
   - Railway will provide connection string

2. Update code to use Redis instead of in-memory cache

### 3. Monitor Resource Usage

- Check Railway metrics regularly
- Upgrade plan if needed (Starter, Developer, Team)

## Scaling

### Vertical Scaling
Upgrade your Railway plan for more:
- CPU
- RAM
- Network bandwidth

### Horizontal Scaling
For high traffic:
1. Deploy multiple instances
2. Use Railway's load balancing
3. Add Redis for shared caching

## Custom Domain

### Step 1: Get Domain Name
Purchase a domain from any registrar (GoDaddy, Namecheap, etc.)

### Step 2: Configure DNS

Add CNAME record pointing to your Railway domain:
```
CNAME: www -> your-app.railway.app
```

### Step 3: Add to Railway

1. Go to **"Settings"** → **"Domains"**
2. Click **"Custom Domain"**
3. Enter your domain
4. Follow verification steps

## Security Best Practices

1. **Use Environment Variables**
   - Never commit secrets to Git
   - Use Railway dashboard to set sensitive variables

2. **Enable HTTPS**
   - Railway provides automatic HTTPS
   - Enforce HTTPS in production

3. **Rate Limiting**
   - Built-in caching helps prevent API abuse
   - Consider adding Flask-Limiter for additional protection

4. **Regular Updates**
   - Keep dependencies updated
   - Monitor for security vulnerabilities

## Backup and Recovery

### Database Backups
If using Railway databases:
1. Railway provides automatic backups
2. Access in **"Backups"** tab

### Code Backups
- Keep repository updated on GitHub
- Tag releases for easy rollback

### Rollback Deployment

**Via Dashboard:**
1. Go to **"Deployments"** tab
2. Find previous successful deployment
3. Click **"Redeploy"**

**Via CLI:**
```bash
railway rollback
```

## Cost Estimation

Railway pricing (as of 2024):

- **Starter Plan**: $5/month
  - $5 usage credit
  - Good for personal projects

- **Developer Plan**: $20/month
  - $20 usage credit
  - Better for production apps

- **Team Plan**: Custom pricing
  - For organizations

Usage costs:
- Compute: ~$0.02/hour per GB RAM
- Bandwidth: Free up to limits

Estimated monthly cost for EPICcrypto:
- Light usage: ~$5-10/month
- Moderate usage: ~$15-25/month
- Heavy usage: ~$30-50/month

## Support

If you encounter issues:

1. **Railway Documentation**: https://docs.railway.app
2. **Railway Discord**: https://discord.gg/railway
3. **Railway Support**: support@railway.app
4. **GitHub Issues**: Create an issue in this repository

## Useful Commands

```bash
# Login to Railway
railway login

# Link to project
railway link

# Deploy current directory
railway up

# View logs
railway logs

# View environment variables
railway variables

# Add environment variable
railway variables set KEY=VALUE

# Open project in browser
railway open

# Get project info
railway status

# Run command in Railway environment
railway run python app.py
```

## Next Steps

After deployment:

1. **Test all endpoints** to ensure API is working
2. **Set up monitoring** using Railway metrics
3. **Configure custom domain** if needed
4. **Enable notifications** for deployment failures
5. **Document your API** using provided endpoints
6. **Share your deployment** URL with users

## Continuous Deployment

Railway automatically deploys when you push to your main branch:

1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```
3. Railway automatically builds and deploys

To disable auto-deployment:
1. Go to **"Settings"** → **"Deployments"**
2. Toggle **"Auto-deploy"** off

---

**Congratulations!** 🎉 Your AI Crypto Prediction platform is now live on Railway.app!

Visit your deployment URL to see it in action.