import pygame
from dino_runner.utils.constants import SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, ICON, BG, GAME_OVER_IMG, FONT_STYLE
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.powerups.shield import Shield
from dino_runner.components.dino import Dino  # NOVO: Importa o dinossauro
import random
from dino_runner.components.cloud import Cloud
import os

SOND_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'sonds')
MUSICA_FUNDO = os.path.join(SOND_DIR, 'musica_fundo.wav')
SOM_MORTE = os.path.join(SOND_DIR, 'morte.mp3')
SOM_PULO1 = os.path.join(SOND_DIR, 'pulo.wav')
SOM_PULO2 = os.path.join(SOND_DIR, 'pulo2.mp3')
SOM_BUTTON = os.path.join(SOND_DIR, 'button.wav')

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = False
        self.playing = False
        self.game_speed = 10
        self.obstacles = []
        self.power_ups = []
        self.dino = Dino()  # NOVO: Instancia o dinossauro
        self.background_x1 = 0  # NOVO: posição do primeiro chão
        self.background_x2 = BG.get_width()  # NOVO: posição do segundo chão
        self.game_over = False  # NOVO: Flag de game over
        self.next_obstacle_score = 50  # Só começa a instanciar obstáculos após 50 pontos
        self.next_bird_score = 400     # Só começa a instanciar pássaros após 400 pontos
        self.next_obstacle_distance = 0  # Controle de distância aleatória
        self.clouds = [Cloud() for _ in range(random.randint(2, 4))]
        self.death_animating = False
        self.high_score = self.load_high_score()
        self.som_pulos = [pygame.mixer.Sound(SOM_PULO1), pygame.mixer.Sound(SOM_PULO2)]
        for som in self.som_pulos:
            som.set_volume(0.2)
        self.som_morte = pygame.mixer.Sound(SOM_MORTE)
        self.som_button = pygame.mixer.Sound(SOM_BUTTON)
        self.musica_fundo = MUSICA_FUNDO

    def tocar_musica_fundo(self):
        pygame.mixer.music.load(self.musica_fundo)
        pygame.mixer.music.play(-1)  # Loop infinito

    def parar_musica_fundo(self):
        pygame.mixer.music.stop()

    def tocar_som_pulo(self):
        random.choice(self.som_pulos).play()

    def tocar_som_morte(self):
        self.som_morte.play()

    def tocar_som_button(self):
        self.som_button.play()

    def execute(self):
        self.running = True
        while self.running:
            self.run(show_start=True)

    def load_high_score(self):
        try:
            with open('highscore.txt', 'r') as f:
                return int(f.read().strip())
        except Exception:
            return 0

    def save_high_score(self):
        try:
            with open('highscore.txt', 'w') as f:
                f.write(str(self.high_score))
        except Exception:
            pass

    def run(self, show_start=False):
        self.playing = True
        self.game_over = False
        self.death_animating = False
        self.obstacles = []
        self.power_ups = []
        self.dino = Dino()  # Reinicia o dino a cada jogo
        self.background_x1 = 0  # Resetar ao iniciar
        self.background_x2 = BG.get_width()  # Resetar ao iniciar
        self.score = 0.0    # Placar em float para precisão
        self.game_speed = 10.0  # Velocidade inicial igual ao Dino original
        self.max_speed = 20.0   # Velocidade máxima igual ao Dino original
        self.acceleration = 0.001  # Aceleração igual ao Dino original
        self.frame_count = 0
        self.next_obstacle_score = 50
        self.next_bird_score = 400
        self.next_obstacle_distance = 0
        self.clouds = []
        for _ in range(random.randint(2, 4)):
            cloud = Cloud()
            cloud.x = float(random.randint(0, SCREEN_WIDTH))
            self.clouds.append(cloud)
        # Estado de tela inicial
        if show_start:
            from dino_runner.utils.constants import DINO_START, FONT_STYLE
            dino_start_img = DINO_START
            dino_rect = dino_start_img.get_rect()
            dino_rect.x = 80
            dino_rect.y = 310
            waiting = True
            self.tocar_musica_fundo()
            while waiting and self.running:
                self.screen.fill((255, 255, 255))
                # Fundo parado
                self.screen.blit(BG, (self.background_x1, 380))
                self.screen.blit(BG, (self.background_x2, 380))
                # Nuvens passando devagar e suave
                for cloud in self.clouds:
                    cloud.x -= cloud.speed * 0.5  # Suave e visível
                    if cloud.x < -cloud.image.get_width():
                        cloud.x = float(random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 800))
                        cloud.y = random.randint(50, 200)
                        cloud.speed = random.uniform(1, 2.5)
                    cloud.draw(self.screen)
                # Dino parado
                self.screen.blit(dino_start_img, dino_rect)
                # Placar e velocidade alinhados
                font = pygame.font.Font(FONT_STYLE, 16)
                high_score_text = font.render(f'High Score: {self.high_score}', True, (0, 0, 0))
                score_text = font.render(f'Score: {int(self.score)}', True, (0, 0, 0))
                speed_text = font.render(f'Vel: {self.game_speed:.1f}', True, (0, 0, 0))
                self.screen.blit(high_score_text, (20, 5))
                self.screen.blit(score_text, (20, 25))
                self.screen.blit(speed_text, (20, 45))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        waiting = False
                    if event.type == pygame.KEYDOWN:
                        self.tocar_som_button()
                        waiting = False
                pygame.time.delay(16)
            pygame.event.clear()
            self.wait_keys_released()
        # Após sair do estado inicial, começa o loop normal mantendo cenário, nuvens e dino
        self.tocar_musica_fundo()
        while self.playing and self.running:
            self.handle_events()
            if not self.death_animating and not self.game_over:
                self.update()
                self.draw()
                self.clock.tick(60)
                if self.game_speed < self.max_speed:
                    self.game_speed = min(self.game_speed + self.acceleration, self.max_speed)
                self.frame_count += 1
                if self.frame_count % 3 == 0:
                    self.score += 1
            elif self.death_animating:
                # Só anima o Dino morto
                self.dino.update({})
                self.draw()
                self.clock.tick(60)
                if not getattr(self.dino, 'is_dead_anim', False):
                    self.death_animating = False
                    self.game_over = True
            elif self.game_over:
                # Atualiza high score se necessário
                if int(self.score) > self.high_score:
                    self.high_score = int(self.score)
                    self.save_high_score()
                self.parar_musica_fundo()
                self.draw()
                self.show_game_over_blocking()
                # Reinicia imediatamente após tecla
                return

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()  # NOVO: Captura input do teclado
        if not self.game_over and not self.death_animating:
            # Som de pulo
            if user_input[pygame.K_UP] and not self.dino.is_jumping:
                self.tocar_som_pulo()
            self.dino.update(user_input)           # NOVO: Atualiza o dino
            if self.score >= self.next_obstacle_score:
                if len(self.obstacles) == 0 or (self.obstacles and self.obstacles[-1].rect.x < (SCREEN_WIDTH - self.next_obstacle_distance)):
                    if self.score >= self.next_bird_score and random.randint(1, 5) == 1:
                        self.obstacles.append(Bird())
                    else:
                        self.obstacles.append(Cactus())
                    self.next_obstacle_distance = random.randint(400, 1000)
            for obstacle in list(self.obstacles):
                obstacle.update(self.game_speed, self.obstacles)
                # Colisão usando hitboxes reduzidas
                if self.dino.get_hitbox().colliderect(obstacle.get_hitbox()):
                    self.tocar_som_morte()
                    self.parar_musica_fundo()
                    self.dino.die()
                    self.death_animating = True
                    return

    def draw(self):
        self.screen.fill((255, 255, 255))
        if self.death_animating:
            # Desenha o fundo e objetos parados
            image_width = BG.get_width()
            self.screen.blit(BG, (self.background_x1, 380))
            self.screen.blit(BG, (self.background_x2, 380))
            for cloud in self.clouds:
                cloud.draw(self.screen)
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)
            for power_up in self.power_ups:
                power_up.draw(self.screen)
            self.dino.draw(self.screen)
            self.draw_score()
            pygame.display.update()
            return
        self.draw_background()
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        for power_up in self.power_ups:
            power_up.draw(self.screen)
        self.dino.draw(self.screen)
        self.draw_score()
        pygame.display.update()

    def draw_background(self):
        if self.death_animating:
            # Não atualiza fundo nem nuvens durante animação de morte
            return
        image_width = BG.get_width()
        self.screen.blit(BG, (self.background_x1, 380))
        self.screen.blit(BG, (self.background_x2, 380))
        # Desenha e atualiza nuvens
        for cloud in self.clouds:
            cloud.update(self.game_speed)
            cloud.draw(self.screen)
        self.background_x1 -= self.game_speed
        self.background_x2 -= self.game_speed
        # Reposicionamento robusto para evitar teleporte
        if self.background_x1 <= -image_width:
            self.background_x1 = self.background_x2 + image_width
        if self.background_x2 <= -image_width:
            self.background_x2 = self.background_x1 + image_width

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 36)
        text = font.render('Pressione qualquer tecla para jogar', True, (0, 0, 0))
        rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, rect)
        pygame.display.update()
        self.wait_for_key()
        pygame.event.clear()  # Limpa eventos para não afetar o Dino
        self.wait_keys_released()  # Aguarda todas as teclas serem soltas

    def wait_for_key(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    self.playing = True
                    waiting = False 

    def draw_score(self):
        from dino_runner.utils.constants import FONT_STYLE
        font = pygame.font.Font(FONT_STYLE, 16)
        high_score_text = font.render(f'High Score: {self.high_score}', True, (0, 0, 0))
        score_text = font.render(f'Score: {int(self.score)}', True, (0, 0, 0))
        speed_text = font.render(f'Vel: {self.game_speed:.1f}', True, (0, 0, 0))
        self.screen.blit(high_score_text, (20, 5))
        self.screen.blit(score_text, (20, 25))
        self.screen.blit(speed_text, (20, 45))

    def show_game_over(self):
        # Exibe o PNG de Game Over centralizado
        img = GAME_OVER_IMG
        rect = img.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40))
        self.screen.blit(img, rect)
        font_small = pygame.font.Font(None, 36)
        text2 = font_small.render('Pressione qualquer tecla para recomeçar', True, (0, 0, 0))
        rect2 = text2.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
        self.screen.blit(text2, rect2)
        pygame.display.update()
        self.wait_for_key()
        self.game_over = False 

    def show_game_over_blocking(self):
        from dino_runner.utils.constants import RESET_IMG, FONT_STYLE
        # Exibe o PNG de Reset centralizado
        img = RESET_IMG
        rect = img.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40))
        self.screen.blit(img, rect)
        pygame.display.update()
        # Espera tecla sem múltiplas confirmações
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    self.tocar_som_button()
                    waiting = False
        pygame.event.clear()  # Limpa eventos para não afetar o Dino
        self.wait_keys_released()  # Aguarda todas as teclas serem soltas

    def wait_keys_released(self):
        # Aguarda até que todas as teclas estejam soltas, processando eventos
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