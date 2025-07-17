import random
import pygame
from dino_runner.utils.constants import CLOUD, SCREEN_WIDTH

class Cloud:
    def __init__(self):
        self.image = CLOUD
        self.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 800)
        self.y = random.randint(50, 200)
        self.speed = random.uniform(1, 2.5)

    def update(self, game_speed):
        self.x -= self.speed + game_speed * 0.2
        if self.x < -self.image.get_width():
            self.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 800)
            self.y = random.randint(50, 200)
            self.speed = random.uniform(1, 2.5)

    def draw(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y))) 