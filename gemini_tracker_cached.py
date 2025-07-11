#!/usr/bin/env python3
"""
Cached Gemini Tracker - Optimized for Dashboard Performance

This script implements intelligent caching:
- Historical weeks: Cached once, never refetched
- Current week: Always fetched live for real-time data
- Uses efficient gemini_app filtering for fast performance

Author: PACT Cline
Date: 2025-07-11
"""

import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Cache file paths
CACHE_DIR = 'cache'
HISTORICAL_CACHE_FILE = os.path.join(CACHE_DIR, 'historical_weeks.json')
CURRENT_WEEK_CACHE_FILE = os.path.join(CACHE_DIR, 'current_week.json')


class CachedGeminiTracker:
    """Optimized Gemini tracker with intelligent caching"""
    
    def __init__(self):
        """Initialize the tracker"""
        self.credentials = None
        self.access_token = None
        
        # Ensure cache directory exists
        os.makedirs(CACHE_DIR, exist_ok=True)
        
        logger.info("🛠️ Initializing Cached Gemini Tracker")
    
    def _load_service_account_credentials(self) -> service_account.Credentials:
        """Load service account credentials"""
        try:
            # Try environment variable first
            service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
            
            if service_account_json:
                service_account_info = json.loads(service_account_json)
                credentials = service_account.Credentials.from_service_account_info(
                    service_account_info,
                    scopes=config.SCOPES
                )
            else:
                credentials = service_account.Credentials.from_service_account_file(
                    config.SERVICE_ACCOUNT_FILE,
                    scopes=config.SCOPES
                )
            
            # Enable domain-wide delegation
            delegated_credentials = credentials.with_subject(config.DOMAIN_ADMIN_EMAIL)
            return delegated_credentials
            
        except Exception as e:
            logger.error(f"❌ Error loading credentials: {e}")
            raise
    
    def get_access_token(self) -> str:
        """Get a valid access token"""
        try:
            if self.credentials is None:
                self.credentials = self._load_service_account_credentials()
            
            self.credentials.refresh(Request())
            self.access_token = self.credentials.token
            return self.access_token
            
        except Exception as e:
            logger.error(f"❌ Error getting access token: {e}")
            raise
    
    def fetch_gemini_app_week(self, start_time: str, end_time: str) -> Dict[str, Any]:
        """Fetch gemini_app data for a specific week with full pagination"""
        try:
            access_token = self.get_access_token()
            url = config.get_api_endpoint('activities')
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Accept': 'application/json'
            }
            
            # Use efficient filtering for gemini_app only
            params = {
                'eventName': config.GEMINI_EVENT_NAME,
                'maxResults': 1000,
                'startTime': start_time,
                'endTime': end_time,
                'filters': 'app_name==gemini_app'
            }
            
            all_activities = []
            gemini_app_users = set()
            page_token = None
            page_count = 0
            
            # Fetch ALL pages
            while True:
                page_count += 1
                
                if page_token:
                    params['pageToken'] = page_token
                
                response = requests.get(url, headers=headers, params=params, timeout=30)
                
                if response.status_code != 200:
                    logger.error(f"❌ API request failed: {response.status_code}")
                    break
                
                data = response.json()
                items = data.get('items', [])
                all_activities.extend(items)
                
                # Count users
                for item in items:
                    actor = item.get('actor', {})
                    user_email = actor.get('email', 'Unknown')
                    gemini_app_users.add(user_email)
                
                # Check for next page
                page_token = data.get('nextPageToken')
                if not page_token:
                    break
                
                # Safety check
                if page_count >= 20:
                    logger.warning(f"⚠️ Reached safety limit ({page_count} pages)")
                    break
            
            return {
                'activities': len(all_activities),
                'users': len(gemini_app_users),
                'user_list': list(gemini_app_users),
                'pages': page_count,
                'fetched_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Error fetching week data: {e}")
            return {'activities': 0, 'users': 0, 'user_list': [], 'pages': 0}
    
    def get_historical_weeks(self) -> Dict[str, Any]:
        """Get historical weeks data (cached)"""
        try:
            # Check if historical cache exists and is valid
            if os.path.exists(HISTORICAL_CACHE_FILE):
                with open(HISTORICAL_CACHE_FILE, 'r') as f:
                    cached_data = json.load(f)
                    logger.info("📋 Using cached historical data")
                    return cached_data
            
            logger.info("🔄 Fetching historical weeks (first time)")
            
            # Define historical weeks (fixed, never change)
            historical_weeks = [
                {
                    'label': 'Week 1 (Jun 20-22)',
                    'start': '2025-06-20T00:00:00Z',
                    'end': '2025-06-23T00:00:00Z'
                },
                {
                    'label': 'Week 2 (Jun 23-29)', 
                    'start': '2025-06-23T00:00:00Z',
                    'end': '2025-06-30T00:00:00Z'
                },
                {
                    'label': 'Week 3 (Jun 30-Jul 6)',
                    'start': '2025-06-30T00:00:00Z', 
                    'end': '2025-07-07T00:00:00Z'
                }
            ]
            
            historical_data = {}
            
            for week in historical_weeks:
                logger.info(f"📅 Fetching {week['label']} (caching for future)")
                week_data = self.fetch_gemini_app_week(week['start'], week['end'])
                historical_data[week['label']] = {
                    'period': week['label'],
                    'start_time': week['start'],
                    'end_time': week['end'],
                    **week_data
                }
            
            # Cache historical data permanently
            with open(HISTORICAL_CACHE_FILE, 'w') as f:
                json.dump(historical_data, f, indent=2)
            
            logger.info("💾 Historical data cached permanently")
            return historical_data
            
        except Exception as e:
            logger.error(f"❌ Error getting historical weeks: {e}")
            return {}
    
    def get_current_week_definition(self) -> Dict[str, str]:
        """Dynamically determine current week based on date"""
        now = datetime.utcnow()
        
        # Define week boundaries (Mondays)
        week_starts = [
            datetime(2025, 6, 20),  # Week 1: Jun 20-22 (Fri-Sun)
            datetime(2025, 6, 23),  # Week 2: Jun 23-29 (Mon-Sun)
            datetime(2025, 6, 30),  # Week 3: Jun 30-Jul 6 (Mon-Sun)
            datetime(2025, 7, 7),   # Week 4: Jul 7-13 (Mon-Sun)
            datetime(2025, 7, 14),  # Week 5: Jul 14-20 (Mon-Sun)
            datetime(2025, 7, 21),  # Week 6: Jul 21-27 (Mon-Sun)
            datetime(2025, 7, 28),  # Week 7: Jul 28-Aug 3 (Mon-Sun)
        ]
        
        # Find current week
        current_week_num = 1
        current_start = week_starts[0]
        
        for i, week_start in enumerate(week_starts):
            if now >= week_start:
                current_week_num = i + 1
                current_start = week_start
            else:
                break
        
        # Calculate week end (Sunday or current time if in progress)
        week_end = current_start + timedelta(days=6, hours=23, minutes=59, seconds=59)
        if now < week_end:
            week_end = now  # Week in progress
        
        # Format dates
        start_str = current_start.strftime('%b %d')
        if week_end.date() == now.date():
            end_str = 'Current'
            label = f'Week {current_week_num} ({start_str}-Current) (Live)'
        else:
            end_str = week_end.strftime('%b %d')
            label = f'Week {current_week_num} ({start_str}-{end_str})'
        
        return {
            'label': label,
            'start': current_start.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'end': week_end.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'week_number': current_week_num
        }

    def get_current_week(self) -> Dict[str, Any]:
        """Get current week data (always live)"""
        try:
            logger.info("🔴 Fetching current week (live data)")
            
            # Dynamically determine current week
            current_week = self.get_current_week_definition()
            logger.info(f"📅 Current week: {current_week['label']}")
            
            week_data = self.fetch_gemini_app_week(current_week['start'], current_week['end'])
            
            current_data = {
                'period': current_week['label'],
                'start_time': current_week['start'],
                'end_time': current_week['end'],
                'week_number': current_week['week_number'],
                **week_data
            }
            
            # Cache current week (short-term, for this request)
            with open(CURRENT_WEEK_CACHE_FILE, 'w') as f:
                json.dump(current_data, f, indent=2)
            
            return current_data
            
        except Exception as e:
            logger.error(f"❌ Error getting current week: {e}")
            return {}
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get optimized dashboard data with caching"""
        try:
            logger.info("📊 Generating optimized dashboard data")
            
            # Get historical data (cached)
            historical_data = self.get_historical_weeks()
            
            # Get current week (live)
            current_data = self.get_current_week()
            
            # Combine all weeks
            all_weeks = {**historical_data}
            if current_data:
                all_weeks[current_data['period']] = current_data
            
            # Prepare time series data
            weeks_list = []
            weekly_users = []
            weekly_activities = []
            
            for week_label in ['Week 1 (Jun 20-22)', 'Week 2 (Jun 23-29)', 'Week 3 (Jun 30-Jul 6)', 'Week 4 (Jul 7-Current) (Live)']:
                if week_label in all_weeks:
                    week_data = all_weeks[week_label]
                    weeks_list.append(week_label.replace(' (Live)', ''))
                    weekly_users.append(week_data.get('users', 0))
                    weekly_activities.append(week_data.get('activities', 0))
            
            # Calculate growth
            wow_growth = []
            for i in range(1, len(weekly_users)):
                if weekly_users[i-1] > 0:
                    growth = ((weekly_users[i] - weekly_users[i-1]) / weekly_users[i-1]) * 100
                    wow_growth.append(round(growth, 1))
                else:
                    wow_growth.append(0)
            
            # Latest week stats
            latest_week = current_data if current_data else {}
            
            dashboard_data = {
                'summary': {
                    'total_cumulative_users': max(weekly_users) if weekly_users else 0,
                    'latest_week_activities': latest_week.get('activities', 0),
                    'latest_week_users': latest_week.get('users', 0),
                    'total_weeks_tracked': len(weeks_list)
                },
                'time_series': {
                    'weeks': weeks_list,
                    'total_weekly_users': weekly_users,
                    'weekly_activities': weekly_activities,
                    'weekly_unique_users': weekly_users,
                    'wow_growth_percent': wow_growth
                },
                'latest_week_breakdown': {
                    'actions': {'classic_use_case_gemini_app': latest_week.get('activities', 0)},
                    'categories': {'standalone_gemini': latest_week.get('activities', 0)},
                    'top_users': latest_week.get('user_list', [])[:10]
                },
                'raw_weekly_data': all_weeks,
                'last_updated': datetime.now().isoformat(),
                'data_source': 'Cached Historical + Live Current Week',
                'cache_status': {
                    'historical_cached': os.path.exists(HISTORICAL_CACHE_FILE),
                    'current_week_live': True
                }
            }
            
            logger.info(f"✅ Dashboard data ready: {len(weekly_users)} weeks, latest: {latest_week.get('users', 0)} users")
            return dashboard_data
            
        except Exception as e:
            logger.error(f"❌ Error generating dashboard data: {e}")
            return {}


def main():
    """Main function for dashboard API"""
    try:
        tracker = CachedGeminiTracker()
        dashboard_data = tracker.get_dashboard_data()
        
        # Output JSON for API consumption
        print(json.dumps(dashboard_data, indent=2))
        
    except Exception as e:
        logger.error(f"❌ Error in main: {e}")
        # Return error response
        error_response = {
            'error': str(e),
            'summary': {'total_cumulative_users': 0, 'latest_week_activities': 0, 'latest_week_users': 0},
            'time_series': {'weeks': [], 'weekly_unique_users': [], 'wow_growth_percent': []},
            'last_updated': datetime.now().isoformat()
        }
        print(json.dumps(error_response, indent=2))


if __name__ == "__main__":
    main()
