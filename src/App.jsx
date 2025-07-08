import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import ScorecardDashboard from './components/ScorecardDashboard'
import GeminiDeepDive from './components/GeminiDeepDive'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background">
        <Routes>
          <Route path="/" element={<ScorecardDashboard />} />
          <Route path="/gemini-deep-dive" element={<GeminiDeepDive />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
