# AI Scorecard Dashboard - Codebase Context

## Project Overview
Building a real-time AI initiative tracking dashboard for Semrush that displays key performance metrics, financial impact, and project status across the organization's AI transformation journey, integrated with Monday.com API.

## Current State
- **Phase**: 🧪 TEST - Ready for testing and deployment
- **Architecture**: Complete React + Express application with GCP deployment
- **Data Source**: Monday.com API (Board ID: 8875778436) - Fully integrated
- **Deployment Target**: Google Cloud Platform (Cloud Run) - Ready to deploy
- **Status**: ✅ All core components implemented and functional

## Key Requirements Analysis

### Visual Design (Based on Mockup)
- **Header**: "AI & Automation Scorecard" - Clean, executive-level design
- **AI Literacy Section**: Multi-line chart showing weekly usage trends for Gemini, Claude, Cursor, ChatGPT
- **Training Cards**: New hire training completion rate, Teams with AI access
- **Active Initiatives**: 4-card row showing Backlog, In Flight, Completed, Total ROI
- **Department Grid**: Breakdown by IT, Marketing, Sales, Retention, Finance, etc.

### Monday.com Data Structure Analysis
From the API response, we have:
- **Total Items**: 47 initiatives across 4 groups
- **Groups**: 
  - "Intake - To evaluate" (24 items) → Backlog
  - "In progress - Active" (26 items) → In Flight  
  - "Completed - Archive" (13 items) → Completed
  - "On Hold or Closed" (7 items) → On Hold

### Key Financial Insights
Major ROI contributors identified:
1. **Conversational Search**: $2,731,820 (highest impact)
2. **Meeting Recording/Transcription**: $1,456,400
3. **AI Sales Assistants**: $515,040
4. **Content Creation Automation**: $360,000
5. **AI Assisted Candidate Management**: $260,000

**Total Calculated ROI**: ~$5.1M+ from active initiatives

### Department Distribution
- **IT**: 8 initiatives (highest count)
- **Marketing**: 7 initiatives  
- **Finance**: 6 initiatives
- **Sales**: 4 initiatives
- **HR**: 2 initiatives
- **Product**: 5 initiatives

## Technical Architecture

### Simple Stack (Following Tech Spec)
```
React App (Cloud Run) ← Express API (Cloud Run) ← Monday.com API
```

### Key Components Needed
1. **Frontend (React + Vite)**
   - ScorecardDashboard.jsx (main component)
   - AILiteracyChart.jsx (usage trends)
   - MetricCard.jsx (reusable cards)
   - DepartmentGrid.jsx (department breakdown)

2. **Backend (Express)**
   - Monday.com API integration
   - Data processing and aggregation
   - RESTful endpoints for dashboard data

3. **Deployment**
   - Single Dockerfile for combined frontend/backend
   - Cloud Run deployment with environment variables
   - Monday.com API key management

## Data Mapping Strategy

### Status Mapping
```javascript
const statusMapping = {
  'Backlog': 'backlog',
  'Evaluation': 'inFlight', 
  'Scoping': 'inFlight',
  'In Progress': 'inFlight',
  'Done': 'completed',
  'Closed': 'completed',
  'On Hold': 'onHold'
};
```

### Column IDs (Monday.com)
- `status`: Initiative status
- `dropdown_mkrbjyg7`: Function/Department
- `dropdown_mkq1ha1j`: Team
- `numeric_mkrd11hy`: Annual Savings Estimate (ROI)
- `text_mkr3b2hk`: Resources Saved (hours)
- `color_mkps7zrr`: Priority level

## Next Steps (🏗️ ARCHITECT Phase)
1. Set up project structure with React + Express
2. Design component hierarchy and data flow
3. Create Monday.com API service layer
4. Implement metrics calculation logic
5. Design responsive UI matching mockup
6. Set up GCP deployment configuration

## Mock Data for Development
Since AI usage metrics (Gemini, Claude, etc.) aren't in Monday.com, we'll use:
- Mock weekly usage data for chart visualization
- Placeholder team access metrics (14/18 teams)
- Sample training completion rates (78%)

## Color Scheme
```css
--primary-red: #FF4444;    /* Gemini line */
--primary-blue: #4A90E2;   /* Claude line */ 
--warning-yellow: #F5A623; /* Cursor line */
--success-green: #7ED321;  /* ChatGPT line */
--background: #F8F9FA;     /* Light background */
--card-bg: #FFFFFF;        /* Card background */
```

## File Structure Plan
```
ai-scorecard/
├── src/                    # React components
│   ├── components/
│   ├── hooks/
│   ├── services/
│   └── App.jsx
├── public/                 # Static files
├── server.js              # Express server
├── package.json           # Dependencies
├── Dockerfile             # Container config
└── README.md              # Documentation
