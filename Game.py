import random

import pygame
import sys
from configs import *


class GAME:
    # INICIA O JOGO
    def __init__(self):
        pygame.init()
        self.score = 0
        self.score_enemie = 0
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False
        self.paused = False
        self.font = pygame.font.SysFont('Arial', 32)
        self.clock.tick(FPS)

    # EVENTOS DO JOGO
    def events(self):
        key = pygame.key.get_pressed()
        self.mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.score = 0
                self.playing = False
                self.running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if self.mouse[0] > WIN_WIDTH / 2 - 100 and self.mouse[0] < WIN_WIDTH / 2 - 100 + 200 and self.mouse[
                    1] > WIN_HEIGHT / 2 and self.mouse[1] < WIN_HEIGHT + 80:
                    self.new()
            if self.score == WIN_POINTS or self.score_enemie == WIN_POINTS and key[pygame.K_ESCAPE]:
                self.playing = False
                self.score = 0
                self.score_enemie = 0
                self.draw()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.game()

    def draw(self):
        self.screen.fill(WHITE)
        self.menu()
        pygame.display.update()

    def menu(self):
        self.font_menu = self.font.render('PLAY', True, WHITE)
        self.buttom_play_rect = pygame.Rect(WIN_WIDTH/2-100, WIN_HEIGHT/2, 200, 80)
        pygame.draw.rect(self.screen, GRAY, self.buttom_play_rect)
        self.screen.blit(self.font_menu, [WIN_WIDTH/2-38, WIN_HEIGHT/2+20])

    def game(self):
        self.screen.fill(GRAY)
        self.sprites()
        pygame.display.update()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y -= 0.6
        if keys[pygame.K_s]:
            self.y += 0.6

        if self.circle_y <= 0 or self.circle_y >= 680:
            self.direction_ball *= -1

        if self.circle_x >= 170 and self.circle_x <= 180 and self.circle_y >= self.y -15 and self.circle_y <= self.y + 95:
            self.direction_ball = random.randint(-1, 1) / 2
            self.SPEED += 0.05
            self.SPEED *= -1

        if self.circle_x >= 1200 and self.circle_x <= 1210 and self.circle_y >= self.npc_y -15 and self.circle_y <= self.npc_y + 95:
            self.direction_ball = random.randint(-1, 1) / 2
            self.SPEED -= 0.05
            self.SPEED *= -1

        if self.circle_x >= 1360:
            self.score += 1
            self.score_sum()


        elif self.circle_x <= 0:
            self.score_enemie += 1
            self.score_sum()

        if self.y <= 2:
            self.y = 2
        elif self.y >= WIN_HEIGHT-82:
            self.y = WIN_HEIGHT - 82

        if self.circle_y > self.npc_y+40:
            self.npc_y += 0.4

        if self.circle_y < self.npc_y+40:
            self.npc_y -= 0.4

        if self.npc_y <= 2:
            self.npc_y = 2

        elif self.npc_y >= WIN_HEIGHT-82:
            self.npc_y = WIN_HEIGHT - 82

        self.circle_y += self.direction_ball
        self.circle_x -= self.SPEED

        if self.score == WIN_POINTS:
            self.Win()

        if self.score_enemie == WIN_POINTS:
            self.game_over()

    def sprites(self):
        #PlAYER

        self.rect = pygame.Rect(150, self.y, 20, 80)
        pygame.draw.rect(self.screen, WHITE, self.rect)
        #NPC
        self.rect = pygame.Rect(1210, self.npc_y, 20, 80)
        pygame.draw.rect(self.screen, WHITE, self.rect)
        #BOLA
        self.pos = (self.circle_x, self.circle_y)
        pygame.draw.circle(self.screen, WHITE, self.pos, 20)
        #SCORE
        self.score_menu = self.font.render(str(self.score), True, WHITE)
        self.screen.blit(self.score_menu, [630, 60])
        self.score_menu = self.font.render(str(self.score_enemie), True, WHITE)
        self.screen.blit(self.score_menu, [730, 60])

    def new(self):
        if not self.playing:
            self.playing = True
            self.direction_ball = 0
            self.SPEED = SPEED
            self.npc_y = NPC_Y
            self.y = PLAYER_POS_Y
            self.circle_y = Y_CIRCLE
            self.circle_x = X_CIRCLE
            self.main()


    def score_sum(self):
        self.npc_y = NPC_Y
        self.y = PLAYER_POS_Y
        self.circle_y = Y_CIRCLE
        self.circle_x = X_CIRCLE
        self.time_new_game = 0
        self.direction_ball = 0
        self.sprites()
        self.time_new_game = 0
        self.SPEED = SPEED

    def Win(self):
        keys = pygame.key.get_pressed()
        while self.score == WIN_POINTS:
            self.playing = False
            self.events()
            self.screen.fill(GRAY)
            self.score_menu = self.font.render(str('You Win'), True, WHITE)
            self.screen.blit(self.score_menu, [WIN_WIDTH/2-50, WIN_HEIGHT/2])
            pygame.display.update()

    def game_over(self):
        keys = pygame.key.get_pressed()
        while self.score_enemie == WIN_POINTS:
            self.playing = False
            self.events()
            self.screen.fill(GRAY)
            self.score_menu = self.font.render(str('You Lose'), True, WHITE)
            self.screen.blit(self.score_menu, [WIN_WIDTH / 2 - 50, WIN_HEIGHT / 2])
            self.score_menu = self.font.render(str('PRESS ESC'), True, WHITE)
            self.screen.blit(self.score_menu, [WIN_WIDTH / 2 - 70, WIN_HEIGHT / 1.75])
            pygame.display.update()


# CARREGA OS DADOS DO JOGO
g = GAME()

while g.running:
    g.events()
    g.draw()

pygame.quit()
sys.exit()
