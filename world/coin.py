import pygame
from core.settings import SCREEN_HEIGHT #

class Coin(pygame.sprite.Sprite):
    """
    Representa uma moeda que o jogador pode coletar.
    Possui física de queda simples.
    """
    def __init__(self, x: int, y: int, value: int = 1, initial_data: dict = None) -> None:
        """
        Inicializa uma moeda.
        Args:
            x (int): Posição inicial X.
            y (int): Posição inicial Y.
            value (int): Valor da moeda.
            initial_data (dict | None): Dados para restaurar o estado da moeda.
        """
        super().__init__()
        try:
            self.image = pygame.image.load("assets/images/coin.png").convert_alpha() #
            self.image = pygame.transform.scale(self.image, (40, 40)) #
        except pygame.error:
            print("Erro: Imagem da moeda (coin.png) não encontrada. Usando um círculo amarelo como placeholder.")
            self.image = pygame.Surface((40, 40), pygame.SRCALPHA) #
            pygame.draw.circle(self.image, (255, 255, 0), (20, 20), 20) #
        
        self.rect = self.image.get_rect(topleft=(x, y)) #
        self.value: int = value
        self.collected: bool = False #

        self.velocity_y: float = 0.0 #
        self.gravity: float = 0.5 #

        if initial_data: 
            self.from_dict(initial_data)

    def update(self) -> None:
        """
        Atualiza a lógica da moeda (principalmente a física de queda).
        """
        if self.collected: #
            return

        self.velocity_y += self.gravity #
        self.rect.y += self.velocity_y #

        ground_level = SCREEN_HEIGHT - 50 #
        if self.rect.bottom >= ground_level: 
            self.rect.bottom = ground_level 
            self.velocity_y = 0 #

    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha a moeda na tela se não foi coletada.
        Args:
            screen (pygame.Surface): A superfície da tela do Pygame.
        """
        if not self.collected: #
            screen.blit(self.image, self.rect) #

    def to_dict(self) -> dict:
        """Converte o estado da moeda em um dicionário para salvamento."""
        return {
            "x": self.rect.x,
            "y": self.rect.y,
            "value": self.value,
            "collected": self.collected,
            "velocity_y": self.velocity_y
        }

    def from_dict(self, data: dict) -> None:
        """Restaura o estado da moeda a partir de um dicionário."""
        self.rect.x = data.get("x", self.rect.x)
        self.rect.y = data.get("y", self.rect.y)
        self.value = data.get("value", self.value)
        self.collected = data.get("collected", self.collected)
        self.velocity_y = data.get("velocity_y", 0.0)