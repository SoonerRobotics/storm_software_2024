# Main Node

import threading
import subprocess
from pupil_apriltags import Detector

def run_script(script_name):
    subprocess.run(["python", script_name])

def networking_thread_func():
    run_script("networking_robot.py")

def control_thread_func():
    run_script("control_robot.py")

if __name__ == "__main__":

    networking_thread = threading.Thread(target=networking_thread_func)
    networking_thread.start()

    control_thread = threading.Thread(target=control_thread_func)
    control_thread.start()