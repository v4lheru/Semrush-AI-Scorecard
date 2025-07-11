#!/usr/bin/env python3
"""
Cached Gemini Deep Dive - All Apps Analysis with Caching

This script provides detailed analysis across ALL Gemini apps:
- Historical weeks: Cached once, never refetched
- Current week: Always fetched live for real-time data
- Includes Gmail, Docs, Sheets, Drive, etc.

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
DEEP_DIVE_HISTORICAL_CACHE = os.path.join(CACHE_DIR, 'deep_dive_historical.json')
DEEP_DIVE_CURRENT_CACHE = os.path.join(CACHE_DIR, 'deep_dive_current.json')


class CachedGeminiDeepDive:
    """Deep dive analysis with intelligent caching for all Gemini apps"""
    
    def __init__(self):
        """Initialize the deep dive tracker"""
        self.credentials = None
        self.access_token = None
        
        # Ensure cache directory exists
        os.makedirs(CACHE_DIR, exist_ok=True)
        
        logger.info("🔍 Initializing Cached Gemini Deep Dive")
    
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
    
    def fetch_all_apps_week(self, start_time: str, end_time: str) -> Dict[str, Any]:
        """Fetch ALL Gemini apps data for a specific week with pagination"""
        try:
            access_token = self.get_access_token()
            url = config.get_api_endpoint('activities')
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Accept': 'application/json'
            }
            
            # Fetch ALL apps (no filtering)
            params = {
                'eventName': config.GEMINI_EVENT_NAME,
                'maxResults': 1000,
                'startTime': start_time,
                'endTime': end_time
            }
            
            all_activities = []
            page_token = None
            page_count = 0
            
            # Fetch with pagination limit for performance
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
                
                # Check for next page
                page_token = data.get('nextPageToken')
                if not page_token:
                    break
                
                # Limit pages for deep dive (balance detail vs performance)
                if page_count >= 15:
                    logger.warning(f"⚠️ Reached page limit ({page_count}) for deep dive")
                    break
            
            # Process activities by app
            app_breakdown = {}
            action_breakdown = {}
            all_users = set()
            
            for item in all_activities:
                actor = item.get('actor', {})
                events = item.get('events', [])
                user_email = actor.get('email', 'Unknown')
                all_users.add(user_email)
                
                for event in events:
                    parameters = event.get('parameters', [])
                    
                    # Extract parameters
                    param_dict = {}
                    for param in parameters:
                        param_name = param.get('name', '')
                        param_value = param.get('value', '')
                        param_dict[param_name] = param_value
                    
                    app_name = param_dict.get('app_name', 'Unknown')
                    action = param_dict.get('action', 'Unknown')
                    
                    # Count by app
                    if app_name not in app_breakdown:
                        app_breakdown[app_name] = {'count': 0, 'users': set()}
                    app_breakdown[app_name]['count'] += 1
                    app_breakdown[app_name]['users'].add(user_email)
                    
                    # Count by action
                    if action not in action_breakdown:
                        action_breakdown[action] = 0
                    action_breakdown[action] += 1
            
            # Convert sets to counts
            for app in app_breakdown:
                app_breakdown[app]['users'] = len(app_breakdown[app]['users'])
            
            return {
                'total_activities': len(all_activities),
                'total_users': len(all_users),
                'pages_fetched': page_count,
                'app_breakdown': app_breakdown,
                'action_breakdown': action_breakdown,
                'fetched_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Error fetching deep dive week data: {e}")
            return {
                'total_activities': 0,
                'total_users': 0,
                'pages_fetched': 0,
                'app_breakdown': {},
                'action_breakdown': {}
            }
    
    def get_historical_deep_dive(self) -> Dict[str, Any]:
        """Get historical deep dive data (cached)"""
        try:
            # Check if historical cache exists
            if os.path.exists(DEEP_DIVE_HISTORICAL_CACHE):
                with open(DEEP_DIVE_HISTORICAL_CACHE, 'r') as f:
                    cached_data = json.load(f)
                    logger.info("📋 Using cached deep dive historical data")
                    return cached_data
            
            logger.info("🔄 Fetching deep dive historical weeks (first time)")
            
            # Define historical weeks
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
                logger.info(f"📅 Deep dive fetching {week['label']} (caching for future)")
                week_data = self.fetch_all_apps_week(week['start'], week['end'])
                historical_data[week['label']] = {
                    'period': week['label'],
                    'start_time': week['start'],
                    'end_time': week['end'],
                    **week_data
                }
            
            # Cache historical data permanently
            with open(DEEP_DIVE_HISTORICAL_CACHE, 'w') as f:
                json.dump(historical_data, f, indent=2)
            
            logger.info("💾 Deep dive historical data cached permanently")
            return historical_data
            
        except Exception as e:
            logger.error(f"❌ Error getting deep dive historical weeks: {e}")
            return {}
    
    def get_current_week_definition(self) -> Dict[str, str]:
        """Dynamically determine current week based on date"""
        now = datetime.utcnow()
        
        # Define week boundaries (same as main tracker)
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

    def get_current_deep_dive(self) -> Dict[str, Any]:
        """Get current week deep dive data (always live)"""
        try:
            logger.info("🔴 Fetching current week deep dive (live data)")
            
            # Dynamically determine current week
            current_week = self.get_current_week_definition()
            logger.info(f"📅 Deep dive current week: {current_week['label']}")
            
            week_data = self.fetch_all_apps_week(current_week['start'], current_week['end'])
            
            current_data = {
                'period': current_week['label'],
                'start_time': current_week['start'],
                'end_time': current_week['end'],
                'week_number': current_week['week_number'],
                **week_data
            }
            
            # Cache current week (short-term)
            with open(DEEP_DIVE_CURRENT_CACHE, 'w') as f:
                json.dump(current_data, f, indent=2)
            
            return current_data
            
        except Exception as e:
            logger.error(f"❌ Error getting current deep dive week: {e}")
            return {}
    
    def get_deep_dive_data(self) -> Dict[str, Any]:
        """Get current week deep dive analysis with consistent Gemini app data"""
        try:
            logger.info("🔍 Generating current week deep dive analysis (fast mode)")
            
            # Get ONLY current week (live) - no historical data to avoid timeouts
            current_data = self.get_current_deep_dive()
            
            if not current_data:
                logger.warning("⚠️ No current week data available")
                return {}
            
            # Extract current week data
            app_breakdown = current_data.get('app_breakdown', {})
            action_breakdown = current_data.get('action_breakdown', {})
            
            # Import main dashboard tracker to get consistent Gemini app data
            from gemini_tracker_cached import CachedGeminiTracker
            main_tracker = CachedGeminiTracker()
            main_current_week = main_tracker.get_current_week()
            
            # Use main dashboard data for gemini_app to ensure consistency
            if main_current_week and 'gemini_app' in app_breakdown:
                app_breakdown['gemini_app'] = {
                    'count': main_current_week.get('activities', app_breakdown['gemini_app']['count']),
                    'users': main_current_week.get('users', app_breakdown['gemini_app']['users'])
                }
                logger.info(f"🔄 Using main dashboard data for gemini_app: {app_breakdown['gemini_app']['users']} users")
            
            # Sort by usage
            sorted_apps = sorted(app_breakdown.items(), key=lambda x: x[1]['count'], reverse=True)
            sorted_actions = sorted(action_breakdown.items(), key=lambda x: x[1], reverse=True)
            
            # Convert to expected format
            top_apps = {}
            for app, data in sorted_apps[:10]:
                top_apps[app] = {
                    'total_activities': data.get('count', 0),
                    'max_weekly_users': data.get('users', 0)
                }
            
            top_actions = dict(sorted_actions[:15])
            
            deep_dive_data = {
                'summary': {
                    'total_apps_used': len(app_breakdown),
                    'total_actions_tracked': len(action_breakdown),
                    'weeks_analyzed': 1,  # Only current week
                    'latest_week_activities': current_data.get('total_activities', 0)
                },
                'app_analysis': {
                    'top_apps': top_apps,
                    'app_trends': app_breakdown
                },
                'action_analysis': {
                    'top_actions': top_actions,
                    'action_trends': action_breakdown
                },
                'weekly_trends': [{
                    'week': 'Current Week (Live)',
                    'total_activities': current_data.get('total_activities', 0),
                    'total_users': current_data.get('total_users', 0)
                }],
                'raw_weekly_data': {
                    'Current Week (Live)': current_data
                },
                'last_updated': datetime.now().isoformat(),
                'data_source': 'Live Current Week Only (All Apps) - Fast Mode',
                'cache_status': {
                    'historical_cached': False,  # No historical data
                    'current_week_live': True
                }
            }
            
            logger.info(f"✅ Fast deep dive data ready: {len(app_breakdown)} apps, {len(action_breakdown)} actions")
            return deep_dive_data
            
        except Exception as e:
            logger.error(f"❌ Error generating fast deep dive data: {e}")
            return {}


def main():
    """Main function for deep dive API"""
    try:
        tracker = CachedGeminiDeepDive()
        deep_dive_data = tracker.get_deep_dive_data()
        
        # Output JSON for API consumption
        print(json.dumps(deep_dive_data, indent=2))
        
    except Exception as e:
        logger.error(f"❌ Error in deep dive main: {e}")
        # Return error response
        error_response = {
            'error': str(e),
            'summary': {'total_apps_used': 0, 'total_actions_tracked': 0, 'weeks_analyzed': 0},
            'app_analysis': {'top_apps': {}, 'app_trends': {}},
            'action_analysis': {'top_actions': {}, 'action_trends': {}},
            'last_updated': datetime.now().isoformat()
        }
        print(json.dumps(error_response, indent=2))


if __name__ == "__main__":
    main()
