"""Implementation of Stargon Model, and a related Manager"""

import math
import pygame

import base

class Stargon(base.Model):
    """Represents the concave form of an 'order' sided polygon"""

    def __init__(self, radius, order):
        # Reference parameters
        self.radius = radius
        self.order = order

    def visual(self):
        # Create a panel 2x the radius, and give it a central origin and standard orientation
        drawing = base.Panel(
            pygame.Surface((self.radius*2, self.radius*2)),
            origin=base.Point(self.radius, self.radius), orientation=(1, -1)
        )
        # Draw each line of the stargon, reaching from a point to the second next point
        for i in range(self.order):
            drawing.draw_line(
                base.radial(self.radius, i*2*math.pi/self.order + math.pi/2),
                base.radial(self.radius, (i+2)*2*math.pi/self.order + math.pi/2)
            )
        # Return the panel
        return drawing

class StargonManager(base.Manager):
    """Manager Class for the Stargon Model"""

    def update(self, events, keyboard):
        """UP/DOWN arrowkeys change order, Holding LEFT/RIGHT change size"""

        # Search for UP/DOWN
        for event in events:

            # Check KEYDOWN events
            if event.type == pygame.KEYDOWN:

                # Match against Up and Down constants
                if event.key == pygame.K_UP:
                    self.model.order += 1
                elif event.key == pygame.K_DOWN:
                    self.model.order -= 1

        # Search for held LEFT/RIGHT keys
        if keyboard[pygame.K_LEFT]:
            self.model.radius -= 1
        if keyboard[pygame.K_RIGHT]:
            self.model.radius += 1

        # Refresh the display
        image = self.model.visual()
        # Find blit coordinate to place in the middle
        # Reference both rects to manipulate them
        screenRect = self.screen.get_rect()
        imageRect = image.surface.get_rect()
        # Center imageRect on screenRect
        imageRect.center = screenRect.center
        # Draw the image, which should be centered
        image.display(self.screen, (imageRect.x, imageRect.y))
