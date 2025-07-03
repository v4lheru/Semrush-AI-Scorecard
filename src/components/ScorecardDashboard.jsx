import React from 'react'
import { useMondayData } from '../hooks/useMondayData'
import MetricCard from './MetricCard'
import AILiteracyChart from './AILiteracyChart'
import DepartmentGrid from './DepartmentGrid'
import { RefreshCw, TrendingUp, Users, Target, DollarSign } from 'lucide-react'

const ScorecardDashboard = () => {
  const { data, loading, error, lastUpdated, refetch } = useMondayData()

  // Calculate metrics from Monday.com data
  const calculateMetrics = () => {
    if (!data || data.length === 0) {
      return {
        backlog: 0,
        inFlight: 0,
        completed: 0,
        totalROI: 0
      }
    }

    const statusMapping = {
      'Backlog': 'backlog',
      'Evaluation': 'inFlight',
      'Scoping': 'inFlight',
      'In Progress': 'inFlight',
      'Done': 'completed',
      'Closed': 'completed',
      'On Hold': 'onHold'
    }

    const metrics = data.reduce((acc, item) => {
      const mappedStatus = statusMapping[item.status] || 'other'
      acc[mappedStatus] = (acc[mappedStatus] || 0) + 1
      acc.totalROI += item.roi || 0
      return acc
    }, { backlog: 0, inFlight: 0, completed: 0, totalROI: 0 })

    return metrics
  }

  const metrics = calculateMetrics()

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-4 text-primary-blue" />
          <p className="text-text-secondary">Loading AI Scorecard...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="bg-primary-red/10 text-primary-red p-4 rounded-lg">
            <p className="font-medium">Error loading data</p>
            <p className="text-sm mt-1">{error}</p>
            <button 
              onClick={refetch}
              className="mt-3 px-4 py-2 bg-primary-red text-white rounded-lg hover:bg-primary-red/90"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-card-bg shadow-sm border-b border-border">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-4xl font-bold text-text-primary">
                AI & Automation Scorecard
              </h1>
              <p className="text-text-secondary mt-2">
                Real-time tracking of AI initiatives across Semrush
              </p>
            </div>
            <div className="text-right">
              <button
                onClick={refetch}
                className="flex items-center gap-2 px-4 py-2 bg-primary-blue text-white rounded-lg hover:bg-primary-blue/90 transition-colors"
              >
                <RefreshCw className="w-4 h-4" />
                Refresh
              </button>
              {lastUpdated && (
                <p className="text-xs text-text-secondary mt-2">
                  Last updated: {lastUpdated.toLocaleTimeString()}
                </p>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">
        {/* AI Literacy Section */}
        <section>
          <h2 className="text-2xl font-semibold text-text-primary mb-6">AI Literacy</h2>
          
          {/* Usage Chart */}
          <div className="mb-6">
            <AILiteracyChart />
          </div>
          
          {/* Training & Access Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <MetricCard
              title="New Hire Training"
              value="0%"
              description="# of employees who have completed their trainings in first x weeks / total employees hired"
              icon={<Users className="w-6 h-6" />}
              subtitle="Not connected to data source"
            />
            <MetricCard
              title="Teams with AI Access"
              value="0/0"
              description="Number of teams with access / total number of teams"
              icon={<Target className="w-6 h-6" />}
              subtitle="Not connected to data source"
            />
          </div>
        </section>

        {/* Active Initiatives */}
        <section>
          <h2 className="text-2xl font-semibold text-text-primary mb-6">Active Initiatives</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <MetricCard
              title="# Initiatives in Backlog"
              value={metrics.backlog}
              icon={<Target className="w-6 h-6" />}
            />
            <MetricCard
              title="# Initiatives in Flight"
              value={metrics.inFlight}
              icon={<TrendingUp className="w-6 h-6" />}
              trend={{ type: 'up', value: '+3', label: 'this week' }}
            />
            <MetricCard
              title="# Initiatives Completed"
              value={metrics.completed}
              icon={<Target className="w-6 h-6" />}
              trend={{ type: 'up', value: '+2', label: 'this month' }}
            />
            <MetricCard
              title="Cumulative Projected ROI"
              value={metrics.totalROI}
              highlight={true}
              icon={<DollarSign className="w-6 h-6" />}
              trend={{ type: 'up', value: '+$1.2M', label: 'this quarter' }}
            />
          </div>
        </section>

        {/* Department Breakdown */}
        <section>
          <h2 className="text-2xl font-semibold text-text-primary mb-6">
            Active initiatives by department
          </h2>
          <DepartmentGrid data={data} />
        </section>

        {/* Footer */}
        <footer className="text-center text-text-secondary text-sm py-8">
          <p>
            Data sourced from Monday.com • Updated every 5 minutes • 
            Total initiatives tracked: {data.length}
          </p>
        </footer>
      </div>
    </div>
  )
}

export default ScorecardDashboard
