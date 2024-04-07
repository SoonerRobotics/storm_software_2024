import socket 
import pygame
import sys
import glob
import struct
import math

MOTORS = 0
ARM = 1

SERVER_IP = "192.168.1.126"
SERVER_PORT = 8000

def map(v):
	if v < -1:
		v = -1
	if v > 1:
		v = 1
	return (v - (-1)) * (255 - (-255)) // (1 - (-1)) + (-255)

def start():

    pygame.init()
    pygame.joystick.init()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', SERVER_PORT))

    num_joysticks = pygame.joystick.get_count()
    if num_joysticks > 0:
        controller = pygame.joystick.Joystick(0)
        controller.init()
        print("Controller connected:", controller.get_name())
    else:
        print("No controller detected")

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == 1:
                    left_y = -controller.get_axis(1)
                    left_x = controller.get_axis(0)
                    packet = MOTORS.to_bytes(1,'little')
                    z = math.sqrt(left_x * left_x + left_y * left_y)
                    rad = math.acos(math.fabs(left_x)/z)
                    angle = rad * 180 / math.pi
                    tcoeff = -1 + (angle/90) * 2
                    turn = tcoeff * math.fabs(math.fabs(left_y) - math.fabs(left_x))
                    turn = round(turn*100,0) / 100
                    mov = max(math.fabs(left_y), math.fabs(left_x))
                    if (left_x >= 0 and left_y>=0) or (left_x < 0 and left_y < 0):
                        rawLeft = mov
                        rawRight = turn
                    else:
                        rawRight = mov
                        rawLeft = turn
                    if left_y < 0:
                        rawLeft = 0 - rawLeft
                        rawRight = 0 - rawRight
                    rightOut = map(rawRight)
                    leftOut = map(rawLeft) 
                    packet = packet + bytearray(struct.pack("<f",rightOut)) + bytearray(struct.pack("<f",leftOut))
                    server_socket.sendto(packet, (SERVER_IP, SERVER_PORT))
                elif event.axis == 2:
                    right_y = -controller.get_axis(3)
                    right_x = controller.get_axis(2)
                    packet = ARM.to_bytes(1,'little')
                    packet = packet + bytearray(struct.pack("<f",right_x)) + bytearray(struct.pack("<f",right_y))
                    server_socket.sendto(packet, (SERVER_IP, SERVER_PORT))
    
    pygame.quit()

if __name__ == "__main__":
    start()
