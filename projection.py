"""Implementation of a Model representing a 3D environment viewed through a perspective camera"""

from __future__ import annotations

from dataclasses import dataclass

import pygame
from pygame import Vector3

from pyquaternion import Quaternion

import base

class Rotation:
    """Represents a 3D rotation based on axis and angle
        Implemented using a quaternion
    """

    def __init__(self, axis: Vector3, angle: float) -> Rotation:
        try:
            # Regular based on axis/angle
            self.quaternion = Quaternion(axis=axis, angle=angle)
        except ZeroDivisionError:
            # Null rotation when no axis ([0, 0, 0]) provided
            self.quaternion = Quaternion()

    def compose(self, rotation: Rotation) -> None:
        """Returns the composition of the two rotations"""
        self.quaternion *= rotation.quaternion

    def rotate(self, vector: Vector3) -> Vector3:
        """Returns a rotated version of the given vector based on this Rotation"""
        return Vector3(*self.quaternion.rotate(vector))

    def __neg__(self) -> Rotation:
        """Returns the negative of this Rotation, around same axis but different direction"""
        return Rotation(self.quaternion.axis, -self.quaternion.angle)

@dataclass
class Observer:
    """Class containing data about an observer in 3D space"""

    origin: Vector3
    orientation: Rotation

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

        # Initialize list of polygons
        self.polygons = []

    def add_polygon(self, *points: Vector3) -> None:
        """Adds a filled 3D polygon to the Model
        Care should be used creating bent high-order polygons, depth may not be properly shown
        Also can be used for lines
        """
        self.polygons.append(points)

    def add_wire_cube(self, center: Vector3, radius: float):
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
                    self.add_polygon(
                        center + start,
                        center + end
                    )

    def add_cube(self, center: Vector3, radius: float):
        """Draws a solid-face cube with points <radius> away from <center>"""
        raise NotImplementedError("Not implemented yet")

    def transformed(self, point: Vector3) -> pygame.Vector3:
        """Returns a point transformed to relative coordinates based on Model observer
        Rotates so that the observer faces into the positive z-axis
        """
        # Translate and then rotate the point
        return self.observer.orientation.rotate(point - self.observer.origin)

    def projected(self, point: Vector3) -> pygame.Vector2:
        """Returns a point  projected onto the viewpoint based on the observer
        Returns None if the point does not project onto the viewpoint
        Does not transform the point first
        """
        # Check if point projects
        if point.z > 0:
            # Project onto viewport
            point = pygame.Vector2(
                self.observer.focal/point.z * point.x,
                self.observer.focal/point.z * point.y
            )
            # Return projected point
            return point
        else:
            # Point is not in front of observer, so not projected
            return None

    def visual(self) -> pygame.Surface:

        # Create blank surface for observation window
        output = base.Panel(
            pygame.Surface(self.observer.window),
            origin=base.Point(self.observer.window)/2,
            orientation=(1, -1)
        )

        # Transform the polygons based on observer
        polygons = [
            tuple(self.transformed(point) for point in polygon)
            for polygon in self.polygons
        ]

        # Sort the polygons by depth
        # TODO use a more intelligent sorting method than a random point depth
        # should determine closest point or something
        polygons = sorted(
            polygons,
            # Sort by the distance to the closest point of the polygon
            key=lambda polygon: sorted(polygon, key=lambda point: point.z)[0].z,
            reverse=True
        )

        # Draw each polygon
        for polygon in polygons:

            # Project point
            polygon = [self.projected(point) for point in polygon]

            # Draw if no issues
            if not None in polygon:
                try:
                    output.draw_polygon(polygon)
                except ValueError:
                    output.draw_line(*polygon)

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
        movement = (-self.model.observer.orientation).rotate(movement)

        # Apply movement vector
        self.model.observer.origin += movement

        # Determine axis
        axis = pygame.Vector3(0, 0, 0)

        # Rotation (units are degrees)
        if keyboard[pygame.K_LEFT]:
            axis.y += 1
        if keyboard[pygame.K_RIGHT]:
            axis.y -= 1
        if keyboard[pygame.K_UP]:
            axis.x += 1
        if keyboard[pygame.K_DOWN]:
            axis.x -= 1
        if keyboard[pygame.K_COMMA]: # ,< key
            axis.z -= 1
        if keyboard[pygame.K_PERIOD]: # .> key
            axis.z += 1

        # Relativize axis based on current rotation
        axis = (-self.model.observer.orientation).rotate(axis)

        # Create change rotation
        rotation = Rotation(axis, self.controller.rotateSpeed)

        # Compose the new rotation on the the main
        self.model.observer.orientation.compose(rotation)

        # Refresh the display
        image = self.model.visual()

        # Temporary debug information
        # Convert to readable strings
        pos = self.model.observer.origin
        position = f"<{pos.x:.1f}, {pos.y:.1f}, {pos.z:.1f}>"

        # Create and display text
        font = pygame.font.SysFont("default", 30)
        text = font.render(position, True, (255, 255, 255), (0, 0, 0))
        image.surface.blit(text, (0, 0))

        # Draw the image (to 0, 0 for now)
        image.display(self.screen, (0, 0))
    