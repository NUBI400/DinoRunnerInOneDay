# Dino Runner - Estrutura e Explicação do Projeto

Este projeto é um clone do famoso jogo Dino Runner, implementado em Python com Pygame. O código foi modularizado para facilitar a manutenção, entendimento e expansão. Abaixo está a explicação de cada parte do projeto, o que cada arquivo faz e um resumo dos principais códigos.

## Estrutura de Pastas

```
dino_runner/
  ├── assets/           # Imagens, sons e fontes do jogo
  ├── components/       # Componentes principais do jogo (Dino, obstáculos, powerups, etc)
  │   ├── obstacles/    # Obstáculos e lógica de spawn
  │   ├── powerups/     # Power-ups (estrela, escudo, etc)
  │   ├── dino.py       # Classe do personagem principal
  │   ├── game.py       # Loop principal e orquestração do jogo
  │   ├── score_manager.py # Gerenciamento de score e highscore
  │   ├── sound_manager.py # Gerenciamento de sons e músicas
  │   ├── cloud.py      # Classe das nuvens
  ├── utils/            # Constantes e utilitários
  ├── main.py           # Ponto de entrada do jogo
  ├── highscore.txt     # Armazena o highscore
  ├── EXPLICACAO_PROJETO.md # Este arquivo de explicação
  ├── requirements.txt  # Dependências do projeto
```

## Descrição dos Arquivos e Códigos

### main.py
- **Função:** Ponto de entrada do jogo. Inicializa e executa a classe `Game`.
- **Código principal:**
```python
from dino_runner.components.game import Game

game = Game()
game.execute()
```

### dino_runner/components/game.py
- **Função:** Orquestra o loop principal do jogo, integrando todos os componentes (Dino, obstáculos, powerups, sons, score, etc).
- **Responsabilidades:**
  - Loop principal (`run`)
  - Atualização do estado do jogo (`update`)
  - Desenho dos elementos na tela (`draw`)
  - Controle de eventos e game over
  - Delegação para managers de som, score, obstáculos e powerups


### dino_runner/components/dino.py
- **Função:** Classe do personagem principal (Dino). Gerencia animações, saltos, agachamentos, colisão e modo arco-íris.
- **Resumo:**
  - Métodos para correr, pular, agachar, morrer e desenhar.
  - Suporte ao modo arco-íris ativado pela estrela.
  - Docstrings e comentários em todos os métodos.

### dino_runner/components/obstacles/spawner.py
- **Função:** Gerencia o spawn de obstáculos (cactos e pássaros) e sinaliza quando deve spawnar uma estrela.
- **Resumo:**
  - Mantém lista de obstáculos ativos.
  - Decide quando spawnar obstáculos e estrela.
  - Reset para nova partida.

### dino_runner/components/obstacles/obstacle.py, cactus.py, bird.py
- **Função:**
  - `obstacle.py`: Classe base para obstáculos.
  - `cactus.py` e `bird.py`: Implementações específicas dos obstáculos.
- **Resumo:**
  - Métodos para atualização, desenho e colisão dos obstáculos.

### dino_runner/components/powerups/star.py
- **Função:** Gerencia o comportamento da estrela (spawn, ativação, duração, desenho).
- **Resumo:**
  - Ativa modo arco-íris e música especial ao ser coletada.
  - Controla duração do efeito.

### dino_runner/components/powerups/shield.py, power_up.py
- **Função:**
  - `power_up.py`: Classe base para powerups.
  - `shield.py`: Implementação do escudo.

### dino_runner/components/score_manager.py
- **Função:** Gerencia o highscore do jogo, salvando e carregando de arquivo.
- **Resumo:**
  - Métodos para salvar, carregar e retornar o highscore.

### dino_runner/components/sound_manager.py
- **Função:** Gerencia todos os sons e músicas do jogo.
- **Resumo:**
  - Controla volumes, efeitos e troca de trilha sonora (fundo e estrela).
  - Métodos para tocar sons de pulo, morte, botão, música de fundo e música da estrela.

### dino_runner/components/cloud.py
- **Função:** Classe das nuvens, para efeito visual no fundo.

### dino_runner/utils/constants.py
- **Função:** Armazena todas as constantes do jogo (imagens, sons, posições, etc).

### dino_runner/assets/
- **Função:** Armazena todos os arquivos de imagem, som e fonte usados no jogo.
  - `Dino/`, `Cactus/`, `Bird/`, `Other/`, `font/`, `sonds/`, `star/`: Subpastas organizadas por tipo de asset.

### highscore.txt
- **Função:** Armazena o maior score já atingido pelo jogador.

### requirements.txt
- **Função:** Lista as dependências do projeto (ex: pygame).

---

## Resumo do Fluxo do Jogo
1. O usuário executa `main.py`, que instancia e executa o `Game`.
2. O `Game` inicializa todos os componentes e entra no loop principal.
3. O Dino pode correr, pular e agachar, desviando de obstáculos.
4. Obstáculos e powerups (estrela) aparecem conforme o score.
5. Ao pegar a estrela, o Dino fica colorido e toca a música especial.
6. O score e o highscore são atualizados e exibidos na tela.
7. Sons e músicas são controlados pelo `SoundManager`.
8. O jogo reinicia ao morrer, mantendo o highscore salvo.

---

Se precisar de detalhes de implementação de algum arquivo específico, consulte o próprio código, que está todo comentado e modularizado! 