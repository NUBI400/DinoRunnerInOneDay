import pygame
from typing import List
from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING, DINO_DEAD
import os

class Dino(pygame.sprite.Sprite):
    """
    Classe do personagem principal (Dino). Gerencia animações, saltos, agachamentos e modo arco-íris.
    """
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340    
    JUMP_VEL = 12
    RAINBOW_COLORS = ['Red', 'Orange', 'Green', 'Blue']

    def __init__(self):
        super().__init__()
        # Imagens padrão
        self.run_img: List[pygame.Surface] = RUNNING
        self.jump_img: List[pygame.Surface] = [JUMPING]
        self.duck_img: List[pygame.Surface] = DUCKING
        # Imagens arco-íris
        self.rainbow_run_imgs = self.load_rainbow_imgs('DinoRun')
        self.rainbow_jump_imgs = self.load_rainbow_imgs('DinoJump')
        self.rainbow_duck_imgs = self.load_rainbow_imgs('DinoDuck')
        self.image = self.run_img[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.pos_y = float(self.Y_POS)
        self.is_running = True
        self.is_jumping = False
        self.is_ducking = False
        self.jump_vel = self.JUMP_VEL
        self.step_index = 0
        self.is_dead_anim = False
        self.death_anim_vx = 0
        self.death_anim_vy = 0
        self.rainbow_mode = False
        self.rainbow_index = 0

    def load_rainbow_imgs(self, prefix):
        """
        Carrega as imagens do dino em modo arco-íris para cada ação.
        """
        base_path = os.path.join('dino_runner', 'assets', 'Dino', 'dino_arcoires')
        imgs = []
        if prefix == 'DinoRun':
            for i in [1,2]:
                imgs.append([
                    pygame.image.load(os.path.join(base_path, f'{prefix}{i}_Red.png')),
                    pygame.image.load(os.path.join(base_path, f'{prefix}{i}_Orange.png')),
                    pygame.image.load(os.path.join(base_path, f'{prefix}{i}_Green.png')),
                    pygame.image.load(os.path.join(base_path, f'{prefix}{i}_Blue.png')),
                ])
            return imgs
        elif prefix == 'DinoJump':
            return [
                pygame.image.load(os.path.join(base_path, f'{prefix}_Red.png')),
                pygame.image.load(os.path.join(base_path, f'{prefix}_Orange.png')),
                pygame.image.load(os.path.join(base_path, f'{prefix}_Green.png')),
                pygame.image.load(os.path.join(base_path, f'{prefix}_Blue.png')),
            ]
        elif prefix == 'DinoDuck':
            return [
                [pygame.image.load(os.path.join(base_path, f'{prefix}1_Red.png')),
                 pygame.image.load(os.path.join(base_path, f'{prefix}1_Orange.png')),
                 pygame.image.load(os.path.join(base_path, f'{prefix}1_Green.png')),
                 pygame.image.load(os.path.join(base_path, f'{prefix}1_Blue.png'))],
                [pygame.image.load(os.path.join(base_path, f'{prefix}2_Red.png')),
                 pygame.image.load(os.path.join(base_path, f'{prefix}2_Orange.png')),
                 pygame.image.load(os.path.join(base_path, f'{prefix}2_Green.png')),
                 pygame.image.load(os.path.join(base_path, f'{prefix}2_Blue.png'))]
            ]
        return []

    def set_rainbow_mode(self, active):
        """
        Ativa ou desativa o modo arco-íris. Reinicia o índice de cor apenas se houver mudança.
        """
        if self.rainbow_mode != active:
            self.rainbow_index = 0
        self.rainbow_mode = active

    def update(self, user_input):
        """
        Atualiza o estado do dino conforme input do usuário e animações.
        """
        if hasattr(self, 'is_dead_anim') and self.is_dead_anim:
            self.rect.x += self.death_anim_vx
            self.pos_y += self.death_anim_vy
            self.death_anim_vy += 1
            self.rect.y = int(self.pos_y)
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
        """
        Atualiza a animação de corrida do dino, incluindo modo arco-íris.
        """
        if self.rainbow_mode:
            color_idx = (self.rainbow_index // 2) % 4
            frame = (self.step_index // 5) % 2
            self.image = self.rainbow_run_imgs[frame][color_idx]
            self.rainbow_index = (self.rainbow_index + 1) % 8
        else:
            self.image = self.run_img[self.step_index // 5]
        self.rect.y = self.Y_POS
        self.pos_y = float(self.Y_POS)
        self.step_index += 1

    def jump(self):
        """
        Atualiza a animação de pulo do dino, incluindo modo arco-íris.
        """
        if self.rainbow_mode:
            color_idx = (self.rainbow_index // 2) % 4
            self.image = self.rainbow_jump_imgs[color_idx]
            self.rainbow_index = (self.rainbow_index + 1) % 8
        else:
            self.image = self.jump_img[0]
        if self.is_jumping:
            gravity = 0.6
            if hasattr(self, 'fast_fall') and self.fast_fall:
                gravity = 1.2
            self.pos_y -= self.jump_vel * 1.5
            self.jump_vel -= gravity
            if self.pos_y > self.Y_POS:
                self.pos_y = float(self.Y_POS)
                self.is_jumping = False
                self.jump_vel = self.JUMP_VEL
                self.fast_fall = False
        self.rect.y = int(self.pos_y)

    def duck(self):
        """
        Atualiza a animação de agachamento do dino, incluindo modo arco-íris.
        """
        if self.rainbow_mode:
            color_idx = (self.rainbow_index // 2) % 4
            frame = (self.step_index // 5) % 2
            self.image = self.rainbow_duck_imgs[frame][color_idx]
            self.rainbow_index = (self.rainbow_index + 1) % 8
        else:
            self.image = self.duck_img[self.step_index // 5]
        self.rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def die(self):
        """
        Inicia a animação de morte do dino.
        """
        from dino_runner.utils.constants import DINO_DEAD
        self.image = DINO_DEAD
        self.is_dead_anim = True
        self.death_anim_vx = 7
        self.death_anim_vy = -13

    def draw(self, screen):
        """
        Desenha o dino na tela.
        """
        screen.blit(self.image, self.rect)

    def get_hitbox(self):
        """
        Retorna um retângulo menor para colisão, facilitando a jogabilidade.
        """
        hitbox = self.rect.copy()
        hitbox.width = int(hitbox.width * 0.7)
        hitbox.height = int(hitbox.height * 0.8)
        hitbox.x += int(self.rect.width * 0.15)
        hitbox.y += int(self.rect.height * 0.1)
        return hitbox 