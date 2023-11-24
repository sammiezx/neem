import time
import subprocess

# Define the path to your graph generation script
graph_script_path = "/home/samir/Desktop/rudraAnalytics/NEEM_PROD/crons/drop_analytics.py"

while True:
    # Run the graph generation script using subprocess
    subprocess.run(["python", graph_script_path], shell=True)

    # Sleep for 1 hour (3600 seconds)
    time.sleep(3600)
