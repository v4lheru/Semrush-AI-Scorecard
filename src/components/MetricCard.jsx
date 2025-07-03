import React from 'react'

const MetricCard = ({ 
  title, 
  value, 
  description, 
  icon, 
  trend, 
  highlight = false,
  onClick,
  subtitle 
}) => {
  const cardClasses = `
    metric-card 
    ${highlight ? 'ring-2 ring-primary-blue bg-gradient-to-br from-primary-blue/5 to-primary-blue/10' : ''}
    ${onClick ? 'cursor-pointer hover:scale-105' : ''}
  `.trim()

  const formatValue = (val) => {
    if (typeof val === 'number') {
      if (val >= 1000000) {
        return `$${(val / 1000000).toFixed(1)}M`
      } else if (val >= 1000) {
        return `$${(val / 1000).toFixed(0)}K`
      }
      return val.toLocaleString()
    }
    return val
  }

  return (
    <div className={cardClasses} onClick={onClick}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="metric-label">{title}</div>
          <div className={`metric-value ${highlight ? 'text-primary-blue' : ''}`}>
            {formatValue(value)}
          </div>
          {description && (
            <div className="metric-description">{description}</div>
          )}
          {subtitle && (
            <div className="text-xs text-text-secondary italic mt-1">{subtitle}</div>
          )}
        </div>
        
        {icon && (
          <div className={`ml-4 ${highlight ? 'text-primary-blue' : 'text-text-secondary'}`}>
            {icon}
          </div>
        )}
      </div>
      
      {trend && (
        <div className="mt-3 flex items-center text-xs">
          <span className={`
            px-2 py-1 rounded-full text-xs font-medium
            ${trend.type === 'up' ? 'bg-success-green/10 text-success-green' : ''}
            ${trend.type === 'down' ? 'bg-primary-red/10 text-primary-red' : ''}
            ${trend.type === 'neutral' ? 'bg-text-secondary/10 text-text-secondary' : ''}
          `}>
            {trend.type === 'up' && '↗'} 
            {trend.type === 'down' && '↘'} 
            {trend.type === 'neutral' && '→'} 
            {trend.value}
          </span>
          <span className="ml-2 text-text-secondary">{trend.label}</span>
        </div>
      )}
    </div>
  )
}

export default MetricCard
