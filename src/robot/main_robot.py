# Main Node

import threading
import subprocess

keep_running = True

def run_script(script_name):
    global keep_running
    while keep_running:
        subprocess.call(["python", script_name])

def stop_all_threads():
    global keep_running
    keep_running = False

if __name__ == "__main__":
    scripts = ["serial.py", "networking_robot.py"]

    threads = []
    for script in scripts:
        thread = threading.Thread(target=run_script, args=(script,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()