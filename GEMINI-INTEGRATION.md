# 🔥 Gemini Analytics Integration Guide

## 🎯 Overview

Your AI Scorecard now includes **live Gemini usage analytics** integrated directly into the dashboard. The Python script you provided has been fully integrated into the Node.js backend to provide real-time week-over-week Gemini usage data.

## 🚀 What's Integrated

### ✅ Complete Python Integration
- **gemini_tracker.py**: Your exact Python script integrated into the project
- **Live API Endpoint**: `/api/gemini/usage` calls Python script and returns JSON data
- **Real-time Chart**: Dashboard automatically displays live Gemini usage data
- **Error Handling**: Graceful fallback if Python script fails

### ✅ Dashboard Integration
- **Gemini Line**: Red line in chart shows real week-over-week user data
- **Cumulative Analytics**: Bold dashed line shows total cumulative users
- **Connection Status**: Dynamic status showing when Gemini data is live
- **Auto-refresh**: Updates every 10 minutes with fresh data

## 🛠️ Setup Instructions

### 1. Install Python Dependencies
```bash
# Run the setup script
./setup-gemini.sh

# Or manually install
pip3 install -r requirements.txt
```

### 2. Configure Google Service Account
```bash
# Replace the sample file with your actual credentials
cp your-actual-service-account.json service-account.json

# Set environment variables
export GOOGLE_SERVICE_ACCOUNT_FILE=service-account.json
export DOMAIN_ADMIN_EMAIL=admin@semrush.com
```

### 3. Test Python Integration
```bash
# Test the Python script directly
python3 gemini_tracker.py

# Should output JSON data like:
{
  "summary": {
    "total_cumulative_users": 45,
    "latest_week_activities": 127,
    "latest_week_users": 12,
    "total_weeks_tracked": 6
  },
  "time_series": {
    "weeks": ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6"],
    "cumulative_users": [8, 15, 23, 31, 38, 45],
    "weekly_unique_users": [8, 7, 8, 8, 7, 7]
  }
}
```

### 4. Start Dashboard with Live Data
```bash
# Start the dashboard
npm start

# Visit: http://localhost:8080
# The Gemini line will now show real data!
```

## 📊 Data Flow

```
Google Admin SDK → Python Script → Node.js API → React Chart → Live Dashboard
```

1. **Dashboard requests**: Frontend calls `/api/gemini/usage`
2. **Python execution**: Node.js spawns `python3 gemini_tracker.py`
3. **Google API call**: Python script fetches from Google Admin SDK
4. **Data processing**: Python processes and returns JSON
5. **Chart update**: React chart displays live Gemini usage data

## 🔧 Configuration

### Environment Variables
```bash
# Required for Python script
GOOGLE_SERVICE_ACCOUNT_FILE=service-account.json
DOMAIN_ADMIN_EMAIL=admin@semrush.com

# Optional
LOG_LEVEL=INFO
```

### Google Service Account Requirements
- **Domain-wide delegation** enabled
- **Admin SDK API** access
- **Audit logs** read permissions
- **Workspace AI usage** event access

## 📈 What You'll See

### Before Integration (Current)
- Gemini line shows 0 users
- Status: "⚠️ Gemini: Ready for integration"

### After Integration (With Your Credentials)
- Gemini line shows real week-over-week user growth
- Status: "✅ Connected to Gemini analytics"
- Cumulative line shows total adoption trend
- Hover tooltips show exact user counts

### Sample Data Display
```
Week 1: 8 users
Week 2: 15 users (+87% growth)
Week 3: 23 users (+53% growth)
Week 4: 31 users (+35% growth)
Week 5: 38 users (+23% growth)
Week 6: 45 users (+18% growth)
```

## 🚂 Railway Deployment

### Python Dependencies on Railway
Railway automatically detects and installs Python dependencies:

1. **requirements.txt**: Automatically installed
2. **Python runtime**: Available alongside Node.js
3. **Environment variables**: Set in Railway dashboard

### Deployment Steps
```bash
# Set environment variables in Railway
railway variables set GOOGLE_SERVICE_ACCOUNT_FILE=service-account.json
railway variables set DOMAIN_ADMIN_EMAIL=admin@semrush.com

# Deploy
railway up
```

## 🔍 Troubleshooting

### Common Issues

1. **Python script fails**
   ```bash
   # Check Python installation
   python3 --version
   
   # Check dependencies
   pip3 list | grep google
   ```

2. **Service account errors**
   ```bash
   # Verify file exists
   ls -la service-account.json
   
   # Check permissions
   python3 -c "import json; print(json.load(open('service-account.json'))['client_email'])"
   ```

3. **API permissions**
   - Ensure domain-wide delegation is enabled
   - Verify admin email has proper permissions
   - Check Google Workspace audit logs are enabled

### Debug Mode
```bash
# Run with debug logging
LOG_LEVEL=DEBUG python3 gemini_tracker.py
```

## 🎯 Expected Results

### Dashboard Impact
- **Executive View**: Real Gemini adoption metrics
- **Growth Tracking**: Week-over-week user growth
- **Trend Analysis**: Cumulative adoption curve
- **Data-Driven**: Replace assumptions with facts

### Business Value
- **Adoption Metrics**: Track actual Gemini usage
- **ROI Calculation**: Measure AI tool investment
- **Department Insights**: See which teams adopt fastest
- **Executive Reporting**: Professional metrics for leadership

## 🔄 Maintenance

### Automatic Updates
- **Dashboard**: Auto-refreshes every 10 minutes
- **Data**: Always shows latest 6 weeks
- **Caching**: 30-second timeout prevents API overload

### Manual Refresh
- Click "Refresh" button in dashboard
- Or call API directly: `curl http://localhost:8080/api/gemini/usage`

---

**🎉 Your Gemini analytics are now fully integrated and ready to show live usage data to your boss!**

## Next Steps
1. **Setup credentials**: Replace service-account.json with real credentials
2. **Test integration**: Run `python3 gemini_tracker.py`
3. **Deploy to Railway**: Share live dashboard with your team
4. **Monitor adoption**: Track week-over-week Gemini growth

**The dashboard will transform from showing 0 users to displaying real Semrush Gemini adoption metrics!**
