import requests
import os
from dotenv import load_dotenv

# Load Jira credentials from .env file
load_dotenv('credentials.env')

JIRA_BASE_URL = os.getenv('atlassian_url')
JIRA_API_TOKEN = os.getenv('atlassian_api_token')

CUSTOM_FIELD_ID = "customfield_10100"
CUSTOM_FIELD_NAME = "Test"

# Set up authentication header
headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {JIRA_API_TOKEN}"
}

# Count the usage of a custom field
start_at = 0
max_results = 100
total_usage = 0

while True:
    # Jira JQL to search for issues containing the custom field
    jql_query = f"{CUSTOM_FIELD_NAME} IS NOT EMPTY"
    search_url = f"{JIRA_BASE_URL}/rest/api/2/search"
    params = {
        'jql': jql_query,
        'startAt': start_at,
        'maxResults': max_results,
        'fields': CUSTOM_FIELD_ID
    }

    response = requests.get(search_url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Failed to fetch data from Jira: {response.status_code} - {response.text}")
        break

    data = response.json()
    issues = data.get('issues', [])
    total_usage += len(issues)

    # Check if there are more issues to fetch
    if len(issues) < max_results:
        break

    start_at += max_results

print(f"Total usage of custom field {CUSTOM_FIELD_NAME}: {total_usage}")