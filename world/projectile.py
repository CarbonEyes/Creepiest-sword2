import pygame
import math
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, SFX_VOLUME #

class Projectile(pygame.sprite.Sprite):
    """
    Representa um projétil genérico (como uma bola de fogo).
    Gerencia seu movimento, dano e se pode ser repelido.
    """
    def __init__(self, x: int, y: int, target_pos: tuple[int, int], speed: int = 5, damage: int = 10) -> None:
        """
        Inicializa um projétil.
        Args:
            x (int): Posição inicial X do projétil.
            y (int): Posição inicial Y do projétil.
            target_pos (tuple[int, int]): Posição (x, y) do alvo para onde o projétil se moverá.
            speed (int): Velocidade do projétil.
            damage (int): Dano que o projétil causa ao colidir.
        """
        super().__init__() 

        try:
            self.image = pygame.image.load("assets/images/fireball.png").convert_alpha() #
            self.image = pygame.transform.scale(self.image, (40, 40)) #
        except pygame.error:
            print("Erro: Imagem da bola de fogo (fireball.png) não encontrada. Usando um círculo laranja como placeholder.")
            self.image = pygame.Surface((40, 40), pygame.SRCALPHA) #
            pygame.draw.circle(self.image, (255, 120, 0), (20, 20), 20) #
        
        self.rect = self.image.get_rect(center=(x, y)) #
        
        self.speed: int = speed
        self.damage: int = damage 
        self.is_active: bool = True 

        # Atributos para repulsão
        self.repelled: bool = False #
        self.repeller_damage: int = 0 #

        # NOVO: Chamar método privado para calcular direção e rotação
        self._calculate_direction_and_rotation(x, y, target_pos)


    def _calculate_direction_and_rotation(self, x: int, y: int, target_pos: tuple[int, int]) -> None: # NOVO MÉTODO PRIVADO
        """
        Calcula o vetor de direção e a rotação da imagem do projétil em direção ao alvo.
        """
        dx = target_pos[0] - x
        dy = target_pos[1] - y
        distance = math.hypot(dx, dy) 

        if distance == 0: 
            self.direction_x = 0.0
            self.direction_y = 0.0
        else:
            self.direction_x = dx / distance
            self.direction_y = dy / distance

        angle = math.degrees(math.atan2(-dy, dx)) 
        self.image = pygame.transform.rotate(self.image, angle) #
        self.rect = self.image.get_rect(center=(x,y)) #


    def update(self) -> None:
        """
        Atualiza a posição do projétil a cada frame.
        """
        if not self.is_active: 
            return

        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed

        self._check_boundary() # Chamada para o método privado

    def _check_boundary(self) -> None: # NOVO MÉTODO PRIVADO
        """
        Verifica se o projétil saiu dos limites da tela e o desativa se sim.
        """
        screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT) #
        if not screen_rect.colliderect(self.rect): 
            self.is_active = False 

    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha o projétil na tela se estiver ativo.
        """
        if self.is_active: 
            screen.blit(self.image, self.rect)