import requests
import os
import csv
from dotenv import load_dotenv

# Load Jira credentials from .env file
load_dotenv('credentials.env')

JIRA_BASE_URL = os.getenv('atlassian_url')
JIRA_API_TOKEN = os.getenv('atlassian_api_token')

CUSTOM_FIELD_ID = 'description'
CUSTOM_FIELD_NAME = 'description'

# Set up authentication header
headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {JIRA_API_TOKEN}"
}

# Count the usage of a custom field per project
start_at = 0
max_results = 100
project_usage = {}

while True:
    # Jira JQL to search for issues containing the custom field
    jql_query = f"{CUSTOM_FIELD_NAME} IS NOT EMPTY"
    search_url = f"{JIRA_BASE_URL}/rest/api/2/search"
    params = {
        'jql': jql_query,
        'startAt': start_at,
        'maxResults': max_results,
        'fields': f"project,{CUSTOM_FIELD_ID}"
    }

    response = requests.get(search_url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Failed to fetch data from Jira: {response.status_code} - {response.text}")
        break

    data = response.json()
    issues = data.get('issues', [])

    for issue in issues:
        project_key = issue['fields']['project']['key']
        if project_key in project_usage:
            project_usage[project_key] += 1
        else:
            project_usage[project_key] = 1

    if len(issues) < max_results:
        break

    start_at += max_results

# Write the usage report per project to a CSV file
csv_file = f'{CUSTOM_FIELD_NAME}_field_usage.csv'
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Project Key', 'Usage Count'])
    for project, usage in project_usage.items():
        writer.writerow([project, usage])

print(f"Report written to {csv_file}")