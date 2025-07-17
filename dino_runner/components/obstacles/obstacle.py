import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, type):
        super().__init__()
        self.image = image[type] if isinstance(image, list) else image
        self.rect = self.image.get_rect()
        self.type = type
        self.rect.x = 1100  # Começa fora da tela à direita
        self.pos_x = float(self.rect.x)  # Usar float para posição precisa

    def update(self, game_speed, obstacles):
        self.pos_x -= game_speed  # Atualiza posição float
        self.rect.x = int(self.pos_x)  # Atualiza posição inteira para o pygame
        if self.rect.x < -self.rect.width:
            obstacles.remove(self)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def get_hitbox(self):
        # Retorna um retângulo menor para colisão (reduzido nas laterais e topo)
        hitbox = self.rect.copy()
        hitbox.width = int(hitbox.width * 0.7)
        hitbox.height = int(hitbox.height * 0.8)
        hitbox.x += int(self.rect.width * 0.15)
        hitbox.y += int(self.rect.height * 0.1)
        return hitbox 