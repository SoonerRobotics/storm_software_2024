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
                    right_stick = -controller.get_axis(0)
                    right_motor = right_stick * 255
                    left_motor = controller.get_axis(0) * 255
                    packet = MOTORS.to_bytes(1,'little')
                    packet = packet + bytearray(struct.pack("<f",right_motor)) + bytearray(struct.pack("<f",left_motor))
                    server_socket.sendto(packet, (SERVER_IP, SERVER_PORT))
                elif event.axis == 2:
                    right_y = -controller.get_axis(3)
                    right_x = controller.get_axis(2)
                    packet = ARM.to_bytes(1,'little')
                    packet = packet + bytearray(struct.pack("<f",right_x)) + bytearray(struct.pack("<f",right_y))
                    server_socket.sendto(packet, (SERVER_IP, SERVER_PORT))
                elif event.axis == 4:
                    left_trig = controller.get_axis(4)
                    left_trig = -((left_trig + 1) / 2)
                    right_motor = left_trig * 255
                    left_motor = left_trig * 255
                    packet = MOTORS.to_bytes(1,'little')
                    packet = packet + bytearray(struct.pack("<f",right_motor)) + bytearray(struct.pack("<f",left_motor))
                    server_socket.sendto(packet, (SERVER_IP, SERVER_PORT))
                elif event.axis == 5:
                    right_trig = controller.get_axis(5)
                    right_trig = (right_trig + 1) / 2
                    right_motor = right_trig * 255
                    left_motor = right_trig * 255
                    packet = MOTORS.to_bytes(1,"little")
                    packet = packet + bytearray(struct.pack("<f",right_motor)) + bytearray(struct.pack("<f",left_motor))
                    server_socket.sendto(packet, (SERVER_IP, SERVER_PORT))

    
    pygame.quit()

if __name__ == "__main__":
    start()
