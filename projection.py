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

            # Dont draw lines behind focal?
            if start.z > self.observer.focal and end.z > self.observer.focal:

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
        if keyboard[pygame.K_a]:
            self.model.observer.origin.x -= self.controller.panSpeed
        if keyboard[pygame.K_d]:
            self.model.observer.origin.x += self.controller.panSpeed
        if keyboard[pygame.K_w]:
            self.model.observer.origin.y += self.controller.panSpeed
        if keyboard[pygame.K_s]:
            self.model.observer.origin.y -= self.controller.panSpeed

        if keyboard[pygame.K_q]:
            self.model.observer.origin.z -= self.controller.panSpeed
        if keyboard[pygame.K_e]:
            self.model.observer.origin.z += self.controller.panSpeed

        # Rotation (units are degrees)
        if keyboard[pygame.K_LEFT]:
            self.model.observer.orientation.y += self.controller.rotateSpeed
        if keyboard[pygame.K_RIGHT]:
            self.model.observer.orientation.y -= self.controller.rotateSpeed

        if keyboard[pygame.K_UP]:
            self.model.observer.orientation.x += self.controller.rotateSpeed
        if keyboard[pygame.K_DOWN]:
            self.model.observer.orientation.x -= self.controller.rotateSpeed

        if keyboard[pygame.K_COMMA]: # ,< key
            self.model.observer.orientation.z -= self.controller.rotateSpeed
        if keyboard[pygame.K_PERIOD]: # .> key
            self.model.observer.orientation.z += self.controller.rotateSpeed

        # Refresh the display
        image = self.model.visual()
        # Draw the image (to 0, 0 for now)
        image.display(self.screen, (0, 0))
    