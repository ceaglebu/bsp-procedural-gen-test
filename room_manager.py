import pygame,sys
from pygame.math import Vector2 as Vector
import random as r
from settings import *
from tile import Tile

class Level:
    def __init__(self, game):
        self.game = game
    
    def create_level(self):
        self.rooms = generate_rooms(2000, 2000, 500, 500, 10)

        for room in self.rooms:
            tiles_wide = room.width // TILE_SIZE
            tiles_tall = room.width // TILE_SIZE
            for x in range(0, tiles_wide):
                self.game.layers['tiles'].append(Tile(x * TILE_SIZE + room.left, room.top, TILE_SIZE, TILE_SIZE))
                self.game.layers['tiles'].append(Tile(x * TILE_SIZE + room.left, room.top + (tiles_tall-1) * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            for y in range(1, tiles_tall - 1):
                self.game.layers['tiles'].append(Tile(room.left, room.top + TILE_SIZE * y, TILE_SIZE, TILE_SIZE))
                self.game.layers['tiles'].append(Tile(room.left + (tiles_wide - 1) * TILE_SIZE, room.top + TILE_SIZE * y, TILE_SIZE, TILE_SIZE))

class Room:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.center = Vector(self.left + self.width // 2, self.top + self.height // 2)

def vertical_split(room, rooms_queue):
    split = r.randint(1, room.width)
    rooms_queue.append(Room(room.left,
                            room.top,
                            split,
                            room.height))
    rooms_queue.append(Room(room.left + split,
                            room.top,
                            room.width - split,
                            room.height))

def horizontal_split(room, rooms_queue):
    split = r.randint(1, room.height)
    rooms_queue.append(Room(room.left,
                            room.top,
                            room.width,
                            split))
    rooms_queue.append(Room(room.left,
                            room.top + split,
                            room.width,
                            room.height - split))

def generate_rooms(space_width, space_height, min_width, min_height, offset):
    rooms_list = []
    rooms_queue = []
    rooms_queue.append(Room(0, 0, space_width, space_height))

    while len(rooms_queue) > 0:
        room = rooms_queue.pop(0)
        if r.randint(0,1) == 1:
            # Split with vertical line
            if room.width >= min_width * 2:
                vertical_split(room, rooms_queue)
            # Split with horizontal line
            elif room.height >= min_height * 2:
                horizontal_split(room, rooms_queue)
            # Don't split, add to list
            elif room.height >= min_height and room.width >= min_width:
                rooms_list.append(room)
        else:
            # Split with horizontal line
            if room.height >= min_height * 2:
                horizontal_split(room, rooms_queue)
            # Split with vertical line
            elif room.width >= min_width * 2:
                vertical_split(room, rooms_queue)
            # Don't split, add to list
            elif room.height >= min_height and room.width >= min_width:
                rooms_list.append(room)
    
    for room in rooms_list:
        room.left += offset
        room.top += offset
        room.width -= offset * 2
        room.height -= offset * 2

    return rooms_list

if __name__ == '__main__':
    WIN = pygame.display.set_mode((1000,1000))
    clock = pygame.time.Clock()
    rooms = generate_rooms(1000,1000,250,250,5)
    while True:
        clock.tick(60)
        WIN.fill('grey')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        for room in rooms:
            pygame.draw.rect(WIN, (r.randint(0,255), r.randint(0,255), r.randint(0,255)), (room.left, room.top, room.width, room.height))
            pass
        pygame.display.update()

    