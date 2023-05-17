import pygame
from pygame.math import Vector2 as Vector

class Tile:
    def __init__(self, left, top, width, height):
        self.rect = pygame.rect.Rect(left, top, width, height)
    
    def draw(self, surface, offset):
        pygame.draw.rect(surface, 'black', (Vector(self.rect.topleft) + offset, self.rect.size))

    def update(self, dt):
        pass

class Ground(Tile):
    def draw(self, surface, offset):
        pygame.draw.rect(surface, 'white', (Vector(self.rect.topleft) + offset, self.rect.size))
