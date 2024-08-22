import os
import requests

TOKEN = os.getenv('TOKEN')
SLACK_API_URL = 'https://slack.com/api'

# Function to fetch users from Slack API
def fetch_users():
    url = f'{SLACK_API_URL}/users.list'
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()