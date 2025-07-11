import React from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts'

const GeminiDeepDive = () => {
  const [deepDiveData, setDeepDiveData] = React.useState(null)
  const [loading, setLoading] = React.useState(true)
  const [error, setError] = React.useState(null)

  // Fetch deep dive data
  React.useEffect(() => {
    const fetchDeepDiveData = async () => {
      try {
        setLoading(true)
        const response = await fetch('/api/gemini/deep-dive')
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data = await response.json()
        setDeepDiveData(data)
        setError(null)
      } catch (err) {
        console.error('Error fetching deep dive data:', err)
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchDeepDiveData()
  }, [])

  // Prepare per-app chart data (simplified for current week only)
  const perAppData = React.useMemo(() => {
    if (!deepDiveData?.raw_weekly_data) {
      return []
    }

    try {
      const currentWeekData = deepDiveData.raw_weekly_data['Current Week (Live)']
      if (!currentWeekData?.app_breakdown) {
        return []
      }

      const apps = ['gemini_app', 'gmail', 'docs', 'sheets', 'slides', 'meet', 'drive', 'chat']
      const chartPoint = { period: 'Current Week' }
      
      apps.forEach(app => {
        const appData = currentWeekData.app_breakdown[app]
        chartPoint[app] = appData ? appData.users : 0
      })
      
      return [chartPoint]
    } catch (error) {
      console.error('Error preparing per-app chart data:', error)
      return []
    }
  }, [deepDiveData])

  // Prepare app summary data
  const appSummary = React.useMemo(() => {
    if (!deepDiveData?.app_analysis?.top_apps) {
      return []
    }

    const appLabels = {
      gemini_app: 'Gemini App',
      gmail: 'Gmail',
      docs: 'Google Docs',
      sheets: 'Google Sheets',
      slides: 'Google Slides',
      meet: 'Google Meet',
      drive: 'Google Drive',
      chat: 'Google Chat'
    }

    const summary = Object.entries(deepDiveData.app_analysis.top_apps).map(([app, data]) => ({
      app,
      label: appLabels[app] || app,
      totalUsers: data.max_weekly_users,
      totalActivities: data.total_activities,
      latestWeekUsers: data.max_weekly_users // Same as total for current week only
    }))

    return summary.sort((a, b) => b.totalActivities - a.totalActivities)
  }, [deepDiveData])

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-card-bg p-4 rounded-lg shadow-card border border-border">
          <p className="font-medium text-text-primary">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color }} className="text-sm">
              {entry.dataKey}: {entry.value} weekly active users
            </p>
          ))}
        </div>
      )
    }
    return null
  }

  const appColors = {
    gemini_app: '#FF4444',
    gmail: '#EA4335',
    docs: '#4285F4',
    sheets: '#34A853',
    slides: '#FBBC04',
    meet: '#9AA0A6',
    drive: '#0F9D58',
    chat: '#F4B400'
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background p-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-blue mx-auto"></div>
            <p className="mt-4 text-text-secondary">Loading Gemini Deep Dive...</p>
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background p-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center py-12">
            <p className="text-primary-red">Error loading Gemini data: {error}</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-text-primary">Gemini Deep Dive</h1>
              <p className="text-text-secondary mt-2">Detailed breakdown of Gemini usage across all Google Workspace applications</p>
            </div>
            <button
              onClick={() => window.close()}
              className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors text-sm font-medium"
            >
              Close
            </button>
          </div>
        </div>

        {/* App Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {appSummary.map(app => (
            <div key={app.app} className="metric-card">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-text-primary">{app.label}</h3>
                <div 
                  className="w-4 h-4 rounded-full"
                  style={{ backgroundColor: appColors[app.app] }}
                ></div>
              </div>
              <div className="space-y-2">
                <div>
                  <p className="text-2xl font-bold text-text-primary">{app.totalUsers}</p>
                  <p className="text-sm text-text-secondary">Total Users</p>
                </div>
                <div>
                  <p className="text-lg font-semibold text-text-primary">{app.latestWeekUsers}</p>
                  <p className="text-sm text-text-secondary">Latest Week</p>
                </div>
                <div>
                  <p className="text-sm text-text-secondary">{app.totalActivities} total activities</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Per-App Usage Chart */}
        <div className="metric-card mb-8">
          <div className="mb-6">
            <h3 className="text-xl font-semibold text-text-primary">Weekly Active Users by Application</h3>
            <p className="text-text-secondary">Breakdown of Gemini usage across different Google Workspace apps</p>
          </div>
          
          <div className="h-96">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={perAppData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E9ECEF" />
                <XAxis 
                  dataKey="period" 
                  stroke="#7F8C8D"
                  fontSize={12}
                  tickLine={false}
                />
                <YAxis 
                  stroke="#7F8C8D"
                  fontSize={12}
                  tickLine={false}
                  axisLine={false}
                />
                <Tooltip content={<CustomTooltip />} />
                <Legend 
                  wrapperStyle={{ paddingTop: '20px' }}
                  iconType="line"
                />
                {Object.entries(appColors).map(([app, color]) => (
                  <Line 
                    key={app}
                    type="monotone" 
                    dataKey={app} 
                    stroke={color} 
                    strokeWidth={2}
                    dot={{ fill: color, strokeWidth: 2, r: 3 }}
                    activeDot={{ r: 5, stroke: color, strokeWidth: 2 }}
                  />
                ))}
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* App Comparison Bar Chart */}
        <div className="metric-card mb-8">
          <div className="mb-6">
            <h3 className="text-xl font-semibold text-text-primary">Total Users by Application</h3>
            <p className="text-text-secondary">Comparison of total unique users across all Gemini-enabled apps</p>
          </div>
          
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={appSummary} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E9ECEF" />
                <XAxis 
                  dataKey="label" 
                  stroke="#7F8C8D"
                  fontSize={12}
                  tickLine={false}
                  angle={-45}
                  textAnchor="end"
                  height={80}
                />
                <YAxis 
                  stroke="#7F8C8D"
                  fontSize={12}
                  tickLine={false}
                  axisLine={false}
                />
                <Tooltip 
                  formatter={(value, name) => [value, 'Total Users']}
                  labelFormatter={(label) => `App: ${label}`}
                />
                <Bar 
                  dataKey="totalUsers" 
                  fill="#4A90E2"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Latest Week Breakdown */}
        {deepDiveData?.action_analysis && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Top Actions */}
            {Object.keys(deepDiveData.action_analysis.top_actions).length > 0 && (
              <div className="metric-card">
                <h3 className="text-lg font-semibold text-text-primary mb-4">Top Actions (Latest Week)</h3>
                <div className="space-y-2">
                  {Object.entries(deepDiveData.action_analysis.top_actions)
                    .sort(([,a], [,b]) => b - a)
                    .slice(0, 10)
                    .map(([action, count]) => (
                      <div key={action} className="flex justify-between items-center">
                        <span className="text-text-secondary text-sm truncate">{action}</span>
                        <span className="text-text-primary font-medium">{count}</span>
                      </div>
                    ))}
                </div>
              </div>
            )}

            {/* App Usage Categories */}
            {Object.keys(deepDiveData.app_analysis.top_apps).length > 0 && (
              <div className="metric-card">
                <h3 className="text-lg font-semibold text-text-primary mb-4">Usage Categories (Latest Week)</h3>
                <div className="space-y-2">
                  {Object.entries(deepDiveData.app_analysis.top_apps)
                    .sort(([,a], [,b]) => b.total_activities - a.total_activities)
                    .map(([app, data]) => (
                      <div key={app} className="flex justify-between items-center">
                        <span className="text-text-secondary text-sm">{app.replace('_', ' ')}</span>
                        <span className="text-text-primary font-medium">{data.total_activities}</span>
                      </div>
                    ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Footer */}
        <div className="mt-8 text-center text-text-secondary text-sm">
          <p>Data includes: Gemini App, Gmail, Docs, Sheets, Slides, Meet, Drive, and Chat</p>
          <p className="mt-1">Last updated: {deepDiveData?.last_updated ? new Date(deepDiveData.last_updated).toLocaleString() : 'Unknown'}</p>
        </div>
      </div>
    </div>
  )
}

export default GeminiDeepDive
