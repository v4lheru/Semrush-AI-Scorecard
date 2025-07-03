#!/usr/bin/env python3
"""
Gemini App Usage Tracker - Week over Week Analytics

This script focuses specifically on gemini_app usage (standalone Gemini, not Workspace integrations)
and provides week-over-week usage analytics for dashboard integration.

Author: PACT Cline
Date: 2025-07-03
"""

import json
import logging
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from tabulate import tabulate
from colorama import init, Fore, Style
import config

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)


class GeminiAppTracker:
    """
    Focused tracker for standalone Gemini app usage with week-over-week analytics
    """
    
    def __init__(self):
        """Initialize the Gemini App Tracker"""
        self.credentials = None
        self.access_token = None
        self.token_expiry = None
        
        # Validate configuration
        if not config.validate_config():
            sys.exit(1)
        
        logger.info("🛠️ Initializing Gemini App Tracker")
        logger.info(f"Service Account: {config.SERVICE_ACCOUNT_FILE}")
        logger.info(f"Domain Admin: {config.DOMAIN_ADMIN_EMAIL}")
    
    def _load_service_account_credentials(self) -> service_account.Credentials:
        """Load service account credentials from JSON file"""
        try:
            logger.info("📋 Loading service account credentials...")
            
            credentials = service_account.Credentials.from_service_account_file(
                config.SERVICE_ACCOUNT_FILE,
                scopes=config.SCOPES
            )
            
            # CRITICAL: Enable domain-wide delegation by setting subject
            delegated_credentials = credentials.with_subject(config.DOMAIN_ADMIN_EMAIL)
            
            logger.info("✅ Service account credentials loaded successfully")
            return delegated_credentials
            
        except Exception as e:
            logger.error(f"❌ Error loading service account credentials: {e}")
            raise
    
    def get_access_token(self) -> str:
        """Get a valid access token for API requests"""
        try:
            # Check if we need to refresh the token
            if (self.credentials is None or 
                self.access_token is None or 
                (self.token_expiry and datetime.utcnow() >= self.token_expiry)):
                
                logger.info("🔑 Getting new access token...")
                
                # Load credentials if not already loaded
                if self.credentials is None:
                    self.credentials = self._load_service_account_credentials()
                
                # Refresh the token
                self.credentials.refresh(Request())
                self.access_token = self.credentials.token
                self.token_expiry = self.credentials.expiry
                
                logger.info("✅ Access token obtained successfully")
            
            return self.access_token
            
        except Exception as e:
            logger.error(f"❌ Error getting access token: {e}")
            raise
    
    def _make_api_request(self, url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make an authenticated API request"""
        try:
            access_token = self.get_access_token()
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Accept': 'application/json',
                'User-Agent': 'GeminiAppTracker/1.0'
            }
            
            logger.info(f"🌐 Making API request to: {url}")
            if params:
                logger.info(f"Parameters: {params}")
            
            response = requests.get(
                url,
                headers=headers,
                params=params or {},
                timeout=config.REQUEST_TIMEOUT
            )
            
            logger.info(f"Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                logger.info("✅ API request successful")
                return data
            else:
                logger.error(f"❌ API request failed: {response.status_code}")
                logger.error(f"Response: {response.text}")
                response.raise_for_status()
                
        except Exception as e:
            logger.error(f"❌ Request error: {e}")
            raise
    
    def get_gemini_app_activities(self, 
                                start_time: str,
                                end_time: str,
                                max_results: int = 1000) -> List[Dict[str, Any]]:
        """
        Get Gemini app activities for a specific time period
        
        Args:
            start_time: Start time in ISO format
            end_time: End time in ISO format
            max_results: Maximum number of results
        
        Returns:
            List of parsed Gemini app activity records
        """
        try:
            logger.info(f"📊 Fetching Gemini app activities from {start_time} to {end_time}")
            
            url = config.get_api_endpoint('activities')
            
            params = {
                'eventName': config.GEMINI_EVENT_NAME,
                'maxResults': max_results,
                'startTime': start_time,
                'endTime': end_time
            }
            
            data = self._make_api_request(url, params)
            
            # Parse and filter for gemini_app only
            items = data.get('items', [])
            gemini_app_activities = []
            
            for item in items:
                actor = item.get('actor', {})
                events = item.get('events', [])
                activity_id = item.get('id', {})
                
                user_email = actor.get('email', 'Unknown')
                timestamp = activity_id.get('time', '')
                
                for event in events:
                    parameters = event.get('parameters', [])
                    
                    # Extract parameters into a dict
                    param_dict = {}
                    for param in parameters:
                        param_name = param.get('name', '')
                        param_value = param.get('value', '')
                        param_dict[param_name] = param_value
                    
                    # Filter for gemini_app only
                    app_name = param_dict.get('app_name', '')
                    if app_name == 'gemini_app':
                        activity_record = {
                            'timestamp': timestamp,
                            'user_email': user_email,
                            'action': param_dict.get('action', 'Unknown'),
                            'event_category': param_dict.get('event_category', 'Unknown'),
                            'feature_source': param_dict.get('feature_source', 'Unknown')
                        }
                        gemini_app_activities.append(activity_record)
            
            logger.info(f"📈 Retrieved {len(gemini_app_activities)} Gemini app activity records")
            return gemini_app_activities
            
        except Exception as e:
            logger.error(f"❌ Error fetching Gemini app activities: {e}")
            raise
    
    def get_week_over_week_data(self, weeks_back: int = None) -> Dict[str, Any]:
        """
        Get week-over-week Gemini app usage data from June 20th onwards
        
        Args:
            weeks_back: Number of weeks to look back (None = all available weeks from June 20th)
        
        Returns:
            Dict containing weekly usage data
        """
        try:
            # Gemini logs are only available from 2025-06-20T00:00:00Z
            gemini_start_date = datetime(2025, 6, 20, 0, 0, 0)
            end_date = datetime.utcnow()
            
            # Calculate how many weeks are available from June 20th
            total_days = (end_date - gemini_start_date).days
            max_weeks = (total_days // 7) + 1  # +1 for partial week
            
            if weeks_back is None:
                weeks_back = max_weeks
                logger.info(f"📊 Generating ALL available week-over-week data from June 20th ({max_weeks} weeks)")
            else:
                logger.info(f"📊 Generating week-over-week data for {weeks_back} weeks")
            
            weekly_data = {}
            
            for week in range(min(weeks_back, max_weeks)):
                # Calculate week boundaries
                week_end = end_date - timedelta(weeks=week)
                week_start = week_end - timedelta(days=7)
                
                # Adjust start time if it's before Gemini availability
                if week_start < gemini_start_date:
                    week_start = gemini_start_date
                    logger.info(f"Adjusted week start to Gemini availability date: {week_start}")
                
                # Skip if week_end is before Gemini availability
                if week_end < gemini_start_date:
                    logger.info(f"Skipping week {week + 1} - entirely before Gemini data availability")
                    continue
                
                # Format for API
                start_time_str = week_start.strftime('%Y-%m-%dT%H:%M:%SZ')
                end_time_str = week_end.strftime('%Y-%m-%dT%H:%M:%SZ')
                
                # Get activities for this week
                activities = self.get_gemini_app_activities(start_time_str, end_time_str)
                
                # Calculate metrics
                unique_users = set(activity['user_email'] for activity in activities)
                total_activities = len(activities)
                
                # Group by action type
                actions = {}
                for activity in activities:
                    action = activity['action']
                    actions[action] = actions.get(action, 0) + 1
                
                # Group by event category
                categories = {}
                for activity in activities:
                    category = activity['event_category']
                    categories[category] = categories.get(category, 0) + 1
                
                week_label = f"Week {weeks_back - week}"
                week_date = week_start.strftime('%Y-%m-%d')
                
                weekly_data[week_label] = {
                    'week_start': week_start.strftime('%Y-%m-%d'),
                    'week_end': week_end.strftime('%Y-%m-%d'),
                    'total_activities': total_activities,
                    'unique_users': len(unique_users),
                    'user_list': list(unique_users),
                    'actions': actions,
                    'categories': categories,
                    'activities': activities
                }
                
                logger.info(f"Week {week + 1}: {total_activities} activities, {len(unique_users)} users")
            
            return weekly_data
            
        except Exception as e:
            logger.error(f"❌ Error generating week-over-week data: {e}")
            raise
    
    def generate_dashboard_data(self, weekly_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate data formatted for dashboard consumption
        
        Args:
            weekly_data: Weekly usage data
        
        Returns:
            Dashboard-ready data structure
        """
        try:
            logger.info("📊 Generating dashboard data format")
            
            # Prepare time series data
            weeks = []
            cumulative_users = []
            weekly_activities = []
            weekly_unique_users = []
            
            all_users = set()
            
            # Sort weeks chronologically
            sorted_weeks = sorted(weekly_data.keys(), key=lambda x: int(x.split()[1]))
            
            for week_label in sorted_weeks:
                week_data = weekly_data[week_label]
                
                weeks.append(week_label)
                weekly_activities.append(week_data['total_activities'])
                weekly_unique_users.append(week_data['unique_users'])
                
                # Add to cumulative users
                all_users.update(week_data['user_list'])
                cumulative_users.append(len(all_users))
            
            # Calculate week-over-week growth
            wow_growth = []
            for i in range(1, len(weekly_unique_users)):
                if weekly_unique_users[i-1] > 0:
                    growth = ((weekly_unique_users[i] - weekly_unique_users[i-1]) / weekly_unique_users[i-1]) * 100
                    wow_growth.append(round(growth, 1))
                else:
                    wow_growth.append(0)
            
            # Most recent week data
            latest_week = weekly_data[sorted_weeks[-1]] if sorted_weeks else {}
            
            dashboard_data = {
                'summary': {
                    'total_cumulative_users': len(all_users),
                    'latest_week_activities': latest_week.get('total_activities', 0),
                    'latest_week_users': latest_week.get('unique_users', 0),
                    'total_weeks_tracked': len(weeks)
                },
                'time_series': {
                    'weeks': weeks,
                    'cumulative_users': cumulative_users,
                    'weekly_activities': weekly_activities,
                    'weekly_unique_users': weekly_unique_users,
                    'wow_growth_percent': wow_growth
                },
                'latest_week_breakdown': {
                    'actions': latest_week.get('actions', {}),
                    'categories': latest_week.get('categories', {}),
                    'top_users': latest_week.get('user_list', [])[:10]  # Top 10 users
                },
                'raw_weekly_data': weekly_data,
                'last_updated': datetime.now().isoformat(),
                'data_source': 'Google Admin SDK - Live Data'
            }
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"❌ Error generating dashboard data: {e}")
            raise


def main():
    """Main function to run the Gemini App Tracker"""
    try:
        # Initialize tracker
        tracker = GeminiAppTracker()
        
        # Test authentication
        access_token = tracker.get_access_token()
        
        # Get week-over-week data (all available weeks from June 20th)
        weekly_data = tracker.get_week_over_week_data(weeks_back=None)
        
        # Generate dashboard data
        dashboard_data = tracker.generate_dashboard_data(weekly_data)
        
        # Output JSON for Node.js consumption
        print(json.dumps(dashboard_data, indent=2, default=str))
        
        return dashboard_data
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        # Return empty data structure on error
        error_data = {
            'summary': {
                'total_cumulative_users': 0,
                'latest_week_activities': 0,
                'latest_week_users': 0,
                'total_weeks_tracked': 0
            },
            'time_series': {
                'weeks': [],
                'cumulative_users': [],
                'weekly_activities': [],
                'weekly_unique_users': [],
                'wow_growth_percent': []
            },
            'latest_week_breakdown': {
                'actions': {},
                'categories': {},
                'top_users': []
            },
            'last_updated': datetime.now().isoformat(),
            'data_source': f'Error: {str(e)}',
            'error': True
        }
        print(json.dumps(error_data, indent=2, default=str))
        return error_data

if __name__ == "__main__":
    main()
