# Networking Node #
# This is client code to receive video frames over UDP

import cv2, imutils, socket
import numpy as np
import time
import base64

UDP_IP = '192.168.1.130'
UDP_PORT = 9999
BUFF_SIZE = 65536

def start():
	
    operator_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    operator_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    host_name = socket.gethostname()
    socket_address = ('', UDP_PORT)
    operator_socket.bind(socket_address)
    fps,st,frames_to_count,cnt = (0,0,20,0)
    while True:
          packet,_ = operator_socket.recvfrom(BUFF_SIZE)
          data = base64.b64decode(packet,' /')
          npdata = np.fromstring(data, dtype=np.uint8)
          frame = cv2.imdecode(npdata,1)
          frame = cv2.putText(frame, 'FPS: ' + str(fps), (10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)
          cv2.imshow(frame)
          key = cv2.waitKey(1) & 0xFF
          if key == ord('q'):
                operator_socket.close()
                break
          if cnt == frames_to_count:
                try:
                      fps = round(frames_to_count/(time.time()-st))
                      st = time.time()
                      cnt = 0
                except:
                      pass
          cnt += 1      

if __name__ == "__main__":
	start()