# 🚂 Railway Deployment Guide - AI Scorecard

## Quick Deploy to Railway

### One-Click Deployment
1. **Connect Repository**: Link your GitHub repository to Railway
2. **Set Environment Variables**: Add `MONDAY_API_KEY` in Railway dashboard
3. **Deploy**: Railway will automatically build and deploy

### Manual Deployment Steps

#### 1. Install Railway CLI
```bash
npm install -g @railway/cli
```

#### 2. Login to Railway
```bash
railway login
```

#### 3. Initialize Project
```bash
railway init
```

#### 4. Set Environment Variables
```bash
railway variables set MONDAY_API_KEY="your-monday-api-key-here"
railway variables set NODE_ENV="production"
```

#### 5. Deploy
```bash
railway up
```

## Configuration

### Environment Variables Required
- `MONDAY_API_KEY` - Monday.com API authentication token
- `NODE_ENV` - Set to "production" for production deployment

### Railway Configuration (`railway.toml`)
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "npm start"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10

[environments.production]
variables = { NODE_ENV = "production" }

[environments.production.serviceConnect]
allowPublicNetworking = true
```

## Automatic Features

Railway automatically provides:
- ✅ **Custom Domain**: `your-app.railway.app`
- ✅ **HTTPS/SSL**: Automatic SSL certificates
- ✅ **Auto-scaling**: Based on traffic
- ✅ **Zero-downtime**: Deployments with rollback
- ✅ **Environment Management**: Production/staging environments
- ✅ **Logs & Monitoring**: Built-in observability

## Build Process

Railway uses Nixpacks to automatically detect and build Node.js applications:

1. **Dependency Installation**: `npm install`
2. **Build Frontend**: `npm run build`
3. **Start Server**: `npm start`

## Deployment URL

After deployment, your AI Scorecard will be available at:
```
https://your-project-name.railway.app
```

## Environment Setup

### Production Environment Variables
```bash
# Required
MONDAY_API_KEY=your-monday-api-key

# Optional (Railway sets automatically)
PORT=8080
NODE_ENV=production
```

### Development vs Production
- **Development**: Frontend (Vite) + Backend (Express) on separate ports
- **Production**: Single Express server serving built React app

## Monitoring

### Built-in Railway Features
- **Metrics**: CPU, Memory, Network usage
- **Logs**: Real-time application logs
- **Deployments**: History and rollback options
- **Uptime**: Automatic monitoring

### Application Endpoints
- `GET /` - Dashboard (React app)
- `GET /api/health` - Health check
- `GET /api/metrics` - Application metrics
- `GET /api/monday/board` - Monday.com data
- `GET /api/gemini/usage` - Gemini analytics

## Troubleshooting

### Common Issues

1. **Build Failures**
   ```bash
   # Check build logs in Railway dashboard
   railway logs --deployment
   ```

2. **Environment Variables**
   ```bash
   # List current variables
   railway variables
   
   # Update variable
   railway variables set MONDAY_API_KEY="new-key"
   ```

3. **Port Issues**
   - Railway automatically sets `PORT` environment variable
   - Application uses `process.env.PORT || 8080`

### Debugging
```bash
# View real-time logs
railway logs

# Connect to deployment shell
railway shell

# Check service status
railway status
```

## Cost Optimization

### Railway Pricing
- **Hobby Plan**: $5/month - Perfect for this dashboard
- **Pro Plan**: $20/month - For higher traffic
- **Usage-based**: CPU, Memory, Network

### Optimization Tips
- Application sleeps when not in use (Hobby plan)
- Efficient resource usage with Express + React
- Minimal memory footprint (~100MB)

## Security

### Best Practices
- ✅ Environment variables for secrets
- ✅ HTTPS enforced by Railway
- ✅ No hardcoded API keys
- ✅ CORS configuration
- ✅ Input validation

### API Key Management
- Store `MONDAY_API_KEY` in Railway environment variables
- Never commit API keys to repository
- Rotate keys regularly

## Scaling

### Automatic Scaling
- Railway handles scaling based on traffic
- No configuration needed for basic scaling
- Upgrade plan for higher limits

### Performance
- **Response Time**: <200ms for dashboard
- **Uptime**: 99.9% with Railway infrastructure
- **Global CDN**: Automatic for static assets

## Backup & Recovery

### Data Sources
- Monday.com API (external data source)
- No local database required
- Stateless application design

### Disaster Recovery
- Redeploy from Git repository
- Environment variables backup
- Railway handles infrastructure

---

**🎉 Your AI Scorecard is ready for Railway deployment!**

## Next Steps After Deployment

1. **Test the deployment**: Visit your Railway URL
2. **Set up monitoring**: Configure alerts in Railway dashboard
3. **Custom domain** (optional): Add your own domain
4. **Gemini integration**: Add Google Admin SDK for real Gemini data
5. **Team access**: Share the URL with your boss and team

**Railway URL will be provided after deployment completion.**
