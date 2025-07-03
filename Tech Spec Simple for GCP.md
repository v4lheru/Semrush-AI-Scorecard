# AI Scorecard Dashboard - Simple GCP Deployment

## Keep It Simple Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React App     │    │   Express API    │    │   Monday.com    │
│   (Cloud Run)   │◄───┤   (Cloud Run)    │◄───┤   API           │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

That's it. No overcomplicated stuff.

## Frontend: React + Vite

### Simple React App Structure
```
src/
├── components/
│   ├── ScorecardDashboard.jsx
│   ├── AILiteracyChart.jsx
│   ├── MetricCard.jsx
│   └── DepartmentGrid.jsx
├── hooks/
│   └── useMondayData.js
├── services/
│   └── api.js
└── App.jsx
```

### Main App Component
```jsx
// App.jsx
import React from 'react';
import { ScorecardDashboard } from './components/ScorecardDashboard';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <ScorecardDashboard />
    </div>
  );
}

export default App;
```

### Scorecard Dashboard
```jsx
// components/ScorecardDashboard.jsx
import React from 'react';
import { useMondayData } from '../hooks/useMondayData';
import { AILiteracyChart } from './AILiteracyChart';
import { MetricCard } from './MetricCard';
import { DepartmentGrid } from './DepartmentGrid';

export const ScorecardDashboard = () => {
  const { data, loading, error } = useMondayData();

  if (loading) return <div className="p-8">Loading...</div>;
  if (error) return <div className="p-8 text-red-500">Error: {error}</div>;

  const metrics = {
    backlog: data.filter(item => item.status === 'Backlog').length,
    inFlight: data.filter(item => ['In Progress', 'Evaluation', 'Scoping'].includes(item.status)).length,
    completed: data.filter(item => ['Done', 'Closed'].includes(item.status)).length,
    totalROI: data.reduce((sum, item) => sum + (parseFloat(item.roi) || 0), 0)
  };

  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-4xl font-bold text-center mb-8">AI & Automation Scorecard</h1>
      
      {/* AI Literacy Section */}
      <div className="mb-8">
        <h2 className="text-2xl font-semibold mb-4">AI Literacy</h2>
        <AILiteracyChart />
        
        <div className="grid grid-cols-2 gap-6 mt-6">
          <MetricCard 
            title="New Hire Training"
            description="# of employees who have completed their trainings in first x weeks / total employees hired"
            value="78%"
          />
          <MetricCard 
            title="Teams with AI Access"
            description="Number of teams with access / total number of teams"
            value="14/18"
          />
        </div>
      </div>

      {/* Active Initiatives */}
      <div className="mb-8">
        <h2 className="text-2xl font-semibold mb-4">Active Initiatives</h2>
        <div className="grid grid-cols-4 gap-6">
          <MetricCard title="# Initiatives in Backlog" value={metrics.backlog} />
          <MetricCard title="# Initiatives in Flight" value={metrics.inFlight} />
          <MetricCard title="# Initiatives Completed" value={metrics.completed} />
          <MetricCard 
            title="Cumulative Projected ROI" 
            value={`$${(metrics.totalROI / 1000000).toFixed(1)}M`}
            highlight 
          />
        </div>
      </div>

      {/* Department Breakdown */}
      <div>
        <h2 className="text-2xl font-semibold mb-4">Active initiatives by department</h2>
        <DepartmentGrid data={data} />
      </div>
    </div>
  );
};
```

### Simple Data Hook
```javascript
// hooks/useMondayData.js
import { useState, useEffect } from 'react';

export const useMondayData = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/api/monday/board');
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    // Refresh every 5 minutes
    const interval = setInterval(fetchData, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  return { data, loading, error };
};
```

## Backend: Express API

### Simple Express Server
```javascript
// server.js
const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8080;

app.use(cors());
app.use(express.json());

// Serve React app
app.use(express.static(path.join(__dirname, 'dist')));

// Monday.com API endpoint
app.get('/api/monday/board', async (req, res) => {
  try {
    const mondayData = await fetchMondayBoard();
    const processedData = processMondayData(mondayData);
    res.json(processedData);
  } catch (error) {
    console.error('Error fetching Monday data:', error);
    res.status(500).json({ error: 'Failed to fetch data' });
  }
});

// Serve React app for all other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

// Monday.com API functions
async function fetchMondayBoard() {
  const query = `
    query {
      boards(ids: [8875778436]) {
        groups {
          items_page(limit: 100) {
            items {
              id
              name
              column_values {
                id
                text
              }
            }
          }
        }
      }
    }
  `;

  const response = await fetch('https://api.monday.com/v2', {
    method: 'POST',
    headers: {
      'Authorization': process.env.MONDAY_API_KEY,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ query })
  });

  const data = await response.json();
  return data.data.boards[0];
}

function processMondayData(boardData) {
  const items = boardData.groups.flatMap(group => group.items_page.items);
  
  return items.map(item => {
    const getColumnValue = (columnId) => {
      const column = item.column_values.find(cv => cv.id === columnId);
      return column?.text || '';
    };

    return {
      id: item.id,
      name: item.name,
      status: getColumnValue('status'),
      priority: getColumnValue('color_mkps7zrr'),
      function: getColumnValue('dropdown_mkrbjyg7'),
      team: getColumnValue('dropdown_mkq1ha1j'),
      roi: getColumnValue('numeric_mkrd11hy'),
      hoursSaved: getColumnValue('text_mkr3b2hk')
    };
  });
}
```

## Deployment: Simple Dockerfiles

### Frontend + Backend Combined
```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Build React app
RUN npm run build

# Start server
EXPOSE 8080
CMD ["npm", "start"]
```

### Simple package.json
```json
{
  "name": "ai-scorecard",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "start": "node server.js"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "recharts": "^2.8.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.1.0",
    "vite": "^4.4.5",
    "tailwindcss": "^3.3.3"
  }
}
```

## GCP Deployment: One Command

### Deploy to Cloud Run
```bash
# Build and deploy in one go
gcloud run deploy ai-scorecard \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars MONDAY_API_KEY="your-api-key-here"
```

That's it. Done.

### Environment Variables
```bash
# Just set this one environment variable
MONDAY_API_KEY=eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjUzMD...
```

## Project Structure
```
ai-scorecard/
├── src/                    # React components
├── public/                 # Static files
├── server.js              # Express server
├── package.json           # Dependencies
├── Dockerfile             # Container config
├── tailwind.config.js     # Styling
└── vite.config.js         # Build config
```

## What You Get
- ✅ **React dashboard** with your exact mockup design
- ✅ **Real Monday.com data** from your API
- ✅ **Automatic refresh** every 5 minutes
- ✅ **Responsive design** that works everywhere
- ✅ **One command deployment** to GCP
- ✅ **No complicated setup** or configuration

Just code it, build it, deploy it. Simple and effective.