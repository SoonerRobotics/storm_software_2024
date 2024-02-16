# Serial Node

import serial
import socket
import threading

BAUD_RATE = 115200
PORT = '/dev/ttyUSB0'


def start():
    ser = serial.Serial(PORT, BAUD_RATE)
    

if __name__ == "__main__":
    start()