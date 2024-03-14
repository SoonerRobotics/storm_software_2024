import socket 
import pygame
import sys
import glob
import struct

LEFT = 0
RIGHT = 1

SERVER_IP = "192.168.1.126"
SERVER_PORT = 8000

def start():

    pygame.init()
    pygame.joystick.init()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))

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
                    packet = LEFT.to_bytes(1,'little')
                    packet = packet + bytearray(struct.pack("<f",left_y))
                    server_socket.sendto(packet, (SERVER_IP, SERVER_PORT))
                elif event.axis == 2:
                    right_y = -controller.get_axis(3)
                    packet = RIGHT.to_bytes(1,'little')
                    packet = packet + bytearray(struct.pack("<f",right_y))
                    server_socket.sendto(packet, (SERVER_IP, SERVER_PORT))
    
    pygame.quit()

if __name__ == "__main__":
    start()
