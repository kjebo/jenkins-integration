import json
from jira import JIRA
from datetime import datetime
import requests

def format_duration(duration):
    hours, remainder = divmod(duration.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

options = {
    'server': 'http://localhost:8082/',
    'headers': {
        'Authorization': 'Bearer MDM0MDMzNDk2NDg4OuXlmR9O5ligBwWKTj61IP+HRdx1'
    },
    'verify': False,
    'session': requests.Session()
}

jira = JIRA(options=options)

class Issue:
    def __init__(self, key, issuetype, parent, subtasks, created, resolutiondate, changelog):
        self.key = key
        self.issuetype = issuetype
        self.parent = parent
        self.subtasks = subtasks
        self.created = created
        self.resolutiondate = resolutiondate
        self.changelog = changelog

    def __str__(self):
        return f"Key: {self.key}\nType: {self.issuetype}\nParent: {self.parent}\nSubtasks: {self.subtasks}\nCreated: {self.created}\nResolution Date: {self.resolutiondate}\nChangelog: {self.changelog}"

try:
    issues = jira.search_issues('')

    issue_list = []

    for issue in issues:
        issue_key = issue.key
        issue_data = jira.issue(issue_key, expand='changelog')

        created_date_str = issue_data.fields.created
        created_date = datetime.strptime(created_date_str, "%Y-%m-%dT%H:%M:%S.%f%z")
        resolution_date_str = issue_data.fields.resolutiondate
        resolution_date = datetime.strptime(resolution_date_str, "%Y-%m-%dT%H:%M:%S.%f%z") if resolution_date_str else None

        parent_key = issue_data.fields.parent.key if hasattr(issue_data.fields, 'parent') and issue_data.fields.parent else None

        subtasks = [subtask.key for subtask in jira.search_issues(f'parent={issue_key}')]

        if not subtasks:
            subtasks = None

        changelog = []
        previous_created = None
        for history in issue_data.changelog.histories:
            for item in history.items:
                if item.fromString in ['In Review', 'To Do', 'In Progress', 'Done'] and item.toString in ['In Review', 'To Do', 'In Progress', 'Done']:
                    created_timestamp = history.created
                    if previous_created:
                        created_diff = datetime.strptime(created_timestamp, "%Y-%m-%dT%H:%M:%S.%f%z") - datetime.strptime(previous_created, "%Y-%m-%dT%H:%M:%S.%f%z")
                        changelog.append({
                            'Created': created_timestamp,
                            'From': item.fromString,
                            'To': item.toString,
                            'time_before_change': format_duration(created_diff)
                        })
                    previous_created = created_timestamp

        # Sort the changelog entries based on the 'Created' timestamp
        changelog.sort(key=lambda x: datetime.strptime(x['Created'], "%Y-%m-%dT%H:%M:%S.%f%z"))

        issue = Issue(issue_key, issue_data.fields.issuetype.name, parent_key, subtasks, created_date_str, resolution_date_str, changelog)
        issue_list.append(issue)

    with open('issues.json', 'w') as file:
        json.dump([issue.__dict__ for issue in issue_list], file, indent=4)

    print("issues.json file created successfully.")

except Exception as e:
    print(f"Failed to fetch issues: {e}")
