import express from 'express'
import cors from 'cors'
import path from 'path'
import axios from 'axios'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const app = express()
const PORT = process.env.PORT || 8080

// Middleware
app.use(cors())
app.use(express.json())

// Serve React app (both development and production)
app.use(express.static(path.join(__dirname, 'dist')))

// Monday.com API configuration
const MONDAY_API_URL = 'https://api.monday.com/v2'
const MONDAY_API_KEY = process.env.MONDAY_API_KEY || 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjUzMDI3Mjg0MCwiYWFpIjoxMSwidWlkIjo3NDE4MDY3OCwiaWFkIjoiMjAyNS0wNi0yNFQxMTo0Nzo0Ni4wMDdaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTc0OTAxMSwicmduIjoidXNlMSJ9.DD-rnSR6oKQmJpwWX5AiaB7Y600WB959l-buFfIbk6U'
const BOARD_ID = '8875778436'

// Monday.com API functions
async function fetchMondayBoard() {
  const query = `
    query {
      boards(ids: [${BOARD_ID}]) {
        id
        name
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
              }
            }
          }
        }
      }
    }
  `

  try {
    const response = await axios.post(MONDAY_API_URL, 
      { query },
      {
        headers: {
          'Authorization': MONDAY_API_KEY,
          'Content-Type': 'application/json'
        }
      }
    )

    if (response.data.errors) {
      throw new Error(`Monday.com API error: ${JSON.stringify(response.data.errors)}`)
    }

    return response.data.data.boards[0]
  } catch (error) {
    console.error('Error fetching Monday board:', error.message)
    throw error
  }
}

function processMondayData(boardData) {
  if (!boardData || !boardData.groups) {
    return []
  }

  const items = boardData.groups.flatMap(group => group.items_page.items)
  
  return items.map(item => {
    const getColumnValue = (columnId) => {
      const column = item.column_values.find(cv => cv.id === columnId)
      return column?.text || ''
    }

    // Parse ROI value
    const roiText = getColumnValue('numeric_mkrd11hy')
    const roi = roiText ? parseFloat(roiText) : 0

    return {
      id: item.id,
      name: item.name,
      status: getColumnValue('status'),
      priority: getColumnValue('color_mkps7zrr'),
      function: getColumnValue('dropdown_mkrbjyg7'),
      team: getColumnValue('dropdown_mkq1ha1j'),
      roi: roi,
      hoursSaved: getColumnValue('text_mkr3b2hk'),
      externalSpendSaved: getColumnValue('text_mkrew80n'),
      complexity: getColumnValue('color_mkpsfh88'),
      protoDelivDate: getColumnValue('date4'),
      goLiveDate: getColumnValue('date_mkpxvzvr')
    }
  })
}

// API Routes
app.get('/api/monday/board', async (req, res) => {
  try {
    console.log('Fetching Monday.com board data...')
    const boardData = await fetchMondayBoard()
    const processedData = processMondayData(boardData)
    
    console.log(`Successfully processed ${processedData.length} initiatives`)
    res.json(processedData)
  } catch (error) {
    console.error('Error in /api/monday/board:', error.message)
    res.status(500).json({ 
      error: 'Failed to fetch Monday.com data',
      message: error.message 
    })
  }
})

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    timestamp: new Date().toISOString(),
    environment: process.env.NODE_ENV || 'development'
  })
})

// Optimized Gemini usage data endpoint (cached + live)
app.get('/api/gemini/usage', async (req, res) => {
  try {
    console.log('🚀 Fetching optimized Gemini data (cached historical + live current)...')
    
    // Execute optimized cached Python script
    const { spawn } = await import('child_process')
    
    const pythonProcess = spawn('python3', ['gemini_tracker_cached.py'], {
      env: {
        ...process.env,
        GOOGLE_SERVICE_ACCOUNT_FILE: process.env.GOOGLE_SERVICE_ACCOUNT_FILE || 'service-account.json',
        DOMAIN_ADMIN_EMAIL: process.env.DOMAIN_ADMIN_EMAIL || 'i.karlakis@semrush.com'
      }
    })

    let pythonOutput = ''
    let pythonError = ''

    pythonProcess.stdout.on('data', (data) => {
      pythonOutput += data.toString()
    })

    pythonProcess.stderr.on('data', (data) => {
      pythonError += data.toString()
    })

    pythonProcess.on('close', (code) => {
      try {
        if (code === 0 && pythonOutput) {
          // Parse JSON output from cached Python script
          const geminiData = JSON.parse(pythonOutput)
          console.log(`✅ Optimized Gemini data: ${geminiData.summary.latest_week_users} users (${geminiData.cache_status.historical_cached ? 'cached' : 'fresh'} historical + live current)`)
          res.json(geminiData)
        } else {
          // Fallback to mock data if Python script fails
          console.log(`⚠️ Cached Python script failed (code: ${code}), using fallback data`)
          console.log('Python error:', pythonError)
          
          const fallbackData = {
            summary: {
              total_cumulative_users: 298,
              latest_week_activities: 6059,
              latest_week_users: 298,
              total_weeks_tracked: 4
            },
            time_series: {
              weeks: ['Week 1 (Jun 20-22)', 'Week 2 (Jun 23-29)', 'Week 3 (Jun 30-Jul 6)', 'Week 4 (Jul 7-Current)'],
              total_weekly_users: [127, 280, 274, 298],
              weekly_activities: [968, 4731, 4738, 6059],
              weekly_unique_users: [127, 280, 274, 298],
              wow_growth_percent: [120.5, -2.1, 8.8]
            },
            latest_week_breakdown: {
              actions: {'classic_use_case_gemini_app': 6059},
              categories: {'standalone_gemini': 6059},
              top_users: []
            },
            last_updated: new Date().toISOString(),
            data_source: `Fallback data - Python error: ${pythonError || 'Unknown error'}`,
            error: true,
            cache_status: {
              historical_cached: false,
              current_week_live: false
            }
          }
          
          res.json(fallbackData)
        }
      } catch (parseError) {
        console.error('Error parsing cached Python output:', parseError)
        res.status(500).json({
          error: 'Failed to parse optimized Gemini data',
          message: parseError.message,
          python_output: pythonOutput,
          python_error: pythonError
        })
      }
    })

    // Set timeout for Python script execution (shorter since it's cached)
    setTimeout(() => {
      pythonProcess.kill('SIGTERM')
      console.log('⚠️ Cached Python script timeout, using fallback data')
    }, 15000) // 15 second timeout (faster with caching)

  } catch (error) {
    console.error('Error in /api/gemini/usage:', error.message)
    res.status(500).json({ 
      error: 'Failed to fetch optimized Gemini usage data',
      message: error.message 
    })
  }
})

// Gemini Deep Dive endpoint (all apps analysis)
app.get('/api/gemini/deep-dive', async (req, res) => {
  try {
    console.log('🔍 Fetching Gemini deep dive data (all apps, cached + live)...')
    
    // Execute deep dive cached Python script
    const { spawn } = await import('child_process')
    
    const pythonProcess = spawn('python3', ['gemini_deep_dive_cached.py'], {
      env: {
        ...process.env,
        GOOGLE_SERVICE_ACCOUNT_FILE: process.env.GOOGLE_SERVICE_ACCOUNT_FILE || 'service-account.json',
        DOMAIN_ADMIN_EMAIL: process.env.DOMAIN_ADMIN_EMAIL || 'i.karlakis@semrush.com'
      }
    })

    let pythonOutput = ''
    let pythonError = ''

    pythonProcess.stdout.on('data', (data) => {
      pythonOutput += data.toString()
    })

    pythonProcess.stderr.on('data', (data) => {
      pythonError += data.toString()
    })

    pythonProcess.on('close', (code) => {
      try {
        if (code === 0 && pythonOutput) {
          // Parse JSON output from deep dive script
          const deepDiveData = JSON.parse(pythonOutput)
          console.log(`✅ Deep dive data: ${deepDiveData.summary.total_apps_used} apps, ${deepDiveData.summary.total_actions_tracked} actions`)
          res.json(deepDiveData)
        } else {
          // Fallback to mock data if Python script fails
          console.log(`⚠️ Deep dive script failed (code: ${code}), using fallback data`)
          console.log('Python error:', pythonError)
          
          const fallbackData = {
            summary: {
              total_apps_used: 7,
              total_actions_tracked: 50,
              weeks_analyzed: 4,
              latest_week_activities: 15000
            },
            app_analysis: {
              top_apps: {
                'gmail': {'total_activities': 35000, 'max_weekly_users': 1200},
                'gemini_app': {'total_activities': 16000, 'max_weekly_users': 300},
                'drive': {'total_activities': 8000, 'max_weekly_users': 200},
                'docs': {'total_activities': 2000, 'max_weekly_users': 50},
                'sheets': {'total_activities': 1500, 'max_weekly_users': 40}
              },
              app_trends: {}
            },
            action_analysis: {
              top_actions: {
                'suggest_full_replies': 25000,
                'classic_use_case_gemini_app': 16000,
                'summarize': 8000,
                'generate_text': 5000,
                'proofread': 3000
              },
              action_trends: {}
            },
            weekly_trends: [],
            last_updated: new Date().toISOString(),
            data_source: `Fallback data - Deep dive error: ${pythonError || 'Unknown error'}`,
            error: true,
            cache_status: {
              historical_cached: false,
              current_week_live: false
            }
          }
          
          res.json(fallbackData)
        }
      } catch (parseError) {
        console.error('Error parsing deep dive output:', parseError)
        res.status(500).json({
          error: 'Failed to parse deep dive data',
          message: parseError.message,
          python_output: pythonOutput,
          python_error: pythonError
        })
      }
    })

    // Set timeout for deep dive script
    setTimeout(() => {
      pythonProcess.kill('SIGTERM')
      console.log('⚠️ Deep dive script timeout, using fallback data')
    }, 20000) // 20 second timeout

  } catch (error) {
    console.error('Error in /api/gemini/deep-dive:', error.message)
    res.status(500).json({ 
      error: 'Failed to fetch Gemini deep dive data',
      message: error.message 
    })
  }
})

// Metrics endpoint for monitoring
app.get('/api/metrics', async (req, res) => {
  try {
    const boardData = await fetchMondayBoard()
    const processedData = processMondayData(boardData)
    
    // Calculate summary metrics
    const statusCounts = processedData.reduce((acc, item) => {
      const status = item.status || 'Unknown'
      acc[status] = (acc[status] || 0) + 1
      return acc
    }, {})

    const departmentCounts = processedData.reduce((acc, item) => {
      const dept = item.function || 'Other'
      acc[dept] = (acc[dept] || 0) + 1
      return acc
    }, {})

    const totalROI = processedData.reduce((sum, item) => sum + (item.roi || 0), 0)

    res.json({
      totalInitiatives: processedData.length,
      statusBreakdown: statusCounts,
      departmentBreakdown: departmentCounts,
      totalROI: totalROI,
      lastUpdated: new Date().toISOString()
    })
  } catch (error) {
    console.error('Error in /api/metrics:', error.message)
    res.status(500).json({ error: 'Failed to calculate metrics' })
  }
})

// Serve React app for all other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'))
})

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err)
  res.status(500).json({ error: 'Internal server error' })
})

// Start server
app.listen(PORT, () => {
  console.log(`🚀 AI Scorecard server running on port ${PORT}`)
  console.log(`📊 Dashboard: http://localhost:${PORT}`)
  console.log(`🔗 API Health: http://localhost:${PORT}/api/health`)
  console.log(`📈 Metrics: http://localhost:${PORT}/api/metrics`)
  
  if (process.env.NODE_ENV !== 'production') {
    console.log(`🛠️  Development mode - Frontend: http://localhost:3000`)
  }
})

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully')
  process.exit(0)
})

process.on('SIGINT', () => {
  console.log('SIGINT received, shutting down gracefully')
  process.exit(0)
})
