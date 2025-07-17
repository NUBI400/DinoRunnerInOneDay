import pygame
import os
import random

# Diretório dos sons
SOND_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'sonds')
MUSICA_FUNDO = os.path.join(SOND_DIR, 'musica_fundo.wav')
SOM_MORTE = os.path.join(SOND_DIR, 'morte.mp3')
SOM_PULO1 = os.path.join(SOND_DIR, 'pulo.wav')
SOM_PULO2 = os.path.join(SOND_DIR, 'pulo2.mp3')
SOM_BUTTON = os.path.join(SOND_DIR, 'button.wav')
ESTRELA_MARIO = os.path.join(SOND_DIR, 'estrelamario.mp3')

class SoundManager:
    """
    Gerencia todos os sons e músicas do jogo.
    Controla volumes, efeitos e troca de trilha sonora.
    """
    def __init__(self):
        pygame.mixer.init()
        # Efeitos sonoros
        self.som_pulos = [pygame.mixer.Sound(SOM_PULO1), pygame.mixer.Sound(SOM_PULO2)]
        for som in self.som_pulos:
            som.set_volume(0.12)  # Volume reduzido em 40%
        self.som_morte = pygame.mixer.Sound(SOM_MORTE)
        self.som_morte.set_volume(0.156)  # Volume de morte 30% maior
        self.som_button = pygame.mixer.Sound(SOM_BUTTON)
        self.som_button.set_volume(0.12)
        # Trilha sonora
        self.musica_fundo = MUSICA_FUNDO
        self.musica_estrela = ESTRELA_MARIO
        self._estrela_tocando = False

    def tocar_musica_fundo(self):
        """Toca a música de fundo em loop com volume reduzido."""
        pygame.mixer.music.load(self.musica_fundo)
        pygame.mixer.music.set_volume(0.42)
        pygame.mixer.music.play(-1)
        self._estrela_tocando = False

    def parar_musica_fundo(self):
        """Para a música de fundo."""
        pygame.mixer.music.stop()

    def tocar_musica_estrela(self):
        """Toca a música da estrela do Mario em loop com volume reduzido."""
        pygame.mixer.music.load(self.musica_estrela)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        self._estrela_tocando = True

    def parar_musica_estrela(self):
        """Para a música da estrela."""
        pygame.mixer.music.stop()
        self._estrela_tocando = False

    def tocar_som_pulo(self):
        """Toca um dos sons de pulo aleatoriamente."""
        random.choice(self.som_pulos).play()

    def tocar_som_morte(self):
        """Toca o som de morte."""
        self.som_morte.play()

    def tocar_som_button(self):
        """Toca o som de botão pressionado."""
        self.som_button.play()

    def tocando_estrela(self):
        """Retorna True se a música da estrela está tocando."""
        return self._estrela_tocando 