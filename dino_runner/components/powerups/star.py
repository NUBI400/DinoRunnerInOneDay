import pygame
import random
from dino_runner.utils.constants import STAR, SCREEN_WIDTH, SCREEN_HEIGHT

class StarPowerUp:
    """
    Gerencia o comportamento da estrela: spawn, ativação, duração e desenho.
    """
    WIDTH = 32
    HEIGHT = 32
    DURATION = 10000  # ms

    def __init__(self, x=None, y=None):
        self.x = x if x is not None else SCREEN_WIDTH
        self.y = y if y is not None else SCREEN_HEIGHT//2 - 16
        self.active = False
        self.activated_time = 0
        self.collected = False
        self.star_img = pygame.transform.smoothscale(STAR, (self.WIDTH, self.HEIGHT))

    def update(self, game_speed, dino_rect):
        """
        Atualiza a posição da estrela e verifica colisão com o dino.
        Ativa o efeito se colidir e controla a duração do efeito.
        """
        if not self.active and not self.collected:
            self.x -= game_speed
            if self.x < -self.WIDTH:
                self.collected = True
            elif dino_rect.colliderect(pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)):
                self.active = True
                self.activated_time = pygame.time.get_ticks()
                self.collected = True
        elif self.active:
            if pygame.time.get_ticks() - self.activated_time > self.DURATION:
                self.active = False

    def draw(self, screen):
        """Desenha a estrela na tela se não foi coletada."""
        if not self.collected:
            screen.blit(self.star_img, (int(self.x), int(self.y)))

    def is_active(self):
        """Retorna True se o efeito da estrela está ativo."""
        return self.active

    def is_collected(self):
        """Retorna True se a estrela já foi coletada ou saiu da tela."""
        return self.collected

    def reset(self):
        """Reseta o estado da estrela para novo spawn."""
        self.__init__() 