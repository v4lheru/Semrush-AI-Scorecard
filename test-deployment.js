#!/usr/bin/env node

/**
 * Simple deployment test script for AI Scorecard
 * Tests API endpoints and basic functionality
 */

import axios from 'axios'

const BASE_URL = process.env.TEST_URL || 'http://localhost:8081'
const MONDAY_API_KEY = process.env.MONDAY_API_KEY

console.log('🧪 Testing AI Scorecard Deployment')
console.log(`📍 Base URL: ${BASE_URL}`)
console.log('=' .repeat(50))

async function testEndpoint(name, url, expectedStatus = 200) {
  try {
    console.log(`Testing ${name}...`)
    const response = await axios.get(`${BASE_URL}${url}`, {
      timeout: 10000,
      validateStatus: (status) => status === expectedStatus
    })
    
    console.log(`✅ ${name}: ${response.status} - ${response.statusText}`)
    return { success: true, data: response.data }
  } catch (error) {
    console.log(`❌ ${name}: ${error.response?.status || 'TIMEOUT'} - ${error.message}`)
    return { success: false, error: error.message }
  }
}

async function testMondayIntegration() {
  if (!MONDAY_API_KEY) {
    console.log('⚠️  Monday.com API key not provided - skipping integration test')
    return { success: true, skipped: true }
  }

  try {
    console.log('Testing Monday.com integration...')
    const response = await axios.get(`${BASE_URL}/api/monday/board`, {
      timeout: 15000
    })
    
    const data = response.data
    if (Array.isArray(data) && data.length > 0) {
      console.log(`✅ Monday.com Integration: ${data.length} initiatives loaded`)
      
      // Validate data structure
      const sample = data[0]
      const requiredFields = ['id', 'name', 'status', 'function']
      const missingFields = requiredFields.filter(field => !sample.hasOwnProperty(field))
      
      if (missingFields.length === 0) {
        console.log('✅ Data structure validation passed')
      } else {
        console.log(`⚠️  Missing fields in data: ${missingFields.join(', ')}`)
      }
      
      return { success: true, data: data }
    } else {
      console.log('❌ Monday.com Integration: No data returned')
      return { success: false, error: 'No data returned' }
    }
  } catch (error) {
    console.log(`❌ Monday.com Integration: ${error.response?.status || 'TIMEOUT'} - ${error.message}`)
    return { success: false, error: error.message }
  }
}

async function runTests() {
  const results = []
  
  // Test health endpoint
  results.push(await testEndpoint('Health Check', '/api/health'))
  
  // Test metrics endpoint
  results.push(await testEndpoint('Metrics Endpoint', '/api/metrics'))
  
  // Test Monday.com integration
  results.push(await testMondayIntegration())
  
  // Test frontend (if available)
  results.push(await testEndpoint('Frontend', '/', 200))
  
  console.log('\n' + '=' .repeat(50))
  console.log('📊 Test Results Summary')
  console.log('=' .repeat(50))
  
  const successful = results.filter(r => r.success).length
  const total = results.length
  const skipped = results.filter(r => r.skipped).length
  
  console.log(`✅ Passed: ${successful}/${total}`)
  if (skipped > 0) {
    console.log(`⚠️  Skipped: ${skipped}`)
  }
  
  if (successful === total) {
    console.log('\n🎉 All tests passed! Deployment is ready.')
    process.exit(0)
  } else {
    console.log('\n❌ Some tests failed. Please check the issues above.')
    process.exit(1)
  }
}

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\n⚠️  Test interrupted by user')
  process.exit(1)
})

process.on('SIGTERM', () => {
  console.log('\n⚠️  Test terminated')
  process.exit(1)
})

// Run tests
runTests().catch(error => {
  console.error('💥 Test runner failed:', error.message)
  process.exit(1)
})
