# Networking Node #
# This is client code to receive video frames over UDP

import argparse
import copy
import cv2 as cv, imutils, socket
import numpy as np
import time
import base64
from pupil_apriltags import Detector

UDP_PORT = 7000
BUFF_SIZE = 65536

def start():
    
    args = get_args()
    families = args.families
    nthreads = args.nthreads
    quad_decimate = args.quad_decimate
    quad_sigma = args.quad_sigma
    refine_edges = args.refine_edges
    decode_sharpening = args.decode_sharpening
    debug = args.debug
    at_detector = Detector(
        families=families,
        nthreads=nthreads,
        quad_decimate=quad_decimate,
        quad_sigma=quad_sigma,
        refine_edges=refine_edges,
        decode_sharpening=decode_sharpening,
        debug=debug,
    )

    video_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    video_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    video_sock.bind(('', UDP_PORT))

    while True:
      packet, _ = video_sock.recvfrom(BUFF_SIZE)
      data = base64.b64decode(packet)
      frame = cv.imdecode(np.frombuffer(data, dtype=np.uint8), cv.IMREAD_COLOR)
      debug_image = copy.deepcopy(frame)
      debug_image = cv.rotate(debug_image, cv.ROTATE_90_COUNTERCLOCKWISE)
      image = cv.cvtColor(debug_image, cv.COLOR_BGR2GRAY)
      tags = at_detector.detect(
          image,
          estimate_tag_pose=False,
          camera_params=None,
          tag_size=None,
      )
      key = cv.waitKey(1)
      if key == 27: 
          break
      debug_image = draw_tags(debug_image, tags)
      cv.namedWindow("Robot Feed", cv.WINDOW_NORMAL)
      cv.resizeWindow("Robot Feed", 1280, 720)
      cv.imshow("Robot Feed", debug_image)
      key = cv.waitKey(1) & 0xFF
      if key == ord('q'):
            break

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--families", type=str, default='tag36h11')
    parser.add_argument("--nthreads", type=int, default=1)
    parser.add_argument("--quad_decimate", type=float, default=2.0)
    parser.add_argument("--quad_sigma", type=float, default=0.0)
    parser.add_argument("--refine_edges", type=int, default=1)
    parser.add_argument("--decode_sharpening", type=float, default=0.25)
    parser.add_argument("--debug", type=int, default=0)
    args = parser.parse_args()
    return args

def draw_tags(
    image,
    tags,
):
    for tag in tags:
        tag_family = tag.tag_family
        tag_id = tag.tag_id
        center = tag.center
        corners = tag.corners
        center = (int(center[0]), int(center[1]))
        corner_01 = (int(corners[0][0]), int(corners[0][1]))
        corner_02 = (int(corners[1][0]), int(corners[1][1]))
        corner_03 = (int(corners[2][0]), int(corners[2][1]))
        corner_04 = (int(corners[3][0]), int(corners[3][1]))
        cv.circle(image, (center[0], center[1]), 5, (0, 0, 255), 2)
        cv.line(image, (corner_01[0], corner_01[1]),
                (corner_02[0], corner_02[1]), (255, 0, 0), 2)
        cv.line(image, (corner_02[0], corner_02[1]),
                (corner_03[0], corner_03[1]), (255, 0, 0), 2)
        cv.line(image, (corner_03[0], corner_03[1]),
                (corner_04[0], corner_04[1]), (0, 255, 0), 2)
        cv.line(image, (corner_04[0], corner_04[1]),
                (corner_01[0], corner_01[1]), (0, 255, 0), 2)
        cv.putText(image, str(tag_id), (center[0] - 10, center[1] - 10),
                   cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv.LINE_AA)
        

    return image

if __name__ == "__main__":
  start()
  cv.destroyAllWindows()