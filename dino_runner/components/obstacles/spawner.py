import random
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.powerups.star import StarPowerUp
from dino_runner.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class ObstacleSpawner:
    """
    Gerencia o spawn de obstáculos e sinaliza quando deve spawnar uma estrela.
    """
    def __init__(self):
        self.obstacles = []
        self.obstacle_count = 0
        self.next_obstacle_distance = 0
        self.star_powerup = None

    def update(self, score, next_obstacle_score, next_bird_score, star_active):
        """
        Atualiza o estado dos obstáculos e decide se deve spawnar uma estrela.
        Retorna True se for hora de spawnar uma estrela.
        """
        spawn_star = False
        if score >= next_obstacle_score:
            if len(self.obstacles) == 0 or (self.obstacles and self.obstacles[-1].rect.x < (SCREEN_WIDTH - self.next_obstacle_distance)):
                if score >= next_bird_score and random.randint(1, 5) == 1:
                    self.obstacles.append(Bird())
                else:
                    self.obstacles.append(Cactus())
                self.next_obstacle_distance = random.randint(400, 1000)
                self.obstacle_count += 1
                if self.obstacle_count % 15 == 0 and not star_active:
                    spawn_star = True
        return spawn_star

    def reset(self):
        """Reseta o estado do spawner para o início do jogo."""
        self.obstacles = []
        self.obstacle_count = 0
        self.next_obstacle_distance = 0 