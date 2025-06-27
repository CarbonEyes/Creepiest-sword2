import pygame
import math
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, SFX_VOLUME # [cite: 9a, 10d]

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
            self.image = pygame.image.load("assets/images/fireball.png").convert_alpha() # Carrega a imagem da bola de fogo [cite: 9a]
            self.image = pygame.transform.scale(self.image, (40, 40)) # Tamanho da bola de fogo [cite: 9a]
        except pygame.error:
            print("Erro: Imagem da bola de fogo (fireball.png) não encontrada. Usando um círculo laranja como placeholder.")
            self.image = pygame.Surface((40, 40), pygame.SRCALPHA) # Placeholder transparente [cite: 9a]
            pygame.draw.circle(self.image, (255, 120, 0), (20, 20), 20) # Círculo laranja [cite: 9a]
        
        self.rect = self.image.get_rect(center=(x, y)) # Define o rect centralizado na posição inicial [cite: 9a]
        
        self.speed: int = speed
        self.damage: int = damage # Dano que o projétil causa a quem ele atinge
        self.is_active: bool = True # Flag para controlar se o projétil ainda deve ser processado/desenhado

        # Calcular direção para o alvo usando vetores
        dx = target_pos[0] - x
        dy = target_pos[1] - y
        distance = math.hypot(dx, dy) # Calcula a distância euclidiana

        # Normaliza o vetor de direção para ter comprimento 1
        if distance == 0: 
            self.direction_x = 0.0
            self.direction_y = 0.0
        else:
            self.direction_x = dx / distance
            self.direction_y = dy / distance

        # Rotação da imagem para apontar para o alvo
        angle = math.degrees(math.atan2(-dy, dx)) 
        self.image = pygame.transform.rotate(self.image, angle) # Rota a imagem [cite: 9a]
        self.rect = self.image.get_rect(center=(x,y)) # Recalcula o rect após rotação para manter o centro [cite: 9a]

        # Atributos para repulsão
        self.repelled: bool = False # Se o projétil foi repelido pelo jogador [cite: 9a]
        self.repeller_damage: int = 0 # O dano que ele causará se for repelido e atingir um inimigo [cite: 9a]


    def update(self) -> None:
        """
        Atualiza a posição do projétil a cada frame.
        """
        if not self.is_active: 
            return

        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed

        # Remover projéteis que saem da tela para evitar sobrecarga de memória
        screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT) # [cite: 9a]
        if not screen_rect.colliderect(self.rect): 
            self.is_active = False 
            # print("Projétil fora da tela.") # Debug removido

    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha o projétil na tela se estiver ativo.
        Args:
            screen (pygame.Surface): A superfície da tela do Pygame onde o projétil será desenhado.
        """
        if self.is_active: 
            screen.blit(self.image, self.rect)
