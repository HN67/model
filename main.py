"""Main script"""

import logging
import pygame

import projection
from config import config

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(config["logging"]["level"])

def main():
    """Main function to start the script"""

    # Initialize pygame
    pygame.init()

    # Reference output screen
    screen = pygame.display.set_mode(config["screen"]["dimensions"])
    pygame.display.set_caption(config["screen"]["name"])

    # Create clock
    clock = pygame.time.Clock()

    # Set the background color
    screen.fill(config["screen"]["color"])

    # Create model and manager
    # This portion of code is modified to implement different managers
    # The event loop expects a base.Manager named `manager`

    # Create and populate model
    model = projection.Projection(projection.Observer(
        origin=pygame.Vector3(0, 0, -400),
        orientation=pygame.Vector3(0, 0, 0),
        focal=200, window=config["screen"]["dimensions"]
    ))

    # Variable for radius of cube
    cube = 100

    # model.add_line(pygame.Vector3(-cube, -cube, -cube), pygame.Vector3(-cube, -cube, cube))
    # model.add_line(pygame.Vector3(-cube, cube, -cube), pygame.Vector3(-cube, cube, cube))
    # model.add_line(pygame.Vector3(cube, -cube, -cube), pygame.Vector3(cube, -cube, cube))
    # model.add_line(pygame.Vector3(cube, cube, -cube), pygame.Vector3(cube, cube, cube))

    # model.add_line(pygame.Vector3(-cube, -cube, -cube), pygame.Vector3(-cube, cube, -cube))
    # model.add_line(pygame.Vector3(-cube, -cube, cube), pygame.Vector3(-cube, cube, cube))
    # model.add_line(pygame.Vector3(cube, -cube, -cube), pygame.Vector3(cube, cube, -cube))
    # model.add_line(pygame.Vector3(cube, -cube, cube), pygame.Vector3(cube, cube, cube))

    # model.add_line(pygame.Vector3(-cube, -cube, -cube), pygame.Vector3(cube, -cube, -cube))
    # model.add_line(pygame.Vector3(-cube, -cube, cube), pygame.Vector3(cube, -cube, cube))
    # model.add_line(pygame.Vector3(-cube, cube, -cube), pygame.Vector3(cube, cube, -cube))
    # model.add_line(pygame.Vector3(-cube, cube, cube), pygame.Vector3(cube, cube, cube))
    model.add_cube(pygame.Vector3(0, 0, 0), cube)

    # Create Manager
    manager = projection.ProjectionManager(
        model, screen, projection.Controller(5, 2)
    )

    # Create a Stargon Manager
    #manager = stargon.StargonManager(stargon.Stargon(200, 9), screen)

    # Event loop
    # Shouldnt need to be changed to implement different models
    running = True
    while running:

        # Retrieve pygame event queue to allow multiple viewings
        # (since pygame.event.get() will clear the queue whenever used)
        events = pygame.event.get()

        # Show information around events
        if events:
            logger.info(events)

        # Iterate through events on top-level for specific situations
        # such as QUIT
        for event in events:

            # Allow window closure by ending main while loop
            if event.type == pygame.QUIT:
                running = False

        # Only continue if program hasnt been terminated
        if running:

            # Clear the background
            screen.fill(config["screen"]["color"])

            # Update manager to allow for interactive input
            manager.update(events, pygame.key.get_pressed())

            # Flip pygame display to actually show changes
            pygame.display.flip()

            # Limit the speed of ticks
            clock.tick(config["app"]["tps"])

# Safeguard so that main code only runs if this file is directly run and not imported
if __name__ == "__main__":
    main()
