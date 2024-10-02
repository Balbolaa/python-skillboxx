import threading
from threading import Semaphore
import time
from datetime import datetime, timedelta
import requests
import logging

# Constants
URL = 'http://127.0.0.1:5000/timestamp/'
sem = Semaphore()  # Semaphore to control thread access
STOP_LOGGING = False

# Set up logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, filename=f'{__name__}.log', filemode='w')

def log_data():
    """Logs timestamp and corresponding date by sending requests to a server."""
    start_time = datetime.now()
    
    while True:
        # Stop after 20 seconds
        if datetime.now() - start_time > timedelta(seconds=20):
            break

        # Acquire the semaphore to ensure only one thread logs at a time
        with sem:
            global URL
            # Get current timestamp
            timestamp = datetime.timestamp(datetime.now())
            try:
                # Fetch corresponding date from the server
                date = requests.get(URL + str(timestamp)).text
                # Log timestamp and date
                logger.info(f'Timestamp: {timestamp:.3f}\tDate: {date}')
            except requests.RequestException as e:
                # Log in case of a request failure
                logger.error(f'Failed to fetch data for timestamp {timestamp}: {e}')

        # Pause for 1 second before next request
        time.sleep(1)

def main():
    """Main function to create and start threads."""
    # Create 10 threads that will log data
    threads = [threading.Thread(target=log_data) for _ in range(10)]
    
    # Start each thread with a 1-second delay between them
    for thread in threads:
        thread.start()
        time.sleep(1)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
