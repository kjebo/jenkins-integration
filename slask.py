import requests
import json

PAT ='f6Eq6u9WBohk7Cei-7SaGryYnYRscWk3f7j7seXk4ou6ftmqtWaQLYcV6Cq5KX8B'

url = f'http://localhost:8080/metrics/{PAT}/metrics?pretty=true'

# Make GET request
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Read the JSON response
    json_data = response.json()
    #Monitoring Parameter: Number of executors in the Jenkins master (e.g., 4 executors)
    jenkins_executor_count_value = json_data['gauges']['jenkins.executor.count.value']
    #Monitoring Parameter: Number of items in the Jenkins build queue (e.g., 10 items)
    jenkins_queue_size = json_data['gauges']['jenkins.queue.size']
    #Monitoring Parameter: Duration of a job while it is being built (e.g., 2 minutes)
    jenkins_job_building_duration = json_data['timers']['jenkins.job.building.duration']
    # Monitoring Parameter: Total duration of a job, including both building and waiting time (e.g., 5 minutes)
    jenkins_job_total_duration = json_data['timers']['jenkins.job.total.duration']
    #Monitoring Parameter: Duration of a job while it is waiting in the build queue (e.g., 3 minutes)
    jenkins_job_waiting_duration = json_data['timers']['jenkins.job.waiting.duration']
    #Monitoring Parameter: Number of online nodes in the Jenkins cluster (e.g., 6 nodes)
    jenkins_node_online_value = json_data['gauges']['jenkins.node.online.value'] 
    #Monitoring Parameter: Number of offline nodes in the Jenkins cluster (e.g., 2 nodes)
    jenkins_node_offline_value = json_data['gauges']['jenkins.node.offline'] 
    #Monitoring Parameter: Number of active plugins in Jenkins (e.g., 50 plugins)
    jenkins_plugin_active = json_data['gauges']['jenkins.plugin.active']
    #Monitoring Parameter: Number of inactive plugins in Jenkins (e.g., 50 plugins)
    jenkins_plugin_inactive = json_data['gauges']['jenkins.plugin.inactive'] 
    #Monitoring Parameter: Number of failed plugins in Jenkins (e.g., 5 plugins)
    jenkins_plugin_failed = json_data['gauges']['jenkins.plugin.failed']
    #Monitoring Parameter: Number of available plugin updates(e.g., 3 updates)
    jenkins_plugin_withUpdate = json_data['gauges']['jenkins.plugin.withUpdate'] 
    #Monitoring Parameter: CPU load for the jenkins controller
    system_cpu_load = ['gauges']['system.cpu.load']
    #Monitoring Parameter: CPU load for the jenkins JVM
    vm_cpu_load = ['gauges']['vm.cpu.load']
    #Monitoring Parameter: The memory used for Jenkins JVM
    vm_memory_heap_usage = ['gauges']['vm.memory.heap.usage']
    #Monitoring Parameter: Free memory  for Jenkins JVM
    vvm_memory_non_heap_usage = ['gauges']['vm.memory.non-heap.usage']






    print(jenkins_executor_count_value)
    # Process the JSON data as needed
    # For example, print the JSON data
else:
    print('Error:', response.status_code)
