# Main Node

import threading
import subprocess
import sys
import os

def run_script(script_name):
    subprocess.run(["python", script_name])

def networking_thread_func():
    run_script("networking_operator.py")

def control_thread_func():
    run_script("control_operator.py")

if __name__ == "__main__":
    
    networking_thread = threading.Thread(target=networking_thread_func)
    networking_thread.start()

    control_thread = threading.Thread(target=control_thread_func)
    control_thread.start()
