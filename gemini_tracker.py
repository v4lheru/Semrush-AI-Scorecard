#!/usr/bin/env python3
"""
Gemini ALL APPS Usage Tracker - Complete Workspace Integration

This script tracks Gemini usage across ALL Google Workspace applications:
- gemini_app (standalone Gemini)
- gmail (Help me write, summarize)
- docs (Help me write, proofread, generate)
- sheets (AI functions, help me organize)
- slides (Generate images, help me visualize)
- meet (Summaries, action items, studio features)
- drive (Summarize files, help me organize)
- chat (Gemini conversations)

Author: PACT Cline
Date: 2025-07-08
"""

import json
import logging
import os
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
        """Load service account credentials from JSON file or environment variable"""
        try:
            logger.info("📋 Loading service account credentials...")
            
            # Try to load from environment variable first (for Railway deployment)
            service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
            
            if service_account_json:
                logger.info("🔑 Using service account JSON from environment variable")
                # Parse JSON from environment variable
                service_account_info = json.loads(service_account_json)
                credentials = service_account.Credentials.from_service_account_info(
                    service_account_info,
                    scopes=config.SCOPES
                )
            else:
                logger.info("📁 Using service account file from filesystem")
                # Fallback to file-based loading
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
    
    def get_all_gemini_activities(self, 
                                start_time: str,
                                end_time: str,
                                max_results: int = 1000) -> List[Dict[str, Any]]:
        """
        Get ALL Gemini activities across ALL Workspace applications
        
        Args:
            start_time: Start time in ISO format
            end_time: End time in ISO format
            max_results: Maximum number of results
        
        Returns:
            List of ALL Gemini activity records across all apps
        """
        try:
            logger.info(f"📊 Fetching ALL Gemini activities across ALL apps from {start_time} to {end_time}")
            
            url = config.get_api_endpoint('activities')
            
            params = {
                'eventName': config.GEMINI_EVENT_NAME,
                'maxResults': max_results,
                'startTime': start_time,
                'endTime': end_time
            }
            
            data = self._make_api_request(url, params)
            
            # Parse ALL Gemini activities (no app filter - include all apps)
            items = data.get('items', [])
            all_gemini_activities = []
            
            # Focus on these main apps
            target_apps = {
                'gemini_app', 'gmail', 'docs', 'sheets', 
                'slides', 'meet', 'drive', 'chat'
            }
            
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
                    
                    # Include ALL target apps (not just gemini_app)
                    app_name = param_dict.get('app_name', 'Unknown')
                    if app_name in target_apps:
                        activity_record = {
                            'timestamp': timestamp,
                            'user_email': user_email,
                            'app_name': app_name,
                            'action': param_dict.get('action', 'Unknown'),
                            'event_category': param_dict.get('event_category', 'Unknown'),
                            'feature_source': param_dict.get('feature_source', 'Unknown')
                        }
                        all_gemini_activities.append(activity_record)
            
            logger.info(f"📈 Retrieved {len(all_gemini_activities)} TOTAL Gemini activity records across ALL apps")
            return all_gemini_activities
            
        except Exception as e:
            logger.error(f"❌ Error fetching ALL Gemini activities: {e}")
            raise
    
    def get_week_over_week_data(self, weeks_back: int = None) -> Dict[str, Any]:
        """
        Get week-over-week Gemini app usage data using FIXED weekly boundaries
        
        Args:
            weeks_back: Number of weeks to look back (None = all available weeks from June 16th)
        
        Returns:
            Dict containing weekly usage data with consistent boundaries
        """
        try:
            # FUTURE-PROOF FIXED WEEKLY BOUNDARIES
            # Generate weeks automatically but with FIXED start point that never changes
            
            # FIXED ANCHOR POINT - This never changes regardless of when script runs
            FIXED_WEEK_1_START = datetime(2025, 6, 16, 0, 0, 0)  # Monday, June 16, 2025 00:00:00
            
            # Calculate how many complete weeks have passed since the fixed anchor
            current_time = datetime.utcnow()
            days_since_anchor = (current_time - FIXED_WEEK_1_START).days
            weeks_since_anchor = days_since_anchor // 7  # Only complete weeks
            
            # Generate weekly periods with FIXED boundaries
            weekly_periods = []
            for week_num in range(weeks_since_anchor + 2):  # +2 to include current partial week
                week_start = FIXED_WEEK_1_START + timedelta(weeks=week_num)
                week_end = week_start + timedelta(days=7)
                
                # Include completed weeks (historical - static data)
                if week_end <= current_time:
                    weekly_periods.append({
                        'start': week_start,
                        'end': week_end,
                        'is_complete': True,
                        'is_current': False
                    })
                # Include current partial week (live - changing data)
                elif week_start <= current_time < week_end:
                    weekly_periods.append({
                        'start': week_start,
                        'end': current_time,  # Use current time as end for partial week
                        'is_complete': False,
                        'is_current': True
                    })
            
            logger.info(f"📊 Generated {len(weekly_periods)} complete weeks from fixed anchor point")
            logger.info(f"🔒 Anchor: {FIXED_WEEK_1_START.strftime('%Y-%m-%d %H:%M:%S')} (never changes)")
            logger.info(f"⏰ Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Limit weeks if specified
            if weeks_back is not None:
                weekly_periods = weekly_periods[-weeks_back:]
            
            logger.info(f"📊 Generating data for {len(weekly_periods)} fixed weekly periods")
            
            weekly_data = {}
            
            for period in weekly_periods:
                week_start = period['start']
                week_end = period['end']
                
                # Skip if week_end is before Gemini availability (June 20th)
                gemini_availability = datetime(2025, 6, 20, 0, 0, 0)
                if week_end < gemini_availability:
                    logger.info(f"Skipping week {week_start.strftime('%Y-%m-%d')} - before Gemini availability")
                    continue
                
                # Adjust start time if it's before Gemini availability
                if week_start < gemini_availability:
                    week_start = gemini_availability
                    logger.info(f"Adjusted week start to Gemini availability date: {week_start}")
                
                # Format for API
                start_time_str = week_start.strftime('%Y-%m-%dT%H:%M:%SZ')
                end_time_str = week_end.strftime('%Y-%m-%dT%H:%M:%SZ')
                
                # Get activities for this week
                activities = self.get_all_gemini_activities(start_time_str, end_time_str)
                
                # Calculate metrics
                unique_users = set(activity['user_email'] for activity in activities)
                total_activities = len(activities)
                
                # Group by app (for detailed breakdown)
                apps_breakdown = {}
                for activity in activities:
                    app = activity['app_name']
                    if app not in apps_breakdown:
                        apps_breakdown[app] = {
                            'users': set(),
                            'activities': 0,
                            'actions': {},
                            'categories': {}
                        }
                    
                    apps_breakdown[app]['users'].add(activity['user_email'])
                    apps_breakdown[app]['activities'] += 1
                    
                    # Track actions per app
                    action = activity['action']
                    apps_breakdown[app]['actions'][action] = apps_breakdown[app]['actions'].get(action, 0) + 1
                    
                    # Track categories per app
                    category = activity['event_category']
                    apps_breakdown[app]['categories'][category] = apps_breakdown[app]['categories'].get(category, 0) + 1
                
                # Convert sets to counts for JSON serialization
                for app in apps_breakdown:
                    apps_breakdown[app]['unique_users'] = len(apps_breakdown[app]['users'])
                    apps_breakdown[app]['user_list'] = list(apps_breakdown[app]['users'])
                    del apps_breakdown[app]['users']  # Remove set object
                
                # Group by action type (overall)
                actions = {}
                for activity in activities:
                    action = activity['action']
                    actions[action] = actions.get(action, 0) + 1
                
                # Group by event category (overall)
                categories = {}
                for activity in activities:
                    category = activity['event_category']
                    categories[category] = categories.get(category, 0) + 1
                
                # Create meaningful week labels with date ranges
                # Handle cross-month and cross-year scenarios properly
                week_start_str = week_start.strftime('%b %d')
                
                # For current week, show "current" indicator and use current time as end
                if period.get('is_current', False):
                    week_end_str = "Current"
                    week_label_suffix = " (Live)"
                else:
                    week_end_str = week_end.strftime('%b %d')
                    week_label_suffix = ""
                
                # If crossing years, include year in the label
                if week_start.year != week_end.year and not period.get('is_current', False):
                    week_start_str = week_start.strftime('%b %d, %Y')
                    week_end_str = week_end.strftime('%b %d, %Y')
                    week_label = f"{week_start_str}-{week_end_str}{week_label_suffix}"
                # If crossing months, show both months
                elif week_start.month != week_end.month and not period.get('is_current', False):
                    week_label = f"{week_start_str}-{week_end_str}{week_label_suffix}"
                elif period.get('is_current', False):
                    # Current week - show start date and "Current"
                    week_label = f"{week_start_str}-{week_end_str}{week_label_suffix}"
                else:
                    # Same month, optimize display
                    week_start_day = week_start.strftime('%d')
                    week_label = f"{week_start.strftime('%b')} {week_start_day}-{week_end.strftime('%d')}{week_label_suffix}"
                
                weekly_data[week_label] = {
                    'week_start': week_start.strftime('%Y-%m-%d'),
                    'week_end': week_end.strftime('%Y-%m-%d'),
                    'total_activities': total_activities,
                    'unique_users': len(unique_users),
                    'user_list': list(unique_users),
                    'actions': actions,
                    'categories': categories,
                    'apps_breakdown': apps_breakdown,  # Per-app detailed breakdown
                    'activities': activities
                }
                
                logger.info(f"Week {week_start.strftime('%Y-%m-%d')}: {total_activities} activities, {len(unique_users)} users")
            
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
            total_weekly_users = []  # Total weekly active users from ALL AI tools
            weekly_activities = []
            weekly_unique_users = []
            
            all_users = set()
            
            # Sort weeks chronologically by start date
            sorted_weeks = sorted(weekly_data.keys(), key=lambda x: weekly_data[x]['week_start'])
            
            for week_label in sorted_weeks:
                week_data = weekly_data[week_label]
                
                weeks.append(week_label)
                weekly_activities.append(week_data['total_activities'])
                weekly_unique_users.append(week_data['unique_users'])
                
                # Calculate total weekly users from ALL AI tools for this week
                # Currently we only have Gemini data, but this structure allows for future expansion
                gemini_users = week_data['unique_users']
                claude_users = 0  # Future: Add Claude analytics
                cursor_users = 0  # Future: Add Cursor analytics  
                chatgpt_users = 0  # Future: Add ChatGPT analytics
                
                # Total weekly active users across all AI tools
                total_weekly = gemini_users + claude_users + cursor_users + chatgpt_users
                total_weekly_users.append(total_weekly)
                
                # Track cumulative unique users ever (for summary stats)
                all_users.update(week_data['user_list'])
            
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
                    'total_weekly_users': total_weekly_users,  # Total weekly active users from ALL AI tools
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
