# Main Node

import threading
import subprocess

stop_threads = False

def stop_robot():
    stop_threads = True
    networking_thread.join()
    serial_thread.join()
    print("Threads stopped.")

def run_script(script_name):
    subprocess.run(["python", script_name])

def networking_thread_func():
    global stop_threads
    while not stop_threads:
        run_script("networking_robot.py")

def serial_thread_func():
    global stop_threads
    while not stop_threads:
        run_script("serial_robot.py")

if __name__ == "__main__":
    networking_thread = threading.Thread(target=networking_thread_func)
    networking_thread.start()

    serial_thread = threading.Thread(target=serial_thread_func)
    serial_thread.start()

    input("Press Enter to stop threads...\n")

    stop_threads = True

    networking_thread.join()
    serial_thread.join()

    print("Threads stopped.")