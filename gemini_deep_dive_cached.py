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
from datetime import datetime
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
    
    def get_current_deep_dive(self) -> Dict[str, Any]:
        """Get current week deep dive data (always live)"""
        try:
            logger.info("🔴 Fetching current week deep dive (live data)")
            
            # Current week definition
            current_week = {
                'label': 'Week 4 (Jul 7-Current) (Live)',
                'start': '2025-07-07T00:00:00Z',
                'end': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            }
            
            week_data = self.fetch_all_apps_week(current_week['start'], current_week['end'])
            
            current_data = {
                'period': current_week['label'],
                'start_time': current_week['start'],
                'end_time': current_week['end'],
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
        """Get complete deep dive analysis with caching"""
        try:
            logger.info("🔍 Generating deep dive analysis")
            
            # Get historical data (cached)
            historical_data = self.get_historical_deep_dive()
            
            # Get current week (live)
            current_data = self.get_current_deep_dive()
            
            # Combine all weeks
            all_weeks = {**historical_data}
            if current_data:
                all_weeks[current_data['period']] = current_data
            
            # Aggregate app usage across all weeks
            total_app_breakdown = {}
            total_action_breakdown = {}
            weekly_totals = []
            
            for week_label in ['Week 1 (Jun 20-22)', 'Week 2 (Jun 23-29)', 'Week 3 (Jun 30-Jul 6)', 'Week 4 (Jul 7-Current) (Live)']:
                if week_label in all_weeks:
                    week_data = all_weeks[week_label]
                    weekly_totals.append({
                        'week': week_label.replace(' (Live)', ''),
                        'total_activities': week_data.get('total_activities', 0),
                        'total_users': week_data.get('total_users', 0)
                    })
                    
                    # Aggregate apps
                    app_breakdown = week_data.get('app_breakdown', {})
                    for app, data in app_breakdown.items():
                        if app not in total_app_breakdown:
                            total_app_breakdown[app] = {'total_activities': 0, 'max_weekly_users': 0}
                        total_app_breakdown[app]['total_activities'] += data.get('count', 0)
                        total_app_breakdown[app]['max_weekly_users'] = max(
                            total_app_breakdown[app]['max_weekly_users'],
                            data.get('users', 0)
                        )
                    
                    # Aggregate actions
                    action_breakdown = week_data.get('action_breakdown', {})
                    for action, count in action_breakdown.items():
                        if action not in total_action_breakdown:
                            total_action_breakdown[action] = 0
                        total_action_breakdown[action] += count
            
            # Sort by usage
            sorted_apps = sorted(total_app_breakdown.items(), key=lambda x: x[1]['total_activities'], reverse=True)
            sorted_actions = sorted(total_action_breakdown.items(), key=lambda x: x[1], reverse=True)
            
            deep_dive_data = {
                'summary': {
                    'total_apps_used': len(total_app_breakdown),
                    'total_actions_tracked': len(total_action_breakdown),
                    'weeks_analyzed': len(weekly_totals),
                    'latest_week_activities': current_data.get('total_activities', 0) if current_data else 0
                },
                'app_analysis': {
                    'top_apps': dict(sorted_apps[:10]),
                    'app_trends': total_app_breakdown
                },
                'action_analysis': {
                    'top_actions': dict(sorted_actions[:15]),
                    'action_trends': total_action_breakdown
                },
                'weekly_trends': weekly_totals,
                'raw_weekly_data': all_weeks,
                'last_updated': datetime.now().isoformat(),
                'data_source': 'Cached Historical + Live Current Week (All Apps)',
                'cache_status': {
                    'historical_cached': os.path.exists(DEEP_DIVE_HISTORICAL_CACHE),
                    'current_week_live': True
                }
            }
            
            logger.info(f"✅ Deep dive data ready: {len(total_app_breakdown)} apps, {len(total_action_breakdown)} actions")
            return deep_dive_data
            
        except Exception as e:
            logger.error(f"❌ Error generating deep dive data: {e}")
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
