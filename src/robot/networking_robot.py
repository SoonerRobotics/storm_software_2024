# Networking Node
# Written by Braden White

import socket
import cv2
import imutils
import base64
import time
import threading
import logging
import queue

UDP_IP = "127.0.0.1"
VIDEO_PORT = 5005
COMMAND_PORT = 5006
BUFF_SIZE = 65536

def start():

    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(message)s')

    video_sock = socket.socket(socket.AF_INIT, socket.SOCK_DGRAM)
    video_sock.bind((UDP_IP, VIDEO_PORT))
    video_thread = threading.Thread(target=video_stream(), args=video_sock)
    video_thread.start()

    command_sock = socket.socket(socket.AF_INIT, socket.SOCK_DGRAM)
    command_sock.bind((UDP_IP, VIDEO_PORT))
    command_queue = queue.Queue()
    command_thread = threading.Thread(target=command_stream, args=(command_sock,queue))
    command_thread.start()

    
def video_stream(sock):

    logging.debug(f'[Video Stream] Starting')
    cap = cv2.VideoCamera(0)
    fps,st,frames,cnt = (0,0,20,0)

    while True:
        msg,client_addr = sock.recvfrom(BUFF_SIZE)
        WIDTH=400
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

def command_stream(command_sock, queue):
    # TODO: Figure out what commands I am accepting
    logging.debug(f'[Command Stream] Starting')

    while True:
        data = command_sock.recv(2048)
        if not data:
            break
        queue.put(data)


if __name__ == "__main__":
    start()
