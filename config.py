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
    # Check if we have JSON credentials in environment variable
    service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
    
    if not service_account_json and not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"Neither GOOGLE_SERVICE_ACCOUNT_JSON environment variable nor service account file found: {SERVICE_ACCOUNT_FILE}")
        return False
    
    if not DOMAIN_ADMIN_EMAIL:
        print("Domain admin email not configured")
        return False
    
    return True
