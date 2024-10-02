from threading import Semaphore, Thread
import time

# Initialize the semaphore
sem: Semaphore = Semaphore()

# Global flag to stop threads
stop_thread = False

def fun1():
    """Thread function to print '1'."""
    while True:
        global stop_thread
        if stop_thread:
            break
        sem.acquire()  # Acquire semaphore (lock)
        print(1)       # Critical section
        sem.release()  # Release semaphore (unlock)
        time.sleep(0.25)  # Wait before next iteration

def fun2():
    """Thread function to print '2'."""
    while True:
        global stop_thread
        if stop_thread:
            break
        sem.acquire()  # Acquire semaphore (lock)
        print(2)       # Critical section
        sem.release()  # Release semaphore (unlock)
        time.sleep(0.25)  # Wait before next iteration

# Create and start the threads
t1: Thread = Thread(target=fun1)
t2: Thread = Thread(target=fun2)

try:
    t1.start()  # Start thread 1
    t2.start()  # Start thread 2

    # Main thread runs indefinitely, unless interrupted
    while True:
        1 + 1  # Dummy operation to keep the main thread alive

except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C)
    print('\nReceived keyboard interrupt, quitting threads.')
    stop_thread = True  # Set the flag to stop the threads

    t1.join()  # Wait for thread 1 to finish
    print('Thread 1 stopped!')
    
    t2.join()  # Wait for thread 2 to finish
    print('Thread 2 stopped!')

    # Exit the program
    exit(1)
