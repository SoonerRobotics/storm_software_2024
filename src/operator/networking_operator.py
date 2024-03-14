# Networking Node #
# This is client code to receive video frames over UDP

import cv2, imutils, socket
import numpy as np
import time
import base64

UDP_IP = '192.168.1.130'
UDP_PORT = 7000
BUFF_SIZE = 65536

def start():
	
    video_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    video_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    socket_address = (UDP_IP,UDP_PORT)
    video_sock.bind(socket_address)   

    while True:
          packet,_ = video_sock.recvfrom(BUFF_SIZE)
          data = base64.b64decode(packet,' /')
          parse = np.fromstring(data,dtype=np.uint8)
          frame = cv2.imdecode(parse,1)
          cv2.imshow("sender", frame)
          key = cv2.waitKey(1) & 0xFF
          if key == ord('q'):
                video_sock.close()
                break

if __name__ == "__main__":
	start()