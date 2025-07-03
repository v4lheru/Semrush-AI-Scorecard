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

// Gemini usage data endpoint
app.get('/api/gemini/usage', async (req, res) => {
  try {
    console.log('Fetching live Gemini usage data from Python script...')
    
    // Execute Python script to get live Gemini data
    const { spawn } = await import('child_process')
    
    const pythonProcess = spawn('python3', ['gemini_tracker.py'], {
      env: {
        ...process.env,
        GOOGLE_SERVICE_ACCOUNT_FILE: process.env.GOOGLE_SERVICE_ACCOUNT_FILE || 'service-account.json',
        DOMAIN_ADMIN_EMAIL: process.env.DOMAIN_ADMIN_EMAIL || 'admin@semrush.com'
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
          // Parse JSON output from Python script
          const geminiData = JSON.parse(pythonOutput)
          console.log(`✅ Successfully fetched Gemini data: ${geminiData.summary.total_cumulative_users} users`)
          res.json(geminiData)
        } else {
          // Fallback to mock data if Python script fails
          console.log(`⚠️ Python script failed (code: ${code}), using fallback data`)
          console.log('Python error:', pythonError)
          
          const fallbackData = {
            summary: {
              total_cumulative_users: 0,
              latest_week_activities: 0,
              latest_week_users: 0,
              total_weeks_tracked: 6
            },
            time_series: {
              weeks: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6'],
              cumulative_users: [0, 0, 0, 0, 0, 0],
              weekly_activities: [0, 0, 0, 0, 0, 0],
              weekly_unique_users: [0, 0, 0, 0, 0, 0],
              wow_growth_percent: [0, 0, 0, 0, 0]
            },
            latest_week_breakdown: {
              actions: {},
              categories: {},
              top_users: []
            },
            last_updated: new Date().toISOString(),
            data_source: `Python script error: ${pythonError || 'Unknown error'}`,
            error: true
          }
          
          res.json(fallbackData)
        }
      } catch (parseError) {
        console.error('Error parsing Python output:', parseError)
        res.status(500).json({
          error: 'Failed to parse Gemini data',
          message: parseError.message,
          python_output: pythonOutput,
          python_error: pythonError
        })
      }
    })

    // Set timeout for Python script execution
    setTimeout(() => {
      pythonProcess.kill('SIGTERM')
      console.log('⚠️ Python script timeout, using fallback data')
    }, 30000) // 30 second timeout

  } catch (error) {
    console.error('Error in /api/gemini/usage:', error.message)
    res.status(500).json({ 
      error: 'Failed to fetch Gemini usage data',
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
