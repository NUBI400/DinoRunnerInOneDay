import pygame

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, image, type):
        super().__init__()
        self.image = image
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x = 1100  # Começa fora da tela à direita
        self.pos_x = float(self.rect.x)  # Usar float para posição precisa
        self.start_time = 0
        self.duration = 0

    def update(self, game_speed, power_ups):
        self.pos_x -= game_speed  # Atualiza posição float
        self.rect.x = int(self.pos_x)  # Atualiza posição inteira para o pygame
        if self.rect.x < -self.rect.width:
            power_ups.remove(self)

    def draw(self, screen):
        screen.blit(self.image, self.rect) 