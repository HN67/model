"""Base classes for manipulating and visualizing Models
Intended to be subclassed, especially Models and Managers
"""

# Imports
from __future__ import annotations

import math
import typing

import pygame

# Typing definition to compress annotations
Pair = typing.Tuple[float, float]

class Point:
    """Object representing two dimensional point\n
        Can be constructed with two numerical parameters, or a single two-element numerical tuple
    """

    def __init__(self, x: typing.Union[Pair, float], y: float = None):
        if y is None:
            # Take single parameter as component pair
            self.position = (x[0], x[1])
        else:
            self.position = (x, y)

    @property
    def x(self):
        """First component of the Point position"""
        return self.position[0]

    @property
    def y(self):
        """Second component of the Point position"""
        return self.position[1]

    def __getitem__(self, key: int):
        """Returns a component of the Point"""
        return self.position[key]

    def __add__(self, other: typing.Union[Point, Pair]):
        """Adds each component of the point independently
            (x1, y1) + (x2, y2) => (x1 + x2, y1 + y2)
        """
        # Allow interacting with tuple
        if isinstance(other, (Point, tuple)):
            return Point(self.position[0] + other[0], self.position[1] + other[1])

        # Invalid type
        return NotImplemented

    def __radd__(self, other: typing.Union[Point, Pair]):
        return self.__add__(other)

    def __sub__(self, other: typing.Union[Point, Pair]):
        """Subtracts each component of the point independently
            (x1, y1) - (x2, y2) => (x1 - x2, y1 - y2)
        """
        # Allow interacting with tuple
        if isinstance(other, (Point, tuple)):
            return Point(self.position[0] - other[0], self.position[1] - other[1])

        # Invalid type
        return NotImplemented

    def __rsub__(self, other: typing.Union[Point, Pair]):
        return self.__sub__(other)

    def __neg__(self):
        """Negates each component of the point
            (x, y) => (-x, -y)
        """
        return Point(-self.position[0], -self.position[1]) #pylint: disable=invalid-unary-operand-type

    def __mul__(self, other: float):
        """Multiplies each component by a scalar
            (x, y) * c => (x*c, y*c)
        """
        return Point(self.position[0] * other, self.position[1] * other)

    def __rmul__(self, other: float):
        return self.__mul__(other)

    def __truediv__(self, other: float):
        """Divides each component by a scalar
            (x, y) / c => (x/c, y/c)
        """
        return Point(self.position[0] / other, self.position[1] / other)

    def __rtruediv__(self, other: float):
        return self.__truediv__(other)

class Panel:
    """Surface wrapper to provide additional functionality and abstractness
        All drawing methods are relative to the given origin based on orientation
    """

    def __init__(self, surface, origin: typing.Union[Point, Pair] = Point(0, 0),
                 orientation: typing.Union[Pair, Point] = Point(1, 1)):

        # Get surface to wrap from passed argument
        self.surface = surface

        # Reference origin
        self.origin = Point(origin)

        # Reference orientation
        self.orientation = Point(orientation)

    def convert(self, point: Point):
        """Converts a theoretical Point into the position to be drawn on the pygame Surface\n
            Based on Panel origin and orientation
        """
        return self.origin + Point(point[0] * self.orientation.x, point[1] * self.orientation.y)

    def clear(self, color: pygame.Color = pygame.Color(0, 0, 0)):
        """Clears the Panel to a specified blank color"""
        self.surface.fill(color)

    def draw_line(self, start: typing.Union[Point, Pair], end: typing.Union[Point, Pair],
                  color: pygame.Color = pygame.Color(255, 255, 255)):
        """Provides an easier but limited interface to pygame.draw.line(self.surface, ...)"""
        pygame.draw.line(
            self.surface, color,
            self.convert(start).position, self.convert(end).position
        )

    def display(self, surface: pygame.Surface, position: typing.Tuple[int, int]):
        """Displays the panel on a surface by blitting it"""
        surface.blit(self.surface, position)

def radial(length: float, angle: float) -> Point:
    """Returns a Point representing the position reached\n
       by travelling the given distance at the given angle in radians.\n
       Assumes clockwise rotation from eastward vector in a v> positive plane
    """
    # Standard vector calculations for horizontal and vertical
    return Point(length * math.cos(angle), length * math.sin(angle))

class Model:
    """Abstrac Class representing a mathematical model, designed to be represented on a Panel"""

    def update(self):
        """Updates the model to the next stage, if the model is dynamic"""
        return

    def visual(self) -> Panel:
        """Returns a Panel containing a visual representation of the Model"""
        raise NotImplementedError

class Manager:
    """Abstract Class that gets pygame events and screen and manages a Model on it"""

    def __init__(self, model: Model, screen: pygame.Surface):

        # Reference model and screen for later use
        self.model = model
        self.screen = screen

    def update(self, events, keyboard):
        """Updates the Manager with the given events and keyboard press state
        The manager should use the events to update the model,
        and then redraw the updated model
        """
        raise NotImplementedError
