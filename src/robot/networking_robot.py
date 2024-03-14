# Networking Node
# Written by Braden White

import socket
import cv2
import imutils
import base64
import time

UDP_IP = "raspberrypi"
UDP_PORT = 9999
BUFF_SIZE = 65536

def start():

    video_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    video_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    socket_address = ('',UDP_PORT)
    video_sock.bind(socket_address)

    while True:
        vid = cv2.VideoCapture(0)
        ret, frame = vid.read()
        vid.release()
        frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        encoded, buff = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
        message = base64.b64encode(buff)
        video_sock.sendto(message,socket_address)
    
if __name__ == "__main__":
    start()
