# Estrutura do Projeto Dino Runner

Este projeto é uma versão do famoso Dino Runner (jogo do dinossauro do Chrome) feita em Python usando a biblioteca Pygame. Abaixo está uma explicação de cada parte do projeto para te ajudar a entender como tudo se conecta.

## Estrutura de Pastas

```
DinoRunnerInOneDay/
│
├── dino_runner/
│   ├── assets/
│   │   ├── Dino/         # Sprites do dinossauro (correndo, pulando, agachando, etc)
│   │   ├── Cactus/       # Sprites dos cactos (obstáculos)
│   │   ├── Bird/         # Sprites dos pássaros (outro obstáculo)
│   │   └── Other/        # Outros recursos gráficos (fundo, corações, power-ups, etc)
│   │
│   ├── components/
│   │   ├── obstacles/    # Código dos obstáculos (cactos e pássaros)
│   │   └── powerups/     # Código dos power-ups (ex: escudo)
│   │
│   ├── utils/            # Utilitários e constantes do jogo
│   └── __init__.py       # Torna a pasta um pacote Python
│
├── main.py               # Arquivo principal para rodar o jogo
├── README.md             # Instruções gerais do projeto
├── requirements.txt      # Dependências do Python
└── venv/                 # Ambiente virtual Python (pode ser ignorado)
```

---

## Detalhamento das Pastas e Arquivos

### dino_runner/assets/
Contém todos os arquivos de imagem e mídia usados no jogo.

- **Dino/**: Imagens do dinossauro em diferentes estados (correndo, pulando, agachado, com escudo, com martelo, etc).
- **Cactus/**: Imagens dos cactos grandes e pequenos, que são obstáculos.
- **Bird/**: Imagens dos pássaros, outro tipo de obstáculo.
- **Other/**: Outros recursos gráficos, como:
  - `Track.png`: imagem do chão
  - `Cloud.png`: nuvem
  - `GameOver.png`: tela de game over
  - `Reset.png`: botão de reset
  - `SmallHeart.png`: coração (vidas)
  - `shield.png`, `hammer.png`: power-ups
  - `Chrome Dino.gif`/`.mp4`: mídia de referência

### dino_runner/components/
Contém o código dos componentes principais do jogo.

- **obstacles/**: Código dos obstáculos.
  - `cactus.py`: Lógica dos cactos.
  - `bird.py`: Lógica dos pássaros.
- **powerups/**: Código dos power-ups.
  - `shield.py`: Lógica do escudo.

### dino_runner/utils/
Funções utilitárias e constantes globais do jogo.

- `constants.py`: Define constantes como tamanho da tela, caminhos das imagens, tipos de power-ups, etc.
- `text_utils.py`: Funções para desenhar textos na tela (ex: placar, mensagens).

### main.py
Arquivo principal que inicia o jogo. É aqui que normalmente você importa a classe principal do jogo e executa o loop principal.

### requirements.txt
Lista as bibliotecas Python necessárias para rodar o projeto (ex: pygame).

### venv/
Ambiente virtual Python. Isola as dependências do projeto. Não precisa se preocupar com essa pasta para entender o código.

---

## Observações

- O projeto está estruturado para facilitar a organização do código e dos recursos gráficos.
- Se faltar algum arquivo (como o principal do jogo), pode ser necessário criá-lo para o jogo funcionar.
- A lógica do jogo (movimentação, colisão, pontuação, etc) normalmente fica em uma classe principal, que pode estar faltando no seu projeto.

---

Se quiser, posso complementar explicando como funciona a lógica de cada parte ou ajudar a criar o arquivo principal do jogo! 

---

## Explicação de Todos os Códigos do Projeto

### main.py
Responsável por iniciar o jogo. Importa a classe principal do jogo (`Game`) e executa o método `execute()` para rodar o loop principal.

> **Nota:** O arquivo `game.py` está faltando, por isso o jogo não inicia. Normalmente, ele conteria a lógica principal do jogo.

### dino_runner/components/obstacles/cactus.py
Define o obstáculo "Cacto" do jogo. Usa imagens de cactos grandes e pequenos, sorteia aleatoriamente o tipo e a posição do cacto. Herda de uma classe base chamada `Obstacle` (referenciada, mas não encontrada no projeto).

### dino_runner/components/obstacles/bird.py
Define o obstáculo "Pássaro" do jogo. Usa imagens de pássaros, define a posição vertical fixa do pássaro e possui um método `draw` para animar o bater de asas alternando as imagens. Também herda de `Obstacle` (referenciado, mas não encontrado).

### dino_runner/components/obstacles/__init__.py
Arquivo vazio. Serve para indicar ao Python que a pasta `obstacles` é um pacote, permitindo importar seus módulos.

### dino_runner/components/powerups/shield.py
Define o power-up "Escudo". Usa a imagem e o tipo de escudo definidos nas constantes. Herda de uma classe base chamada `PowerUp` (referenciada, mas não encontrada).

### dino_runner/components/powerups/__init__.py
Arquivo vazio. Serve para indicar ao Python que a pasta `powerups` é um pacote, permitindo importar seus módulos.

### dino_runner/components/__init__.py
Arquivo vazio. Serve para indicar ao Python que a pasta `components` é um pacote.

### dino_runner/utils/constants.py
Contém todas as constantes globais do jogo: título, tamanho da tela, FPS, caminhos das imagens, sprites do dinossauro, obstáculos, power-ups, fundo, etc. Centraliza valores fixos usados em todo o projeto.

### dino_runner/utils/text_utils.py
Funções utilitárias para desenhar textos na tela. Define cor, tamanho e fonte padrão. Função `draw_message_component` desenha uma mensagem centralizada na tela, útil para placar, mensagens de início/fim de jogo, etc.

### dino_runner/utils/__init__.py
Arquivo vazio. Serve para indicar ao Python que a pasta `utils` é um pacote.

### dino_runner/__init__.py
Arquivo vazio. Serve para indicar ao Python que a pasta `dino_runner` é um pacote.

---

### Sobre arquivos referenciados mas ausentes
- **dino_runner/components/obstacles/obstacle.py**: Deveria conter a classe base `Obstacle`, da qual os obstáculos (cacto, pássaro) herdam comportamento comum (como colisão, movimentação, etc).
- **dino_runner/components/powerups/power_up.py**: Deveria conter a classe base `PowerUp`, da qual os power-ups (como escudo) herdam comportamento comum.
- **dino_runner/components/game.py**: Deveria conter a classe principal do jogo (`Game`), responsável pelo loop principal, controle de fases, placar, etc.

Se esses arquivos não existirem, o jogo não funcionará corretamente. Se precisar, posso te ajudar a criar versões básicas deles! 