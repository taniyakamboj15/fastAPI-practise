"""
scripts/cron_email_sender.py

This script simulates an INTERNAL SERVICE (like a Cron Job).
It runs outside the browser, directly on the server (or another server).

Scenario:
Every night, this script runs to send status emails.
It needs to talk to the Backend API, but it cannot "Login" like a user.
So it uses the "X-API-Key" header to authenticate.

Usage:
python scripts/cron_email_sender.py
"""

import requests
import sys

# Configuration
API_URL = "http://127.0.0.1:8000/api/v1/utils/test-email"
# This key MUST match what is in app/core/config.py
API_KEY = "internal_secret_key_12345" 

def trigger_email_sending():
    print(f"🔄 Connecting to Internal API: {API_URL}")
    
    # 1. Prepare Headers (This is where we put the Key)
    headers = {
        "X-API-Key": API_KEY,  # <--- AUTHENTICATION MAGIC
        "Content-Type": "application/json"
    }
    
    # 2. Prepare Data (Query Params)
    params = {
        "email_to": "admin@company.com"
    }
    
    try:
        # 3. Send Request
        response = requests.post(API_URL, headers=headers, params=params)
        
        # 4. Check Result
        if response.status_code == 200:
            print("✅ Success! API accepted our Key.")
            print("Response:", response.json())
        elif response.status_code == 403:
            print("❌ Access Denied! Invalid API Key.")
        else:
            print(f"⚠️ Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Is it running?")

if __name__ == "__main__":
    trigger_email_sending()
