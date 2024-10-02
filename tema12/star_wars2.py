from multiprocessing.pool import ThreadPool, Pool  # Importing ThreadPool and Pool for multithreading and multiprocessing.
import datetime  # Used for tracking the time taken for tasks.
import sqlite3  # Module to interact with SQLite databases.
import threading  # For using thread synchronization (Locks).
import requests  # To make HTTP requests to the API.
import time  # Used for adding delays or measuring execution time.

# Base URL for accessing the Star Wars API (SWAPI) people endpoint.
BASE_URL = 'https://www.swapi.tech/api/people/'

# Name of the SQLite database file.
DATABASE = 'sqlite3.db'

# Function to initialize the SQLite database.
# If the 'People' table exists, it will clear the data; otherwise, it creates the table.
def init_db():
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        try:
            # Trying to clear the table if it exists.
            cur.execute('DELETE FROM People')
            con.commit()
        except sqlite3.OperationalError:
            # If the table doesn't exist, create it with three columns: name, gender, and birth year.
            cur.execute('CREATE TABLE People (id INTEGER PRIMARY KEY, name VARCHAR(255), '
                        'gender VARCHAR(255), birth_year VARCHAR(255))')

# Create a threading lock to ensure safe access to the database by multiple threads.
lock = threading.Lock()

# Function to fetch data from the SWAPI for a specific character by ID, then insert it into the database.
def get_and_add_person_by_request(i):
    # Make a GET request to the API and fetch data for a person with the given ID (i).
    data = dict(requests.get(BASE_URL + str(i)).json())
    
    # Ensure that the result and properties fields exist in the response data.
    if 'result' in data and 'properties' in data['result']:
        data = data['result']['properties']
    
    # Acquire a lock before modifying the shared resource (the database).
    with lock:
        with sqlite3.connect(DATABASE) as con:
            cur = con.cursor()
            # If the name field exists in the data, insert the person's details into the database.
            if 'name' in data:
                cur.execute(f'INSERT INTO People VALUES(\'{i}\', \'{data["name"]}\', \'{data["gender"]}\', \'{data["birth_year"]}\')')
                con.commit()  # Commit the transaction to save the data.

# Function to process data using a multiprocessing pool with 20 processes.
def pool_adding():
    print('Pool started!')
    start = datetime.datetime.now()  # Mark the start time.
    
    # Use a multiprocessing Pool to concurrently process 20 people (IDs 1 to 20).
    with Pool(processes=20) as pool:
        it = pool.map(get_and_add_person_by_request, range(1, 21))
    
    # Print the total time taken by the multiprocessing pool.
    print(f'Pool time: {datetime.datetime.now() - start}')

# Function to process data using a thread pool with 20 threads.
def thread_pool_adding():
    print('Thread pool started!')
    start = datetime.datetime.now()  # Mark the start time.
    
    # Use a ThreadPool to concurrently process 20 people (IDs 1 to 20).
    with ThreadPool(processes=20) as thread_pool:
        it = thread_pool.map(get_and_add_person_by_request, range(1, 21))
    
    # Print the total time taken by the thread pool.
    print(f'Thread pool time: {datetime.datetime.now() - start}')

# Main function to initialize the database and run both the thread pool and multiprocessing pool functions.
def main():
    init_db()  # Initialize (or reset) the database.
    
    # First, run the thread pool function.
    thread_pool_adding()
    
    init_db()  # Reset the database again for the multiprocessing pool test.
    
    # Then, run the multiprocessing pool function.
    pool_adding()

# Check if this script is being run directly (not imported as a module).
if __name__ == '__main__':
    main()  # If run directly, execute the main function.
