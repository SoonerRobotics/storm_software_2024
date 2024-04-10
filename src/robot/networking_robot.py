# Networking Node
# Written by Braden White

import socket
import cv2
import base64

UDP_IP = "192.168.1.130"
BUFF_SIZE = 65536
UDP_PORT = 7000

def start():
    
    video_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    video_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    video_sock.bind(('', UDP_PORT))
    vid = cv2.VideoCapture(0)
    vid.set(3,640)
    vid.set(4,480)
    if not vid.isOpened():
        print("Error: Failed to open camera")
        return

    print("Starting video capture.")
    while True:
        ret, frame = vid.read()
        if not ret:
            print("Error: Failed to read frame")
            break
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        encoded, buff = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        message = base64.b64encode(buff)
        video_sock.sendto(message, (UDP_IP, UDP_PORT))

    vid.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start()

