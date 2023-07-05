import requests
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, Interval, func
from sqlalchemy.orm import declarative_base, sessionmaker
from jira import JIRA
from datetime import datetime

options = {
    'server': 'http://localhost:8082/',
    'headers': {
        'Authorization': 'Bearer MDM0MDMzNDk2NDg4OuXlmR9O5ligBwWKTj61IP+HRdx1'
    },
    'verify': False,
    'session': requests.Session()
}

# Define the database connection
engine = create_engine('postgresql://postgres:postgres@192.168.68.100/postgres')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class JiraExport(Base):
    __tablename__ = 'jira_export'
    changelog_id = Column(Integer, primary_key=True)
    issue_id = Column(Integer)
    issuetype = Column(String)
    changelog_from = Column(String)
    changelog_to = Column(String)
    previous_update = Column(TIMESTAMP)
    this_update = Column(TIMESTAMP)
    duration = Column(Interval)


class Issue:
    def __init__(self, id, issuetype, changelog):
        self.id = id
        self.issuetype = issuetype
        self.changelog = changelog

    def __str__(self):
        return f"ID: {self.id}\nType: {self.issuetype}\nChangelog: {self.changelog}"


def fetch_issues():
    try:
        jira = JIRA(options=options)
        issues = jira.search_issues('')
        return jira, issues
    except Exception as e:
        print(f"Failed to fetch issues: {e}")
        return None, []


def process_issues(jira, issues):
    try:
        for issue in issues:
            issue_id = issue.id
            issue_data = jira.issue(issue.key, expand='changelog')
            changelog = extract_changelog(issue_data)

            previous_update = None  # Initialize previous_update to None for the first changelog item

            for changelog_item in changelog:
                changelog_id = changelog_item['Changelog ID']
                existing_entry = session.query(JiraExport).filter_by(changelog_id=changelog_id).first()

                if existing_entry:
                    existing_entry.changelog_from = changelog_item['From']
                    existing_entry.changelog_to = changelog_item['To']
                    existing_entry.this_update = changelog_item['Created']
                    if existing_entry.previous_update:
                        previous_update = func.timezone('UTC', existing_entry.previous_update)  # Convert previous_update to UTC timezone
                        duration = existing_entry.this_update - previous_update
                        existing_entry.duration = duration
                else:
                    jira_export = JiraExport(
                        issue_id=issue_id,
                        changelog_id=changelog_id,
                        issuetype=issue_data.fields.issuetype.name,
                        changelog_from=changelog_item['From'],
                        changelog_to=changelog_item['To'],
                        previous_update=previous_update,
                        this_update=changelog_item['Created'],
                    )

                    if previous_update is not None:
                        duration = changelog_item['Created'] - previous_update
                        jira_export.duration = duration

                    previous_update = changelog_item['Created']  # Update the previous update

                    session.add(jira_export)

        session.commit()
        print("Data inserted/updated successfully into the PostgreSQL database.")
    except Exception as e:
        session.rollback()
        print(f"Failed to insert/update data: {e}")
    finally:
        session.close()


def extract_changelog(issue_data):
    changelog = []
    for history in issue_data.changelog.histories:
        for item in history.items:
            created_timestamp = datetime.strptime(history.created, "%Y-%m-%dT%H:%M:%S.%f%z")
            changelog.append({
                'Changelog ID': history.id,
                'Created': created_timestamp,
                'From': item.fromString,
                'To': item.toString,
            })
    return changelog


if __name__ == '__main__':
    jira, issues = fetch_issues()
    if jira is not None:
        process_issues(jira, issues)
