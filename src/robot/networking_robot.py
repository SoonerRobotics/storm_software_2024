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
    host_name = socket.gethostname()
    socket_address = ('',UDP_PORT)
    video_sock.bind(socket_address)
    video_stream(video_sock)
    
def video_stream(sock):

    cap = cv2.VideoCamera(0)
    fps,st,frames,cnt = (0,0,20,0)

    while True:
        msg,client_addr = sock.recvfrom(BUFF_SIZE)
        WIDTH = 400
        while (cap.isOpened()):
            _,frame = cap.read()
            frame = imutils.resize(frame,width=WIDTH)
            encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
            message = base64.b64encode(buffer)
            sock.sendto(message, client_addr)
            frame = cv2.putText(frame,'FPS: ', + str(fps), (10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                sock.close()
                break
            if cnt == frames:
                try:
                    fps = round(frames/(time.time()-st))
                    st = time.time()
                    cnt = 0
                except:
                    pass
            cnt+=1

if __name__ == "__main__":
    start()
