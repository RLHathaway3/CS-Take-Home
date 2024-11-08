import os
import requests
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv('credentials.env')

# Define your credentials
JIRA_BASE_URL = os.getenv('atlassian_url')
JIRA_API_TOKEN = os.getenv('atlassian_api_token')

HEADERS = {
    'Authorization': f'Bearer {JIRA_API_TOKEN}',
    'Content-Type': 'application/json'
}

# Define your field ID
MULTI_SELECT_FIELD = 'customfield_10101'

# Define source and target issue keys
SOURCE_ISSUE_KEY = 'CS8-50'
TARGET_ISSUE_KEY = 'CS4-47'

# Get the values from the source issue's multi-select field
url = f"{JIRA_BASE_URL}/rest/api/2/issue/{SOURCE_ISSUE_KEY}"
response = requests.get(url, headers=HEADERS)
if response.status_code != 200:
    print(f"Failed to fetch data from Jira: {response.status_code} - {response.text}")
    exit(1)
source_issue = response.json()

source_field_values = source_issue['fields'].get(MULTI_SELECT_FIELD, [])

# Update the target issue's multi-select field with the values from the source issue
if source_field_values:
    values = [{'value': item['value']} for item in source_field_values]
    url = f"{JIRA_BASE_URL}/rest/api/2/issue/{TARGET_ISSUE_KEY}"
    data = {
        'fields': {
            MULTI_SELECT_FIELD: values
        }
    }
    response = requests.put(url, headers=HEADERS, json=data)
    if response.status_code != 204:
        print(f"Failed to fetch data from Jira: {response.status_code} - {response.text}")
        exit(1)
    print(f"Copied values from issue {SOURCE_ISSUE_KEY} to issue {TARGET_ISSUE_KEY} successfully.")
else:
    print(f"No values found in the multi-select field for issue {SOURCE_ISSUE_KEY}.")