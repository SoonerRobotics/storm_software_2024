import socket 
import pygame
import sys
import glob
import struct

ARM = 1
MOTORS = 0

def start():

    pygame.init()
    pygame.joystick.init()

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
                    right_motor = right_stick
                    left_motor = controller.get_axis(0)
                    packet = MOTORS.to_bytes(1,'little')
                    packet = packet + bytearray(struct.pack("<f",right_motor)) + bytearray(struct.pack("<f",left_motor))
                    print(left_motor, right_motor)
                elif event.axis == 2:
                    right_y = -controller.get_axis(3)
                    right_x = controller.get_axis(2)
                    packet = ARM.to_bytes(1,'little')
                    packet = packet + bytearray(struct.pack("<f",right_x)) + bytearray(struct.pack("<f",right_y))
                    print(right_x, right_y)
                elif event.axis == 4:
                    left_trig = controller.get_axis(4)
                    left_trig = -((left_trig + 1) / 2)
                    right_motor = left_trig
                    left_motor = left_trig
                    print(left_motor, right_motor)
                elif event.axis == 5:
                    right_trig = controller.get_axis(5)
                    right_trig = (right_trig + 1) / 2
                    right_motor = right_trig
                    left_motor = right_trig
                    print(left_motor, right_motor)
    
    pygame.quit()

if __name__ == "__main__":
    start()
