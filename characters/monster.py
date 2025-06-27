import pygame
from core.settings import COINS_PER_MONSTER_KILL, SCREEN_HEIGHT

class Monster(pygame.sprite.Sprite):
    """
    Representa um inimigo genérico com movimento básico, vida e dano.
    """
    def __init__(self, x: int, y: int, speed: int = 2, health: int = 20, damage: int = 5, initial_data: dict = None) -> None:
        """
        Inicializa um monstro.
        Args:
            x (int): Posição inicial X.
            y (int): Posição inicial Y.
            speed (int): Velocidade de movimento.
            health (int): Pontos de vida.
            damage (int): Dano que o monstro causa.
            initial_data (dict | None): Dados para restaurar o estado do monstro.
        """
        super().__init__()
        try:
            self.image = pygame.image.load("assets/images/monster.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (90, 90)) # Tamanho do monstro [cite: 9a]
        except pygame.error:
            print("Erro: Imagem do monstro (monster.png) não encontrada. Usando um retângulo vermelho como placeholder.")
            self.image = pygame.Surface((90, 90), pygame.SRCALPHA) # Placeholder [cite: 9a]
            self.image.fill((255, 0, 0)) # Vermelho
        
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed: int = speed
        self.health: int = health
        self.damage: int = damage # Dano que o monstro causa ao jogador
        self.coins_on_defeat: int = COINS_PER_MONSTER_KILL
        self.is_alive: bool = True

        # Atributos de Física para Monstro (para gravidade e colisão com chão)
        self.velocity_y: float = 0.0 # [cite: 9a]
        self.gravity: float = 0.8 # Mesma gravidade do jogador para consistência [cite: 9a]

        # Para movimento simples de ir e vir (patrulha)
        self.direction: int = 1 # 1 para direita, -1 para esquerda
        self.patrol_start_x: int = x # Ponto inicial de patrulha
        self.walk_limit_left: int = x - 100 # Monstro anda 100px para a esquerda
        self.walk_limit_right: int = x + 100 # Monstro anda 100px para a direita

        if initial_data: # Restaura o estado do monstro se dados forem fornecidos
            self.from_dict(initial_data)


    def take_damage(self, damage: int) -> int:
        """
        Recebe dano. Reduz a saúde do monstro e retorna moedas se derrotado.
        Args:
            damage (int): Quantidade de dano recebido.
        Returns:
            int: Quantidade de moedas se o monstro for derrotado, 0 caso contrário.
        """
        if not self.is_alive:
            return 0

        self.health -= damage
        # print(f"Monstro atingido! Vida restante: {self.health}") # Debug removido
        if self.health <= 0:
            self.is_alive = False
            print("Monstro derrotado!")
            # TODO: Tocar som de monstro morrendo
            return self.coins_on_defeat
        return 0

    def update(self) -> None: 
        """
        Atualiza a lógica do monstro (movimento, física).
        Este método é para monstros que não precisam da posição do jogador.
        """
        if not self.is_alive:
            return

        # Movimento simples de patrulha
        self.rect.x += self.speed * self.direction
        
        # Ajuste para virar o monstro quando atinge o limite da patrulha
        if self.direction == 1 and self.rect.x >= self.walk_limit_right:
            self.direction = -1
        elif self.direction == -1 and self.rect.x <= self.walk_limit_left:
            self.direction = 1

        # Física de Gravidade para Monstro
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Colisão com o CHÃO VERDE (SCREEN_HEIGHT - 50) [cite: 9a]
        ground_level = SCREEN_HEIGHT - 50 
        if self.rect.bottom >= ground_level:
            self.rect.bottom = ground_level
            self.velocity_y = 0 
            
    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha o monstro na tela se estiver vivo.
        Args:
            screen (pygame.Surface): A superfície da tela do Pygame.
        """
        if self.is_alive:
            # Se o monstro estiver virado para a esquerda, espelha a imagem
            if self.direction == -1:
                flipped_image = pygame.transform.flip(self.image, True, False)
                screen.blit(flipped_image, self.rect)
            else:
                screen.blit(self.image, self.rect)

    def to_dict(self) -> dict:
        """Converte o estado do monstro em um dicionário para salvamento."""
        return {
            "x": self.rect.x,
            "y": self.rect.y,
            "health": self.health,
            "is_alive": self.is_alive,
            "speed": self.speed,
            "damage": self.damage,
            "direction": self.direction,
            "patrol_start_x": self.patrol_start_x,
            "type": "Monster" # Adiciona o tipo para saber qual classe instanciar ao carregar
        }

    def from_dict(self, data: dict) -> None:
        """Restaura o estado do monstro a partir de um dicionário."""
        self.rect.x = data.get("x", self.rect.x)
        self.rect.y = data.get("y", self.rect.y)
        self.health = data.get("health", self.health)
        self.is_alive = data.get("is_alive", self.is_alive)
        self.speed = data.get("speed", self.speed) # Garante que velocidade e dano sejam restaurados
        self.damage = data.get("damage", self.damage)
        self.direction = data.get("direction", self.direction)
        self.patrol_start_x = data.get("patrol_start_x", self.patrol_start_x)
        # Recalcula os limites de patrulha com base no patrol_start_x restaurado
        self.walk_limit_left = self.patrol_start_x - 100
        self.walk_limit_right = self.patrol_start_x + 100

        """
        Atualiza a lógica do monstro (movimento, física).
        """
        if not self.is_alive:
            return

        # Movimento simples de patrulha
        self.rect.x += self.speed * self.direction
        
        # Ajuste para virar o monstro quando atinge o limite
        if self.direction == 1 and self.rect.x >= self.walk_limit_right:
            self.direction = -1
        elif self.direction == -1 and self.rect.x <= self.walk_limit_left:
            self.direction = 1

        # Física de Gravidade para Monstro
        self.velocity_y += self.gravity #
        self.rect.y += self.velocity_y

        # Colisão com o CHÃO VERDE
        ground_level = SCREEN_HEIGHT - 50 
        if self.rect.bottom >= ground_level:
            self.rect.bottom = ground_level
            self.velocity_y = 0 