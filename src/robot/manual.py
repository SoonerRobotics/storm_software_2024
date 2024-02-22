# Node to 

import pygame
import serial
import sys
import glob

def start():

    pygame.init()
    pygame.joystick.init()

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
                    print(left_y)
                    pico.write(f'L{left_y}\n'.encode())
                elif event.axis == 3:
                    right_y = -controller.get_axis(3)
                    print(right_y)
                    pico.write(f'R{right_y}\n'.encode())

    pygame.quit()

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


if __name__ == "__main__":
    start()
