import socket
import serial
import sys
import glob

SERVER_IP = "192.168.1.130"
SERVER_PORT = 8000

def start():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', SERVER_PORT))
    list_of_ports = serial_ports()
    print("Please choose a connection port:")
    port_range = range(len(list_of_ports))
    for index, port in zip(port_range, list_of_ports):
        print(index, port)
    selection = input('Enter option number:')
    if selection == 'q' or selection == 'Q':
        sys.exit(0)
    selected_port = list_of_ports[int(selection)-1]
    pico = serial.Serial(port=selected_port, baudrate=115200)
    while True:
        data, address = server_socket.recvfrom(1024)
        print("Received: ", data)
        pico.write(data)

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