#!/usr/bin/env python3
"""
Configuration file for Gemini App Usage Tracker
"""

import os

# Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE', 'service-account.json')
DOMAIN_ADMIN_EMAIL = os.getenv('DOMAIN_ADMIN_EMAIL', 'i.karlakis@semrush.com')
REQUEST_TIMEOUT = 30
GEMINI_EVENT_NAME = 'feature_utilization'

# Scopes for Google Admin SDK
SCOPES = [
    'https://www.googleapis.com/auth/admin.reports.audit.readonly'
]

def get_api_endpoint(endpoint_type):
    """Get API endpoint URL"""
    base_url = 'https://admin.googleapis.com/admin/reports/v1'
    endpoints = {
        'activities': f'{base_url}/activity/users/all/applications/gemini_in_workspace_apps'
    }
    return endpoints.get(endpoint_type)

def validate_config():
    """Validate configuration"""
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"Service account file not found: {SERVICE_ACCOUNT_FILE}")
        return False
    
    if not DOMAIN_ADMIN_EMAIL:
        print("Domain admin email not configured")
        return False
    
    return True
