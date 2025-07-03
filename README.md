# AI & Automation Scorecard - Semrush

A real-time dashboard tracking AI initiatives across Semrush, integrated with Monday.com API and deployed on Google Cloud Platform.

## 🚀 Features

- **Real-time Data**: Live integration with Monday.com board
- **Executive Dashboard**: Clean, professional interface matching mockup requirements
- **Interactive Components**: Clickable department cards with detailed breakdowns
- **AI Usage Tracking**: Visual charts showing tool adoption trends
- **Financial Metrics**: ROI calculations and savings tracking
- **Responsive Design**: Works on desktop, tablet, and mobile

## 📊 Dashboard Sections

1. **AI Literacy**: Usage trends for Gemini, Claude, Cursor, ChatGPT
2. **Training Metrics**: New hire completion rates and team access
3. **Active Initiatives**: Backlog, In Flight, Completed, Total ROI
4. **Department Breakdown**: Interactive grid showing initiatives by department

## 🛠️ Tech Stack

- **Frontend**: React 18 + Vite + Tailwind CSS
- **Backend**: Express.js + Node.js
- **Charts**: Recharts
- **Icons**: Lucide React
- **Deployment**: Google Cloud Run
- **Data Source**: Monday.com API

## 🏗️ Architecture

```
React App (Cloud Run) ← Express API (Cloud Run) ← Monday.com API
```

Simple, scalable architecture following GCP best practices.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Monday.com API key
- Google Cloud SDK (for deployment)

### Local Development

1. **Clone and install dependencies**:
```bash
git clone <repository-url>
cd semrush-ai-scorecard
npm install
```

2. **Set environment variables**:
```bash
export MONDAY_API_KEY="your-monday-api-key"
```

3. **Start development servers**:
```bash
npm run dev
```

This starts both frontend (http://localhost:3000) and backend (http://localhost:8080).

### Production Build

```bash
npm run build
npm start
```

## 🌐 GCP Deployment

### One-Command Deployment

```bash
gcloud run deploy ai-scorecard \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars MONDAY_API_KEY="your-api-key-here" \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10
```

### Manual Docker Deployment

1. **Build and push image**:
```bash
docker build -t gcr.io/YOUR_PROJECT_ID/ai-scorecard .
docker push gcr.io/YOUR_PROJECT_ID/ai-scorecard
```

2. **Deploy to Cloud Run**:
```bash
gcloud run deploy ai-scorecard \
  --image gcr.io/YOUR_PROJECT_ID/ai-scorecard \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars MONDAY_API_KEY="your-api-key"
```

## 📡 API Endpoints

- `GET /api/monday/board` - Fetch processed Monday.com data
- `GET /api/health` - Health check
- `GET /api/metrics` - Summary metrics for monitoring

## 🔧 Configuration

### Environment Variables

- `MONDAY_API_KEY` - Monday.com API authentication token
- `PORT` - Server port (default: 8080)
- `NODE_ENV` - Environment (development/production)

### Monday.com Board Structure

The dashboard expects these column IDs:
- `status` - Initiative status
- `dropdown_mkrbjyg7` - Function/Department
- `dropdown_mkq1ha1j` - Team
- `numeric_mkrd11hy` - Annual Savings Estimate
- `text_mkr3b2hk` - Resources Saved (hours)

## 📈 Key Metrics Tracked

### From Monday.com Data
- **Total Initiatives**: 47 across all departments
- **Total ROI**: $5.1M+ projected savings
- **Top Contributors**:
  - Conversational Search: $2.7M
  - Meeting Recording: $1.5M
  - AI Sales Assistants: $515K

### Mock Data (for development)
- AI tool usage trends
- Team access metrics
- Training completion rates

## 🎨 Design System

### Color Palette
- **Gemini**: #FF4444 (Red)
- **Claude**: #4A90E2 (Blue)
- **Cursor**: #F5A623 (Yellow)
- **ChatGPT**: #7ED321 (Green)
- **Background**: #F8F9FA
- **Cards**: #FFFFFF

### Typography
- **Font**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700

## 🔄 Data Flow

1. **Frontend** requests data from `/api/monday/board`
2. **Backend** fetches from Monday.com API using GraphQL
3. **Data Processing** maps columns to standardized format
4. **Response** returns processed initiatives array
5. **Frontend** calculates metrics and renders dashboard
6. **Auto-refresh** every 5 minutes

## 🚨 Monitoring

### Health Checks
- `/api/health` - Basic health status
- Docker health check every 30s
- Cloud Run health monitoring

### Logging
- Structured JSON logs
- Error tracking and reporting
- Performance metrics

## 🔒 Security

- Non-root user in Docker container
- Environment variable for API keys
- CORS configuration
- Input validation and sanitization

## 🧪 Testing

```bash
# Run tests (when implemented)
npm test

# Test API endpoints
curl http://localhost:8080/api/health
curl http://localhost:8080/api/metrics
```

## 📝 Development Notes

### Component Structure
```
src/
├── components/
│   ├── ScorecardDashboard.jsx  # Main dashboard
│   ├── MetricCard.jsx          # Reusable metric cards
│   ├── AILiteracyChart.jsx     # Usage trend chart
│   └── DepartmentGrid.jsx      # Department breakdown
├── hooks/
│   └── useMondayData.js        # Data fetching hook
└── App.jsx                     # Root component
```

### Status Mapping
```javascript
const statusMapping = {
  'Backlog': 'backlog',
  'Evaluation': 'inFlight',
  'Scoping': 'inFlight', 
  'In Progress': 'inFlight',
  'Done': 'completed',
  'Closed': 'completed'
}
```

## 🤝 Contributing

1. Follow the PACT framework principles
2. Update `codebase-context.md` for significant changes
3. Test locally before deployment
4. Use semantic commit messages

## 📄 License

MIT License - see LICENSE file for details.

---

**Built with ❤️ by the Semrush AI Team**
