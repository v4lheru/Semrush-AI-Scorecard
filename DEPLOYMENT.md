# 🚀 AI Scorecard - Deployment Guide

## Quick Deploy to GCP Cloud Run

### One-Command Deployment
```bash
gcloud run deploy ai-scorecard \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars MONDAY_API_KEY="eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjUzMDI3Mjg0MCwiYWFpIjoxMSwidWlkIjo3NDE4MDY3OCwiaWFkIjoiMjAyNS0wNi0yNFQxMTo0Nzo0Ni4wMDdaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTc0OTAxMSwicmduIjoidXNlMSJ9.DD-rnSR6oKQmJpwWX5AiaB7Y600WB959l-buFfIbk6U" \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10
```

## Local Development

### 1. Install Dependencies
```bash
npm install
```

### 2. Start Development
```bash
npm run dev
```
- Frontend: http://localhost:3000
- Backend: http://localhost:8080

### 3. Test Deployment
```bash
npm run test:local
```

## Production Deployment Steps

### 1. Build Application
```bash
npm run build
```

### 2. Test Production Build
```bash
npm start
npm run test
```

### 3. Deploy to Cloud Run
```bash
# Using source deployment (recommended)
gcloud run deploy ai-scorecard \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars MONDAY_API_KEY="your-api-key"

# Or using Docker
docker build -t gcr.io/YOUR_PROJECT_ID/ai-scorecard .
docker push gcr.io/YOUR_PROJECT_ID/ai-scorecard
gcloud run deploy ai-scorecard \
  --image gcr.io/YOUR_PROJECT_ID/ai-scorecard \
  --region us-central1
```

### 4. Verify Deployment
```bash
# Test the deployed service
TEST_URL="https://your-service-url" npm run test
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MONDAY_API_KEY` | Monday.com API authentication token | Yes |
| `PORT` | Server port (Cloud Run sets this automatically) | No |
| `NODE_ENV` | Environment (production/development) | No |

## Monitoring & Health Checks

### Health Endpoints
- `GET /api/health` - Basic health check
- `GET /api/metrics` - Application metrics
- `GET /api/monday/board` - Data endpoint

### Cloud Run Monitoring
- Automatic health checks every 30s
- Request/response logging
- Error rate monitoring
- Performance metrics

## Troubleshooting

### Common Issues

1. **Monday.com API Key Invalid**
   ```bash
   # Check API key format
   echo $MONDAY_API_KEY | cut -d'.' -f1 | base64 -d
   ```

2. **Build Failures**
   ```bash
   # Clear cache and rebuild
   rm -rf node_modules dist
   npm install
   npm run build
   ```

3. **Memory Issues**
   ```bash
   # Increase Cloud Run memory
   gcloud run services update ai-scorecard \
     --memory 1Gi \
     --region us-central1
   ```

### Logs
```bash
# View Cloud Run logs
gcloud logs read --service ai-scorecard --region us-central1

# Stream logs in real-time
gcloud logs tail --service ai-scorecard --region us-central1
```

## Performance Optimization

### Cloud Run Settings
- **Memory**: 512Mi (can increase to 1Gi if needed)
- **CPU**: 1 vCPU
- **Concurrency**: 80 requests per instance
- **Max Instances**: 10 (adjust based on traffic)

### Caching
- Frontend assets cached via CDN
- API responses cached for 5 minutes
- Monday.com data refreshed every 5 minutes

## Security

### Best Practices
- ✅ Non-root user in container
- ✅ Environment variables for secrets
- ✅ CORS configuration
- ✅ Input validation
- ✅ Health checks enabled

### API Key Security
- Store in Google Secret Manager for production
- Never commit to version control
- Rotate regularly

## Cost Optimization

### Cloud Run Pricing
- **CPU**: $0.00002400 per vCPU-second
- **Memory**: $0.00000250 per GiB-second
- **Requests**: $0.40 per million requests

### Estimated Monthly Cost
- **Low Traffic** (1K requests/day): ~$5-10/month
- **Medium Traffic** (10K requests/day): ~$20-30/month
- **High Traffic** (100K requests/day): ~$50-100/month

### Optimization Tips
- Scale to zero when not in use
- Use minimum required memory
- Enable request-based scaling
- Monitor and adjust based on usage

## Backup & Recovery

### Data Sources
- Monday.com API (primary data source)
- No local data storage required
- Stateless application design

### Disaster Recovery
- Redeploy from source code
- Environment variables backup
- Configuration as code

---

**🎉 Your AI Scorecard is ready for production!**
