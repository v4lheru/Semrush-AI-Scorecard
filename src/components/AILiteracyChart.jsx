import React from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { useGeminiData } from '../hooks/useGeminiData'

const AILiteracyChart = () => {
  const { data: geminiData, loading, error } = useGeminiData()

  // Prepare chart data
  const usageData = React.useMemo(() => {
    if (!geminiData?.time_series) {
      // Fallback data when no connection
      return [
        { period: 'Week 1', Gemini: 0, Claude: 0, Cursor: 0, ChatGPT: 0, Cumulative: 0 },
        { period: 'Week 2', Gemini: 0, Claude: 0, Cursor: 0, ChatGPT: 0, Cumulative: 0 },
        { period: 'Week 3', Gemini: 0, Claude: 0, Cursor: 0, ChatGPT: 0, Cumulative: 0 },
        { period: 'Week 4', Gemini: 0, Claude: 0, Cursor: 0, ChatGPT: 0, Cumulative: 0 },
        { period: 'Week 5', Gemini: 0, Claude: 0, Cursor: 0, ChatGPT: 0, Cumulative: 0 },
        { period: 'Week 6', Gemini: 0, Claude: 0, Cursor: 0, ChatGPT: 0, Cumulative: 0 },
      ]
    }

    // Safely extract data with fallbacks
    const timeSeriesData = geminiData.time_series || {}
    const weeks = timeSeriesData.weeks || []
    const weekly_unique_users = timeSeriesData.weekly_unique_users || []
    const total_weekly_users = timeSeriesData.total_weekly_users || []

    // Ensure we have data to work with
    if (weeks.length === 0) {
      return [
        { period: 'No Data', Gemini: 0, Claude: 0, Cursor: 0, ChatGPT: 0, Cumulative: 0 }
      ]
    }

    return weeks.map((week, index) => ({
      period: week || `Week ${index + 1}`,
      Gemini: (weekly_unique_users && weekly_unique_users[index]) || 0,
      Claude: 0, // Not connected to Claude analytics
      Cursor: 0, // Not connected to Cursor analytics  
      ChatGPT: 0, // Not connected to ChatGPT analytics
      Cumulative: (total_weekly_users && total_weekly_users[index]) || 0  // Total weekly active users from ALL AI tools
    }))
  }, [geminiData])

  const isConnected = geminiData && !geminiData.data_source?.includes('Not connected')

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-card-bg p-4 rounded-lg shadow-card border border-border">
          <p className="font-medium text-text-primary">{label}</p>
          {payload.map((entry, index) => {
            const isCumulative = entry.dataKey === 'Cumulative'
            const description = isCumulative ? 'total weekly active users (all AI tools)' : 'weekly active users'
            return (
              <p key={index} style={{ color: entry.color }} className="text-sm">
                {entry.dataKey}: {entry.value} {description}
              </p>
            )
          })}
        </div>
      )
    }
    return null
  }

  return (
    <div className="metric-card">
      <div className="mb-4">
        <div className="flex justify-between items-start">
          <div>
            <h3 className="text-lg font-semibold text-text-primary">Week over Week AI Usage</h3>
            <p className="text-sm text-text-secondary">Weekly active users across ALL Gemini-enabled Workspace apps</p>
            {loading ? (
              <p className="text-xs text-text-secondary italic mt-1">Loading Gemini analytics...</p>
            ) : error ? (
              <p className="text-xs text-primary-red italic mt-1">Error loading data: {error}</p>
            ) : isConnected ? (
              <p className="text-xs text-success-green italic mt-1">✅ Connected to Gemini analytics (8 apps tracked)</p>
            ) : (
              <p className="text-xs text-text-secondary italic mt-1">⚠️ Gemini: Ready for integration • Claude, Cursor, ChatGPT: Not connected</p>
            )}
          </div>
          <button
            onClick={() => window.open('/gemini-deep-dive', '_blank')}
            className="px-4 py-2 bg-primary-blue text-white rounded-lg hover:bg-blue-600 transition-colors text-sm font-medium flex items-center gap-2"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            Gemini Deep Dive
          </button>
        </div>
      </div>
      
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={usageData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
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
            <Line 
              type="monotone" 
              dataKey="Gemini" 
              stroke="#FF4444" 
              strokeWidth={3}
              dot={{ fill: '#FF4444', strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6, stroke: '#FF4444', strokeWidth: 2 }}
            />
            <Line 
              type="monotone" 
              dataKey="Claude" 
              stroke="#4A90E2" 
              strokeWidth={3}
              dot={{ fill: '#4A90E2', strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6, stroke: '#4A90E2', strokeWidth: 2 }}
            />
            <Line 
              type="monotone" 
              dataKey="Cursor" 
              stroke="#F5A623" 
              strokeWidth={3}
              dot={{ fill: '#F5A623', strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6, stroke: '#F5A623', strokeWidth: 2 }}
            />
            <Line 
              type="monotone" 
              dataKey="ChatGPT" 
              stroke="#7ED321" 
              strokeWidth={3}
              dot={{ fill: '#7ED321', strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6, stroke: '#7ED321', strokeWidth: 2 }}
            />
            <Line 
              type="monotone" 
              dataKey="Cumulative" 
              stroke="#2C3E50" 
              strokeWidth={4}
              strokeDasharray="8 4"
              dot={{ fill: '#2C3E50', strokeWidth: 2, r: 5 }}
              activeDot={{ r: 7, stroke: '#2C3E50', strokeWidth: 2 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default AILiteracyChart
