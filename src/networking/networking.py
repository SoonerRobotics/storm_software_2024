import pygame
import sys
from pygame.locals import *

pygame.init()
pygame.joystick.init()

num_joysticks = pygame.joystick.get_count()

if num_joysticks > 0:
    # TODO: does not support multiple joysticks, make sure Joystick instance not created each time joystick is plugged back in
    controller = pygame.joystick.Joystick(0) 
    controller.init()
    print("Controller connected:", controller.get_name())
else:
    print("No controller detected.")


running = True
while(running):
    for event in pygame.event.get():
        # todo: may be unnecessary, provides way to shut down pygame
        if event.type == pygame.QUIT: 
            running = False
            pygame.quit()
        # button press down
        if event.type == JOYBUTTONDOWN:
            print("button pressed down")
            print(event)
            print("BUTTON PRESSED: " + str(event.button))
        if event.type == JOYBUTTONUP:
            print("button released")
            print(event)
        if event.type == JOYHATMOTION: 
            print("hat button pressed")
            print(event)