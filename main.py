import pygame, os, sys
from pygame.math import Vector2 as Vector
from settings import *
from player import Player
from tile import Tile
from room_manager import Level

class Game:
    def __init__(self):
        self.WIN = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()

        self.layers = {
            'tiles': [],
            'player': [],
        }

        self.player = Player((640, 360), self, self.layers['player'])

        self.camera_offset = Vector()

        level = Level(self)
        level.create_level()
        
    def update(self, dt):
        for layer in self.layers.values():
            for object in layer:
                object.update(dt)
    
    def draw(self):
        self.WIN.fill(BACKGROUND_COLOR)
        self.camera_offset = -(self.player.rect.center - Vector(640, 360) + 5 * (pygame.mouse.get_pos() - Vector(640, 360)))
        for layer in self.layers.values():
            for object in layer:
                object.draw(self.WIN, self.camera_offset)

    def run(self):
        dt = self.clock.tick(144) / 1000
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.update(dt)
            self.draw()
            pygame.display.update()
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()