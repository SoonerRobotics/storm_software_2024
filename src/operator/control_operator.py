import socket 
import pygame
import struct
import time

MOTORS = 0
ARM = 1
MAGNET_ON = 2
MAGNET_OFF = 3

SERVER_IP = "10.10.1.36"
SERVER_PORT = 8000

SPEED_PERCENTAGE = 0.75
TURN_PERCENTAGE = 0.95

def start():

    pygame.init()
    pygame.joystick.init()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', SERVER_PORT))
    magnet_press = 0

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
                    if (abs(controller.get_axis(0)) > 0.25):
                        right_motor = (-controller.get_axis(0) * 255) * TURN_PERCENTAGE
                        left_motor = (controller.get_axis(0) * 255) * TURN_PERCENTAGE
                        packet = MOTORS.to_bytes(1,'little')
                        packet = packet + bytearray(struct.pack("<f",right_motor)) + bytearray(struct.pack("<f",left_motor))
                        server_socket.sendto(packet, (SERVER_IP, SERVER_PORT))
                    else:
                        packet = MOTORS.to_bytes(1, "little")
                        packet = packet + bytearray(struct.pack("<f",0.0)) + bytearray(struct.pack("<f", 0.0))
                        server_socket.sendto(packet, (SERVER_IP, SERVER_PORT))
                elif event.axis == 2:
                    right_y = (-controller.get_axis(3)) * 255
                    right_x = controller.get_axis(2) * 255
                    packet = ARM.to_bytes(1,'little')
                    packet = packet + bytearray(struct.pack("<f",right_x)) + bytearray(struct.pack("<f",right_y))
                    server_socket.sendto(packet, (SERVER_IP, SERVER_PORT))
                elif event.axis == 4:
                    left_trig = controller.get_axis(4)
                    left_trig = -((left_trig + 1) / 2)
                    right_motor = (left_trig * 255) * SPEED_PERCENTAGE
                    left_motor = (left_trig * 255) * SPEED_PERCENTAGE
                    packet = MOTORS.to_bytes(1,'little')
                    packet = packet + bytearray(struct.pack("<f",right_motor)) + bytearray(struct.pack("<f",left_motor))
                    server_socket.sendto(packet, (SERVER_IP, SERVER_PORT))
                elif event.axis == 5:
                    right_trig = controller.get_axis(5)
                    right_trig = (right_trig + 1) / 2
                    right_motor = (right_trig * 255) * SPEED_PERCENTAGE
                    left_motor = (right_trig * 255) * SPEED_PERCENTAGE
                    packet = MOTORS.to_bytes(1,"little")
                    packet = packet + bytearray(struct.pack("<f",right_motor)) + bytearray(struct.pack("<f",left_motor))
                    server_socket.sendto(packet, (SERVER_IP, SERVER_PORT))
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    if magnet_press == 0:
                        packet = MAGNET_ON.to_bytes(1,"little")
                        packet = packet + bytearray(struct.pack("<f",0)) + bytearray(struct.pack("<f",0))
                        server_socket.sendto(packet, (SERVER_IP, SERVER_PORT))
                        magnet_press = magnet_press + 1
                    elif magnet_press == 1:
                        packet = MAGNET_OFF.to_bytes(1,"little")
                        packet = packet + bytearray(struct.pack("<f",0.0)) + bytearray(struct.pack("<f",0.0))
                        server_socket.sendto(packet, (SERVER_IP, SERVER_PORT))
                        magnet_press = 0
    
    pygame.quit()

if __name__ == "__main__":

    start()
