# Deployment Guide for EPICcrypto

This guide provides step-by-step instructions for deploying EPICcrypto to various platforms.

## Railway.app Deployment (Recommended)

Railway.app offers the easiest deployment experience with automatic builds and HTTPS.

### Step 1: Prerequisites
- GitHub account with the EPICcrypto repository
- Railway.app account (free tier available at https://railway.app)

### Step 2: Deploy from GitHub

1. **Sign in to Railway**
   - Go to https://railway.app
   - Click "Login" and authenticate with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `Islamhassana3/EPICcrypto` from your repositories
   - Click "Deploy Now"

3. **Automatic Configuration**
   Railway automatically detects:
   - Python environment (from `runtime.txt`)
   - Dependencies (from `requirements.txt`)
   - Start command (from `Procfile`)

4. **Environment Variables** (Optional)
   - Click on your deployment
   - Go to "Variables" tab
   - Railway automatically sets `PORT` variable
   - Add custom variables if needed:
     ```
     FLASK_ENV=production
     ```

5. **Generate Domain**
   - Go to "Settings" tab
   - Click "Generate Domain" under "Networking"
   - Your app will be available at: `your-app-name.up.railway.app`

### Step 3: Verify Deployment

1. Wait for build to complete (usually 2-5 minutes)
2. Click on the generated domain
3. You should see the EPICcrypto interface
4. Test the API health check: `https://your-app.railway.app/api/health`

### Step 4: Monitor and Maintain

- **View Logs**: Click "Deployments" → Select your deployment → "View Logs"
- **Metrics**: Check CPU, Memory, and Network usage in the dashboard
- **Redeploy**: Any push to your main branch triggers automatic redeployment

---

## Heroku Deployment

### Prerequisites
- Heroku account (https://heroku.com)
- Heroku CLI installed (https://devcenter.heroku.com/articles/heroku-cli)

### Step 1: Setup

```bash
# Login to Heroku
heroku login

# Create new app
heroku create epiccrypto-app

# Set environment variables
heroku config:set FLASK_ENV=production
```

### Step 2: Deploy

```bash
# Add Heroku remote (if not already added)
heroku git:remote -a epiccrypto-app

# Push to Heroku
git push heroku main

# Open the app
heroku open
```

### Step 3: Scale and Monitor

```bash
# Ensure at least one dyno is running
heroku ps:scale web=1

# View logs
heroku logs --tail

# Check app status
heroku ps
```

---

## Docker Deployment

Deploy to any platform that supports Docker (AWS, GCP, Azure, DigitalOcean, etc.)

### Step 1: Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Step 2: Build and Run Locally

```bash
# Build image
docker build -t epiccrypto .

# Run container
docker run -p 5000:5000 -e PORT=5000 epiccrypto

# Test
curl http://localhost:5000/api/health
```

### Step 3: Deploy to Docker Hub

```bash
# Tag image
docker tag epiccrypto your-username/epiccrypto:latest

# Push to Docker Hub
docker push your-username/epiccrypto:latest
```

### Step 4: Deploy to Cloud Platform

#### AWS Elastic Beanstalk
```bash
eb init -p docker epiccrypto-app
eb create epiccrypto-env
eb open
```

#### Google Cloud Run
```bash
gcloud run deploy epiccrypto \
  --image your-username/epiccrypto:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Azure Container Instances
```bash
az container create \
  --resource-group myResourceGroup \
  --name epiccrypto \
  --image your-username/epiccrypto:latest \
  --dns-name-label epiccrypto \
  --ports 5000
```

---

## Render Deployment

### Step 1: Create Render Account
- Sign up at https://render.com

### Step 2: Deploy from GitHub
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: epiccrypto
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. Click "Create Web Service"

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| PORT | Yes (Auto) | 5000 | Port for the application |
| FLASK_ENV | No | production | Flask environment |

---

## Post-Deployment Checklist

- [ ] Application loads successfully
- [ ] Health check endpoint responds: `/api/health`
- [ ] Can fetch coin list: `/api/coins`
- [ ] Predictions work for at least one coin
- [ ] Multi-timeframe analysis returns data
- [ ] UI loads and displays properly
- [ ] No errors in application logs

---

## Troubleshooting

### Build Fails
**Problem**: Dependencies fail to install

**Solution**:
- Check Python version in `runtime.txt` matches platform support
- Verify all packages in `requirements.txt` are available
- Check build logs for specific error messages

### Application Crashes
**Problem**: App starts but crashes immediately

**Solution**:
- Check environment variables are set correctly
- Review application logs for error messages
- Verify PORT environment variable is available
- Ensure all required files are present

### API Errors
**Problem**: Endpoints return 500 errors

**Solution**:
- Check yfinance API is accessible
- Verify network connectivity
- Review logs for specific error messages
- Test with different cryptocurrencies

### Slow Response Times
**Problem**: Application responds slowly

**Solution**:
- Implement caching for API responses
- Scale to more powerful instance
- Add Redis for session/data caching
- Optimize database queries (if using database)

---

## Scaling Considerations

### For High Traffic
1. **Use CDN**: Serve static files via CDN
2. **Add Caching**: Implement Redis for API responses
3. **Load Balancing**: Deploy multiple instances
4. **Database**: Add PostgreSQL for data persistence
5. **Queue System**: Use Celery for background tasks

### Performance Optimization
- Enable response compression (gzip)
- Minimize API calls with intelligent caching
- Use connection pooling
- Implement rate limiting

---

## Security Best Practices

1. **HTTPS**: Always use HTTPS in production
2. **CORS**: Configure CORS properly for your domain
3. **Rate Limiting**: Implement to prevent abuse
4. **API Keys**: Use environment variables, never commit to git
5. **Updates**: Keep dependencies updated
6. **Monitoring**: Set up error tracking (Sentry, Rollbar)

---

## Support and Maintenance

### Monitoring Tools
- **Railway**: Built-in metrics and logs
- **Sentry**: Error tracking and monitoring
- **UptimeRobot**: Uptime monitoring
- **New Relic**: Application performance monitoring

### Regular Maintenance
- Update dependencies monthly
- Monitor API usage and costs
- Review and optimize database queries
- Check security advisories
- Backup data regularly

---

## Getting Help

If you encounter issues:
1. Check the logs first
2. Review this deployment guide
3. Search for similar issues on GitHub
4. Open an issue on the repository
5. Contact the maintainers

---

Happy Deploying! 🚀
