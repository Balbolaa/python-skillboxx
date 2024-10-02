import os  # Importing os module to execute shell commands from Python.

# Function to count the number of processes for a given username.
def process_count(username: str) -> int:
    # Using os.popen() to run the 'ps' command to list processes of the specified user.
    # 'wc -l' counts the number of lines, i.e., the number of processes.
    data = os.popen(f'ps --user {username} | wc -l').read()
    
    # The output includes a header, so subtracting 1 to get the actual process count.
    return int(data) - 1

# Function to calculate the total memory usage of a process and its children.
def total_memory_usage(root_pid: int) -> float:
    # Get memory usage (in KB) of the root process using 'ps -v'.
    process_mem = float(os.popen(f'ps -v {root_pid}').readlines()[1].split()[8])
    
    # Get memory usage of all child processes using 'ps -v --ppid' (parent process ID).
    data = os.popen(f'ps -v --ppid {root_pid}').readlines()[1:]
    
    # Extract memory usage (8th column) for each child process.
    raw_arr = list(map(str.split, data))
    memory = sum(float(i[8]) for i in raw_arr)
    
    # Return the total memory usage (root process + child processes).
    return process_mem + memory

# Example usage of the process_count function.
print(f'Root process count: {process_count("root")}')

# Example usage of the total_memory_usage function with a specific PID (e.g., 40970).
print(f'Total memory usage of process_pid 40970 (Firefox): {total_memory_usage(40970)}')
