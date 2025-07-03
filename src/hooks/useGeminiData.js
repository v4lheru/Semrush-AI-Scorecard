import { useState, useEffect } from 'react'

export const useGeminiData = () => {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [lastUpdated, setLastUpdated] = useState(null)

  const fetchData = async () => {
    try {
      setLoading(true)
      const response = await fetch('/api/gemini/usage')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const result = await response.json()
      setData(result)
      setLastUpdated(new Date())
      setError(null)
    } catch (err) {
      console.error('Error fetching Gemini data:', err)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
    
    // Refresh every 10 minutes (less frequent than Monday.com data)
    const interval = setInterval(fetchData, 10 * 60 * 1000)
    
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
