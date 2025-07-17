import pygame
from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING, DINO_DEAD

class Dino(pygame.sprite.Sprite):
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340    
    JUMP_VEL = 12

    def __init__(self):
        super().__init__()
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.duck_img = DUCKING
        self.image = self.run_img[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.pos_y = float(self.Y_POS)  # Posição vertical precisa
        self.is_running = True
        self.is_jumping = False
        self.is_ducking = False
        self.jump_vel = self.JUMP_VEL
        self.step_index = 0
        self.is_dead_anim = False
        self.death_anim_vx = 0
        self.death_anim_vy = 0

    def update(self, user_input):
        if hasattr(self, 'is_dead_anim') and self.is_dead_anim:
            # Animação de morte: vai para frente e para cima, depois cai
            self.rect.x += self.death_anim_vx
            self.pos_y += self.death_anim_vy
            self.death_anim_vy += 1  # gravidade
            self.rect.y = int(self.pos_y)
            # Se sair da tela, trava a posição
            if self.rect.y > 700 or self.rect.x > 1200:
                self.is_dead_anim = False
            return
        if self.is_running:
            self.run()
        if self.is_jumping and user_input[pygame.K_DOWN]:
            if not hasattr(self, 'fast_fall') or not self.fast_fall:
                self.fast_fall = True
                if self.jump_vel > 0:
                    self.jump_vel = 0
        if not self.is_jumping:
            self.fast_fall = False
        if self.is_jumping:
            self.jump()
        if self.is_ducking:
            self.duck()

        if user_input[pygame.K_UP] and not self.is_jumping:
            self.is_jumping = True
            self.is_running = False
            self.is_ducking = False
        elif user_input[pygame.K_DOWN] and not self.is_jumping:
            self.is_ducking = True
            self.is_running = False
            self.is_jumping = False
        elif not self.is_jumping:
            self.is_running = True
            self.is_ducking = False
            self.is_jumping = False

        if self.step_index >= 10:
            self.step_index = 0

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.rect.y = self.Y_POS
        self.pos_y = float(self.Y_POS)
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.is_jumping:
            gravity = 0.6
            if hasattr(self, 'fast_fall') and self.fast_fall:
                gravity = 1.2  # Gravidade maior para fast fall
            self.pos_y -= self.jump_vel * 1.5
            self.jump_vel -= gravity
            # Corrige se passar do chão
            if self.pos_y > self.Y_POS:
                self.pos_y = float(self.Y_POS)
                self.is_jumping = False
                self.jump_vel = self.JUMP_VEL
                self.fast_fall = False
        self.rect.y = int(self.pos_y)

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def die(self):
        from dino_runner.utils.constants import DINO_DEAD
        self.image = DINO_DEAD
        self.is_dead_anim = True
        self.death_anim_vx = 7  # velocidade horizontal para frente
        self.death_anim_vy = -13  # impulso inicial para cima

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