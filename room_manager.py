import pygame,sys
from pygame.math import Vector2 as Vector
import random as r
from settings import *
from tile import Tile, Ground

class Level:
    def __init__(self, game):
        self.game = game
    
    def create_level(self):
        self.rooms = generate_rooms(2000, 2000, 500, 500, 10)

        for room in self.rooms:
            tiles_wide = room.width // TILE_SIZE
            tiles_tall = room.height // TILE_SIZE
            for x in range(0, tiles_wide):
                self.game.layers['tiles'].append(Tile(x * TILE_SIZE + room.left, room.top, TILE_SIZE, TILE_SIZE))
                self.game.layers['tiles'].append(Tile(x * TILE_SIZE + room.left, room.top + (tiles_tall-1) * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            for y in range(1, tiles_tall - 1):
                self.game.layers['tiles'].append(Tile(room.left, room.top + TILE_SIZE * y, TILE_SIZE, TILE_SIZE))
                self.game.layers['tiles'].append(Tile(room.left + (tiles_wide - 1) * TILE_SIZE, room.top + TILE_SIZE * y, TILE_SIZE, TILE_SIZE))

    def create_level_dict(self):
        rooms = generate_rooms(50, 50, 10, 10, 1)
        hallways = generate_hallways(rooms)
        print_hallways(hallways)
        level = {}

        for room in rooms:
            for x in range(room.width):
                level[f'{x + room.left}, {room.top}'] = 'X'
                level[f'{x + room.left}, {room.top + room.height - 1}'] = 'X'
                for y in range(1, room.height - 1):
                    if x == 0 or x == room.width - 1:
                        level[f'{x + room.left}, {y + room.top}'] = 'X'
                    else:
                        level[f'{x + room.left}, {y + room.top}'] = 'O'
        
        for hallway in hallways:
            draw_hallway(level, hallway)            
        return level

    def create_level_from_dict(self, dict):
        for coord, tile_type in dict.items():
            x, y = (int(x) for x in coord.split(', '))
            if tile_type == 'X':
                self.game.layers['tiles'].append(Tile(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile_type == 'O':
                self.game.layers['ground'].append(Ground(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def has_key(dict, key):
    has_key = False
    for item in dict.keys():
        if item == key:
            has_key = True
    return has_key

def draw_hallway(level, hallway):
    if hallway.start.y == hallway.corner.y and hallway.start.x != hallway.corner.x:
        hallway_left, hallway_right = int(min(hallway.start.x, hallway.corner.x)), int(max(hallway.start.x, hallway.corner.x))
        initial_y  = int(hallway.start.y)
        for x in range(hallway_left, hallway_right + 1):
            level[f'{x}, {initial_y}'] = 'O'
            make_hallway_edge(level, f'{x}, {initial_y - 1}')
            make_hallway_edge(level, f'{x}, {initial_y + 1}')
        
        hallway_top, hallway_bottom = int(min(hallway.corner.y, hallway.end.y)), int(max(hallway.corner.y, hallway.end.y))
        initial_x = int(hallway.corner.x)
        for y in range(hallway_top, hallway_bottom + 1):
            level[f'{initial_x}, {y}'] = 'O'
            make_hallway_edge(level, f'{initial_x - 1}, {y}')
            make_hallway_edge(level, f'{initial_x + 1}, {y}')
    elif hallway.start.x == hallway.corner.x:
        hallway_top, hallway_bottom = int(min(hallway.start.y, hallway.corner.y)), int(max(hallway.start.y, hallway.corner.y))
        initial_x = int(hallway.start.x)
        for y in range(hallway_top, hallway_bottom + 1):
            level[f'{initial_x}, {y}'] = 'O'
            make_hallway_edge(level, f'{initial_x - 1}, {y}')
            make_hallway_edge(level, f'{initial_x + 1}, {y}')

        hallway_left, hallway_right = int(min(hallway.corner.x, hallway.end.x)), int(max(hallway.corner.x, hallway.end.x))
        initial_y  = int(hallway.corner.y)
        for x in range(hallway_left, hallway_right + 1):
            print(hallway_left, hallway_right)
            level[f'{x}, {initial_y}'] = 'O'
            make_hallway_edge(level, f'{x}, {initial_y - 1}')
            make_hallway_edge(level, f'{x}, {initial_y + 1}')


def make_hallway_edge(level, key):
    if has_key(level, key):
        if level[key] != 'O':
            level[key] = 'X'
    else:
        level[key] = 'X'
class Room:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.center = Vector(self.left + self.width // 2, self.top + self.height // 2)

class Hallway:
    def __init__(self, start, corner, end):
        self.start = Vector(int(start.x), int(start.y))
        self.corner = Vector(int(corner.x), int(corner.y))
        self.end = Vector(int(end.x), int(end.y))

def print_hallways(hallways):
    for hallway in hallways:
        print(f"start: {hallway.start}, corner: {hallway.corner}, end: {hallway.end}")

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

def generate_hallways(rooms):
    available_rooms = rooms.copy()
    hallways = []

    current_room = available_rooms.pop(0)

    while len(available_rooms) > 0:
        connect_room = None
        for i, room in enumerate(available_rooms):
            if i == 0:
                max_dist = current_room.center.distance_to(room.center)
                connect_room = room
            else:
                dist = room.center.distance_to(current_room.center)
                if dist < max_dist:
                    max_dist = dist
                    connect_room = room
        
        if connect_room:
            available_rooms.remove(connect_room)
            if r.randint(0,1) == 0:
                # Have corner on same y axis as start
                hallways.append(Hallway(start = current_room.center,
                                        corner = Vector(connect_room.center.x, current_room.center.y),
                                        end = connect_room.center))
            else:
                # Have corner on same x axis as start
                hallways.append(Hallway(start = current_room.center,
                                        corner = Vector(current_room.center.x, connect_room.center.y),
                                        end = connect_room.center))
        current_room = connect_room
    return hallways
        

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

    