import pygame
from pygame.math import Vector2 as Vector
from settings import *

class Player:
    def __init__(self, pos, game, layer):
        self.game = game
        layer.append(self)
        self.position = Vector(pos)
        self.rect = pygame.rect.Rect(pos, (0,0)).inflate(PLAYER_SIZE)

    def handle_movement(self, dt):
        keys = pygame.key.get_pressed()
        movement_control = Vector()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            movement_control.y = -1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            movement_control.y = 1
        else:
            movement_control.y = 0
        
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            movement_control.x = 1
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            movement_control.x = -1
        else:
            movement_control.x = 0
        
        if movement_control.magnitude() > 0:
            movement_control = movement_control.normalize()
        
        self.velocity = movement_control * PLAYER_SPEED 
        self.position += self.velocity * dt

        self.rect.centerx = self.position.x
        for tile in self.game.layers['tiles']:
            if self.rect.colliderect(tile.rect):
                if self.velocity.x > 0:
                    self.rect.right = tile.rect.left
                else:
                    self.rect.left = tile.rect.right

                self.position.x = self.rect.centerx

        self.rect.center = self.position 
        for tile in self.game.layers['tiles']:
            if self.rect.colliderect(tile.rect):
                if self.velocity.y > 0:
                    self.rect.bottom = tile.rect.top
                else:
                    self.rect.top = tile.rect.bottom

                self.position.y = self.rect.centery
        

    
    def draw(self, surface, offset):
        pygame.draw.rect(surface, 'red', (Vector(self.rect.topleft) + offset, self.rect.size))

    def update(self, dt):
        self.handle_movement(dt)