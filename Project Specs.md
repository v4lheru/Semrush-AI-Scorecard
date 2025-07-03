# AI Scorecard Dashboard - Technical Specification

## Project Overview

Build a real-time AI initiative tracking dashboard for Semrush that displays key performance metrics, financial impact, and project status across the organization's AI transformation journey, integrated with Monday.com API.

## Visual Design Requirements & Mockup Analysis

### Executive Mockup Overview
Based on your boss's visual requirements, the scorecard should match this exact layout and design:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          AI & Automation Scorecard                          │
│                                                                             │
│  AI Literacy                                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │               Week over Week AI Usage Chart                          │   │
│  │  ┌─ Gemini (Red line, trending up)                                  │   │
│  │  ├─ Claude (Blue line, steady growth)                               │   │
│  │  ├─ Cursor (Yellow line, moderate growth)                           │   │
│  │  └─ ChatGPT (Green line, steady)                                    │   │
│  │                                                                     │   │
│  │   April 1-7   April 8-14   April 15-22   Etc...                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────┐  ┌─────────────────────────────────────────┐  │
│  │   New Hire Training     │  │        Teams with AI Access            │  │
│  │                         │  │                                         │  │
│  │ # of employees who have │  │ Number of teams with access / total    │  │
│  │ completed their         │  │ number of teams                         │  │
│  │ trainings in first x    │  │                                         │  │
│  │ weeks / total employees │  │                                         │  │
│  │ hired                   │  │                                         │  │
│  └─────────────────────────┘  └─────────────────────────────────────────┘  │
│                                                                             │
│  Active Initiatives                                                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐  │
│  │ # Initiatives│ │ # Initiatives│ │ # Initiatives│ │   Cumulative        │  │
│  │ in Backlog  │ │ in Flight   │ │ Completed   │ │   Projected ROI     │  │
│  │             │ │             │ │             │ │                     │  │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────────────┘  │
│                                                                             │
│  Active initiatives by department                                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐│
│  │     IT      │ │  Marketing  │ │    Sales    │ │  Retention  │ │ Finance ││
│  │             │ │             │ │             │ │             │ │         ││
│  │10 initiatives│ │10 initiatives│ │10 initiatives│ │10 initiatives│ │10 init..││
│  │   100K ROI  │ │   100K ROI  │ │   100K ROI  │ │   100K ROI  │ │100K ROI ││
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘│
│                                                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │    etc...   │ │    etc...   │ │    etc...   │ │    etc...   │           │
│  │             │ │             │ │             │ │             │           │
│  │10 initiatives│ │10 initiatives│ │10 initiatives│ │10 initiatives│           │
│  │   100K ROI  │ │   100K ROI  │ │   100K ROI  │ │   100K ROI  │           │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Detailed Design Specifications

#### 1. Header Section
- **Title**: "AI & Automation Scorecard" - Large, bold, centered
- **Background**: Clean white/light gray
- **Font**: Modern sans-serif (Inter, Roboto, or similar)

#### 2. AI Literacy Section
- **Line Chart**: Multi-colored trend lines showing weekly usage
  - **Gemini**: Red line (#FF4444) - Shows highest growth
  - **Claude**: Blue line (#4A90E2) - Steady upward trend  
  - **Cursor**: Yellow line (#F5A623) - Moderate growth
  - **ChatGPT**: Green line (#7ED321) - Steady baseline
- **X-Axis**: Weekly periods (April 1-7, April 8-14, etc.)
- **Y-Axis**: Usage metrics (cumulative users)
- **Chart Style**: Clean lines, subtle grid, legend on right

#### 3. Training & Access Cards
Two side-by-side rounded rectangular cards:
- **Left Card**: "New Hire Training"
  - Metric description in smaller text
  - Large number/percentage display
- **Right Card**: "Teams with AI Access" 
  - Shows ratio format (e.g., "14/18 teams")
  - Percentage completion bar

#### 4. Active Initiatives Row
Four equally-sized cards in a row:
- **Card 1**: "# Initiatives in Backlog" 
- **Card 2**: "# Initiatives in Flight"
- **Card 3**: "# Initiatives Completed"
- **Card 4**: "Cumulative Projected ROI" (highlighted/special styling)

#### 5. Department Breakdown Grid
- **Grid Layout**: 4-5 cards per row, multiple rows as needed
- **Card Design**: 
  - Department name at top
  - Initiative count (large number)
  - ROI value (formatted as $XXXk)
- **Departments**: IT, Marketing, Sales, Retention, Finance, HR, etc.
- **Styling**: Consistent card design with subtle shadows

### Color Scheme & Styling
```css
:root {
  --primary-red: #FF4444;    /* Gemini line */
  --primary-blue: #4A90E2;   /* Claude line */
  --warning-yellow: #F5A623; /* Cursor line */
  --success-green: #7ED321;  /* ChatGPT line */
  --background: #F8F9FA;     /* Light background */
  --card-bg: #FFFFFF;        /* Card background */
  --text-primary: #2C3E50;   /* Main text */
  --text-secondary: #7F8C8D; /* Secondary text */
  --border: #E9ECEF;         /* Card borders */
}
```

### Responsive Design Notes
- **Desktop**: Full grid layout as shown
- **Tablet**: Cards stack in 2-3 columns
- **Mobile**: Single column, stacked vertically
- **Charts**: Responsive and touch-friendly

### Data Visualization Requirements
1. **Usage Chart**: Real-time trend data with smooth animations
2. **Progress Indicators**: Visual bars/circles for completion rates
3. **Number Formatting**: Large, readable metrics (e.g., "$2.7M" instead of "2731820")
4. **Status Colors**: Green for completed, yellow for in-progress, red for backlog

### Interactive Elements
- **Hover Effects**: Cards lift slightly on hover
- **Click Actions**: Cards expand to show detailed breakdown
- **Real-time Updates**: Smooth transitions when data refreshes
- **Filtering**: Ability to filter by department or time period

This design prioritizes clarity, executive-level overview, and real-time monitoring of AI adoption across the organization.

### Monday.com API Response Structure
```json
{
  "data": {
    "boards": [{
      "id": "8875778436",
      "name": "AI Use Case Board",
      "columns": [
        {"id": "name", "title": "Name", "type": "name"},
        {"id": "status", "title": "Status", "type": "status"},
        {"id": "color_mkps7zrr", "title": "Priority", "type": "status"},
        {"id": "dropdown_mkrbjyg7", "title": "Function", "type": "dropdown"},
        {"id": "dropdown_mkq1ha1j", "title": "Team", "type": "dropdown"},
        {"id": "numeric_mkrd11hy", "title": "Annual Savings Est", "type": "numbers"},
        {"id": "text_mkr3b2hk", "title": "Resources Saved (in hrs)", "type": "text"},
        {"id": "text_mkrew80n", "title": "External Spend Saved", "type": "text"}
      ],
      "groups": [
        {"id": "group_mkq1qxks", "title": "Intake - To evaluate"},
        {"id": "topics", "title": "In progress - Active"},
        {"id": "group_mkpwxnsx", "title": "Completed - Archive"},
        {"id": "group_mkregf5g", "title": "On Hold or Closed"}
      ]
    }]
  }
}
```

### Key Financial Insights from Your Data

Based on the Monday.com API response, here are the major ROI contributors:

1. **Conversational Search**: $2,731,820 (massive impact!)
2. **Meeting Recording/Transcription**: $1,456,400  
3. **AI Sales Assistants**: $515,040
4. **Content Creation Automation**: $360,000
5. **AI Lead Routing**: $38,628
6. **IT Support Agent**: $26,832

**Total Calculated ROI**: ~$5.1M+ from active initiatives

#### Core Metrics Extraction
```typescript
interface ScorecardMetrics {
  // AI Literacy & Usage
  weeklyAIUsage: {
    gemini: number;
    claude: number;
    cursor: number;
    chatgpt: number;
  };
  
  // Team Access & Training
  teamsWithAIAccess: number;
  totalTeams: number;
  newHireTrainingRate: number;
  
  // Initiative Status
  initiativesInBacklog: number;
  initiativesInFlight: number;
  initiativesCompleted: number;
  cumulativeProjectedROI: number;
  
  // Department Breakdown
  departmentInitiatives: {
    IT: { count: number; roi: number };
    Marketing: { count: number; roi: number };
    Sales: { count: number; roi: number };
    Retention: { count: number; roi: number };
    Finance: { count: number; roi: number };
    HR: { count: number; roi: number };
  };
}
```

#### Status Mapping
```typescript
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

#### Financial Impact Extraction
```typescript
const extractFinancialImpact = (items: MondayItem[]) => {
  return items.reduce((total, item) => {
    // ROI is already calculated in Monday.com board
    const annualSavingsText = item.column_values.find(cv => cv.id === 'numeric_mkrd11hy')?.text;
    const annualSavings = annualSavingsText ? parseFloat(annualSavingsText) : 0;
    
    return total + annualSavings;
  }, 0);
};

// Example data points from your API:
// - Conversational Search: $2,731,820 ROI
// - AI Sales Assistants: $515,040 ROI  
// - Content Creation Automation: $360,000 ROI
// - Meeting Recording: $1,456,400 ROI
```

## GCP-Optimized Architecture

### Infrastructure Overview
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Cloud CDN     │    │   Load Balancer  │    │   Cloud Run     │
│   (Static       │◄───┤   (Global HTTPS) │◄───┤   (Frontend)    │
│    Assets)      │    │                  │    │   React App     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Cloud Storage │    │   Cloud Run      │    │   Cloud SQL     │
│   (Artifacts)   │    │   (Backend API)  │    │   (PostgreSQL)  │
│                 │    │   Node.js/Express│    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Cloud Build   │    │   Memorystore    │    │   Secret Manager│
│   (CI/CD)       │    │   (Redis Cache)  │    │   (API Keys)    │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### GCP Services Selection

#### 1. Frontend Hosting: Cloud Run
```dockerfile
# Frontend Dockerfile optimized for Cloud Run
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

COPY . .
RUN npm run build

# Multi-stage build for smaller image
FROM nginx:alpine AS runtime
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

# Cloud Run optimization
EXPOSE $PORT
CMD ["sh", "-c", "envsubst '$PORT' < /etc/nginx/nginx.conf > /tmp/nginx.conf && nginx -c /tmp/nginx.conf -g 'daemon off;'"]
```

#### 2. Backend API: Cloud Run
```dockerfile
# Backend Dockerfile optimized for Cloud Run
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM node:18-alpine AS runtime
WORKDIR /app

# Copy only production dependencies
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./

# Cloud Run requirements
ENV NODE_ENV=production
EXPOSE $PORT

# Health check for Cloud Run
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:$PORT/health || exit 1

CMD ["npm", "start"]
```

#### 3. Database: Cloud SQL (PostgreSQL)
```typescript
// Database connection optimized for Cloud SQL
import { Pool } from 'pg';

const createConnectionPool = () => {
  // Cloud SQL connection via Unix socket (recommended)
  const isProduction = process.env.NODE_ENV === 'production';
  
  if (isProduction && process.env.DB_SOCKET_PATH) {
    return new Pool({
      user: process.env.DB_USER,
      password: process.env.DB_PASSWORD,
      database: process.env.DB_NAME,
      host: process.env.DB_SOCKET_PATH,
      max: 5, // Cloud Run concurrency optimization
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 10000,
    });
  }
  
  // Development/local connection
  return new Pool({
    connectionString: process.env.DATABASE_URL,
    max: 5,
    ssl: isProduction ? { rejectUnauthorized: false } : false
  });
};

export const db = createConnectionPool();
```

#### 4. Caching: Memorystore (Redis)
```typescript
// Redis connection optimized for Memorystore
import Redis from 'ioredis';

const createRedisClient = () => {
  const isProduction = process.env.NODE_ENV === 'production';
  
  if (isProduction) {
    return new Redis({
      host: process.env.REDIS_HOST, // Memorystore internal IP
      port: parseInt(process.env.REDIS_PORT || '6379'),
      retryDelayOnFailover: 100,
      enableReadyCheck: false,
      maxRetriesPerRequest: 3,
      lazyConnect: true,
      connectTimeout: 10000,
      commandTimeout: 5000,
    });
  }
  
  return new Redis(process.env.REDIS_URL || 'redis://localhost:6379');
};

export const redis = createRedisClient();
```

### Cloud Build Configuration

#### CI/CD Pipeline
```yaml
# cloudbuild.yaml
steps:
  # Install dependencies
  - name: 'node:18'
    entrypoint: 'npm'
    args: ['ci']
    env:
      - 'NODE_ENV=production'

  # Run tests
  - name: 'node:18'
    entrypoint: 'npm'
    args: ['test']
    env:
      - 'CI=true'

  # Build application
  - name: 'node:18'
    entrypoint: 'npm'
    args: ['run', 'build']

  # Build and push frontend container
  - name: 'gcr.io/cloud-builders/docker'
    args: 
      - 'build'
      - '-t'
      - 'gcr.io/$PROJECT_ID/scorecard-frontend:$COMMIT_SHA'
      - '-f'
      - 'Dockerfile.frontend'
      - '.'

  # Build and push backend container  
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build' 
      - '-t'
      - 'gcr.io/$PROJECT_ID/scorecard-backend:$COMMIT_SHA'
      - '-f'
      - 'Dockerfile.backend'
      - '.'

  # Deploy frontend to Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: 'gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'scorecard-frontend'
      - '--image'
      - 'gcr.io/$PROJECT_ID/scorecard-frontend:$COMMIT_SHA'
      - '--region'
      - 'us-central1'
      - '--platform'
      - 'managed'
      - '--allow-unauthenticated'
      - '--memory'
      - '512Mi'
      - '--cpu'
      - '1'
      - '--max-instances'
      - '10'
      - '--concurrency'
      - '80'

  # Deploy backend to Cloud Run  
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: 'gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'scorecard-backend'
      - '--image'
      - 'gcr.io/$PROJECT_ID/scorecard-backend:$COMMIT_SHA'
      - '--region'
      - 'us-central1'
      - '--platform'
      - 'managed'
      - '--allow-unauthenticated'
      - '--memory'
      - '1Gi'
      - '--cpu'
      - '2'
      - '--max-instances'
      - '20'
      - '--concurrency'
      - '100'
      - '--set-env-vars'
      - 'NODE_ENV=production'

images:
  - 'gcr.io/$PROJECT_ID/scorecard-frontend:$COMMIT_SHA'
  - 'gcr.io/$PROJECT_ID/scorecard-backend:$COMMIT_SHA'

options:
  machineType: 'E2_HIGHCPU_8'
  logging: CLOUD_LOGGING_ONLY
```

### Secret Manager Integration
```typescript
// Secret Manager service for API keys
import { SecretManagerServiceClient } from '@google-cloud/secret-manager';

class SecretService {
  private client: SecretManagerServiceClient;
  private projectId: string;

  constructor() {
    this.client = new SecretManagerServiceClient();
    this.projectId = process.env.GOOGLE_CLOUD_PROJECT || '';
  }

  async getSecret(secretName: string): Promise<string> {
    try {
      const name = `projects/${this.projectId}/secrets/${secretName}/versions/latest`;
      const [version] = await this.client.accessSecretVersion({ name });
      
      return version.payload?.data?.toString() || '';
    } catch (error) {
      console.error(`Failed to get secret ${secretName}:`, error);
      throw error;
    }
  }

  // Cache secrets for the container lifetime
  private secretCache = new Map<string, string>();
  
  async getCachedSecret(secretName: string): Promise<string> {
    if (this.secretCache.has(secretName)) {
      return this.secretCache.get(secretName)!;
    }
    
    const secret = await this.getSecret(secretName);
    this.secretCache.set(secretName, secret);
    return secret;
  }
}

export const secretService = new SecretService();

// Usage in application
const mondayApiKey = await secretService.getCachedSecret('monday-api-key');
```

### Cloud Monitoring & Logging
```typescript
// Monitoring and error reporting setup
import { createPrometheusMetrics } from 'prom-client';
import winston from 'winston';
import { LoggingWinston } from '@google-cloud/logging-winston';

// Cloud Logging setup
const loggingWinston = new LoggingWinston({
  projectId: process.env.GOOGLE_CLOUD_PROJECT,
  keyFilename: process.env.GOOGLE_APPLICATION_CREDENTIALS,
});

export const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
    loggingWinston,
  ],
});

// Custom metrics for monitoring
import client from 'prom-client';

export const metrics = {
  httpRequests: new client.Counter({
    name: 'http_requests_total',
    help: 'Total number of HTTP requests',
    labelNames: ['method', 'route', 'status'],
  }),
  
  mondayApiCalls: new client.Counter({
    name: 'monday_api_calls_total', 
    help: 'Total Monday.com API calls',
    labelNames: ['status'],
  }),
  
  responseTime: new client.Histogram({
    name: 'http_request_duration_seconds',
    help: 'HTTP request duration in seconds',
    labelNames: ['method', 'route'],
  }),
};
```

### Environment Configuration
```typescript
// GCP-optimized environment configuration
export const config = {
  // Cloud Run environment
  port: process.env.PORT || 8080,
  
  // Cloud SQL
  database: {
    host: process.env.DB_SOCKET_PATH || process.env.DB_HOST,
    port: parseInt(process.env.DB_PORT || '5432'),
    name: process.env.DB_NAME || 'scorecard',
    user: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD,
    ssl: process.env.NODE_ENV === 'production',
    pool: {
      min: 1,
      max: 5, // Cloud Run concurrency limit
      acquire: 30000,
      idle: 10000,
    },
  },
  
  // Memorystore Redis
  redis: {
    host: process.env.REDIS_HOST,
    port: parseInt(process.env.REDIS_PORT || '6379'),
    ttl: 300, // 5 minutes default TTL
  },
  
  // Monday.com API
  monday: {
    apiUrl: 'https://api.monday.com/v2',
    boardId: '8875778436',
    rateLimitDelay: 1000, // 1 second between requests
  },
  
  // Cloud Storage
  storage: {
    bucketName: process.env.GCS_BUCKET_NAME,
    keyFilename: process.env.GOOGLE_APPLICATION_CREDENTIALS,
  },
  
  // Monitoring
  monitoring: {
    enableMetrics: true,
    metricsPath: '/metrics',
    healthPath: '/health',
  },
};
```

### Performance Optimizations

#### Frontend Optimizations
```typescript
// Code splitting for Cloud CDN
import { lazy, Suspense } from 'react';

const ScorecardDashboard = lazy(() => import('./components/ScorecardDashboard'));
const AdminPanel = lazy(() => import('./components/AdminPanel'));

// Service Worker for caching
// public/sw.js
const CACHE_NAME = 'scorecard-v1';
const urlsToCache = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/api/scorecard/overview'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});
```

#### Backend Optimizations
```typescript
// Connection pooling and caching middleware
import compression from 'compression';
import helmet from 'helmet';

app.use(helmet()); // Security headers
app.use(compression()); // Gzip compression

// Caching middleware
const cacheMiddleware = (ttl = 300) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    const key = `cache:${req.originalUrl}`;
    
    try {
      const cached = await redis.get(key);
      if (cached) {
        return res.json(JSON.parse(cached));
      }
      
      // Store original json method
      const originalJson = res.json;
      res.json = function(data) {
        redis.setex(key, ttl, JSON.stringify(data));
        return originalJson.call(this, data);
      };
      
      next();
    } catch (error) {
      logger.error('Cache middleware error:', error);
      next();
    }
  };
};

// Apply caching to scorecard endpoints
app.get('/api/scorecard/overview', cacheMiddleware(300), getScorecardOverview);
```

### Cost Optimization Strategies

#### 1. Auto-scaling Configuration
```yaml
# Cloud Run auto-scaling for cost efficiency
metadata:
  annotations:
    run.googleapis.com/execution-environment: gen2
    autoscaling.knative.dev/minScale: "0"  # Scale to zero when not in use
    autoscaling.knative.dev/maxScale: "10"
    run.googleapis.com/cpu-throttling: "true"
```

#### 2. Scheduled Jobs for Data Sync
```typescript
// Cloud Scheduler integration for batch updates
import { CloudSchedulerClient } from '@google-cloud/scheduler';

// Update Monday.com data every 5 minutes during business hours
const scheduledSync = async () => {
  const now = new Date();
  const hour = now.getHours();
  
  // Only sync during business hours (9 AM - 6 PM EST)
  if (hour >= 9 && hour <= 18) {
    await syncMondayData();
  }
};
```

This GCP-optimized architecture provides:
- **Serverless scaling** with Cloud Run
- **Managed database** with Cloud SQL
- **Global CDN** for static assets
- **Integrated monitoring** with Cloud Operations
- **Secure secret management**
- **Cost-effective auto-scaling**
- **Production-ready CI/CD** with Cloud Build

## Frontend Architecture

### Framework Choice: React + TypeScript
```typescript
// Core Tech Stack
- React 18+ with TypeScript
- State Management: Zustand (lightweight alternative to Redux)
- Styling: Tailwind CSS + Framer Motion
- Charts: Recharts for data visualization
- HTTP Client: Axios with React Query
- Build Tool: Vite
- Testing: Vitest + React Testing Library
```

### Component Structure
```
src/
├── components/
│   ├── common/
│   │   ├── MetricCard.tsx
│   │   ├── ProgressBar.tsx
│   │   ├── StatusIndicator.tsx
│   │   └── LoadingSpinner.tsx
│   ├── scorecard/
│   │   ├── ScorecardHeader.tsx
│   │   ├── AILiteracySection.tsx
│   │   ├── ActiveInitiatives.tsx
│   │   ├── DepartmentBreakdown.tsx
│   │   └── FinancialMetrics.tsx
│   └── charts/
│       ├── UsageTrendChart.tsx
│       ├── DepartmentChart.tsx
│       └── ROIChart.tsx
├── hooks/
│   ├── useMondayData.ts
│   ├── useMetricsCalculation.ts
│   └── useRealTimeUpdates.ts
├── services/
│   ├── mondayAPI.ts
│   ├── metricsCalculator.ts
│   └── websocket.ts
├── stores/
│   ├── scorecardStore.ts
│   └── settingsStore.ts
├── types/
│   ├── monday.types.ts
│   ├── scorecard.types.ts
│   └── api.types.ts
└── utils/
    ├── dateHelpers.ts
    ├── formatters.ts
    └── constants.ts
```

### Key React Components

#### Main Scorecard Component
```typescript
// ScorecardDashboard.tsx
import React from 'react';
import { useMondayData } from '@/hooks/useMondayData';
import { useMetricsCalculation } from '@/hooks/useMetricsCalculation';
import { ScorecardHeader } from '@/components/scorecard/ScorecardHeader';
import { AILiteracySection } from '@/components/scorecard/AILiteracySection';
import { ActiveInitiatives } from '@/components/scorecard/ActiveInitiatives';
import { DepartmentBreakdown } from '@/components/scorecard/DepartmentBreakdown';

export const ScorecardDashboard: React.FC = () => {
  const { data: mondayData, isLoading, error } = useMondayData();
  const metrics = useMetricsCalculation(mondayData);

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <ScorecardHeader />
      <div className="container mx-auto px-6 py-8 space-y-8">
        <AILiteracySection metrics={metrics} />
        <ActiveInitiatives metrics={metrics} />
        <DepartmentBreakdown metrics={metrics} />
      </div>
    </div>
  );
};
```

#### Custom Hook for Monday.com Data
```typescript
// hooks/useMondayData.ts
import { useQuery } from '@tanstack/react-query';
import { mondayAPI } from '@/services/mondayAPI';
import type { MondayBoard } from '@/types/monday.types';

export const useMondayData = () => {
  return useQuery({
    queryKey: ['monday-board', '8875778436'],
    queryFn: () => mondayAPI.getBoard('8875778436'),
    refetchInterval: 5 * 60 * 1000, // Refetch every 5 minutes
    staleTime: 2 * 60 * 1000, // Consider data stale after 2 minutes
  });
};
```

#### Metrics Calculation Hook
```typescript
// hooks/useMetricsCalculation.ts
import { useMemo } from 'react';
import type { MondayBoard, ScorecardMetrics } from '@/types';

export const useMetricsCalculation = (mondayData: MondayBoard | undefined): ScorecardMetrics => {
  return useMemo(() => {
    if (!mondayData) return defaultMetrics;

    const items = mondayData.groups.flatMap(group => group.items_page.items);
    
    // Calculate initiative counts by status
    const statusCounts = items.reduce((acc, item) => {
      const status = item.column_values.find(cv => cv.id === 'status')?.text || 'Unknown';
      const mappedStatus = statusMapping[status] || 'other';
      acc[mappedStatus] = (acc[mappedStatus] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    // Calculate department breakdown
    const departmentBreakdown = items.reduce((acc, item) => {
      const function_val = item.column_values.find(cv => cv.id === 'dropdown_mkrbjyg7')?.text;
      const annualSavings = parseFloat(item.column_values.find(cv => cv.id === 'numeric_mkrd11hy')?.text || '0');
      
      if (function_val && acc[function_val]) {
        acc[function_val].count += 1;
        acc[function_val].roi += annualSavings;
      }
      
      return acc;
    }, {} as Record<string, {count: number, roi: number}>);

    // Calculate total financial impact
    const totalROI = calculateFinancialImpact(items);

    return {
      initiativesInBacklog: statusCounts.backlog || 0,
      initiativesInFlight: statusCounts.inFlight || 0,
      initiativesCompleted: statusCounts.completed || 0,
      cumulativeProjectedROI: totalROI,
      departmentInitiatives: departmentBreakdown,
      // Mock data for AI usage - would come from separate API
      weeklyAIUsage: {
        gemini: 45,
        claude: 32,
        cursor: 28,
        chatgpt: 38
      },
      teamsWithAIAccess: 14,
      totalTeams: 18,
      newHireTrainingRate: 0.78
    };
  }, [mondayData]);
};
```

## Backend Architecture

### API Design
```typescript
// Core API Endpoints
GET  /api/scorecard/overview           // Main dashboard data
GET  /api/scorecard/monday-sync        // Sync with Monday.com
GET  /api/scorecard/ai-usage          // AI tool usage metrics
GET  /api/scorecard/financial-impact  // ROI calculations
POST /api/scorecard/refresh           // Force data refresh
PUT  /api/scorecard/settings          // Update dashboard settings

// WebSocket for real-time updates
WebSocket: /ws/scorecard-updates
```

### Node.js Backend Implementation
```typescript
// server.ts
import express from 'express';
import cors from 'cors';
import { createServer } from 'http';
import { Server } from 'socket.io';
import { mondayRouter } from './routes/monday';
import { scorecardRouter } from './routes/scorecard';

const app = express();
const server = createServer(app);
const io = new Server(server, {
  cors: { origin: process.env.CLIENT_URL }
});

app.use(cors());
app.use(express.json());

// Routes
app.use('/api/monday', mondayRouter);
app.use('/api/scorecard', scorecardRouter);

// WebSocket connection
io.on('connection', (socket) => {
  console.log('Client connected');
  
  socket.on('subscribe-scorecard', () => {
    socket.join('scorecard-updates');
  });
});

// Periodic data sync
setInterval(async () => {
  const updatedData = await syncMondayData();
  io.to('scorecard-updates').emit('data-updated', updatedData);
}, 5 * 60 * 1000); // Every 5 minutes

server.listen(process.env.PORT || 3001);
```

### Monday.com API Service
```typescript
// services/mondayService.ts
import axios from 'axios';

const MONDAY_API_URL = 'https://api.monday.com/v2';

export class MondayService {
  private readonly apiKey: string;
  private readonly boardId: string = '8875778436';

  constructor(apiKey: string) {
    this.apiKey = apiKey;
  }

  async getBoardData() {
    const query = `
      query {
        boards(ids: [${this.boardId}]) {
          id
          name
          description
          columns {
            id
            title
            type
          }
          groups {
            id
            title
            items_page(limit: 100) {
              items {
                id
                name
                column_values {
                  id
                  text
                  value
                }
              }
            }
          }
        }
      }
    `;

    const response = await axios.post(MONDAY_API_URL, 
      { query },
      {
        headers: {
          'Authorization': this.apiKey,
          'Content-Type': 'application/json'
        }
      }
    );

    return response.data.data.boards[0];
  }

  async getUpdatedItems(since: Date) {
    // Implementation for incremental updates
  }
}
```

### Metrics Calculator Service
```typescript
// services/metricsCalculator.ts
export class MetricsCalculator {
  static calculateScorecardMetrics(mondayData: MondayBoard): ScorecardMetrics {
    const items = this.flattenBoardItems(mondayData);
    
    return {
      initiativesInBacklog: this.countByStatus(items, 'Backlog'),
      initiativesInFlight: this.countByStatus(items, ['In Progress', 'Evaluation', 'Scoping']),
      initiativesCompleted: this.countByStatus(items, ['Done', 'Closed']),
      cumulativeProjectedROI: this.calculateTotalROI(items),
      departmentInitiatives: this.calculateDepartmentBreakdown(items),
      weeklyAIUsage: this.getAIUsageMetrics(), // From separate tracking
      teamsWithAIAccess: this.calculateTeamAccess(items),
      totalTeams: this.getTotalTeamsCount(),
      newHireTrainingRate: this.getTrainingCompletionRate()
    };
  }

  private static calculateTotalROI(items: MondayItem[]): number {
    return items.reduce((total, item) => {
      // ROI is pre-calculated in Monday.com board
      const annualSavingsText = item.column_values.find(cv => cv.id === 'numeric_mkrd11hy')?.text;
      const annualSavings = annualSavingsText ? parseFloat(annualSavingsText) : 0;
      
      return total + annualSavings;
    }, 0);
  }

  private static getTopROIInitiatives(items: MondayItem[], limit: number = 5) {
    return items
      .map(item => ({
        name: item.name,
        roi: parseFloat(item.column_values.find(cv => cv.id === 'numeric_mkrd11hy')?.text || '0'),
        status: item.column_values.find(cv => cv.id === 'status')?.text || 'Unknown',
        function: item.column_values.find(cv => cv.id === 'dropdown_mkrbjyg7')?.text || 'Unknown'
      }))
      .filter(item => item.roi > 0)
      .sort((a, b) => b.roi - a.roi)
      .slice(0, limit);
  }
}
```

## Data Flow & State Management

### Zustand Store
```typescript
// stores/scorecardStore.ts
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

interface ScorecardState {
  metrics: ScorecardMetrics | null;
  isLoading: boolean;
  error: string | null;
  lastUpdated: Date | null;
  
  // Actions
  setMetrics: (metrics: ScorecardMetrics) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  updateLastUpdated: () => void;
}

export const useScorecardStore = create<ScorecardState>()(
  devtools((set) => ({
    metrics: null,
    isLoading: false,
    error: null,
    lastUpdated: null,
    
    setMetrics: (metrics) => set({ metrics }),
    setLoading: (isLoading) => set({ isLoading }),
    setError: (error) => set({ error }),
    updateLastUpdated: () => set({ lastUpdated: new Date() })
  }))
);
```

## Deployment & Infrastructure

### Docker Configuration
```dockerfile
# Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM node:18-alpine AS runtime
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

EXPOSE 3001
CMD ["npm", "start"]
```

### Environment Configuration
```env
# .env
NODE_ENV=production
PORT=3001
CLIENT_URL=http://localhost:3000

# Monday.com API
MONDAY_API_KEY=your_monday_api_key
MONDAY_BOARD_ID=8875778436

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/scorecard
REDIS_URL=redis://localhost:6379

# WebSocket
WS_PORT=3002
```

### CI/CD Pipeline
```yaml
# .github/workflows/deploy.yml
name: Deploy Scorecard
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
      
      - name: Build application
        run: npm run build
      
      - name: Deploy to production
        run: |
          docker build -t scorecard-app .
          docker push ${{ secrets.DOCKER_REGISTRY }}/scorecard-app:latest
```

## Testing Strategy

### Unit Tests
```typescript
// __tests__/metricsCalculator.test.ts
import { MetricsCalculator } from '@/services/metricsCalculator';
import { mockMondayData } from '@/tests/fixtures/mondayData';

describe('MetricsCalculator', () => {
  it('should calculate correct initiative counts', () => {
    const metrics = MetricsCalculator.calculateScorecardMetrics(mockMondayData);
    
    expect(metrics.initiativesInBacklog).toBe(17);
    expect(metrics.initiativesInFlight).toBe(17);
    expect(metrics.initiativesCompleted).toBe(13);
  });

  it('should calculate accurate ROI from hours saved', () => {
    const metrics = MetricsCalculator.calculateScorecardMetrics(mockMondayData);
    
    expect(metrics.cumulativeProjectedROI).toBeGreaterThan(0);
  });
});
```

### Integration Tests
```typescript
// __tests__/api.integration.test.ts
import request from 'supertest';
import { app } from '@/server';

describe('/api/scorecard', () => {
  it('should return scorecard overview', async () => {
    const response = await request(app)
      .get('/api/scorecard/overview')
      .expect(200);
    
    expect(response.body).toHaveProperty('metrics');
    expect(response.body.metrics).toHaveProperty('initiativesInBacklog');
  });
});
```

## Performance Considerations

### Caching Strategy
- Redis for API response caching (5-minute TTL)
- Browser caching for static assets
- Service worker for offline support

### Optimization Techniques
- React.memo for component memoization
- useMemo/useCallback for expensive calculations
- Lazy loading for dashboard sections
- WebSocket for real-time updates instead of polling

### Monitoring & Analytics
- Application Performance Monitoring (APM)
- Error tracking with Sentry
- Custom metrics for dashboard usage
- Monday.com API rate limit monitoring

## Security Considerations

### Authentication & Authorization
- JWT tokens for API authentication
- Role-based access control
- Monday.com API key security
- CORS configuration

### Data Protection
- Input validation and sanitization
- API rate limiting
- Secure WebSocket connections
- Environment variable protection

This specification provides a complete technical roadmap for building the AI Scorecard Dashboard with real Monday.com integration, matching your mockup requirements while ensuring scalability and maintainability.