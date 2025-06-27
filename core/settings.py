SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 720
CAPTION: str = "A Lenda da Espada Crescente"
FPS: int = 60

# Cores (em RGB)
WHITE: tuple[int, int, int] = (255, 255, 255)
BLACK: tuple[int, int, int] = (0, 0, 0)
GREEN: tuple[int, int, int] = (0, 255, 0)
RED: tuple[int, int, int] = (255, 0, 0)
BLUE: tuple[int, int, int] = (0, 0, 255)
YELLOW: tuple[int, int, int] = (255, 255, 0)

# Configurações do Jogador
PLAYER_SPEED: int = 5
PLAYER_HEALTH: int = 100

# Configurações da Espada
SWORD_GROWTH_PER_COIN: float = 0.5 # 0.5 unidades de crescimento por moeda (multiplicado por um fator para ficar visível)
COINS_FOR_SWORD_LEVEL_UP: int = 5 # A cada 5 moedas coletadas, a espada aumenta de tamanho

# Ganhos
COINS_PER_TREE_CUT: int = 1
COINS_PER_MONSTER_KILL: int = 3
COINS_PER_DRAGON_KILL: int = 50 # Dragão dá mais moedas

# Volumes (serão configuráveis no menu)
MUSIC_VOLUME: float = 0.5
SFX_VOLUME: float = 0.7

# Caminhos de Assets
ASSETS_DIR: str = "assets/"
IMAGE_DIR: str = ASSETS_DIR + "images/"
SOUND_DIR: str = ASSETS_DIR + "sounds/"
FONT_DIR: str = ASSETS_DIR + "fonts/"
