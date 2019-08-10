"""Implementation of a Model representing a 3D environment viewed through a perspective camera"""

from dataclasses import dataclass

import pygame
from pygame import Vector3

import base

@dataclass
class Observer:
    """Class containing data about an observer in 3D space"""

    origin: Vector3
    perspective: Vector3

    focal: float
    window: base.Point

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
            start.rotate_x(self.observer.perspective.x)
            start.rotate_y(self.observer.perspective.y)
            start.rotate_z(self.observer.perspective.z)

            end.rotate_x(self.observer.perspective.x)
            end.rotate_y(self.observer.perspective.y)
            end.rotate_z(self.observer.perspective.z)

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

    def update(self, events, keyboard):
        """UP/DOWN arrowkeys change order, Holding LEFT/RIGHT change size"""

        # Search for Keypresses
        for event in events:

            # Check KEYDOWN events
            if event.type == pygame.KEYDOWN:
                pass

        # Search for held keys
        if keyboard[pygame.K_a]:
            self.model.observer.origin.x -= 1
        if keyboard[pygame.K_d]:
            self.model.observer.origin.x += 1

        # Refresh the display
        image = self.model.visual()
        # Draw the image (to 0, 0 for now)
        image.display(self.screen, (0, 0))
    