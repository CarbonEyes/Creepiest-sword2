import pygame
from core.settings import SCREEN_HEIGHT # [cite: 9a]

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
            self.image = pygame.image.load("assets/images/coin.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 40)) # Tamanho da moeda [cite: 9a]
        except pygame.error:
            print("Erro: Imagem da moeda (coin.png) não encontrada. Usando um círculo amarelo como placeholder.")
            self.image = pygame.Surface((40, 40), pygame.SRCALPHA) # Placeholder [cite: 9a]
            pygame.draw.circle(self.image, (255, 255, 0), (20, 20), 20) # Círculo amarelo [cite: 9a]
        
        self.rect = self.image.get_rect(topleft=(x, y)) # [cite: 9a]
        self.value: int = value
        self.collected: bool = False # Flag para saber se já foi coletada [cite: 9a]

        # Atributos de Física para Moeda (para cair)
        self.velocity_y: float = 0.0 # Velocidade vertical da moeda, para queda [cite: 9a]
        self.gravity: float = 0.5 # Força da gravidade aplicada à moeda (pode ser ajustada) [cite: 9a]

        if initial_data: # Restaura o estado da moeda se dados forem fornecidos
            self.from_dict(initial_data)

    def update(self) -> None:
        """
        Atualiza a lógica da moeda (principalmente a física de queda).
        """
        if self.collected: # Moedas coletadas não precisam de atualização [cite: 9a]
            return

        self.velocity_y += self.gravity # Aplica a gravidade à velocidade vertical [cite: 9a]
        self.rect.y += self.velocity_y # Atualiza a posição Y da moeda com base na velocidade [cite: 9a]

        # Colisão com o CHÃO VERDE
        ground_level = SCREEN_HEIGHT - 50 # [cite: 9a]
        if self.rect.bottom >= ground_level: # Se a parte inferior da moeda atingiu ou passou do chão
            self.rect.bottom = ground_level # Posiciona a moeda exatamente no chão
            self.velocity_y = 0 # Zera a velocidade vertical para parar a queda [cite: 9a]

    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha a moeda na tela se não foi coletada.
        Args:
            screen (pygame.Surface): A superfície da tela do Pygame.
        """
        if not self.collected: # Só desenha a moeda se ela ainda não foi coletada [cite: 9a]
            screen.blit(self.image, self.rect) # Desenha a imagem da moeda na sua posição [cite: 9a]

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
