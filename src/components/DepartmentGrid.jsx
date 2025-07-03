import React, { useState } from 'react'

const DepartmentGrid = ({ data = [] }) => {
  const [selectedDepartment, setSelectedDepartment] = useState(null)

  // Process data to group by department
  const processDepartmentData = () => {
    const departments = {}
    
    data.forEach(item => {
      const dept = item.function || 'Other'
      if (!departments[dept]) {
        departments[dept] = {
          name: dept,
          count: 0,
          roi: 0,
          initiatives: []
        }
      }
      
      departments[dept].count += 1
      departments[dept].roi += item.roi || 0
      departments[dept].initiatives.push(item)
    })

    return Object.values(departments).sort((a, b) => b.count - a.count)
  }

  const departmentData = processDepartmentData()

  const formatROI = (value) => {
    if (value >= 1000000) {
      return `$${(value / 1000000).toFixed(1)}M`
    } else if (value >= 1000) {
      return `$${(value / 1000).toFixed(0)}K`
    }
    return value > 0 ? `$${value.toLocaleString()}` : 'TBD'
  }

  const getDepartmentColor = (dept) => {
    const colors = {
      'IT': 'bg-primary-blue/10 border-primary-blue/20 text-primary-blue',
      'Marketing': 'bg-primary-red/10 border-primary-red/20 text-primary-red',
      'Finance': 'bg-success-green/10 border-success-green/20 text-success-green',
      'Sales': 'bg-warning-yellow/10 border-warning-yellow/20 text-warning-yellow',
      'HR': 'bg-purple-100 border-purple-200 text-purple-700',
      'Product': 'bg-indigo-100 border-indigo-200 text-indigo-700',
      'Retention': 'bg-teal-100 border-teal-200 text-teal-700'
    }
    return colors[dept] || 'bg-gray-100 border-gray-200 text-gray-700'
  }

  const handleDepartmentClick = (dept) => {
    setSelectedDepartment(selectedDepartment?.name === dept.name ? null : dept)
  }

  return (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {departmentData.map((dept) => (
          <div
            key={dept.name}
            className={`
              department-card border-2 
              ${getDepartmentColor(dept.name)}
              ${selectedDepartment?.name === dept.name ? 'ring-2 ring-offset-2 ring-primary-blue' : ''}
            `}
            onClick={() => handleDepartmentClick(dept)}
          >
            <div className="text-center">
              <h3 className="font-semibold text-lg mb-2">{dept.name}</h3>
              <div className="space-y-1">
                <div className="text-2xl font-bold">
                  {dept.count} initiative{dept.count !== 1 ? 's' : ''}
                </div>
                <div className="text-sm font-medium">
                  {formatROI(dept.roi)} ROI
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Department Details Modal/Expansion */}
      {selectedDepartment && (
        <div className="mt-6 metric-card">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-xl font-semibold text-text-primary">
              {selectedDepartment.name} Initiatives
            </h3>
            <button
              onClick={() => setSelectedDepartment(null)}
              className="text-text-secondary hover:text-text-primary"
            >
              ✕
            </button>
          </div>
          
          <div className="grid gap-3">
            {selectedDepartment.initiatives.map((initiative, index) => (
              <div
                key={index}
                className="p-3 bg-background rounded-lg border border-border"
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h4 className="font-medium text-text-primary mb-1">
                      {initiative.name}
                    </h4>
                    <div className="flex items-center gap-4 text-sm text-text-secondary">
                      <span className={`
                        px-2 py-1 rounded-full text-xs font-medium
                        ${initiative.status === 'In Progress' ? 'bg-primary-blue/10 text-primary-blue' : ''}
                        ${initiative.status === 'Backlog' ? 'bg-text-secondary/10 text-text-secondary' : ''}
                        ${initiative.status === 'Done' ? 'bg-success-green/10 text-success-green' : ''}
                        ${initiative.status === 'Scoping' ? 'bg-warning-yellow/10 text-warning-yellow' : ''}
                      `}>
                        {initiative.status}
                      </span>
                      {initiative.team && (
                        <span>Team: {initiative.team}</span>
                      )}
                      {initiative.priority && (
                        <span>Priority: {initiative.priority}</span>
                      )}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="font-semibold text-text-primary">
                      {formatROI(initiative.roi)}
                    </div>
                    {initiative.hoursSaved && (
                      <div className="text-xs text-text-secondary">
                        {initiative.hoursSaved}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default DepartmentGrid
