import pygame
from settings import *
import sys
import copy
from player_class import *
from enemy_class import *

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = maze_width//28
        self.cell_height = maze_height//30
        self.walls = []
        self.coins = []
        self.enemies = []
        self.e_pos = []
        self.p_pos = None

        self.load()

        self.player = Player(self, vec(self.p_pos))
        self.make_enemies()


    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()

            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()

            elif self.state == 'endgame':
                self.endgame_events()
                self.endgame_update()
                self.endgame_draw()
            else:
                self.running = False
            self.clock.tick(fps)
        pygame.quit()
        sys.exit()

    def draw_text(self, words, screen, pos, size, colour, font_name, centered = False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0]//2
            pos[1] = pos[1] - text_size[1]//2
        screen.blit(text, pos)

    def load(self):

        self.background = pygame.image.load('background.png')
        self.background = pygame.transform.scale(self.background, (maze_width, maze_height))

        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == '1':
                        self.walls.append(vec(xidx, yidx))
                    elif char == 'C':
                        self.coins.append(vec(xidx, yidx))
                    elif char == 'P':
                        self.p_pos = [xidx, yidx]
                    elif char in ['2', '3', '4', '5']:
                        self.e_pos.append([xidx, yidx])
                    elif char == 'B':
                        pygame.draw.rect(self.background, black, (xidx*self.cell_width, yidx*self.cell_height, self.cell_width, self.cell_height))

    def make_enemies(self):
        for index, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), index))
                        

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
    
    def start_update(self):
        pass
    
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
                    self.player.move(vec(-1,0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1,0))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0,1))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0,-1))
    
    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
        
        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.hit_player()
    
    def playing_draw(self):
        self.screen.fill(black)
        self.screen.blit(self.background, (top_bottom_buffer//2, top_bottom_buffer//2))
        #self.draw_grid()
        self.draw_coins()
        self.draw_text('CURRENT SCORE: {}'.format(self.player.current_score), self.screen, [top_bottom_buffer, 0], 18, white, start_font)
        self.draw_text('HIGH SCORE: {}'.format(self.player.high_score), self.screen, [width//2+top_bottom_buffer, 0], 18, white, start_font)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()
        #self.coins.pop()


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
    
    def endgame_update(self):
        pass
    
    def endgame_draw(self):
        self.screen.fill(black)
        self.draw_text('GAMEOVER', self.screen, [width//2, height//2], start_text_size, (170, 130, 60), start_font, centered=True)
        self.draw_text('SCORE: {}'.format(self.player.current_score), self.screen, [width//2, height//2 + 50], start_text_size, (33, 140, 160), start_font, centered=True)
        self.draw_text('HIGH SCORE: {}'.format(self.player.high_score), self.screen, [width//2, height//2 + 100], start_text_size, (170, 130, 60), start_font, centered=True)
        self.draw_text('TO PLAY AGAIN PRESS SPACE', self.screen, [width//2, height//2 + 150], start_text_size, (33, 140, 160), start_font, centered=True)
        pygame.display.update()


    def hit(self):
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0


    def reset(self):
        self.player.lives = 3
        self.player.current_score = 0
        self.coins = []
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == '1':
                        self.walls.append(vec(xidx, yidx))
                    elif char == 'C':
                        self.coins.append(vec(xidx, yidx))
        
        self.state = 'playing'



