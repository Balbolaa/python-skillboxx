# Import necessary libraries
import flask
import subprocess  # Used for running shell commands
import os  # For interacting with the operating system (like killing processes)
import signal  # To send signals to processes (like SIGINT to stop them)
import time  # To add delays between operations

# Importing Flask's current_app
from flask import current_app

# Initialize a Flask application
app = flask.Flask(__name__)

# Define a Flask endpoint called 'test'
@app.endpoint('test')
def test_endpoint():
    # When the /test endpoint is hit, this message will be returned
    return 'Test endpoint was called!'

# Function to start the Flask application
def start():
    # Run the command `lsof -i:5000` to check if any process is using port 5000
    out = subprocess.getoutput('lsof -i:5000')
    
    # If there is output, it means something is running on port 5000
    if out != '':
        pid = get_pid(out)  # Get the PID (Process ID) of the process using port 5000
        os.kill(pid, signal.SIGINT)  # Kill the process by sending a SIGINT signal
        time.sleep(1)  # Pause for 1 second to allow time for the process to stop

    # After ensuring nothing is running on port 5000, start the Flask application
    app.run()

# Helper function to extract the PID from the `lsof` command output
def get_pid(s: str) -> int:
    # `lsof` output is split into lines, then we extract the second column (the PID) from the first result
    return int(list(i.split()[1] for i in s.split('\n'))[1:][0])

# If the script is run directly (not imported), call the start() function
if __name__ == '__main__':
    start()
