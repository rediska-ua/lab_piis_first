import pygame, random
from settings import *

vec = pygame.math.Vector2

class Enemy:
    def __init__(self, app, pos, index):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.starting_pos = [pos.x, pos.y]
        self.radius = 10
        self.number = index
        self.colour = self.set_colour()
        self.direction = vec(0, 0)
        self.personality = self.set_personality()

    def get_pix_pos(self):
        return vec((self.grid_pos.x*self.app.cell_width) + top_bottom_buffer//2 + self.app.cell_width//2, 
        self.grid_pos.y*self.app.cell_height + top_bottom_buffer//2 + self.app.cell_height//2)

    def update(self):
        self.pix_pos += self.direction
        if self.time_to_move():
            self.move()

        self.grid_pos[0] = (self.pix_pos[0] - top_bottom_buffer + self.app.cell_width//2)//self.app.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1] - top_bottom_buffer + self.app.cell_height//2)//self.app.cell_height+1

    def time_to_move(self):
        if int(self.pix_pos.x + top_bottom_buffer//2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True

        if int(self.pix_pos.y + top_bottom_buffer//2) % self.app.cell_height == 0:
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

            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in self.app.walls:
                break

        return vec(x_dir, y_dir)

    
    def draw(self):
        pygame.draw.circle(self.app.screen, self.colour, (int(self.pix_pos.x), int(self.pix_pos.y)), self.radius)

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