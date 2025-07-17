from dino_runner.utils.constants import BIRD
from dino_runner.components.obstacles.obstacle import Obstacle


class Bird(Obstacle):
    def __init__(self, y_pos=None):
        super().__init__(BIRD, 0)
        self.image = BIRD  # Garante que seja uma lista de imagens
        if y_pos is not None:
            self.rect.y = y_pos
        else:
            # Menor chance para a altura mais alta
            import random
            bird_heights = [250, 310, 180]  # 250: normal, 310: chão, 180: alto
            weights = [0.4, 0.4, 0.2]       # 20% de chance para o mais alto
            self.rect.y = random.choices(bird_heights, weights)[0]
        self.step_index = 0

    def draw(self, screen):
        screen.blit(self.image[self.step_index // 10], self.rect)
        self.step_index += 1
        if self.step_index >= 20:
            self.step_index = 0