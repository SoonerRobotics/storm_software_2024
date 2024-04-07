# Node to drive robot manually without operator computer #

import pygame
import serial
import sys
import glob
import struct
import math

MOTORS = 0
ARM = 1

def map(v):
	if v < -1:
		v = -1
	if v > 1:
		v = 1
	return (v - (-1)) * (255 - (-255)) // (1 - (-1)) + (-255)

def start():

    pygame.init()
    pygame.joystick.init()

    '''
    list_of_ports = serial_ports()
    print("Please choose a connection port:")
    port_range = range(len(list_of_ports))
    for index, port in zip(port_range, list_of_ports):
        print(index, port)
    selection = input('Enter option number:')
    if selection == 'q' or selection == 'Q':
        sys.exit(0)
    selected_port = list_of_ports[int(selection)-1]
    pico = serial.Serial(port=selected_port, baudrate=112500)
    '''

    num_joysticks = pygame.joystick.get_count()
    if num_joysticks > 0:
        controller = pygame.joystick.Joystick(0)
        controller.init()
        print("Controller connected:", controller.get_name())
    else:
        print("No controller detected.")

    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == 1:
                    left_y = -controller.get_axis(1)
                    left_x = controller.get_axis(0)
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
                    print(rightOut, leftOut)
                    packet = MOTORS.to_bytes(1,'little') 
                    packet = packet + bytearray(struct.pack("<f",rawRight)) + bytearray(struct.pack("<f",rawLeft))
                    # pico.write(packet)
                elif event.axis == 3:
                    right_y = -controller.get_axis(3)
                    right_x = controller.get_axis(2)
                    packet = ARM.to_bytes(1,'little')
                    packet = packet + bytearray(struct.pack("<f",right_x)) + bytearray(struct.pack("<f",right_y))
                    # pico.write(packet)

    pygame.quit()

'''
def serial_ports():

    ports = ["-----"]
    if sys.platform.startswith('win'):
        ports += ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports += glob.glob('/dev/tty[A-za-a]*')
    elif sys.platform.startswith('darwin'):
        ports += glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
'''

if __name__ == "__main__":
    start()
