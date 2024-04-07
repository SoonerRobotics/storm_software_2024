# Networking Node #
# This is client code to receive video frames over UDP

import cv2, imutils, socket
import numpy as np
import time
import base64

UDP_PORT = 7000
BUFF_SIZE = 65536

def start():
    video_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    video_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    video_sock.bind(('', UDP_PORT))
    while True:
      packet, _ = video_sock.recvfrom(BUFF_SIZE)
      data = base64.b64decode(packet)
      frame = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)
      frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
      cv2.namedWindow("Robot Feed", cv2.WINDOW_NORMAL)
      cv2.resizeWindow("Robot Feed", 1280, 720)
      cv2.imshow("Robot Feed", frame)
      key = cv2.waitKey(1) & 0xFF
      if key == ord('q'):
            break

if __name__ == "__main__":
  start()
  cv2.destroyAllWindows()