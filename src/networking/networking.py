import pygame

pygame.init()
pygame.joystick.init()

num_joysticks = pygame.joystick.get_count()

if num_joysticks > 0:
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