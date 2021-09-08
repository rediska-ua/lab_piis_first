import pygame, random
from settings import *

vec = pygame.math.Vector2

class Enemy:
    def __init__(self, app, position, index):
        self.app = app
        self.grid_position = position
        self.pixel_position = self.get_pixel_position()
        self.starting_position = [position.x, position.y]
        self.radius = 10
        self.number = index
        self.colour = self.set_colour()
        self.direction = vec(0, 0)
        self.personality = self.set_personality()

    def get_pixel_position(self):
        return vec((self.grid_position.x*self.app.cell_width) + top_bottom_buffer//2 + self.app.cell_width//2, 
        self.grid_position.y*self.app.cell_height + top_bottom_buffer//2 + self.app.cell_height//2)

    def update(self):
        self.pixel_position += self.direction
        if self.time_to_move():
            self.move()

        self.grid_position[0] = (self.pixel_position[0] - top_bottom_buffer + self.app.cell_width//2)//self.app.cell_width+1
        self.grid_position[1] = (self.pixel_position[1] - top_bottom_buffer + self.app.cell_height//2)//self.app.cell_height+1

    def time_to_move(self):
        if int(self.pixel_position.x + top_bottom_buffer//2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True

        if int(self.pixel_position.y + top_bottom_buffer//2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

        return False

    def move(self):
        if self.personality == 'random':
            self.direction = self.get_random_direction()

    def get_random_direction(self):
        while True:
            number = random.randint(-2, 2)
            if number == -2:
                x_dir, y_dir = 1,0
            elif number == -1:
                x_dir, y_dir = 0,1
            elif number == 0:
                x_dir, y_dir = -1,0
            else:
                x_dir, y_dir = 0,-1

            next_pos = vec(self.grid_position.x + x_dir, self.grid_position.y + y_dir)
            if next_pos not in self.app.walls:
                break

        return vec(x_dir, y_dir)

    
    def draw(self):
        pygame.draw.circle(self.app.screen, self.colour, (int(self.pixel_position.x), int(self.pixel_position.y)), self.radius)

    def set_colour(self):
        if self.number == 0:
            return white
        elif self.number == 1:
            return red
        elif self.number == 2:
            return blue
        elif self.number == 3:
            return grey

    def set_personality(self):
        if self.number == 0:
            return 'speedy'
        elif self.number == 1:
            return 'slow'
        elif self.number == 2:
            return 'random'
        else:
            return 'scared'