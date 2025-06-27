import pygame
from core.settings import COINS_PER_TREE_CUT # [cite: 9a]

class Tree(pygame.sprite.Sprite):
    """
    Representa uma árvore no cenário que pode ser cortada.
    """
    def __init__(self, x: int, y: int, initial_data: dict = None) -> None:
        """
        Inicializa uma árvore.
        Args:
            x (int): Posição inicial X.
            y (int): Posição inicial Y.
            initial_data (dict | None): Dados para restaurar o estado da árvore.
        """
        super().__init__()
        try:
            self.image = pygame.image.load("assets/images/tree.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (120, 180)) # Tamanho da árvore [cite: 9a]
        except pygame.error:
            print("Erro: Imagem da árvore (tree.png) não encontrada. Usando um retângulo verde como placeholder.")
            self.image = pygame.Surface((120, 180), pygame.SRCALPHA) # Placeholder [cite: 9a]
            self.image.fill((0, 100, 0)) # Verde escuro
            pygame.draw.rect(self.image, (139, 69, 19), (40, 150, 40, 30)) # Tronco marrom no placeholder [cite: 9a]

        self.rect = self.image.get_rect(topleft=(x, y))
        self.health: int = 3 # Quantos "hits" para cortar a árvore
        self.coins_on_cut: int = COINS_PER_TREE_CUT
        self.is_cut: bool = False

        if initial_data: # Restaura o estado da árvore se dados forem fornecidos
            self.from_dict(initial_data)

    def take_hit(self, damage: int) -> int:
        """
        Recebe dano. Reduz a saúde da árvore e retorna moedas se for cortada.
        Args:
            damage (int): Quantidade de dano recebido.
        Returns:
            int: Quantidade de moedas se a árvore for cortada, 0 caso contrário.
        """
        if self.is_cut:
            return 0
            
        self.health -= damage
        # print(f"Árvore atingida! Vida restante: {self.health}") # Debug removido
        if self.health <= 0:
            self.is_cut = True
            print("Árvore cortada!")
            # TODO: Tocar som de árvore caindo/cortando
            return self.coins_on_cut
        return 0

    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha a árvore na tela se não estiver cortada.
        Args:
            screen (pygame.Surface): A superfície da tela do Pygame.
        """
        if not self.is_cut:
            screen.blit(self.image, self.rect)

    def to_dict(self) -> dict:
        """Converte o estado da árvore em um dicionário para salvamento."""
        return {
            "x": self.rect.x,
            "y": self.rect.y,
            "health": self.health,
            "is_cut": self.is_cut
        }

    def from_dict(self, data: dict) -> None:
        """Restaura o estado da árvore a partir de um dicionário."""
        self.rect.x = data.get("x", self.rect.x)
        self.rect.y = data.get("y", self.rect.y)
        self.health = data.get("health", self.health)
        self.is_cut = data.get("is_cut", self.is_cut)
