import requests
from sqlalchemy import create_engine, Column, Integer, Float, String, UniqueConstraint, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

PAT = 'f6Eq6u9WBohk7Cei-7SaGryYnYRscWk3f7j7seXk4ou6ftmqtWaQLYcV6Cq5KX8B'
URL = f'http://localhost:8080/metrics/{PAT}/metrics?pretty=true'

# Define the database connection
engine = create_engine('postgresql://postgres:postgres@192.168.68.100/postgres')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class MonitoringData(Base):
    __tablename__ = 'monitoring_data'
    __table_args__ = (
        UniqueConstraint('time', 'key', name='uq_time_key'),
    )

    time = Column(DateTime, primary_key=True)
    key = Column(String)
    value = Column(Float)


class MonitoringDataExtractor:
    def __init__(self, json_data):
        self.json_data = json_data

    def extract_parameter(self, key, metric_type):
        metric_data = self.json_data.get(metric_type, {})
        if key in metric_data:
            value = metric_data[key]
            if isinstance(value, dict):
                value = value.get('mean') or value.get('value')
            if value is not None:
                monitoring_data = MonitoringData(time=datetime.now(), key=key, value=value)
                session.add(monitoring_data)

    def extract_all(self):
        metrics = {
            'gauges': [
                'jenkins.executor.count.value',
                'jenkins.executor.free.value',
                'jenkins.queue.size.value',
                'jenkins.queue.pending.value',
                'system.cpu.load',
                'vm.cpu.load',
                'vm.memory.heap.usage',
                'vm.memory.non-heap.usage',
                'jenkins.node.online.value',
                'jenkins.node.offline.value',
                'jenkins.plugin.active.value',
                'jenkins.plugin.inactive.value',
                'jenkins.plugin.failed.value',
                'jenkins.plugin.withUpdate.value'
            ],
            'timers': [
                'jenkins.job.building.duration',
                'jenkins.job.total.duration',
                'jenkins.job.waiting.duration',
                'jenkins.job.execution.time',
                'jenkins.job.queuing.duration',
                'jenkins.node.builds'
            ]
        }

        for metric_type, keys in metrics.items():
            for key in keys:
                self.extract_parameter(key, metric_type)

        # Commit the changes to the database
        session.commit()
        print('Monitoring data saved to the database')


# Make GET request
response = requests.get(URL)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Read the JSON response
    json_data = response.json()

    # Create an instance of the monitoring data extractor
    data_extractor = MonitoringDataExtractor(json_data)

    # Extract and save the monitoring data to the database
    data_extractor.extract_all()
else:
    print('Error:', response.status_code)
