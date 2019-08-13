"""Implementation of a Model representing a 3D environment viewed through a perspective camera"""

from dataclasses import dataclass

import pygame
from pygame import Vector3

import base

@dataclass
class Observer:
    """Class containing data about an observer in 3D space"""

    origin: Vector3
    orientation: Vector3

    focal: float
    window: base.Point

@dataclass
class Controller:
    """Class containing data about the controls of the Projection"""

    panSpeed: float
    rotateSpeed: float

class Projection(base.Model):
    """Represents a 3 dimensional space projected into 2D based on an observer"""

    def __init__(self, observer: Observer):

        # Reference observer
        self.observer = observer

        # Initalize set of lines belonging to the space
        self.lines = []

    def add_line(self, start: Vector3, end: Vector3):
        """Add line to the 3D space of the projection, stretching from start to end"""
        self.lines.append((start, end))

    def add_cube(self, center: Vector3, radius: float):
        """Draws a wire-frame cube with points <radius> away from <center>"""
        # Draws 3 sets of 4 lines, where each set is a different dimension
        # Each set has the negative of that dimension to the positive
        # And the 4 lines are iteration of -1, -1 -> 1, 1 (sorta binary)
        # Iterate through the 3 dimensions
        for dimension in range(3):
            # Iterate through -1/-1, -1/1, 1/-1, 1/1 for non base dimensions
            for first in (-radius, radius):
                for second in (-radius, radius):
                    # Init base vector
                    start = pygame.Vector3(0, 0, 0)
                    # Start on negative of the main dimension
                    start[dimension] = -radius
                    # Fill the other two dimensions
                    start[(dimension + 1)%3] = first
                    start[(dimension + 2)%3] = second
                    # Duplicate start to end but change the main dimension
                    end = pygame.Vector3(start)
                    end[dimension] = radius
                    # Add the line
                    self.add_line(
                        center + start,
                        center + end
                    )

    def visual(self) -> pygame.Surface:

        # Create blank surface for observation window
        output = base.Panel(
            pygame.Surface(self.observer.window),
            origin=base.Point(self.observer.window)/2,
            orientation=(1, -1)
        )

        # Draw every line projected
        for start, end in self.lines:

            # Transform the endpoints
            # Translate relative to observer position
            start = start - self.observer.origin
            end = end - self.observer.origin

            # Rotate each vector point
            start.rotate_x_ip(self.observer.orientation.x)
            start.rotate_y_ip(self.observer.orientation.y)
            start.rotate_z_ip(self.observer.orientation.z)

            end.rotate_x_ip(self.observer.orientation.x)
            end.rotate_y_ip(self.observer.orientation.y)
            end.rotate_z_ip(self.observer.orientation.z)

            # Dont draw lines behind camera? Old was focal: self.observer.focal
            if start.z > 0 and end.z > 0:

                # Project each point onto the 2D focal plane
                start = pygame.Vector2(
                    self.observer.focal/start.z * start.x,
                    self.observer.focal/start.z * start.y
                )
                end = pygame.Vector2(
                    self.observer.focal/end.z * end.x,
                    self.observer.focal/end.z * end.y
                )

                # Draw the projected line onto the 2D output
                output.draw_line(start, end)

        # Return the finished output
        return output

class ProjectionManager(base.Manager):
    """Manager Class for the Projection Model"""

    def __init__(self, model: base.Model, screen: pygame.Surface, controller: Controller):
        # Delegate super init
        super().__init__(model, screen)

        # Reference controller
        self.controller = controller

    def update(self, events, keyboard):
        """UP/DOWN arrowkeys change order, Holding LEFT/RIGHT change size"""

        # Search for Keypresses
        for event in events:

            # Check KEYDOWN events
            if event.type == pygame.KEYDOWN:
                pass

        # Search for held keys
        # Translation movement
        # Create base movement vector
        movement = pygame.Vector3(0, 0, 0)
        # Change movement vector based on held keys
        if keyboard[pygame.K_a]:
            movement.x -= self.controller.panSpeed
        if keyboard[pygame.K_d]:
            movement.x += self.controller.panSpeed
        if keyboard[pygame.K_w]:
            movement.y += self.controller.panSpeed
        if keyboard[pygame.K_s]:
            movement.y -= self.controller.panSpeed
        if keyboard[pygame.K_q]:
            movement.z -= self.controller.panSpeed
        if keyboard[pygame.K_e]:
            movement.z += self.controller.panSpeed

        # Rotate movement vector based on current orientation
        # Countercompensates by counterclockwise so that
        # eg D always moves right from camera perspective
        movement.rotate_x_ip(-self.model.observer.orientation.x)
        movement.rotate_y_ip(-self.model.observer.orientation.y)
        movement.rotate_z_ip(-self.model.observer.orientation.z)

        # Apply movement vector
        self.model.observer.origin += movement

        # Create base rotation vector
        rotation = pygame.Vector3(0, 0, 0)

        # Rotation (units are degrees)
        if keyboard[pygame.K_LEFT]:
            rotation.y += self.controller.rotateSpeed
        if keyboard[pygame.K_RIGHT]:
            rotation.y -= self.controller.rotateSpeed

        if keyboard[pygame.K_UP]:
            rotation.x += self.controller.rotateSpeed
        if keyboard[pygame.K_DOWN]:
            rotation.x -= self.controller.rotateSpeed

        if keyboard[pygame.K_COMMA]: # ,< key
            rotation.z -= self.controller.rotateSpeed
        if keyboard[pygame.K_PERIOD]: # .> key
            rotation.z += self.controller.rotateSpeed

        # Relatavize rotation
        # TODO
        

        # Add the rotation temp vector
        self.model.observer.orientation += rotation

        # Refresh the display
        image = self.model.visual()
        
        # Temporary debug information
        font = pygame.font.SysFont("default", 30)
        text = font.render(
            f"{self.model.observer.origin}, {self.model.observer.orientation}",
            True, (255, 255, 255), (0, 0, 0)
        )
        image.surface.blit(text, (0, 0))

        # Draw the image (to 0, 0 for now)
        image.display(self.screen, (0, 0))
    