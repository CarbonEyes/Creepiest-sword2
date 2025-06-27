import pygame
from core.settings import ASSETS_DIR # [cite: 9a]

class Platform(pygame.sprite.Sprite):
    """
    Representa uma plataforma estática no cenário sobre a qual o jogador pode ficar.
    """
    def __init__(self, x: int, y: int, width: int, height: int, initial_data: dict = None) -> None:
        """
        Inicializa uma plataforma.
        Args:
            x (int): Posição inicial X da plataforma (topleft).
            y (int): Posição inicial Y da plataforma (topleft).
            width (int): Largura da plataforma.
            height (int): Altura da plataforma.
            initial_data (dict | None): Dados para restaurar o estado da plataforma (para save/load).
        """
        super().__init__()
        
        # Tenta carregar uma imagem para a plataforma, caso contrário, usa um placeholder
        try:
            # Assumimos uma imagem de plataforma genérica ou de "grama"
            self.image = pygame.image.load(ASSETS_DIR + "images/platform.png").convert_alpha() # [cite: 9a]
            self.image = pygame.transform.scale(self.image, (width, height)) # Redimensiona para o tamanho especificado [cite: 9a]
        except pygame.error:
            print("Erro: Imagem da plataforma (platform.png) não encontrada. Usando um retângulo cinza como placeholder.")
            self.image = pygame.Surface((width, height), pygame.SRCALPHA) # Placeholder [cite: 9a]
            self.image.fill((100, 100, 100)) # Cinza
            pygame.draw.rect(self.image, (150, 150, 150), (0, 0, width, height), 2) # Borda

        self.rect = self.image.get_rect(topleft=(x, y)) # Retângulo de colisão/posição [cite: 9a]

        # Para o sistema de save/load
        if initial_data:
            self.from_dict(initial_data)

    def to_dict(self) -> dict:
        """Converte o estado da plataforma em um dicionário para salvamento."""
        return {
            "x": self.rect.x,
            "y": self.rect.y,
            "width": self.rect.width,
            "height": self.rect.height
        }

    def from_dict(self, data: dict) -> None:
        """Restaura o estado da plataforma a partir de um dicionário."""
        self.rect.x = data.get("x", self.rect.x)
        self.rect.y = data.get("y", self.rect.y)
        # Se a imagem for redimensionada no init, width/height não precisam ser setados diretamente no rect
        # self.rect.width = data.get("width", self.rect.width)
        # self.rect.height = data.get("height", self.rect.height)
