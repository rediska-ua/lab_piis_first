import pygame
from settings import *
import sys
from player import *
from enemy import *

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = maze_width//columns
        self.cell_height = maze_height//rows
        self.walls = []
        self.coins = []
        self.enemies = []
        self.enemy_position = []
        self.player_position = None

        self.load()

        self.player = Player(self, vec(self.player_position))
        self.make_enemies()


    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_draw()

            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()

            elif self.state == 'endgame':
                self.endgame_events()
                self.endgame_draw()
            else:
                self.running = False
            self.clock.tick(fps)
        pygame.quit()
        sys.exit()

    def draw_text(self, words, screen, position, size, colour, font_name, centered = False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            position[0] = position[0] - text_size[0]//2
            position[1] = position[1] - text_size[1]//2
        screen.blit(text, position)

    def load(self):

        self.background = pygame.image.load('background.png')
        self.background = pygame.transform.scale(self.background, (maze_width, maze_height))

        with open("walls.txt", 'r') as file:
            for y_index, line in enumerate(file):
                for x_index, char in enumerate(line):
                    if char == '1':
                        self.walls.append(vec(x_index, y_index))
                    elif char == 'C':
                        self.coins.append(vec(x_index, y_index))
                    elif char == 'P':
                        self.player_position = [x_index, y_index]
                    elif char in ['2', '3', '4', '5']:
                        self.enemy_position.append([x_index, y_index])
                    elif char == 'B':
                        pygame.draw.rect(self.background, black, (x_index*self.cell_width, y_index*self.cell_height, self.cell_width, self.cell_height))

    def make_enemies(self):
        for index, position in enumerate(self.enemy_position):
            self.enemies.append(Enemy(self, vec(position), index))
                        

    def draw_grid(self):

        for x in range(width//self.cell_width):
            pygame.draw.line(self.background, grey, (x*self.cell_width, 0), (x*self.cell_width, height))
        for y in range(height//self.cell_height):
            pygame.draw.line(self.background, grey, (0, y*self.cell_height), (width, y*self.cell_height))

        for wall in self.walls:
            pygame.draw.rect(self.background, (110, 55, 160), (wall.x*self.cell_width, wall.y*self.cell_height, self.cell_width, self.cell_height))

        for coin in self.coins:
            pygame.draw.circle(self.screen, yellow, (int(coin.x*self.cell_width + self.cell_width//2 + top_bottom_buffer//2), int(coin.y*self.cell_height + self.cell_height//2 + top_bottom_buffer//2)), coin_radius)

    def draw_coins(self):

        for coin in self.coins:
            pygame.draw.circle(self.screen, yellow, (int(coin.x*self.cell_width + self.cell_width//2 + top_bottom_buffer//2), int(coin.y*self.cell_height + self.cell_height//2 + top_bottom_buffer//2)), coin_radius)


##################################################### Start functions #####################################################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'
    
    def start_draw(self):
        self.screen.fill(black)
        self.draw_text('PUSH SPACE BAR', self.screen, [width//2, height//2], start_text_size, (170, 130, 60), start_font, centered=True)
        self.draw_text('1 PLAYER ONLY', self.screen, [width//2, height//2 + 50], start_text_size, (33, 140, 160), start_font, centered=True)
        self.draw_text('HIGH SCORE', self.screen, [10, 0], start_text_size, (255, 255, 255), start_font)
        pygame.display.update()



##################################################### Playing functions #####################################################



    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
    
    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
        
        for enemy in self.enemies:
            if enemy.grid_position == self.player.grid_position:
                self.hit_player()
    
    def playing_draw(self):
        self.screen.fill(black)
        self.screen.blit(self.background, (top_bottom_buffer // 2, top_bottom_buffer // 2))
        self.draw_coins()
        self.draw_text('CURRENT SCORE: {}'.format(self.player.current_score), self.screen, [top_bottom_buffer, 0], 18, white, start_font)
        self.draw_text('HIGH SCORE: {}'.format(self.player.high_score), self.screen, [width // 2+top_bottom_buffer, 0], 18, white, start_font)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()


    def hit_player(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = 'endgame'
        else:
            self.hit()

##################################################### Endgame functions #####################################################

    def endgame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
    
    def endgame_draw(self):
        self.screen.fill(black)
        self.draw_text('GAMEOVER', self.screen, [width//2, height//2], start_text_size, (170, 130, 60), start_font, centered=True)
        self.draw_text('SCORE: {}'.format(self.player.current_score), self.screen, [width//2, height//2 + 50], start_text_size, (33, 140, 160), start_font, centered=True)
        self.draw_text('HIGH SCORE: {}'.format(self.player.high_score), self.screen, [width//2, height//2 + 100], start_text_size, (170, 130, 60), start_font, centered=True)
        self.draw_text('TO PLAY AGAIN PRESS SPACE', self.screen, [width//2, height//2 + 150], start_text_size, (33, 140, 160), start_font, centered=True)
        pygame.display.update()


    def hit(self):
        self.player.grid_position = vec(self.player.starting_position)
        self.player.pixel_position = self.player.get_pixel_position()
        self.player.direction *= 0
        for enemy in self.enemies:
            enemy.grid_position = vec(enemy.starting_position)
            enemy.pixel_position = enemy.get_pixel_position()
            enemy.direction *= 0


    def reset(self):
        self.player.lives = 3
        self.player.current_score = 0
        self.coins = []
        self.player.grid_position = vec(self.player.starting_position)
        self.player.pixel_position = self.player.get_pixel_position()
        self.player.direction *= 0
        for enemy in self.enemies:
            enemy.grid_position = vec(enemy.starting_position)
            enemy.pixel_position = enemy.get_pixel_position()
            enemy.direction *= 0
        with open("walls.txt", 'r') as file:
            for y_index, line in enumerate(file):
                for x_index, char in enumerate(line):
                    if char == '1':
                        self.walls.append(vec(x_index, y_index))
                    elif char == 'C':
                        self.coins.append(vec(x_index, y_index))
        
        self.state = 'playing'



