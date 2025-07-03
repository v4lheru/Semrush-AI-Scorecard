import { useState, useEffect } from 'react'

export const useMondayData = () => {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [lastUpdated, setLastUpdated] = useState(null)

  const fetchData = async () => {
    try {
      setLoading(true)
      const response = await fetch('/api/monday/board')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const result = await response.json()
      setData(result)
      setLastUpdated(new Date())
      setError(null)
    } catch (err) {
      console.error('Error fetching Monday data:', err)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
    
    // Refresh every 5 minutes
    const interval = setInterval(fetchData, 5 * 60 * 1000)
    
    return () => clearInterval(interval)
  }, [])

  return { 
    data, 
    loading, 
    error, 
    lastUpdated,
    refetch: fetchData 
  }
}
