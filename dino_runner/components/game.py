import pygame
import random
from dino_runner.utils.constants import SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, ICON, BG, GAME_OVER_IMG, FONT_STYLE
from dino_runner.components.dino import Dino
from dino_runner.components.cloud import Cloud
from dino_runner.components.score_manager import ScoreManager
from dino_runner.components.sound_manager import SoundManager
from dino_runner.components.obstacles.spawner import ObstacleSpawner
from dino_runner.components.powerups.star import StarPowerUp

class Game:
    """
    Classe principal do jogo. Orquestra o loop, entrada, desenho e integração dos componentes.
    """
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = False
        self.playing = False
        self.dino = Dino()
        self.clouds = [Cloud() for _ in range(random.randint(2, 4))]
        self.score_manager = ScoreManager()
        self.sound_manager = SoundManager()
        self.spawner = ObstacleSpawner()
        self.star_powerup = None
        self.score = 0
        self.game_speed = 10
        self.max_speed = 20
        self.acceleration = 0.001
        self.background_x1 = 0
        self.background_x2 = BG.get_width()
        self.death_animating = False
        self.game_over = False
        self.showing_start_screen = True  # Novo estado para tela inicial
        self.init_clouds()

    def execute(self):
        """Inicia o loop principal do jogo."""
        self.running = True
        while self.running:
            if self.showing_start_screen:
                self.show_start_screen()
            else:
                self.run()

    def run(self):
        """Loop de uma partida do jogo."""
        self.playing = True
        # Não reinicializa nuvens/cenário ao sair da tela inicial
        self.dino = Dino()
        self.spawner.reset()
        self.star_powerup = None
        self.score = 0
        self.game_speed = 10
        self.background_x1 = 0
        self.background_x2 = BG.get_width()
        self.death_animating = False
        self.game_over = False
        self.sound_manager.tocar_musica_fundo()
        while self.playing and self.running:
            self.handle_events()
            if not self.death_animating and not self.game_over:
                self.update()
                self.draw()
                self.clock.tick(60)
                if self.game_speed < self.max_speed:
                    self.game_speed = min(self.game_speed + self.acceleration, self.max_speed)
            elif self.death_animating:
                # Só nuvens e dino animam, obstáculos e power-ups ficam visíveis e parados
                original_game_speed = self.game_speed
                self.game_speed = 0  # Chão para
                # Zera velocidade dos obstáculos
                for obstacle in self.spawner.obstacles:
                    if hasattr(obstacle, 'speed'):
                        obstacle.original_speed = getattr(obstacle, 'speed', 0)
                        obstacle.speed = 0
                # Zera velocidade dos power-ups se aplicável
                if self.star_powerup and hasattr(self.star_powerup, 'speed'):
                    self.star_powerup.original_speed = getattr(self.star_powerup, 'speed', 0)
                    self.star_powerup.speed = 0
                for cloud in self.clouds:
                    cloud.update(1)  # Movimento lento das nuvens
                self.dino.update({})  # Garante animação de morte
                self.draw()
                self.clock.tick(60)
                # Restaura velocidades
                self.game_speed = original_game_speed
                for obstacle in self.spawner.obstacles:
                    if hasattr(obstacle, 'original_speed'):
                        obstacle.speed = obstacle.original_speed
                if self.star_powerup and hasattr(self.star_powerup, 'original_speed'):
                    self.star_powerup.speed = self.star_powerup.original_speed
                if not getattr(self.dino, 'is_dead_anim', False):
                    self.death_animating = False
                    self.game_over = True
            elif self.game_over:
                self.sound_manager.parar_musica_fundo()
                self.draw()
                self.show_game_over_blocking()
                return

    def reset(self):
        """Reseta o estado do jogo para uma nova partida."""
        self.dino = Dino()
        self.clouds = [Cloud() for _ in range(random.randint(2, 4))]
        self.spawner.reset()
        self.star_powerup = None
        self.score = 0
        self.game_speed = 10
        self.background_x1 = 0
        self.background_x2 = BG.get_width()
        self.death_animating = False
        self.game_over = False

    def handle_events(self):
        """Processa eventos do pygame (teclado, fechar janela)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        """Atualiza o estado do jogo: dino, obstáculos, estrela, score, sons."""
        user_input = pygame.key.get_pressed()
        # Atualiza nuvens
        for cloud in self.clouds:
            cloud.update(self.game_speed)
        if not self.game_over and not self.death_animating:
            if user_input[pygame.K_UP] and not self.dino.is_jumping:
                self.sound_manager.tocar_som_pulo()
            self.dino.update(user_input)
            # Obstáculos
            self.spawner.update(self.score, 50, 400, self.star_powerup and self.star_powerup.is_active())
            # Estrela: spawna a cada 400 pontos, 50% de chance
            if int(self.score) > 0 and int(self.score) % 400 == 0 and not self.star_powerup:
                if random.random() < 0.5:
                    self.star_powerup = StarPowerUp()
            # Atualiza estrela
            if self.star_powerup:
                self.star_powerup.update(self.game_speed, self.dino.rect)
                if self.star_powerup.is_active():
                    self.dino.set_rainbow_mode(True)
                    if not self.sound_manager.tocando_estrela():
                        self.sound_manager.parar_musica_fundo()
                        self.sound_manager.tocar_musica_estrela()
                else:
                    self.dino.set_rainbow_mode(False)
                    if self.sound_manager.tocando_estrela():
                        self.sound_manager.parar_musica_estrela()
                        self.sound_manager.tocar_musica_fundo()
                if self.star_powerup.is_collected() and not self.star_powerup.is_active():
                    self.star_powerup = None
            # Colisão com obstáculos
            for obstacle in list(self.spawner.obstacles):
                obstacle.update(self.game_speed, self.spawner.obstacles)
                if not (self.star_powerup and self.star_powerup.is_active()) and self.dino.get_hitbox().colliderect(obstacle.get_hitbox()):
                    self.sound_manager.tocar_som_morte()
                    self.sound_manager.parar_musica_fundo()
                    self.dino.die()
                    self.death_animating = True
                    return
            # Score
            self.score += 1/3  # Aproxima 1 ponto a cada 3 frames

    def draw(self):
        """Desenha todos os elementos do jogo na tela."""
        self.screen.fill((255, 255, 255))
        self.draw_background()
        for cloud in self.clouds:
            cloud.draw(self.screen)
        for obstacle in self.spawner.obstacles:
            obstacle.draw(self.screen)
        self.dino.draw(self.screen)
        if self.star_powerup:
            self.star_powerup.draw(self.screen)
        self.draw_score()
        pygame.display.update()

    def draw_background(self):
        """Desenha o fundo e move o chão."""
        image_width = BG.get_width()
        self.screen.blit(BG, (self.background_x1, 380))
        self.screen.blit(BG, (self.background_x2, 380))
        self.background_x1 -= self.game_speed
        self.background_x2 -= self.game_speed
        if self.background_x1 <= -image_width:
            self.background_x1 = self.background_x2 + image_width
        if self.background_x2 <= -image_width:
            self.background_x2 = self.background_x1 + image_width

    def draw_score(self):
        """Desenha o score e o high score na tela."""
        font = pygame.font.Font(FONT_STYLE, 16)
        high_score_text = font.render(f'High Score: {self.score_manager.get_high_score()}', True, (0, 0, 0))
        score_text = font.render(f'Score: {int(self.score)}', True, (0, 0, 0))
        self.screen.blit(high_score_text, (20, 5))
        self.screen.blit(score_text, (20, 25))

    def show_game_over_blocking(self):
        """Exibe a tela de game over e espera o jogador pressionar uma tecla."""
        from dino_runner.utils.constants import RESET_IMG
        img = RESET_IMG
        rect = img.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40))
        self.screen.blit(img, rect)
        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    self.sound_manager.tocar_som_button()
                    waiting = False
        pygame.event.clear()
        self.wait_keys_released()

    def show_start_screen(self):
        """Exibe a tela inicial com dinossauro parado (sprite DINO_START), nuvens passando, chão parado e placar."""
        from dino_runner.utils.constants import DINO_START
        # Garante dino parado
        self.dino.is_running = False
        self.dino.is_jumping = False
        self.dino.is_ducking = False
        self.dino.step_index = 0
        self.dino.image = DINO_START  # Sprite de início
        waiting = True
        while waiting and self.running:
            self.screen.fill((255, 255, 255))
            # Fundo e chão parados
            self.draw_background_static()
            # Nuvens se movendo
            for cloud in self.clouds:
                cloud.update(1)  # Movimento lento das nuvens
                cloud.draw(self.screen)
            # Dino parado
            self.dino.draw(self.screen)
            # Placar
            self.draw_score()
            pygame.display.update()
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    self.showing_start_screen = False
                    waiting = False
        pygame.event.clear()
        self.wait_keys_released()

    def draw_background_static(self):
        """Desenha o fundo e o chão parados (sem movimento)."""
        image_width = BG.get_width()
        self.screen.blit(BG, (0, 380))
        self.screen.blit(BG, (image_width, 380))

    def draw_start_text(self):
        """Desenha o texto de início na tela inicial."""
        font = pygame.font.Font(FONT_STYLE, 24)
        text = font.render('Pressione qualquer tecla para começar', True, (83, 83, 83))
        rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, rect)

    def wait_keys_released(self):
        """Aguarda até que todas as teclas estejam soltas."""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
            pressed = pygame.key.get_pressed()
            if not any(pressed):
                waiting = False
            else:
                pygame.time.delay(10) 

    def init_clouds(self):
        """Instancia de 7 a 10 nuvens distribuídas uniformemente na horizontal."""
        import random
        from dino_runner.utils.constants import SCREEN_WIDTH
        self.clouds = []
        num_clouds = random.randint(7, 10)
        min_gap = SCREEN_WIDTH // num_clouds
        positions = [i * min_gap + random.randint(0, min_gap // 2) for i in range(num_clouds)]
        random.shuffle(positions)
        for x in positions:
            cloud = Cloud()
            cloud.x = x
            self.clouds.append(cloud) 

    def draw_background_frozen(self):
        """Desenha o fundo e o chão parados na posição atual (sem mover)."""
        image_width = BG.get_width()
        self.screen.blit(BG, (self.background_x1, 380))
        self.screen.blit(BG, (self.background_x2, 380)) 